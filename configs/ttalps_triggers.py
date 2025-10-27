IsoMu24 = (
    "HLT_IsoMu24",
)
IsoMu27 = (
    "HLT_IsoMu27",
)
DoubleMu = (
    "HLT_DoubleL2Mu23NoVtx_2Cha",
    "HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed",
)
Ele32_WPTight = (
    "HLT_Ele32_WPTight_Gsf",
)

def get_IsoMu_trigger(year):
  if year == "2017":
    return IsoMu27
  return IsoMu24

def get_DoubleMu_trigger(year):
  if year != "2018":
    error(f"Double Mu trigger only implemented for 2018. No trigger given for year {year}")
    return
  return DoubleMu

def get_Ele_Tight_trigger(year):
  if year != "2018":
    error(f"Ele WO Tight trigger only implemented for 2018. No trigger given for year {year}")
    return
  return Ele32_WPTight

