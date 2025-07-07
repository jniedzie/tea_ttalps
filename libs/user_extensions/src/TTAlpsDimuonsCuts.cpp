
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

  map<string, vector<float>> dimuonVertexCuts;
  try {
    config.GetMap(dimuonSelection+"Cuts", dimuonVertexCuts);
  } catch (const Exception &e) {
    warn() << "Couldn't read " << dimuonSelection << "Cuts from config file - is needed for good dimuon vertex collections" << endl;
  }
  // input vector of dimuon categories cut values should be in order PAT-PAT,PAT-DSA,DSA-DSA
  for (const auto& [cutName, cuts] : dimuonVertexCuts) {
    dimuonVertexPATCuts[cutName] = cuts[0];
    dimuonVertexPATDSACuts[cutName] = cuts[1];
    dimuonVertexDSACuts[cutName] = cuts[2];
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
    {"DeltaPixelHitsCut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesDeltaPixelHitsCut(v); }},
    {"BarrelDeltaEtaCut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesBarrelDeltaEtaCut(v); }},
    {"LogLxyCut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesLogLxyCut(v); }},
    {"LogLxyMinus1Cut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesLogLxyCut(v,&LogLxyMinus1); }},
    {"LogLxyMinus2Cut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesLogLxyCut(v,&LogLxyMinus2); }},
    {"LogLxyMinus3Cut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesLogLxyCut(v,&LogLxyMinus3); }},
    {"Chi2DCACut", [this](std::shared_ptr<NanoDimuonVertex> v) { return PassesChi2DCACut(v); }},
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
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  if (!dimuonVertex->IsValid()) return false;
  if ((float)dimuonVertex->Get("dca") > dimuonVertexCuts["maxDCA"]) return false;
  return true;
}

bool TTAlpsDimuonCuts::PassesInvariantMassCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  float invMass = dimuonVertex->GetInvariantMass();
  if(dimuonVertexCuts.find("maxInvariantMass") == dimuonVertexCuts.end()) return true;

  if(invMass > dimuonVertexCuts["maxInvariantMass"]) return false;
  if(invMass < dimuonVertexCuts["minInvariantMass"]) return false;
  if(invMass > dimuonVertexCuts["minJpsiMass"] && invMass < dimuonVertexCuts["maxJpsiMass"]) return false;
  if(invMass > dimuonVertexCuts["minpsiMass"] && invMass < dimuonVertexCuts["maxpsiMass"]) return false;
  return true;
}

bool TTAlpsDimuonCuts::PassesChargeCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  if(dimuonVertex->GetDimuonChargeProduct() > dimuonVertexCuts["maxChargeProduct"]) return false;
  return true;
}

bool TTAlpsDimuonCuts::PassesDisplacedIsolationCut(shared_ptr<NanoDimuonVertex> dimuonVertex, string isolationVariable) {
  string category = dimuonVertex->GetVertexCategory();
  auto dimuonVertexCuts = GetDimuonCategoryMap(category);
  if(category == "DSA") return true;
  if((float)dimuonVertex->Get(isolationVariable+"1") > dimuonVertexCuts["max"+isolationVariable]) return false;
  if(category == "PatDSA") return true;
  if((float)dimuonVertex->Get(isolationVariable+"2") > dimuonVertexCuts["max"+isolationVariable]) return false;
  return true;
}

bool TTAlpsDimuonCuts::PassesPFRelIsolationCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  string category = dimuonVertex->GetVertexCategory();
  auto dimuonVertexCuts = GetDimuonCategoryMap(category);
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

bool TTAlpsDimuonCuts::PassesLogLxyCut(shared_ptr<NanoDimuonVertex> dimuonVertex, float* logLxyMin) {
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  float minLogLxy = 0.;
  if (logLxyMin != nullptr) minLogLxy = *logLxyMin;
  else minLogLxy = dimuonVertexCuts["minLogLxy"];
  float logLxy = log10(dimuonVertex->GetLxyFromPV());
  if(logLxy < minLogLxy) return false;
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

bool TTAlpsDimuonCuts::PassesBarrelDeltaEtaCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  auto muon1eta = dimuonVertex->Muon1()->GetAs<float>("eta");
  auto muon2eta = dimuonVertex->Muon2()->GetAs<float>("eta");
  if(abs(muon1eta-muon2eta) > dimuonVertexCuts["maxDeltaEta"]) return false;
  return true;
}

bool TTAlpsDimuonCuts::PassesChi2DCACut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  if (dimuonVertexCuts["applyChi2DCA"] == 0.0) return true;

  auto logNormChi2 = TMath::Log10(float(dimuonVertex->Get("normChi2")));
  auto logDca = TMath::Log10(float(dimuonVertex->Get("dca")));
  float logNormChi2Min = 2 * logDca - 1.5;
  if (logNormChi2 < logNormChi2Min) return false;
  return true;
}
