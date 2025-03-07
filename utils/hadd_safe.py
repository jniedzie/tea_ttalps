import ROOT
import argparse
import sys
import glob
import os
import uuid

username = os.environ["USER"]
tmp_path = f"/data/dust/user/{username}/tmp/"

def get_missing_branches(input_files):
    all_trees = {}

    # First pass: Collect all tree names and their branches from all files
    for filename in input_files:
        file = ROOT.TFile.Open(filename)
        if not file or file.IsZombie():
            print(f"Warning: Skipping {filename} (corrupted or unreadable)")
            continue

        for key in file.GetListOfKeys():
            obj = key.ReadObj()
            if obj.InheritsFrom("TTree"):
                tree_name = obj.GetName()
                branches = set(branch.GetName() for branch in obj.GetListOfBranches())
                if tree_name not in all_trees:
                    all_trees[tree_name] = set()
                all_trees[tree_name].update(branches)

        file.Close()

    # Second pass: Identify missing branches in any file
    missing_branches = {tree: set() for tree in all_trees}

    for filename in input_files:
        file = ROOT.TFile.Open(filename)
        if not file or file.IsZombie():
            continue

        for tree_name, all_branches in all_trees.items():
            obj = file.Get(tree_name)
            if not obj or not obj.InheritsFrom("TTree"):
                missing_branches[tree_name].update(all_branches)
            else:
                branches = set(branch.GetName() for branch in obj.GetListOfBranches())
                missing_branches[tree_name].update(all_branches - branches)

        file.Close()

    # Convert sets to lists for output
    return {tree: list(missing) for tree, missing in missing_branches.items() if missing}


def copy_directory(source_dir, target_dir):
    target_dir.cd()
    for key in source_dir.GetListOfKeys():
        obj = key.ReadObj()
        if obj.InheritsFrom("TDirectoryFile"):
            new_dir = target_dir.mkdir(obj.GetName())
            copy_directory(obj, new_dir)
        else:
            obj.Write()


def create_filtered_files(input_files, missing_branches_per_tree):
    temp_files = []

    for filename in input_files:
        file = ROOT.TFile.Open(filename)
        if not file or file.IsZombie():
            print(f"Warning: Skipping {filename} (corrupted or unreadable)")
            continue

        random_string = str(uuid.uuid4().hex[:30])        
        temp_filename = f"{tmp_path}/filtered_{random_string}.root"
        temp_files.append(temp_filename)
        temp_file = ROOT.TFile(temp_filename, "RECREATE")

        for key in file.GetListOfKeys():
            obj = key.ReadObj()
            if obj.InheritsFrom("TTree"):
                tree_name = obj.GetName()
                tree = file.Get(tree_name)

                temp_file.cd()
                tree.SetBranchStatus("*", 1)  # Enable all branches first
                if tree_name in missing_branches_per_tree:
                    for branch_name in missing_branches_per_tree[tree_name]:
                        if tree.GetBranch(branch_name):
                            tree.SetBranchStatus(branch_name, 0)  # Disable missing branches

                new_tree = tree.CloneTree(0)  # Create an empty clone
                for i in range(tree.GetEntries()):
                    tree.GetEntry(i)
                    new_tree.Fill()

                new_tree.Write()
            elif obj.InheritsFrom("TDirectoryFile"):
                new_dir = temp_file.mkdir(obj.GetName())
                copy_directory(obj, new_dir)
            else:
                temp_file.cd()
                obj.Write()

        temp_file.Close()
        file.Close()

    return temp_files


def main():
    parser = argparse.ArgumentParser(description="Safe version of hadd for merging ROOT files.")
    parser.add_argument("output_file", type=str, help="Output ROOT file.")
    parser.add_argument("input_files", type=str, nargs="+", help="Input ROOT files (accepts wildcards).")
    args, unknown_args = parser.parse_known_args()

    input_files = []
    hadd_flags = unknown_args  # Capture all unrecognized arguments as hadd flags
    
    for item in args.input_files:
        if item.startswith("-"):  # Identify hadd flags
            hadd_flags.append(item)
        else:
            input_files.extend(glob.glob(item))
    
    if not input_files:
        print("Error: No input files found.")
        sys.exit(1)

    missing_branches_per_tree = get_missing_branches(input_files)

    print("Missing branches:")
    for tree, missing in missing_branches_per_tree.items():
        print(f"  {tree}: {', '.join(missing)}")

    filtered_files = create_filtered_files(input_files, missing_branches_per_tree)

    hadd_command = ["hadd"] + hadd_flags + [args.output_file] + filtered_files
    print("Running hadd command:")
    print(" ".join(hadd_command))
    os.system(" ".join(hadd_command))

    for filename in filtered_files:
        os.remove(filename)


if __name__ == "__main__":
    main()
