import ROOT
import os

input_dir = "/data/dust/user/jniedzie/ttalps_cms/collision_data2018/SingleMuon2018A/skimmed_tmp/*.txt"
# input_path = "../crazyBugTest.txt"
# input_path = "../crazyBugTest_new.txt"
# input_path = "../skimmed_crazyBugTest_oneStep.txt"
input_path = "../crazyBugTest_fullCutFlow.txt"

skip_merging = True

def main():
    # batch mode
    ROOT.gROOT.SetBatch(True)
    
    if not skip_merging:
        command = f"rm {input_path}; cat {input_dir} > {input_path}"
        print("Executing command: ", command)
        os.system(command)
        print("Command executed")

    ROOT.gStyle.SetLineScalePS(1)

    hist = ROOT.TH1F("hist", "hist", 100, 0, 1)
    
    n_value_error = 0
    n_index_error = 0
    n_not_passing_goldenJson = 0
    n_not_passing_met_filters = 0

    n_initial_total = 0

    n_pre_total = 0
    n_post_total = 0

    cut_flow_total = {}

    with open(input_path, "r") as f:
        lines = f.readlines()

        for line in lines:
            parts = line.split(":")

            try:
                path = parts[0]
                
                cut_flow = {}
                
                for i in range(1, int((len(parts) - 1)/2)):
                    key = parts[2*i - 1]
                    value = float(parts[2*i])
                    cut_flow[key] = value
                    
                    if key not in cut_flow_total:
                        cut_flow_total[key] = value
                    else:
                        cut_flow_total[key] += value
                        
                n_initial = cut_flow["0_initial"]
                n_goldenJson = cut_flow["1_goldenJson"]
                n_met_filters = cut_flow["3_metFilters"]
                n_additional_muons = cut_flow["4_nAdditionalLooseMuons"]
                
                n_initial_total += n_initial
                n_pre_total += n_met_filters
                n_post_total += n_additional_muons
                
                if n_goldenJson == 0:
                    n_not_passing_goldenJson += 1
                    continue
                
                if n_met_filters == 0:
                    n_not_passing_met_filters += 1
                    continue
                
                eff = n_additional_muons/n_met_filters
                
                if "nan" in parts[1]:
                    eff = 0.99
                
                if eff < 0 or eff > 1:
                    print(f"eff: {eff}")

                hist.Fill(eff)
            except IndexError:
                n_index_error += 1
                print(f"Index error path: {path}, line: {line}")
                exit()
                
            except ValueError:
                n_value_error += 1
                print(f"Value error path: {path}, line: {line}")
                exit()

    print(f"n_value_error: {n_value_error}")
    print(f"n_index_error: {n_index_error}")
    print(f"n_not_passing_goldenJson: {n_not_passing_goldenJson}")
    print(f"n_not_passing_met_filters: {n_not_passing_met_filters}")

    print(f"\nn_initial: {n_initial_total}")
    print(f"n_pre_total: {n_pre_total}")
    print(f"n_post_total: {n_post_total}")
    print(f"Eff: {n_post_total/float(n_pre_total)}")

    print("\nCut flow:")
    for key, value in cut_flow_total.items():
        print(f"{key}: {value}")

    c = ROOT.TCanvas("c", "c", 800, 600)
    
    ROOT.gPad.SetLogy()
    hist.Sumw2()
    hist.SetTitle("Crazy bug test")
    hist.GetXaxis().SetTitle("#epsilon^{cut}_{#mu}")
    hist.GetYaxis().SetTitle("N_{files}")
    hist.Draw()
    hist.GetXaxis().SetRangeUser(0.0, 1.0)
        
    c.SaveAs("../crazyBugTest.pdf")


if __name__ == '__main__':
    main()
