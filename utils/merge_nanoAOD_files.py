from ttalps_samples_list import dasSamples2018, dasData2018, QCD_dasBackgrounds2018, TT_dasBackgrounds2018, dasData2018_standard

import argparse
import glob
import os

base_path = "/data/dust/user/jniedzie/ttalps_cms"
# base_path = "/data/dust/user/lrygaard/ttalps_cms"

# skim = "skimmed_looseSemimuonic_v2"
skim = "skimmed_looseSemimuonic_v2_reproduce"

# sample_paths = dasSamples2018.keys()
sample_paths = dasData2018.keys()

input_pattern = "output_*.root"
output_pattern = "output_{}.root"

condor_commands = []

def get_args():
    parser = argparse.ArgumentParser(description="merger")
    parser.add_argument("--dry_run", action="store_true", default=False, help="dry run")
    parser.add_argument("--n", type=int, default=10, help="Number of files to merge into one")
    parser.add_argument("--condor", action="store_true", default=False, help="run on condor")
    args = parser.parse_args()
    return args


def get_file_paths(input_path):
    path_pattern = os.path.join(input_path, input_pattern)
    file_paths = glob.glob(path_pattern)
    print(f"Found {len(file_paths)} files matching pattern {path_pattern}")
    return file_paths


def get_file_name(index, output_path):
    output_filename = output_pattern.format(index)
    output_filename = os.path.join(output_path, output_filename)
    return output_filename


def run_on_condor(commands, dry_run=False):
    submit_file = "condor_submit_file.sub"
    
    # Create wrapper scripts for each job
    for idx, command in enumerate(commands):
        script_file = f"tmp/condor_command_{idx}.sh"
        with open(script_file, "w") as f:
            f.write("#!/bin/bash\n")
            f.write(command + "\n")
        os.chmod(script_file, 0o755)  # Make it executable

    # Create the Condor submit file
    with open(submit_file, "w") as f:
        f.write("universe = vanilla\n")
        f.write("getenv = True\n")  # Ensure environment variables are inherited
        f.write("request_memory = 8 GB\n")
        f.write("+JobFlavour = \"espresso\"\n")

        # Logging (separate files per job)
        if not dry_run:
            f.write("output = /dev/null\n")
            f.write("error = /dev/null\n")
            f.write("log = /dev/null\n")
        else:
            f.write("output = condor_output_$(Process).txt\n")
            f.write("error = condor_error_$(Process).txt\n")
            f.write("log = condor_log_$(Process).txt\n")

        f.write("\n")

        f.write("max_materialize = 5000\n")

        # Use a single queue submission for all jobs
        f.write("executable = tmp/condor_command_$(Process).sh\n")
        f.write(f"queue {len(commands)}\n")  # Submit all jobs in one go

    # Submit the jobs
    if not dry_run:
        os.system(f"condor_submit {submit_file}")
        os.system(f"rm {submit_file}")
    else:
        exit(0)
    
def merge_batch_of_files(files_to_merge, output_ntuple_counter, output_path, dry_run, condor):
    output_filename = get_file_name(output_ntuple_counter, output_path)

    command = f"python3 hadd_safe.py -f -j -k {output_filename} {' '.join(files_to_merge)}"

    if condor:
        condor_commands.append(command)
    elif dry_run:
        print(command)    
    else:
        os.system(command)


def merge_n_files(input_path, output_path, args):
    file_paths = get_file_paths(input_path)
    files_to_merge = []
    output_ntuple_counter = 0

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # merge files in batches of n_files_to_merge:
    for filename in file_paths:

        # if full, merge and move to the next batch:
        if len(files_to_merge) == args.n:
            merge_batch_of_files(files_to_merge, output_ntuple_counter, output_path, args.dry_run, args.condor)
            files_to_merge = []
            output_ntuple_counter += 1

        files_to_merge.append(filename)

    # merge any remaining files:
    if len(files_to_merge) != 0:
        merge_batch_of_files(files_to_merge, output_ntuple_counter, output_path, args.dry_run, args.condor)


def main():
    args = get_args()

    for path in sample_paths:
        input_path = f"{base_path}/{path}/{skim}/"
        output_path = f"{base_path}/{path}/{skim}_merged/"
        merge_n_files(input_path, output_path, args)


    if args.condor:
        run_on_condor(condor_commands, args.dry_run)

if __name__ == "__main__":
    main()
