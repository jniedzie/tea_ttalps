"""
Generator filter efficiencies for ttALPs signal samples.

Filter configuration these efficiencies correspond to:
  muGenFilter (MCSmartSingleParticleFilter) AND muGenMultiAncestorFilter (PythiaFilterMultiAncestor),
  applied in sequence, both with:
    Status = 1
    |eta| < 3
    MinPt = 1 GeV
    MinDecayRadius = 0 mm, MaxDecayRadius = 7000 mm
    MinDecayZ = -10000 mm, MaxDecayZ = 10000 mm
  ProductionFilterSequence = generator*muGenFilter*muGenMultiAncestorFilter

Source: 2024_bothFilters sheet, ttALPs_genFilterEfficiency.xlsx
        (config: "muGenFilter_maxRadius7m_maxZ10m_status1_eta3_pt1;
                  muGenMultiAncestorFilter_status1_eta3_pt1")

KNOWN COVERAGE GAPS (as of writing -- check before trusting a lookup blindly):
  - mAlp-1GeV has NO entry in GEN_FILTER_EFFICIENCIES. It appears in
    dasSignalsPrivate2018 but was never scanned in the filter-efficiency
    measurement. Any lookup for this mass point will warn and default to 1.0,
    which is almost certainly WRONG if this mass point was actually produced
    with the gen filter -- measure it and add it to the table before trusting
    normalization for mAlp-1GeV.
  - mAlp-7GeV and ctau=1e4mm/1e5mm exist in the table but have no matching
    sample (yet) -- harmless, just currently unused.
  - Some dasSignalsPrivate2018 entries (mAlp-12/30/60GeV @ ctau=1e-5mm, as of
    the current sample list) point at the exact same DAS path as the
    "official"/unfiltered dasSignals2018_*GeV dicts -- i.e. those specific
    files were never actually reprocessed with the gen filter, despite being
    listed in the "private" dict. Use find_reused_unfiltered_paths() /
    compute_effective_cross_sections() below to detect and exclude these
    automatically, rather than trusting dict membership alone.

Usage (single sample):
    from ttalps_samples_genfilter_efficiencies import get_effective_cross_section

    eff_xsec, filt_eff, filt_eff_unc = get_effective_cross_section(sample_key, raw_xsec)

Usage (a whole signal dict at once, with automatic reused-path detection):
    from ttalps_samples_genfilter_efficiencies import compute_effective_cross_sections

    results = compute_effective_cross_sections(
        sample_xsecs=my_private_signal_xsecs,       # {sample_key: raw_xsec}
        filtered_das_dict=dasSignalsPrivate2018,     # {sample_key: das_path}
        unfiltered_reference_dicts=[                 # list of "official" dicts to check against
            dasSignals2018_12GeV, dasSignals2018_30GeV, dasSignals2018_60GeV,
            dasSignals2018_0p35GeV, dasSignals2018_2GeV,
        ],
    )
    # results[sample_key] = (effective_xsec, filter_efficiency, filter_efficiency_unc, reused_unfiltered_path)
"""

import re

# -----------------------------------------------------------------------------
# Global switch: set to False to disable the correction entirely (e.g. to
# reproduce pre-genfilter-era normalization exactly, or for debugging/comparison).
# Samples with no gen filter applied always get efficiency=1.0 regardless of
# this switch, since they're simply absent from GEN_FILTER_EFFICIENCIES below
# (or explicitly detected as reusing an unfiltered path -- see below).
# -----------------------------------------------------------------------------
APPLY_GEN_FILTER_EFFICIENCY = True

# Matches the physics-relevant part of a sample key regardless of year/category
# prefix, e.g. both "signals2018/tta_mAlp-12GeV_ctau-1e-5mm" and
# "signals2018private/tta_mAlp-12GeV_ctau-1e-5mm" extract to
# "mAlp-12GeV_ctau-1e-5mm".
_ALP_NAME_PATTERN = re.compile(r"(mAlp-[\w\.]+GeV_ctau-[\w\.\-]+mm)")


def extract_alp_point_name(sample_key):
    """Returns the canonical 'mAlp-{mass}GeV_ctau-{ctau}mm' substring from any
    sample key (any year/category prefix), or None if the key doesn't look
    like a ttALPs signal point at all (background, data, etc.)."""
    match = _ALP_NAME_PATTERN.search(sample_key)
    return match.group(1) if match else None


# Canonical signal-point name -> {filter_efficiency, uncertainty}
GEN_FILTER_EFFICIENCIES = {
    "mAlp-0p35GeV_ctau-1e-5mm": {"filter_efficiency": 0.986, "uncertainty": 0.005254},
    "mAlp-2GeV_ctau-1e-5mm":    {"filter_efficiency": 0.992, "uncertainty": 0.003984},
    "mAlp-7GeV_ctau-1e-5mm":    {"filter_efficiency": 0.986, "uncertainty": 0.005254},
    "mAlp-12GeV_ctau-1e-5mm":   {"filter_efficiency": 0.990, "uncertainty": 0.004450},
    "mAlp-30GeV_ctau-1e-5mm":   {"filter_efficiency": 0.996, "uncertainty": 0.002823},
    "mAlp-60GeV_ctau-1e-5mm":   {"filter_efficiency": 0.998, "uncertainty": 0.001998},

    "mAlp-0p35GeV_ctau-1e-3mm": {"filter_efficiency": 0.986, "uncertainty": 0.005254},
    "mAlp-2GeV_ctau-1e-3mm":    {"filter_efficiency": 0.992, "uncertainty": 0.003984},
    "mAlp-7GeV_ctau-1e-3mm":    {"filter_efficiency": 0.986, "uncertainty": 0.005254},
    "mAlp-12GeV_ctau-1e-3mm":   {"filter_efficiency": 0.990, "uncertainty": 0.004450},
    "mAlp-30GeV_ctau-1e-3mm":   {"filter_efficiency": 0.996, "uncertainty": 0.002823},
    "mAlp-60GeV_ctau-1e-3mm":   {"filter_efficiency": 0.998, "uncertainty": 0.001998},

    "mAlp-0p35GeV_ctau-1e0mm":  {"filter_efficiency": 0.986, "uncertainty": 0.005254},
    "mAlp-2GeV_ctau-1e0mm":     {"filter_efficiency": 0.992, "uncertainty": 0.003984},
    "mAlp-7GeV_ctau-1e0mm":     {"filter_efficiency": 0.986, "uncertainty": 0.005254},
    "mAlp-12GeV_ctau-1e0mm":    {"filter_efficiency": 0.990, "uncertainty": 0.004450},
    "mAlp-30GeV_ctau-1e0mm":    {"filter_efficiency": 0.996, "uncertainty": 0.002823},
    "mAlp-60GeV_ctau-1e0mm":    {"filter_efficiency": 0.998, "uncertainty": 0.001998},

    "mAlp-0p35GeV_ctau-1e1mm":  {"filter_efficiency": 0.896, "uncertainty": 0.013650},
    "mAlp-2GeV_ctau-1e1mm":     {"filter_efficiency": 0.986, "uncertainty": 0.005254},
    "mAlp-7GeV_ctau-1e1mm":     {"filter_efficiency": 0.986, "uncertainty": 0.005254},
    "mAlp-12GeV_ctau-1e1mm":    {"filter_efficiency": 0.990, "uncertainty": 0.004450},
    "mAlp-30GeV_ctau-1e1mm":    {"filter_efficiency": 0.996, "uncertainty": 0.002823},
    "mAlp-60GeV_ctau-1e1mm":    {"filter_efficiency": 0.998, "uncertainty": 0.001998},

    "mAlp-0p35GeV_ctau-1e2mm":  {"filter_efficiency": 0.642, "uncertainty": 0.021440},
    "mAlp-2GeV_ctau-1e2mm":     {"filter_efficiency": 0.838, "uncertainty": 0.016480},
    "mAlp-7GeV_ctau-1e2mm":     {"filter_efficiency": 0.954, "uncertainty": 0.009368},
    "mAlp-12GeV_ctau-1e2mm":    {"filter_efficiency": 0.974, "uncertainty": 0.007117},
    "mAlp-30GeV_ctau-1e2mm":    {"filter_efficiency": 0.996, "uncertainty": 0.002823},
    "mAlp-60GeV_ctau-1e2mm":    {"filter_efficiency": 0.998, "uncertainty": 0.001998},

    "mAlp-0p35GeV_ctau-1e3mm":  {"filter_efficiency": 0.522, "uncertainty": 0.022340},
    "mAlp-2GeV_ctau-1e3mm":     {"filter_efficiency": 0.610, "uncertainty": 0.021810},
    "mAlp-7GeV_ctau-1e3mm":     {"filter_efficiency": 0.708, "uncertainty": 0.020330},
    "mAlp-12GeV_ctau-1e3mm":    {"filter_efficiency": 0.740, "uncertainty": 0.019620},
    "mAlp-30GeV_ctau-1e3mm":    {"filter_efficiency": 0.864, "uncertainty": 0.015330},
    "mAlp-60GeV_ctau-1e3mm":    {"filter_efficiency": 0.930, "uncertainty": 0.011410},

    "mAlp-0p35GeV_ctau-1e4mm":  {"filter_efficiency": 0.512, "uncertainty": 0.022350},
    "mAlp-2GeV_ctau-1e4mm":     {"filter_efficiency": 0.548, "uncertainty": 0.022260},
    "mAlp-7GeV_ctau-1e4mm":     {"filter_efficiency": 0.566, "uncertainty": 0.022170},
    "mAlp-12GeV_ctau-1e4mm":    {"filter_efficiency": 0.582, "uncertainty": 0.022060},
    "mAlp-30GeV_ctau-1e4mm":    {"filter_efficiency": 0.612, "uncertainty": 0.021790},
    "mAlp-60GeV_ctau-1e4mm":    {"filter_efficiency": 0.654, "uncertainty": 0.021270},

    "mAlp-0p35GeV_ctau-1e5mm":  {"filter_efficiency": 0.506, "uncertainty": 0.022360},
    "mAlp-2GeV_ctau-1e5mm":     {"filter_efficiency": 0.534, "uncertainty": 0.022310},
    "mAlp-7GeV_ctau-1e5mm":     {"filter_efficiency": 0.546, "uncertainty": 0.022270},
    "mAlp-12GeV_ctau-1e5mm":    {"filter_efficiency": 0.552, "uncertainty": 0.022240},
    "mAlp-30GeV_ctau-1e5mm":    {"filter_efficiency": 0.538, "uncertainty": 0.022300},
    "mAlp-60GeV_ctau-1e5mm":    {"filter_efficiency": 0.552, "uncertainty": 0.022240},
}

_UNFILTERED = {"filter_efficiency": 1.0, "uncertainty": 0.0}


def find_reused_unfiltered_paths(filtered_das_dict, unfiltered_das_dict):
    """
    Compares a 'filtered' DAS dict against one or more 'official'/unfiltered
    DAS dicts and returns the set of sample keys in `filtered_das_dict` whose
    DAS path is IDENTICAL to a path found in `unfiltered_das_dict` -- i.e.
    samples that are nominally in the new/private list but actually still
    point at a dataset that was never reprocessed with the gen filter.

    These keys must NOT get the gen filter efficiency correction applied,
    regardless of what their name looks like.
    """
    unfiltered_paths = set(unfiltered_das_dict.values())
    return {key for key, path in filtered_das_dict.items() if path in unfiltered_paths}


def get_gen_filter_efficiency(sample_key, force_unfiltered=False, warn_if_missing_for_signal=True):
    """
    Raw lookup, independent of the global switch.

    sample_key: the full sample identifier as used in your DAS dicts, e.g.
        "signals2018private/tta_mAlp-12GeV_ctau-1e3mm"
        (any year/category prefix is fine -- the mAlp/ctau part is extracted internally)
    force_unfiltered: pass True for keys identified by find_reused_unfiltered_paths()
        (or any other reason you know this particular sample wasn't actually filtered).

    Returns (filter_efficiency, uncertainty). Defaults to (1.0, 0.0) for
    backgrounds/data, for signal points with no table entry (with a warning),
    and for anything explicitly forced unfiltered.
    """
    if force_unfiltered:
        return _UNFILTERED["filter_efficiency"], _UNFILTERED["uncertainty"]

    point_name = extract_alp_point_name(sample_key)
    if point_name is None:
        # Not a ttALPs signal sample name at all -- background, data, etc.
        return _UNFILTERED["filter_efficiency"], _UNFILTERED["uncertainty"]

    entry = GEN_FILTER_EFFICIENCIES.get(point_name)
    if entry is None:
        if warn_if_missing_for_signal:
            print(
                f"[WARNING] signal point '{point_name}' (from sample key '{sample_key}') "
                f"has no gen filter efficiency entry -- treating as unfiltered (eff=1.0). "
                f"Confirm this point really had no gen filter applied, or measure it and "
                f"extend GEN_FILTER_EFFICIENCIES."
            )
        return _UNFILTERED["filter_efficiency"], _UNFILTERED["uncertainty"]
    return entry["filter_efficiency"], entry["uncertainty"]


def get_effective_cross_section(sample_key, raw_xsec, force_unfiltered=False, warn_if_missing_for_signal=True):
    """
    Single entry point for one sample. Respects APPLY_GEN_FILTER_EFFICIENCY:
    when False, returns raw_xsec unmodified and (1.0, 0.0) for every sample,
    exactly reproducing pre-genfilter-era behavior with no other code changes.

    Returns (effective_cross_section, filter_efficiency, filter_efficiency_uncertainty).
    """
    if not APPLY_GEN_FILTER_EFFICIENCY:
        return raw_xsec, 1.0, 0.0
    eff, unc = get_gen_filter_efficiency(
        sample_key, force_unfiltered=force_unfiltered, warn_if_missing_for_signal=warn_if_missing_for_signal
    )
    return raw_xsec * eff, eff, unc


def compute_effective_cross_sections(sample_xsecs, filtered_das_dict, unfiltered_reference_dicts=None):
    """
    Batch helper matching the dasSignalsPrivate2018-style workflow.

    sample_xsecs: {sample_key: raw_xsec} for the samples you're about to process.
    filtered_das_dict: the DAS dict these samples come from (e.g. dasSignalsPrivate2018),
        used only to look up each sample's DAS path for reused-path detection.
    unfiltered_reference_dicts: list of 'official'/unfiltered DAS dicts to check
        filtered_das_dict against (e.g. [dasSignals2018_12GeV, dasSignals2018_30GeV, ...]).
        If None, no reused-path detection is performed.

    Returns {sample_key: (effective_xsec, filter_efficiency, filter_efficiency_unc, was_forced_unfiltered)}
    """
    reused_keys = set()
    if unfiltered_reference_dicts:
        for ref_dict in unfiltered_reference_dicts:
            reused_keys |= find_reused_unfiltered_paths(filtered_das_dict, ref_dict)

    results = {}
    for sample_key, raw_xsec in sample_xsecs.items():
        force_unfiltered = sample_key in reused_keys
        if force_unfiltered:
            print(
                f"[INFO] '{sample_key}' reuses a DAS path identical to an unfiltered "
                f"reference sample -- treating as unfiltered (eff=1.0), NOT applying "
                f"the gen filter correction despite being in the 'private' dict."
            )
        eff_xsec, filt_eff, filt_eff_unc = get_effective_cross_section(
            sample_key, raw_xsec, force_unfiltered=force_unfiltered
        )
        results[sample_key] = (eff_xsec, filt_eff, filt_eff_unc, force_unfiltered)
    return results


if __name__ == "__main__":
    # Quick sanity check using realistic keys from ttalps_samples_list_2018.py
    print(f"APPLY_GEN_FILTER_EFFICIENCY = {APPLY_GEN_FILTER_EFFICIENCY}\n")

    test_unfiltered_12 = {
        "signals2018/tta_mAlp-12GeV_ctau-1e-5mm": "/TTALPto2Mu_.../RunIISummer20UL18RECO-106X_v11-v2.../USER",
    }
    test_private = {
        "signals2018private/tta_mAlp-12GeV_ctau-1e-5mm": "/TTALPto2Mu_.../RunIISummer20UL18RECO-106X_v11-v2.../USER",  # reused!
        "signals2018private/tta_mAlp-12GeV_ctau-1e3mm": "/ttalps/lrygaard-LLPnanoAODv1_m-12GeV_ctau-1e3mm.../USER",   # genuinely new
        "signals2018private/tta_mAlp-1GeV_ctau-1e0mm": "/ttalps/lrygaard-ttalps_m-1GeV_ctau-1e0mm.../USER",           # missing from table
    }
    test_xsecs = {k: 10.0 for k in test_private}

    print("--- compute_effective_cross_sections demo ---")
    results = compute_effective_cross_sections(test_xsecs, test_private, [test_unfiltered_12])
    for k, v in results.items():
        print(k, "->", v)