from ttalps_samples_list import dasSamples2018, dasBackgrounds2018, dasData2018, dasSignalsPrivate2018, dasData2018_standard, dasSignals2018
from ttalps_samples_list import dasData2022preEE, dasData2022postEE, dasSignals2022preEE
from ttalps_samples_list import dasBackgrounds2017, dasData2017, dasSignals2017
from ttalps_samples_list import dasBackgrounds2016PostVFP, dasData2016PostVFP, dasSignals2016PostVFP
from ttalps_samples_list import dasBackgrounds2022postEE, dasData2023postBPix, dasSignals2023postBPix
import os

max_files = -1

# input_user = "jniedzie"
input_user = "lrygaard"
# input_user = "jalimena"
input_base_path = f"/data/dust/user/{input_user}/ttalps_cms"
output_base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"


# Signal like skim: SR, J/Psi CR and Z CR with no isolation requirement on the loose muons
input_skim = "skimmed_looseSemimuonic_v2_merged"
# output_skim = "skimmed_looseSemimuonic_v2_SR"
# output_skim = "skimmed_looseSemimuonic_v2_SR_looseMuonPtGt8GeV"
output_skim = "skimmed_looseSemimuonic_v2_SR_segmentMatch1p5"

# tt̄ (μ+jets) CR
# input_skim = "skimmed_looseSemimuonic_v2_merged"
# output_skim = "skimmed_looseSemimuonic_v2_ttbarCR"
# output_skim = "skimmed_looseSemimuonic_v2_ttbarCR_segmentMatchedDSA"

# tt̄ (μ+jets) + 1 DSA Muon CR
# input_skim = "skimmed_looseSemimuonic_v2_merged"
# output_skim = "skimmed_looseSemimuonic_v2_ttbarLike1DSA"

# tt̄ (e+jets) CR
# input_skim = "skimmed_looseSemielectronic_v1_merged"
# output_skim = "skimmed_looseSemielectronic_v1_ttbarCR"

# VV CR
# input_skim = "skimmed_looseNonTT_v1_merged"
# output_skim = "skimmed_looseNonTT_v1_VVCR"

# QCD CR
# input_skim = "skimmed_looseNoBjets_lt4jets_v1_merged"
# output_skim = "skimmed_looseNoBjets_lt4jets_v1_looseMuonPtGt8GeV"

# W+jets CR
# input_skim = "skimmed_loose_lt3bjets_lt4jets_v1_merged"
# output_skim = "skimmed_loose_lt3bjets_lt4jets_v1_WjetsCR"

# bb CR
# input_skim = "skimmed_loose_lt3bjets_lt4jets_v1_merged"
# output_skim = "skimmed_loose_lt3bjets_lt4jets_v1_bbCR"

# Skims with no triggers for LLP trigger study
# input_skim = "skimmed_looseSemimuonic_v2_notrigger_merged"
# output_skim = "skimmed_looseSemimuonic_v2_notrigger_SR"

# Inverted MET skims
# input_skim = "skimmed_looseInvertedMet_v1_merged"
# output_skim = "skimmed_looseInvertedMet_v1_SR"

# input_skim = "skimmed_looseNoMet_v1_merged"
# output_skim = "skimmed_looseNoMet_v1_SR"

output_trees_dir = ""
output_hists_dir = ""
input_directory = ""

# For local inputs:
sample_path = ""

input_directory = f"{input_base_path}/{sample_path}/{input_skim}"
output_trees_dir = f"{output_base_path}/{sample_path}/{output_skim}/"

# samples = dasBackgrounds2016.keys()

# samples = dasSamples2018.keys()
samples = dasBackgrounds2018.keys()
# samples = list(dasBackgrounds2018.keys()) + list(dasData2018.keys())
