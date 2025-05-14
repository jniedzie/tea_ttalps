from Logger import error

rhoBranchName = "fixedGridRhoFastjetAll"

def get_jec_era(year, sample):
    if not sample.startswith("collision_data"):
       return ""

    parts = sample.split("/")
    sample_type = parts[1]
    year_index = sample_type.find(year)
    if year_index == -1 or year_index + len(year) >= len(sample_type):
        error(f"Data era for sample {sample} could not be found. JET era set to MC.")
        return ""
    era = sample_type[year_index + len(year)]
    return "_Run"+era
