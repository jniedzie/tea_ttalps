
#include "TTAlpsDimuonCuts.hpp"

#include "ExtensionsHelpers.hpp"
#include "TLorentzVector.h"

using namespace std;

TTAlpsDimuonCuts::TTAlpsDimuonCuts(){

  auto &config = ConfigManager::GetInstance();

  string selection = "SR";
  try {
    config.GetValue("dimuonSelection", selection);
  } catch (const Exception &e) {
    warn() << "Couldn't read dimuonSelection from config file - will use SR selection for LooseMuons" << endl;
  }
  dimuonSelection = selection;

  try {
    config.GetMap(dimuonSelection+"BaseCuts", dimuonVertexBaseCuts);
  } catch (const Exception &e) {
    info() << "Couldn't read " << dimuonSelection << "BaseCuts from config file - is needed for GoodLooseMuonVertex collections" << endl;
  }
  try {
    config.GetMap(dimuonSelection+"PATCuts", dimuonVertexPATCuts);
  } catch (const Exception &e) {
    info() << "Couldn't read " << dimuonSelection << "PATCuts from config file - is needed for GoodLooseMuonVertex collections" << endl;
  }
  try {
    config.GetMap(dimuonSelection+"PATDSACuts", dimuonVertexPATDSACuts);
  } catch (const Exception &e) {
    info() << "Couldn't read " << dimuonSelection << "PATDSACuts from config file - is needed for GoodLooseMuonVertex collections" << endl;
  }
  try {
    config.GetMap(dimuonSelection+"DSACuts", dimuonVertexDSACuts);
  } catch (const Exception &e) {
    info() << "Couldn't read " << dimuonSelection << "DSACuts from config file - is needed for GoodLooseMuonVertex collections" << endl;
  }

  using namespace std::placeholders;
  PassesCutsMap = {
    {"LLPnanoAODVertexCuts", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesLLPnanoAODVertexCuts(v); }},
    {"InvariantMassCut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesInvariantMassCut(v); }},
    {"ChargeCut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesChargeCut(v); }},
    {"DisplacedIsolationCut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesDisplacedIsolationCut(v); }},
    {"PFRelIsolationCut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesPFRelIsolationCut(v); }},
    {"HitsInFrontOfVertexCut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesHitsInFrontOfVertexCut(v); }},
    {"DPhiBetweenMuonpTAndLxyCut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesDPhiBetweenMuonpTAndLxyCut(v); }},
    {"DCACut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesDCACut(v); }},
    {"Chi2Cut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesChi2Cut(v); }},
    {"LxyCut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesLxyCut(v); }},
    {"CollinearityAngleCut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesCollinearityAngleCut(v); }},
    {"DeltaEtaCut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesDeltaEtaCut(v); }},
    {"DeltaPhiCut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesDeltaPhiCut(v); }},
    {"DeltaRCut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesDeltaRCut(v); }},
    {"DeltaPixelHitsCut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesDeltaPixelHitsCut(v); }}
  };
}

map<string, float> TTAlpsDimuonCuts::GetDimuonCategoryMap(string category) {
  if (category == "Pat") return dimuonVertexPATCuts;
  if (category == "PatDSA") return dimuonVertexPATDSACuts;
  if (category == "DSA") return dimuonVertexDSACuts;
  return {};
}

bool TTAlpsDimuonCuts::PassesCut(std::shared_ptr<NanoDimuonVertex> dimuonVertex, std::string cutName) {
  return PassesCutsMap[cutName](dimuonVertex);
}

bool TTAlpsDimuonCuts::PassesLLPnanoAODVertexCuts(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  if (!dimuonVertex->isValid()) return false;
  if ((float)dimuonVertex->Get("dca") > dimuonVertexBaseCuts["maxDCA"]) return false;
  return true;
}

bool TTAlpsDimuonCuts::PassesInvariantMassCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  float invMass = dimuonVertex->GetInvariantMass();
  if(dimuonVertexBaseCuts.find("maxInvariantMass") == dimuonVertexBaseCuts.end()) return true;

  if(invMass > dimuonVertexBaseCuts["maxInvariantMass"]) return false;
  if(invMass < dimuonVertexBaseCuts["minInvariantMass"]) return false;
  if(invMass > dimuonVertexBaseCuts["minJpsiMass"] && invMass < dimuonVertexBaseCuts["maxJpsiMass"]) return false;
  if(invMass > dimuonVertexBaseCuts["minpsiMass"] && invMass < dimuonVertexBaseCuts["maxpsiMass"]) return false;
  return true;
}

bool TTAlpsDimuonCuts::PassesChargeCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  if(dimuonVertex->GetDimuonChargeProduct() > dimuonVertexBaseCuts["maxChargeProduct"]) return false;
  return true;
}

bool TTAlpsDimuonCuts::PassesDisplacedIsolationCut(shared_ptr<NanoDimuonVertex> dimuonVertex, string isolationVariable) {
  string category = dimuonVertex->GetVertexCategory();
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  if(category == "DSA") return true;
  if((float)dimuonVertex->Get(isolationVariable+"1") > dimuonVertexCuts["max"+isolationVariable]) return false;
  if(category == "PatDSA") return true;
  if((float)dimuonVertex->Get(isolationVariable+"2") > dimuonVertexCuts["max"+isolationVariable]) return false;
  return true;
}

bool TTAlpsDimuonCuts::PassesPFRelIsolationCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  string category = dimuonVertex->GetVertexCategory();
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  if(category == "DSA") return true;
  if((float)dimuonVertex->Muon1()->Get("pfRelIso04_all") > dimuonVertexCuts["maxPFRelIso"]) return false;
  if(category == "PatDSA") return true;
  if((float)dimuonVertex->Muon2()->Get("pfRelIso04_all") > dimuonVertexCuts["maxPFRelIso"]) return false;
  return true;
}

bool TTAlpsDimuonCuts::PassesHitsInFrontOfVertexCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  string category = dimuonVertex->GetVertexCategory();
  if(category == "DSA") return true;
  auto dimuonVertexCuts = GetDimuonCategoryMap(category);
  float maxHits = max((float)dimuonVertex->Get("hitsInFrontOfVert1"),(float)dimuonVertex->Get("hitsInFrontOfVert2"));
  if(maxHits > dimuonVertexCuts["maxHitsInFrontOfVertex"]) return false;
  return true;
}

bool TTAlpsDimuonCuts::PassesDPhiBetweenMuonpTAndLxyCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  string category = dimuonVertex->GetVertexCategory();
  if(category == "Pat" || category == "DSA") return true;
  auto dimuonVertexCuts = GetDimuonCategoryMap(category);
  if(abs(dimuonVertex->GetDPhiBetweenMuonpTAndLxy(1)) > dimuonVertexCuts["maxpTLxyDPhi"]) return false;
  return true;
}

bool TTAlpsDimuonCuts::PassesDCACut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  if((float)dimuonVertex->Get("dca") > dimuonVertexCuts["maxDCA"]) return false;
  return true;
}

bool TTAlpsDimuonCuts::PassesChi2Cut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  if((float)dimuonVertex->Get("normChi2") > dimuonVertexCuts["maxChi2"]) return false;
  return true;
}

bool TTAlpsDimuonCuts::PassesLxyCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  if((float)dimuonVertex->GetLxyFromPV() < dimuonVertexCuts["minLxy"]) return false;
  return true;
}

bool TTAlpsDimuonCuts::PassesCollinearityAngleCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  if(abs(dimuonVertex->GetCollinearityAngle()) > dimuonVertexCuts["maxCollinearityAngle"]) return false;
  return true;
}

bool TTAlpsDimuonCuts::PassesDeltaEtaCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  auto category = dimuonVertex->GetVertexCategory();
  float deltaEta = dimuonVertex->GetDeltaEta();
  string cutName = "maxDEta";
  if(category == "DSA") {
    deltaEta = dimuonVertex->GetOuterDeltaEta();
    cutName = "maxOuterDR";
  }
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  if(deltaEta > dimuonVertexCuts[cutName]) return false;
  return true;
}

bool TTAlpsDimuonCuts::PassesDeltaPhiCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  auto category = dimuonVertex->GetVertexCategory();
  float deltaPhi = dimuonVertex->GetDeltaPhi();
  string cutName = "maxDPhi";
  if(category == "DSA") {
    deltaPhi = dimuonVertex->GetOuterDeltaPhi();
    cutName = "maxOuterDPhi";
  }
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  if(deltaPhi > dimuonVertexCuts[cutName]) return false;
  return true;
}

bool TTAlpsDimuonCuts::PassesDeltaRCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  auto category = dimuonVertex->GetVertexCategory();
  float deltaR = dimuonVertex->Get("dR");
  if(category == "DSA") deltaR = dimuonVertex->GetOuterDeltaR();
  if(category == "PatDSA") deltaR = dimuonVertex->Get("dRprox");
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  if(deltaR > dimuonVertexCuts["maxDR"]) return false;
  return true;
}

bool TTAlpsDimuonCuts::PassesDeltaPixelHitsCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  auto category = dimuonVertex->GetVertexCategory();
  if(category == "DSA" || category == "PatDSA") return true;
  auto dimuonVertexCuts = GetDimuonCategoryMap(category);
  if(dimuonVertex->GetDeltaPixelHits() > dimuonVertexCuts["maxDeltaPixelHits"]) return false;
  return true;
}
