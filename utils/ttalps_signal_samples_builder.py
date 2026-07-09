"""
ttalps_signal_samples_builder.py -- shared across all years.

Builds signal Sample objects exactly matching TTAlpsABCDConfigHelper's own
convention (same file_path pattern, same "signal_"+name.split("/")[-1]
naming, same cross_sections-dict-based cross section resolution), but with
the gen filter efficiency correction folded in, and with same-physics-point
filtered/unfiltered pairs kept as separate, distinctly-named Samples ready
for merging (see merge_signal_histograms.py) rather than colliding under
one name.

WHY NOT REUSE Sample.__post_init__'s dict-based lookup directly:
We still need the *resolved* base cross section (whatever
TTAlpsABCDConfigHelper would have used) so we can multiply it by the gen
filter efficiency -- so resolve_base_cross_section() below replicates that
exact substring-match logic, then we pass the final product as an explicit
Sample(cross_section=...), which bypasses Sample.__post_init__'s own lookup
(since it only fires when cross_section < 0).
"""

from Sample import Sample, SampleType
from ttalps_cross_sections import get_cross_sections
from ttalps_luminosities import get_luminosity
from ttalps_samples_genfilter_efficiencies import (
    extract_alp_point_name,
    get_gen_filter_efficiency,
    find_reused_unfiltered_paths,
)


def resolve_base_cross_section(signal_name, cross_sections):
    """
    Replicates Sample.__post_init__'s substring-match lookup exactly:
    signal_name (e.g. 'tta_mAlp-12GeV_ctau-1e3mm') must appear as a substring
    of a cross_sections dict key. Raises if no match, same as the real
    Sample class does via fatal()/exit().
    """
    for key, cross_section in cross_sections.items():
        if signal_name in key:
            return cross_section
    raise ValueError(f"Signal '{signal_name}' not found in cross sections dict")


def build_signal_samples(
    filtered_das_dict,     # e.g. dasSignalsPrivate2018
    unfiltered_das_dicts,  # e.g. [dasSignals2018_0p35GeV, ..., dasSignals2018_60GeV]
    year,                  # e.g. "2018" -- string, matching get_cross_sections/get_luminosity's convention
    base_path,             # matching TTAlpsABCDConfigHelper's self.base_path
    skim,                  # matching TTAlpsABCDConfigHelper's self.background_skim (used for signals too,
                           # exactly reproducing the existing helper's own convention)
    hist_path,             # matching TTAlpsABCDConfigHelper's self.background_hist_path
):
    """
    Returns (single_samples, samples_to_merge):

      single_samples: list of final, ready-to-use Sample objects for signal
        points that only exist in ONE of the two dicts (either only
        official/unfiltered, or only private/filtered e.g. mAlp-1GeV) --
        these need no merge step, use them directly in TTAlpsABCDConfigHelper-
        style code exactly like any other signal Sample.

      samples_to_merge: list of (sample_unfiltered, sample_filtered,
        canonical_name, canonical_file_path) tuples for points present in
        BOTH dicts. sample_unfiltered/sample_filtered are "intermediate"
        Samples (distinctly named, e.g. one gets a '_genfiltered' suffix, so
        HistogramNormalizer's per-name bookkeeping never collides between
        them) pointing at their own separate raw histograms.root files.
        Feed each tuple to merge_signal_histograms.merge_signal_samples(...)
        (after both have actually been histogrammed) to get the final
        canonical Sample for that point.
    """
    cross_sections = get_cross_sections(year)
    luminosity = get_luminosity(year)

    unfiltered_flat = {}
    for d in unfiltered_das_dicts:
        unfiltered_flat.update(d)

    reused_keys = set()
    for ref_dict in unfiltered_das_dicts:
        reused_keys |= find_reused_unfiltered_paths(filtered_das_dict, ref_dict)

    def _file_path(das_key):
        return f"{base_path}/{das_key}/{skim[0]}/{hist_path}/histograms.root"

    def _make_sample(sample_name, das_key, force_unfiltered):
        signal_name = das_key.split("/")[-1]  # matches TTAlpsABCDConfigHelper's stripping exactly
        base_xsec = resolve_base_cross_section(signal_name, cross_sections)

        point_name = extract_alp_point_name(das_key)
        filt_eff, filt_eff_unc = get_gen_filter_efficiency(das_key, force_unfiltered=force_unfiltered)
        eff_xsec = base_xsec * filt_eff
        assert eff_xsec > 0, f"Non-positive effective cross section for '{das_key}': {eff_xsec}"

        sample = Sample(
            name=sample_name,
            file_path=_file_path(das_key),
            type=SampleType.signal,
            cross_section=eff_xsec,  # explicit >=0 => __post_init__ skips its own dict lookup
            luminosity=luminosity,
            year=year,
        )
        sample.gen_filter_efficiency = filt_eff
        sample.gen_filter_efficiency_unc = filt_eff_unc
        return sample, point_name

    # Group DAS keys (from both dicts) by canonical physics point name
    points = {}  # point_name -> {"filtered": das_key or None, "unfiltered": das_key or None}
    for das_key in filtered_das_dict:
        point_name = extract_alp_point_name(das_key)
        if point_name is None:
            continue
        points.setdefault(point_name, {})["filtered"] = das_key
    for das_key in unfiltered_flat:
        point_name = extract_alp_point_name(das_key)
        if point_name is None:
            continue
        points.setdefault(point_name, {})["unfiltered"] = das_key

    single_samples = []
    samples_to_merge = []

    for point_name, sources in points.items():
        filtered_key = sources.get("filtered")
        unfiltered_key = sources.get("unfiltered")

        if filtered_key and unfiltered_key:
            # Present in both -- build two distinctly-named intermediate
            # Samples, to be merged once both are histogrammed.
            force_unfiltered = filtered_key in reused_keys
            canonical_signal_name = filtered_key.split("/")[-1]  # e.g. "tta_mAlp-12GeV_ctau-1e3mm"

            sample_filtered, _ = _make_sample(
                "signal_" + canonical_signal_name + "_genfiltered", filtered_key, force_unfiltered
            )
            sample_unfiltered, _ = _make_sample(
                "signal_" + canonical_signal_name, unfiltered_key, force_unfiltered=True
            )
            canonical_name = "signal_" + canonical_signal_name
            canonical_file_path = _file_path(unfiltered_key.rsplit("/", 1)[0] + "/MERGED_" + canonical_signal_name)
            samples_to_merge.append((sample_unfiltered, sample_filtered, canonical_name, canonical_file_path))

        elif filtered_key:
            # Only in the private/filtered dict (e.g. mAlp-1GeV) -- single Sample, canonical name, no merge.
            force_unfiltered = filtered_key in reused_keys
            signal_name = filtered_key.split("/")[-1]
            sample, _ = _make_sample("signal_" + signal_name, filtered_key, force_unfiltered)
            single_samples.append(sample)

        elif unfiltered_key:
            # Only in the official/unfiltered dict -- exactly reproduces
            # TTAlpsABCDConfigHelper's existing behavior, untouched.
            signal_name = unfiltered_key.split("/")[-1]
            sample, _ = _make_sample("signal_" + signal_name, unfiltered_key, force_unfiltered=True)
            single_samples.append(sample)

    return single_samples, samples_to_merge


if __name__ == "__main__":
    from real_samples_excerpt import (
        dasSignalsPrivate2018,
        dasSignals2018_0p35GeV, dasSignals2018_2GeV,
        dasSignals2018_12GeV, dasSignals2018_30GeV, dasSignals2018_60GeV,
    )

    single_samples, samples_to_merge = build_signal_samples(
        dasSignalsPrivate2018,
        [dasSignals2018_0p35GeV, dasSignals2018_2GeV, dasSignals2018_12GeV, dasSignals2018_30GeV, dasSignals2018_60GeV],
        year="2018",
        base_path="/data/dust/user/lrygaard/ttalps_cms",
        skim=("skimmed_looseSemimuonic_v3_SR", "SRDimuons", "LooseNonLeadingMuonsVertexSegmentMatch"),
        hist_path="histograms_SRDimuons_ABCD_ANv2",
    )

    print(f"\n{len(single_samples)} single (no-merge) samples, {len(samples_to_merge)} pairs needing a merge.\n")
    print("Example single sample:")
    s = single_samples[0]
    print(f"  name={s.name!r} cross_section={s.cross_section:.6f} file_path={s.file_path!r}")

    print("\nExample merge pair:")
    su, sf, cname, cpath = samples_to_merge[0]
    print(f"  unfiltered: name={su.name!r} cross_section={su.cross_section:.6f} file_path={su.file_path!r}")
    print(f"  filtered:   name={sf.name!r} cross_section={sf.cross_section:.6f} file_path={sf.file_path!r}")
    print(f"  -> canonical_name={cname!r}")
    print(f"  -> canonical_file_path={cpath!r}")