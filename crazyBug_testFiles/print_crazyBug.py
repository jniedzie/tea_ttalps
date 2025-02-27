import ROOT

input_path_unmerged_hadded = "skimmed_unmerged.root"
input_path_unmerged_hadded_safe = "skimmed_unmerged_safe.root"
input_path_merged = "skimmed_merged/output_0.root"
input_path_merged_safe = "skimmed_merged_safe/output_0.root"

input_path_unmerged = "skimmed_unmerged/"

def main():
    file_unmerged_hadded = ROOT.TFile.Open(input_path_unmerged_hadded)
    file_unmerged_hadded_safe = ROOT.TFile.Open(input_path_unmerged_hadded_safe)
    file_merged = ROOT.TFile.Open(input_path_merged)
    file_merged_safe = ROOT.TFile.Open(input_path_merged_safe)
    
    tree_unmerged_hadded = file_unmerged_hadded.Get("Events")
    tree_unmerged_hadded_safe = file_unmerged_hadded_safe.Get("Events")
    tree_merged = file_merged.Get("Events")
    tree_merged_safe = file_merged_safe.Get("Events")
    
    hist_unmerged_hadded = file_unmerged_hadded.Get("CutFlow/14_nGoodMediumBtaggedJets")
    hist_unmerged_hadded_safe = file_unmerged_hadded_safe.Get("CutFlow/14_nGoodMediumBtaggedJets")
    hist_merged = file_merged.Get("CutFlow/14_nGoodMediumBtaggedJets")
    hist_merged_safe = file_merged_safe.Get("CutFlow/14_nGoodMediumBtaggedJets")
    
    print("\nUnmerged hadded:")
    print(f"Events.GetEntries(): {tree_unmerged_hadded.GetEntries()}")
    print(f"CutFlow, 14_nGoodMediumBtaggedJets: {hist_unmerged_hadded.GetBinContent(1)}")
    
    print("\nUnmerged hadded safe:")
    print(f"Events.GetEntries(): {tree_unmerged_hadded_safe.GetEntries()}")
    print(f"CutFlow, 14_nGoodMediumBtaggedJets: {hist_unmerged_hadded_safe.GetBinContent(1)}")
    
    print("\nMerged:")
    print(f"Events.GetEntries(): {tree_merged.GetEntries()}")
    print(f"CutFlow, 14_nGoodMediumBtaggedJets: {hist_merged.GetBinContent(1)}")
    
    print("\nMerged safe:")
    print(f"Events.GetEntries(): {tree_merged_safe.GetEntries()}")
    print(f"CutFlow, 14_nGoodMediumBtaggedJets: {hist_merged_safe.GetBinContent(1)}")
    
    unmerged_entries_safeotal = 0
    unmerged_hist_safeotal = 0
    
    for i in range(10):
        file_unmerged = ROOT.TFile.Open(f"{input_path_unmerged}output_546{i}.root")
        tree_unmerged = file_unmerged.Get("Events")
        hist_unmerged = file_unmerged.Get("CutFlow/14_nGoodMediumBtaggedJets")
        
        unmerged_entries_safeotal += tree_unmerged.GetEntries()
        unmerged_hist_safeotal += hist_unmerged.GetBinContent(1)
        
        file_unmerged.Close()
    
    print("\nUnmerged:")
    print(f"Total number of entries: {unmerged_entries_safeotal}")
    print(f"Total number of nGoodMediumBtaggedJets: {unmerged_hist_safeotal}")
    

if __name__ == "__main__":
    main()