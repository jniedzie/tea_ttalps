import teaHelpers as tea
import os

from ttalps_samples_list import dasData2016preVFP, dasBackgrounds2016preVFP, dasSignals2016preVFP
from ttalps_samples_list import dasData2016postVFP, dasBackgrounds2016postVFP, dasSignals2016postVFP
from ttalps_samples_list import dasData2017, dasBackgrounds2017, dasSignals2017
from ttalps_samples_list import dasData2018, dasBackgrounds2018, dasSignals2018

from ttalps_samples_list import dasData2022preEE, dasBackgrounds2022preEE, dasSignals2022preEE
from ttalps_samples_list import dasData2022postEE, dasBackgrounds2022postEE, dasSignals2022postEE

from ttalps_samples_list import dasData2023preBPix, dasBackgrounds2023preBPix, dasSignals2023preBPix
from ttalps_samples_list import dasData2023postBPix, dasBackgrounds2023postBPix, dasSignals2023postBPix

max_files = -1

# input_user = "jniedzie"
input_user = "lrygaard"
# input_user = "jalimena"
input_base_path = f"/data/dust/user/{input_user}/ttalps_cms"
output_base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"


# Signal like skim: SR, J/Psi CR and Z CR with no isolation requirement on the loose muons
input_skim = "skimmed_looseSemimuonic_v3_merged"
output_skim = "skimmed_looseSemimuonic_v3_SR"

# tt̄ (μ+jets) CR
# input_skim = "skimmed_looseSemimuonic_v2_merged"
# output_skim = "skimmed_looseSemimuonic_v2_ttbarCR"
# output_skim = "skimmed_looseSemimuonic_v2_ttbarCR_withHemVeto"
# output_skim = "skimmed_looseSemimuonic_v2_ttbarCR_noHemVeto"

# tt̄ (μ+jets) + 1 DSA Muon CR
# input_skim = "skimmed_looseSemimuonic_v2_merged"
# output_skim = "skimmed_looseSemimuonic_v2_ttbarLike1DSA"

# tt̄ (e+jets) CR
# input_skim = "skimmed_looseSemielectronic_v1_merged"
# output_skim = "skimmed_looseSemielectronic_v1_ttbarCR"

# Skims with no triggers for LLP trigger study
# input_skim = "skimmed_looseSemimuonic_v2_notrigger_merged"
# output_skim = "skimmed_looseSemimuonic_v2_notrigger_SR"

output_trees_dir = ""
input_directory = ""

# For local inputs:
sample_path = ""

input_directory = f"{input_base_path}/{sample_path}/{input_skim}"
output_trees_dir = f"{output_base_path}/{sample_path}/{output_skim}/"

# samples = dasSamples2018.keys()
samples = dasBackgrounds2018.keys()
# samples = dasData2018.keys()
# samples = list(dasBackgrounds2018.keys()) + list(dasData2018.keys())

year = tea.get_year_from_samples(samples)
