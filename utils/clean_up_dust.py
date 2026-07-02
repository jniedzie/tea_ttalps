from ttalps_samples_list import dasBackgrounds2017, dasSignals2017, dasData2017
from ttalps_samples_list import dasBackgrounds2018, dasSignals2018, dasData2018
from ttalps_samples_list import dasBackgrounds2016preVFP, dasData2016preVFP, dasSignals2016preVFP
from ttalps_samples_list import dasBackgrounds2016postVFP, dasData2016postVFP, dasSignals2016postVFP
from ttalps_samples_list import dasBackgrounds2022preEE, dasData2022preEE, dasSignals2022preEE
from ttalps_samples_list import dasBackgrounds2022postEE, dasData2022postEE, dasSignals2022postEE
from ttalps_samples_list import dasBackgrounds2023postBPix, dasData2023postBPix, dasSignals2023postBPix
from ttalps_samples_list import dasBackgrounds2023preBPix, dasData2023preBPix, dasSignals2023preBPix
from ttalps_samples_list import dasBackgrounds, dasSignals, dasData

from Logger import error, info
import os
import shutil
import argparse
import glob
from pathlib import Path
import filecmp

parser = argparse.ArgumentParser()
parser.add_argument("--dry", action="store_true", default=False, help="Dry run.")
args = parser.parse_args()

# samples = dasSignals.keys()
samples = dasBackgrounds2023postBPix.keys()
# samples = dasData.keys()

compare_to_jalimena = False

base_path = f"/data/dust/user/{os.environ['USER']}/ttalps_cms"
# base_path_jalimena = f"/data/dust/user/jalimena/ttalps_cms"
base_path_jalimena = f"/data/dust/user/lrygaard/ttalps_cms"
# base_path_jalimena = f"/data/dust/group/cms/ttALPs-desy"
skim_jalimena = "skimmed_looseSemimuonic_v3_SR"

# skim = "skimmed_looseSemimuonic_v3_SR_noBTag"
skim = "skimmed_looseSemimuonic_v3_SR"

# hist_path = "" # Optional subdirectory
hist_path = "/histograms_SRDimuons_ABCD_ANv10_regionA"

# root_path = "" # Optional subdirectory
# root_path = "/*.root"
root_path = "/output*"

destination = "" # Optional: if destination is given directory will be moved not deleted
# destination = f"{skim}/histograms_SRDimuons_ABCD_ANv5"
# destination = f"skimmed_looseSemimuonic_v3_SR/histograms_SRDimuons_ABCD_ANv10_regionABCD"

dust_destination = "" # Optional: if destination is given directory will be moved not deleted
# dust_destination = "/data/dust/group/cms/ttALPs-desy/" 

def dirs_are_identical(dir1, dir2):
    comparison = filecmp.dircmp(dir1, dir2)

    if comparison.left_only or comparison.right_only or comparison.diff_files:
        return False

    return all(
        dirs_are_identical(f"{dir1}/{subdir}", f"{dir2}/{subdir}")
        for subdir in comparison.common_dirs
    )

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
    total_path_jalimena = f"{base_path_jalimena}/{sample}/{skim_jalimena}{hist_path}"

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

    root_files = glob.glob(f"{total_path}/*.root")

    if compare_to_jalimena:
        root_files_jalimena = glob.glob(f"{total_path_jalimena}/*.root")
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
                        if not args.dry:
                            os.remove(file)
            else:
                if not args.dry:
                    shutil.rmtree(total_path)
        elif (len(root_files_jalimena) == 0 and len(root_files) == 0):
            if dirs_are_identical(total_path, total_path_jalimena):
                info(f"directories are identical: {total_path} and {total_path_jalimena}")
                if not args.dry:
                    shutil.rmtree(total_path)
            else:
                error(f"directories are not identical: {total_path} and {total_path_jalimena}")

        else:
            error(f"not the same number of files in {total_path_jalimena}")

    elif destination != "":
        total_destination = Path(base_path) / sample / destination
        total_path = Path(total_path)
        print(f"moving:")
        print(total_path)
        print("to:")
        print(total_destination)
        if not args.dry:
            if total_destination.parent.exists():
                # Check if both are on the same filesystem
                same_fs = os.stat(total_path).st_dev == os.stat(total_destination.parent).st_dev

                # If they share the same base path (except last directory) and filesystem → rename
                same_base = total_path.parent == total_destination.parent
                if same_fs and same_base:
                    # total_path.rename(total_destination)
                    shutil.copytree(total_path, total_destination, dirs_exist_ok=True)
                else:
                    # shutil.move(total_path, total_destination)
                    shutil.copytree(total_path, total_destination, dirs_exist_ok=True)

    elif dust_destination != "":
        total_destination = f"{dust_destination}/{sample}/{skim}{hist_path}"
        # total_path = Path(total_path)
        print(f"copying:")
        print(total_path)
        print("to:")
        print(total_destination)
        if not args.dry:
            if not Path(total_destination).exists():
                os.makedirs(total_destination)

            if root_path == "":
                # Check if both are on the same filesystem
                same_fs = os.stat(total_path).st_dev == os.stat(Path(total_destination).parent).st_dev
                src = Path(total_path)
                dst = Path(total_destination)

                for item in src.iterdir():
                    target = dst / item.name
                    if item.is_dir():
                        shutil.copytree(item, target, dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, target)

            else: 
                files_to_remove = glob.glob(f"{total_path}{root_path}")
                for file in files_to_remove:
                    dust_file = file.replace(total_path, total_destination)
                    if Path(dust_file).exists():
                        error(f"Error: File {dust_file} already exists!")
                        continue
                    info(f"Copying file: {file} to {dust_file}")

                    shutil.copy(file,dust_file)

    elif root_path != "":
        files_to_remove = glob.glob(f"{total_path}{root_path}")
        for file in files_to_remove:
            info(f"Removing file: {file}")
            if not args.dry:
                os.remove(file)
    else:
        if not args.dry:
            shutil.rmtree(total_path)

info(f"Total size removed/moved: {total_size/(1024*1024*1024):.2f} GB")
