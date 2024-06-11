import glob
import os

# input_path = "/eos/cms/store/cmst3/group/lightbylight/Pranati/Final_afterTrigger/Data/Data_29thJune"
# input_pattern = "ntuples_loose_selections_*.root"

# input_base_path = "/nfs/dust/cms/user/lrygaard/ttalps_cms/backgrounds2018/"
input_base_path = "/nfs/dust/cms/user/lrygaard/ttalps_cms/signals/"
input_dataset = "tta_mAlp-1GeV_ctau-1e-5mm"
# input_dataset = "QCD_Pt-800To1000"
# input_path = input_base_path+input_dataset+"/LLPnanoAODv2/"
input_path = input_base_path+input_dataset+"/skimmed_looseSemimuonic_SRmuonic_Segmentv1_unmerged/"
# input_pattern = input_dataset+"*.root"
input_pattern = "output_*.root"

# output_path = input_base_path+input_dataset+"/LLPnanoAODv2merged/"
output_path = input_base_path+input_dataset+"/skimmed_looseSemimuonic_SRmuonic_Segmentv1/"
output_pattern = input_dataset+"_{}.root"

n_files_to_merge = 30


def get_file_paths():
    path_pattern = os.path.join(input_path, input_pattern)
    file_paths = glob.glob(path_pattern)
    print(f"Found {len(file_paths)} files matching pattern {path_pattern}")
    return file_paths


def get_file_name(index):
    output_filename = output_pattern.format(index)
    output_filename = os.path.join(output_path, output_filename)
    return output_filename


def merge_batch_of_files(files_to_merge, output_ntuple_counter):
    output_filename = get_file_name(output_ntuple_counter)
    os.system(f"hadd -f -j -k {output_filename} {' '.join(files_to_merge)}")


def merge_n_files():
    file_paths = get_file_paths()
    files_to_merge = []
    output_ntuple_counter = 0

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # merge files in batches of n_files_to_merge:
    for filename in file_paths:

        # if full, merge and move to the next batch:
        if len(files_to_merge) == n_files_to_merge:
            merge_batch_of_files(files_to_merge, output_ntuple_counter)
            files_to_merge = []
            output_ntuple_counter += 1

        files_to_merge.append(filename)

    # merge any remaining files:
    if len(files_to_merge) != 0:
        merge_batch_of_files(files_to_merge, output_ntuple_counter)


def main():
    merge_n_files()


if __name__ == "__main__":
    main()
