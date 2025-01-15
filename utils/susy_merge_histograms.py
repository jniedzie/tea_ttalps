from ttalps_samples_list import dasData2018, dasData2016_standard, dasData2017_standard, dasData2018_standard, dasData2022_standard, dasData2023_standard
import os
import re

base_path = "/nfs/dust/cms/user/jniedzie/susy_test"

# skim = "minimalCuts"
# skim = "minimalCuts_tighterMuons"
# skim = "minimalCuts_standardNanoAOD"
# skim = "minimalCuts_standardNanoAOD_tighterMuons"
# skim = "minimalCuts_muonPtCategories"
skim = "minimalCuts_standardNanoAOD_muonPtCategories"

dasSamples = {} 
# dasSamples.update(dasData2018)

dasSamples.update(dasData2016_standard)
dasSamples.update(dasData2017_standard)
dasSamples.update(dasData2018_standard)
dasSamples.update(dasData2022_standard)
dasSamples.update(dasData2023_standard)

def extract_year_from_path(path):
  # grab the 4 digits representing the year in the path with a regex (could look like SingleMuon2018C_hists.root -> 2018)
  year = re.search(r"\d{4}", path).group(0)
  return year

def main():
  
  to_merge_per_year = {}
  
  for directory in dasSamples.keys():
    input_path = f"{base_path}/{skim}/hists/{directory}/*.root"
    output_path = f"{base_path}/{skim}/{directory.split('/')[-1]}_hists.root"

    print(f"{directory=}")
    print(f"{output_path=}")
    
    os.system(f"rm {output_path}")
    os.system(f"hadd -f -j -k {output_path} {input_path}")
    
    year = extract_year_from_path(output_path)
    to_merge_per_year.setdefault(year, []).append(output_path)
    print(f"\n\nAdding for year merging: {year=}, {output_path=}\n\n")
    
  for year, paths in to_merge_per_year.items():
    output_path = paths[0].replace(f"{year}", f"_{year}")
    # if year is followed by a letter, we need to remove it from the output path
    output_path = re.sub(r"\d{4}[A-Z]", f"merged_{year}", output_path)
    
    print(f"\n\nMerging for year {year}: {paths=}, {output_path=}\n\n")
    os.system(f"rm {output_path}")
    os.system(f"hadd -f -j -k {output_path} {' '.join(paths)}")
    

if __name__ == "__main__":
  main()
