from ttalps_samples_list import dasBackgrounds2022preEE, dasBackgrounds2022postEE, dasBackgrounds2017, dasData2017
from ttalps_samples_list import dasBackgrounds2017, dasSignals2017, dasData2017
from ttalps_samples_list import dasBackgrounds2018, dasSignals2018, dasData2018
from ttalps_samples_list import dasBackgrounds2016PreVFP, dasData2016PreVFP, dasSignals2016PreVFP
from ttalps_samples_list import dasBackgrounds2016PostVFP, dasData2016PostVFP, dasSignals2016PostVFP
from ttalps_samples_list import dasBackgrounds2023postBPix, dasData2023postBPix, dasSignals2023postBPix
from ttalps_samples_list import dasBackgrounds, dasSignals, dasData

from Logger import error, info
import os
import shutil
import argparse
import glob

parser = argparse.ArgumentParser()
parser.add_argument("--dry", action="store_true", default=False, help="Dry run.")
args = parser.parse_args()

# samples = dasBackgrounds.keys()
samples = dasBackgrounds2017.keys()

compare_to_jalimena = False

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"
base_path_jalimena = f"/data/dust/user/jalimena/ttalps_cms"

# skim = "skimmed_looseSemimuonic_v2"

hist_path = "" # Optional subdirectory
# hist_path = "/histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs"

root_path = "" # Optional subdirectory
# root_path = "/*.root"

destination = "" # Optional: if destination is given directory will be moved not deleted
# destination = f"{skim}/histograms_muonSFs_muonTriggerSFs_pileupSFs_bTaggingSFs_PUjetIDSFs_jecSFs_SRDimuons_LooseNonLeadingMuonsVertexSegmentMatch"


def get_dir_size(path):
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total += os.path.getsize(fp)
            except FileNotFoundError:
                # Handles race conditions if a file was deleted mid-scan
                pass
    return total

if args.dry:
    info("Dry run: no directories will be removed")

total_size = 0

for sample in samples:
    total_path = f"{base_path}/{sample}/{skim}{hist_path}"
    total_path_jalimena = f"{base_path_jalimena}/{sample}/{skim}{hist_path}"

    if base_path == "" or sample == "" or skim == "":
        error(f"Error: cannot remove directory {total_path} as part of the path is missing")
        continue
    
    if not os.path.exists(total_path):
        error(f"Path does not exist: {total_path}")
        continue

    if compare_to_jalimena and not os.path.exists(total_path_jalimena):
        error(f"Path does not exist: {total_path_jalimena}")
        continue

    size = get_dir_size(total_path)
    total_size += size

    info(f"Removing: {total_path} - size: {size/(1024*1024):.2f} MB")


    if args.dry:
        root_files = glob.glob(f"{total_path}/*.root")
        info(f"Files in lrygaard directory: {len(root_files)}")
        root_files_jalimena = glob.glob(f"{total_path_jalimena}/*.root")
        if compare_to_jalimena:
            info(f"Files in jalimena directory: {len(root_files_jalimena)}")
            if (len(root_files) != len(root_files_jalimena)):
                error(f"not the same number of files in {total_path_jalimena}")
    else:
        root_files = glob.glob(f"{total_path}/*.root")
        root_files_jalimena = glob.glob(f"{total_path_jalimena}/*.root")
        if compare_to_jalimena:
            if (len(root_files_jalimena) != 0 and len(root_files) == len(root_files_jalimena)):
                info(f"the same number of files in {total_path_jalimena}")
                if root_path != "":
                    files_to_remove = glob.glob(f"{total_path}{root_path}")
                    for file in files_to_remove:
                        jalimena_file = file.replace(base_path, base_path_jalimena)
                        jalimena_file = glob.glob(jalimena_file)
                        info(f"Removing file: {file}")
                        # check if the file exists in jalimena's directory
                        if len(jalimena_file) == 0:
                            error(f"File does not exist in jalimena's directory: {jalimena_file}")
                        else:
                            info(f"File exists in jalimena's directory: {jalimena_file}")
                            os.remove(file)
                else:
                    shutil.rmtree(total_path)
            else:
                error(f"not the same number of files in {total_path_jalimena}")
        else:
            if destination != "":
                total_destination = f"{base_path}/{sample}/{destination}"
                print(f"moving:")
                print(total_path)
                print("to:")
                print(total_destination)
                shutil.move(total_path, destination)
            else:
                if root_path != "":
                    files_to_remove = glob.glob(f"{total_path}{root_path}")
                    for file in files_to_remove:
                        info(f"Removing file: {file}")
                        os.remove(file)
                else:
                    shutil.rmtree(total_path)

info(f"Total size removed: {total_size/(1024*1024*1024):.2f} GB")