
import json
import math


# chi2/ndof = 0.678413
# Year            Pt Bin  Fit(0.0)           Fit(1.0)     
data = [
    {"Year":"2016postVFP",     "Pt":3,       "Fit0":(1.58,0.13),        "Fit1":(0.84,0.11)},       
    {"Year":"2016postVFP",     "Pt":30,      "Fit0":(1.37,0.11),        "Fit1":(0.63,0.08)},       
    {"Year":"2016postVFP",     "Pt":60,      "Fit0":(1.40,0.14),        "Fit1":(0.66,0.12)},       
    
    {"Year":"2016preVFP",      "Pt":3,       "Fit0":(1.07,0.12),        "Fit1":(0.32,0.10)},       
    {"Year":"2016preVFP",      "Pt":30,      "Fit0":(1.17,0.11),        "Fit1":(0.43,0.08)},       
    {"Year":"2016preVFP",      "Pt":60,      "Fit0":(0.98,0.12),        "Fit1":(0.24,0.10)}, 

    {"Year":"2017",            "Pt":3,       "Fit0":(1.54,0.09),        "Fit1":(0.80,0.07)},       
    {"Year":"2017",            "Pt":30,      "Fit0":(1.13,0.08),        "Fit1":(0.39,0.05)},       
    {"Year":"2017",            "Pt":60,      "Fit0":(1.10,0.09),        "Fit1":(0.36,0.06)},   

    {"Year":"2018",            "Pt":3,       "Fit0":(1.35,0.09),        "Fit1":(0.61,0.08)},       
    {"Year":"2018",            "Pt":30,      "Fit0":(1.28,0.08),        "Fit1":(0.53,0.04)},       
    {"Year":"2018",            "Pt":60,      "Fit0":(0.99,0.09),        "Fit1":(0.25,0.05)},  

    {"Year":"2022postEE",      "Pt":3,       "Fit0":(1.46,0.13),        "Fit1":(0.72,0.12)},       
    {"Year":"2022postEE",      "Pt":30,      "Fit0":(1.32,0.11),        "Fit1":(0.58,0.08)},       
    {"Year":"2022postEE",      "Pt":60,      "Fit0":(1.13,0.11),        "Fit1":(0.38,0.09)},   

    {"Year":"2022preEE",       "Pt":3,       "Fit0":(1.28,0.18),        "Fit1":(0.54,0.18)},       
    {"Year":"2022preEE",       "Pt":30,      "Fit0":(1.33,0.14),        "Fit1":(0.59,0.12)},       
    {"Year":"2022preEE",       "Pt":60,      "Fit0":(1.09,0.14),        "Fit1":(0.35,0.12)},       

    {"Year":"2023postBPix",    "Pt":3,       "Fit0":(1.31,0.17),        "Fit1":(0.57,0.15)},       
    {"Year":"2023postBPix",    "Pt":30,      "Fit0":(1.09,0.13),        "Fit1":(0.35,0.10)},       
    {"Year":"2023postBPix",    "Pt":60,      "Fit0":(1.06,0.18),        "Fit1":(0.32,0.17)},       
    
    {"Year":"2023preBPix",     "Pt":3,       "Fit0":(1.91,0.14),        "Fit1":(1.16,0.13)},       
    {"Year":"2023preBPix",     "Pt":30,      "Fit0":(1.55,0.11),        "Fit1":(0.81,0.08)},       
    {"Year":"2023preBPix",     "Pt":60,      "Fit0":(1.22,0.13),        "Fit1":(0.48,0.11)},
]

# data = [
#     {"Year":"2016postVFP","Pt":3,"Fit0":(1.81,0.17),"Fit1":(0.94,0.15)},
#     {"Year":"2016postVFP","Pt":30,"Fit0":(1.48,0.14),"Fit1":(0.61,0.09)},
#     {"Year":"2016postVFP","Pt":60,"Fit0":(1.47,0.17),"Fit1":(0.61,0.14)},
#     {"Year":"2016preVFP","Pt":3,"Fit0":(1.11,0.14),"Fit1":(0.24,0.10)},
#     {"Year":"2016preVFP","Pt":30,"Fit0":(1.26,0.13),"Fit1":(0.40,0.08)},
#     {"Year":"2016preVFP","Pt":60,"Fit0":(1.16,0.15),"Fit1":(0.29,0.11)},
#     {"Year":"2017","Pt":3,"Fit0":(1.74,0.12),"Fit1":(0.87,0.08)},
#     {"Year":"2017","Pt":30,"Fit0":(1.39,0.11),"Fit1":(0.53,0.06)},
#     {"Year":"2017","Pt":60,"Fit0":(1.31,0.13),"Fit1":(0.44,0.08)},
#     {"Year":"2018","Pt":3,"Fit0":(1.62,0.11),"Fit1":(0.75,0.07)},
#     {"Year":"2018","Pt":30,"Fit0":(1.46,0.11),"Fit1":(0.59,0.05)},
#     {"Year":"2018","Pt":60,"Fit0":(1.12,0.11),"Fit1":(0.25,0.05)},
#     {"Year":"2022postEE","Pt":3,"Fit0":(1.57,0.15),"Fit1":(0.70,0.12)},
#     {"Year":"2022postEE","Pt":30,"Fit0":(1.45,0.13),"Fit1":(0.59,0.08)},
#     {"Year":"2022postEE","Pt":60,"Fit0":(1.23,0.14),"Fit1":(0.36,0.09)},
#     {"Year":"2022preEE","Pt":3,"Fit0":(1.32,0.21),"Fit1":(0.45,0.19)},
#     {"Year":"2022preEE","Pt":30,"Fit0":(1.48,0.17),"Fit1":(0.62,0.14)},
#     {"Year":"2022preEE","Pt":60,"Fit0":(1.27,0.19),"Fit1":(0.40,0.15)},
#     {"Year":"2023postBPix","Pt":3,"Fit0":(1.51,0.21),"Fit1":(0.64,0.19)},
#     {"Year":"2023postBPix","Pt":30,"Fit0":(1.23,0.14),"Fit1":(0.36,0.11)},
#     {"Year":"2023postBPix","Pt":60,"Fit0":(1.22,0.24),"Fit1":(0.35,0.21)},
#     {"Year":"2023preBPix","Pt":3,"Fit0":(2.11,0.18),"Fit1":(1.24,0.16)},
#     {"Year":"2023preBPix","Pt":30,"Fit0":(1.69,0.14),"Fit1":(0.83,0.10)},
#     {"Year":"2023preBPix","Pt":60,"Fit0":(1.31,0.16),"Fit1":(0.44,0.12)}
# ]

pt_edges = [3.0, 30.0, 60.0, "inf"]

for year in set(d['Year'] for d in data):
    year_data = [d for d in data if d['Year'] == year]
    
    # Build resonance binning (0 and 1)
    resonance_content = []
    for res in [0,1]:
        pt_content = []
        for i, pt_min in enumerate(pt_edges[:-1]):
            pt_max = pt_edges[i+1]
            # Find matching data
            match = next((d for d in year_data if d['Pt']==pt_min), None)
            if match:
                SF, unc = match[f"Fit{res}"]
                pt_content.append({
                    "nodetype": "category",
                    "input": "scale_factors",
                    "content": [
                        {"key": "nominal", "value": SF},
                        {"key": "up", "value": SF + unc},
                        {"key": "down", "value": SF - unc}
                    ]
                })
        resonance_content.append({
            "nodetype": "binning",
            "input": "pt",
            "edges": pt_edges,
            "content": pt_content,
            "flow": "error"
        })
    
    # Final JSON structure
    json_structure = {
        "schema_version": 2,
        "corrections": [
            {
                "name": "dimuonEff_PatDSA",
                "description": "Scale factors for PAT-DSA dimuon efficiency",
                "version": 1,
                "inputs": [
                    {"name": "resonance","type":"real","description":"Resonant (1) or nonresonant (0) dimuon"},
                    {"name": "pt","type":"real","description":"Dimuon pt of the PAT-DSA dimuon candidate"},
                    {"name": "scale_factors","type":"string","description":"Choose nominal scale factor or one of the uncertainties"}
                ],
                "output": {"name":"weight","type":"real","description":"Output scale factor (nominal) or uncertainty"},
                "data": {
                    "nodetype": "binning",
                    "input": "resonance",
                    "edges": [0.0,1.0,2.0],
                    "content": resonance_content,
                    "flow": "error"
                }
            }
        ],
    }

    # filename = f"{year}_scale_factors.json"
    filename = f"../data/dimuonEffSFs_ANv3/dimuonEffSFs{year}_PatDSA_pt_irr_v3.json"

    with open(filename, "w") as f:
        json.dump(json_structure, f, indent=4)

print("Nested binning JSON files created!")

# import json
# import glob

# # Loop over all files matching the pattern
# for filename in glob.glob("../data/dimuonEffSFs_ANv3/dimuonEffSFs*_DSA_pt_irr_v3.json"):
#     with open(filename, "r") as f:
#         content = json.load(f)
    
#     # Loop over all corrections
#     for corr in content.get("corrections", []):
#         # Update the name
#         if corr.get("name") == "dimuonEff_DSA_pt":
#             corr["name"] = "dimuonEff_DSA"
        
#         # Update the inputs
#         for inp in corr.get("inputs", []):
#             if inp.get("name") == "DSA_pt_irr":
#                 inp["name"] = "pt"
#                 inp["description"] = "Dimuon pt of the DSA-DSA dimuon candidate"
        
#         # Update the data input
#         if "data" in corr and corr["data"].get("input") == "DSA_pt_irr":
#             corr["data"]["input"] = "pt"
    
#     # Save the updated JSON back (overwrite)
#     with open(filename, "w") as f:
#         json.dump(content, f, indent=4)

#     print(f"Updated {filename}")

# print("All files updated successfully!")
