"""
Merges a filtered and unfiltered Sample's raw histograms.root files for the
SAME physics point into one canonical, already-normalized-to-lumi output
file, plus a Sample object to represent it downstream.

WHY THIS ISN'T JUST TH1::Add() ON THE TWO RAW FILES:
This framework's HistogramNormalizer normalizes histograms.root ON THE FLY,
at analysis time (reading sample.cross_section, sample.luminosity, and the
sample's own cutFlow histogram fresh each run) -- the ROOT files written by
the C++ histogrammer are NOT pre-normalized. Since the filtered and
unfiltered productions have different cross_section and different sumw,
simply adding their raw (differently-scaled) histograms would be wrong.
This script explicitly computes each sample's own lumi-normalization scale
(replicating HistogramNormalizer.__normalizeToLumi's exact formula for
SampleType.signal) and applies it BEFORE summing.

WHY THE OUTPUT SAMPLE NEEDS A "NO-OP RENORMALIZATION" TRICK:
Downstream code (e.g. TTAlpsABCDConfigHelper-style Sample lists feeding into
HistogramNormalizer again for plotting/limits) will call normalize() on
every Sample uniformly -- there's no per-sample "skip me" switch in that
class. So the merged Sample here is deliberately constructed with
luminosity=1.0, cross_section=1.0, initial_weight_sum=1.0, making
HistogramNormalizer's later scale = lumi*xsec/sumw = 1.0*1.0/1.0 = 1.0 --
a guaranteed no-op, regardless of what config.luminosity happens to be at
that point, since all three values are pinned explicitly rather than left
to fall back to external state.

HistogramNormalizer also requires a 'cutFlow' histogram to exist in every
sample's file (it errors and skips the sample otherwise) -- so a placeholder
cutFlow is written into the merged output even though its value is never
actually used for this sample's scale (initial_weight_sum is pinned above).
"""

from ROOT import TFile, TH1, TObject
from Sample import Sample, SampleType


def compute_signal_normalization_scale(sample):
    """
    Replicates HistogramNormalizer.__normalizeToLumi's exact formula for a
    SampleType.signal sample: scale = luminosity * cross_section / initial_weight_sum,
    reading initial_weight_sum from the sample's own cutFlow bin 1 if not
    explicitly set on the Sample (matching __setBackgroundEntries exactly).

    Requires sample.luminosity > 0 (no config.luminosity fallback here --
    this script is meant to be self-contained, so pass real values in).
    """
    if sample.luminosity <= 0:
        raise ValueError(
            f"Sample '{sample.name}' has no explicit luminosity set -- "
            f"this script doesn't have access to a global config.luminosity fallback, "
            f"set sample.luminosity explicitly before calling."
        )

    if sample.initial_weight_sum > 0:
        initial_weight_sum = sample.initial_weight_sum
    else:
        f = TFile.Open(sample.file_path, "READ")
        if not f or f.IsZombie():
            raise IOError(f"Couldn't open file for sample '{sample.name}': {sample.file_path}")
        cut_flow = f.Get("cutFlow")
        if cut_flow is None or type(cut_flow) == TObject:
            raise RuntimeError(f"Couldn't find cutFlow histogram for sample '{sample.name}' in {sample.file_path}")
        initial_weight_sum = cut_flow.GetBinContent(1)
        f.Close()

    if initial_weight_sum == 0:
        raise ValueError(f"Sample '{sample.name}' has initial_weight_sum == 0 -- can't normalize.")

    return sample.luminosity * sample.cross_section / initial_weight_sum


def _collect_histogram_keys(root_file):
    keys = {}
    for key in root_file.GetListOfKeys():
        obj = key.ReadObj()
        if isinstance(obj, TH1):
            keys[key.GetName()] = key.GetClassName()
    return keys


def merge_signal_samples(sample_unfiltered, sample_filtered, canonical_name, canonical_file_path,
                          warn_on_mismatch=True):
    """
    sample_unfiltered, sample_filtered: intermediate Samples for the SAME
    physics point (as produced by ttalps_signal_samples_builder.build_signal_samples),
    each pointing at its own raw (not-yet-normalized) histograms.root.

    Writes canonical_file_path containing every histogram, correctly
    lumi-normalized-and-summed, plus a placeholder cutFlow.

    Returns the final canonical Sample object (SampleType.signal, name=canonical_name,
    file_path=canonical_file_path) with luminosity/cross_section/initial_weight_sum
    pinned to make any future HistogramNormalizer pass over it a no-op --
    ready to be used exactly like any other signal Sample downstream.
    """
    scale_unfiltered = compute_signal_normalization_scale(sample_unfiltered)
    scale_filtered = compute_signal_normalization_scale(sample_filtered)

    file_unfiltered = TFile.Open(sample_unfiltered.file_path, "READ")
    file_filtered = TFile.Open(sample_filtered.file_path, "READ")
    if not file_unfiltered or file_unfiltered.IsZombie():
        raise IOError(f"Couldn't open unfiltered file: {sample_unfiltered.file_path}")
    if not file_filtered or file_filtered.IsZombie():
        raise IOError(f"Couldn't open filtered file: {sample_filtered.file_path}")

    keys_unfiltered = _collect_histogram_keys(file_unfiltered)
    keys_filtered = _collect_histogram_keys(file_filtered)

    only_in_unfiltered = set(keys_unfiltered) - set(keys_filtered)
    only_in_filtered = set(keys_filtered) - set(keys_unfiltered)
    in_both = set(keys_unfiltered) & set(keys_filtered)

    if warn_on_mismatch and (only_in_unfiltered or only_in_filtered):
        print(
            f"[WARNING] Histogram sets differ for '{canonical_name}' "
            f"({len(only_in_unfiltered)} only in unfiltered, {len(only_in_filtered)} only in filtered). "
            f"Confirm both jobs used the same histogrammer config."
        )

    file_output = TFile.Open(canonical_file_path, "RECREATE")

    n_merged = 0
    for name in sorted(in_both):
        if name == "cutFlow":
            continue  # handled separately below as a placeholder
        hist_unfiltered = file_unfiltered.Get(name).Clone(name)
        hist_unfiltered.SetDirectory(0)
        hist_unfiltered.Scale(scale_unfiltered)

        hist_filtered = file_filtered.Get(name)
        hist_filtered_scaled = hist_filtered.Clone("tmp_" + name)
        hist_filtered_scaled.SetDirectory(0)
        hist_filtered_scaled.Scale(scale_filtered)

        hist_unfiltered.Add(hist_filtered_scaled)  # now physically-normalized-and-summed
        hist_unfiltered.SetDirectory(file_output)
        hist_unfiltered.Write(name)
        n_merged += 1

    for name in sorted(only_in_unfiltered):
        if name == "cutFlow":
            continue
        h = file_unfiltered.Get(name).Clone(name)
        h.Scale(scale_unfiltered)
        h.SetDirectory(file_output)
        h.Write(name)

    for name in sorted(only_in_filtered):
        if name == "cutFlow":
            continue
        h = file_filtered.Get(name).Clone(name)
        h.Scale(scale_filtered)
        h.SetDirectory(file_output)
        h.Write(name)

    # Placeholder cutFlow: HistogramNormalizer requires SOME cutFlow histogram
    # to exist for every sample, but this sample's initial_weight_sum is
    # pinned explicitly below (=1.0), so the placeholder's actual bin
    # contents are never read for normalization -- only its existence matters.
    placeholder_cutflow = file_unfiltered.Get("cutFlow")
    if placeholder_cutflow is not None:
        placeholder_cutflow = placeholder_cutflow.Clone("cutFlow")
        placeholder_cutflow.SetDirectory(file_output)
        placeholder_cutflow.Write("cutFlow")
    else:
        print(f"[WARNING] No cutFlow histogram found in {sample_unfiltered.file_path} to use as a placeholder "
              f"-- HistogramNormalizer may error on '{canonical_name}' later if it requires one to exist.")

    file_output.Close()
    file_unfiltered.Close()
    file_filtered.Close()

    print(
        f"[INFO] Merged '{canonical_name}': {n_merged} shared histograms "
        f"(scale_unfiltered={scale_unfiltered:.6g}, scale_filtered={scale_filtered:.6g}) "
        f"-> {canonical_file_path}"
    )

    merged_sample = Sample(
        name=canonical_name,
        file_path=canonical_file_path,
        type=SampleType.signal,
        cross_section=1.0,       # pinned no-op values: any later
        initial_weight_sum=1.0,  # HistogramNormalizer.__normalizeToLumi pass
        luminosity=1.0,          # over this Sample computes scale = 1.0
        year=sample_unfiltered.year,
    )
    merged_sample.gen_filter_efficiency = sample_filtered.gen_filter_efficiency
    merged_sample.gen_filter_efficiency_unc = sample_filtered.gen_filter_efficiency_unc
    merged_sample.merged_from = (sample_unfiltered.name, sample_filtered.name)
    return merged_sample