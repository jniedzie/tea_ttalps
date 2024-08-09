
#include "TTAlpsDimuonSelections.hpp"

#include "ExtensionsHelpers.hpp"
#include "TLorentzVector.h"

using namespace std;

TTAlpsDimuonSelections::TTAlpsDimuonSelections(){

  auto &config = ConfigManager::GetInstance();

  string selection = "SR";
  try {
    config.GetValue("objectSelection", selection);
  } catch (const Exception &e) {
    info() << "Couldn't read objectSelection from config file - will use SR selection for LooseMuons" << endl;
  }
  objectSelection = selection;

  try {
    config.GetMap(objectSelection+"dimuonVertexBaseCuts", dimuonVertexBaseCuts);
  } catch (const Exception &e) {
    info() << "Couldn't read dimuonVertexBaseCuts from config file - is needed for GoodLooseMuonVertex collections" << endl;
  }
  try {
    config.GetMap(objectSelection+"dimuonVertexPATCuts", dimuonVertexPATCuts);
  } catch (const Exception &e) {
    info() << "Couldn't read dimuonVertexPATCuts from config file - is needed for GoodLooseMuonVertex collections" << endl;
  }
  try {
    config.GetMap(objectSelection+"dimuonVertexPATDSACuts", dimuonVertexPATDSACuts);
  } catch (const Exception &e) {
    info() << "Couldn't read dimuonVertexPATDSACuts from config file - is needed for GoodLooseMuonVertex collections" << endl;
  }
  try {
    config.GetMap(objectSelection+"dimuonVertexDSACuts", dimuonVertexDSACuts);
  } catch (const Exception &e) {
    info() << "Couldn't read dimuonVertexDSACuts from config file - is needed for GoodLooseMuonVertex collections" << endl;
  }
}

map<string, float> TTAlpsDimuonSelections::GetDimuonCategoryMap(string category) {
  if (category == "Pat") return dimuonVertexPATCuts;
  if (category == "PatDSA") return dimuonVertexPATDSACuts;
  if (category == "DSA") return dimuonVertexDSACuts;
  return {};
}

bool TTAlpsDimuonSelections::PassesLLPnanoAODVertexCuts(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  if (!dimuonVertex->isValid()) return false;
  if ((float)dimuonVertex->Get("dca") > dimuonVertexBaseCuts["maxDCA"]) return false;
  return true;
}

bool TTAlpsDimuonSelections::PassesInvariantMassCuts(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  float invMass = dimuonVertex->GetInvariantMass();
  if(dimuonVertexBaseCuts.find("maxInvariantMass") == dimuonVertexBaseCuts.end()) return true;

  if(objectSelection == "SR") {
    if(invMass > dimuonVertexBaseCuts["maxInvariantMass"]) return false;
    if(invMass > dimuonVertexBaseCuts["minJpsiMass"] && invMass < dimuonVertexBaseCuts["maxJpsiMass"]) return false;
    if(invMass > dimuonVertexBaseCuts["minpsiMass"] && invMass < dimuonVertexBaseCuts["maxpsiMass"]) return false;
  }
  if(objectSelection == "JPsi") {
    if(invMass < dimuonVertexBaseCuts["minJpsiMass"]) return false;
    if(invMass > dimuonVertexBaseCuts["maxJpsiMass"]) return false;
  }
  return true;
}

bool TTAlpsDimuonSelections::PassesChargeCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  if(dimuonVertex->GetDimuonChargeProduct() > dimuonVertexBaseCuts["maxChargeProduct"]) return false;
  return true;
}

bool TTAlpsDimuonSelections::PassesDisplacedIsolationCut(shared_ptr<NanoDimuonVertex> dimuonVertex, string isolationVariable) {
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  if((float)dimuonVertex->Get(isolationVariable+"1") > dimuonVertexCuts["max"+isolationVariable]) return false;
  if((float)dimuonVertex->Get(isolationVariable+"2") > dimuonVertexCuts["max"+isolationVariable]) return false;
  return true;
}

bool TTAlpsDimuonSelections::PassesHitsInFrontOfVertexCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  string category = dimuonVertex->GetVertexCategory();
  if(category == "DSA") return true;
  auto dimuonVertexCuts = GetDimuonCategoryMap(category);
  float maxHits = max((float)dimuonVertex->Get("hitsInFrontOfVert1"),(float)dimuonVertex->Get("hitsInFrontOfVert2"));
  if(maxHits > dimuonVertexCuts["maxHitsInFrontOfVertex"]) return false;
  return true;
}

bool TTAlpsDimuonSelections::PassesDPhiBetweenMuonpTAndLxyCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  string category = dimuonVertex->GetVertexCategory();
  if(category == "Pat" || category == "DSA") return true;
  auto dimuonVertexCuts = GetDimuonCategoryMap(category);
  if(abs(dimuonVertex->GetDPhiBetweenMuonpTAndLxy(1)) > dimuonVertexCuts["maxpTLxyDPhi"]) return false;
  return true;
}

bool TTAlpsDimuonSelections::PassesDCACut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  if((float)dimuonVertex->Get("dca") > dimuonVertexCuts["maxDCA"]) return false;
  return true;
}

bool TTAlpsDimuonSelections::PassesChi2Cut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  if((float)dimuonVertex->Get("normChi2") > dimuonVertexCuts["maxChi2"]) return false;
  return true;
}

bool TTAlpsDimuonSelections::PassesVxyCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  if((float)dimuonVertex->Get("vxy") < dimuonVertexCuts["minVxy"]) return false;
  return true;
}

bool TTAlpsDimuonSelections::PassesCollinearityAngleCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  if(abs(dimuonVertex->GetCollinearityAngle()) > dimuonVertexCuts["maxCollinearityAngle"]) return false;
  return true;
}

bool TTAlpsDimuonSelections::PassesDeltaEtaCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
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

bool TTAlpsDimuonSelections::PassesDeltaPhiCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  auto category = dimuonVertex->GetVertexCategory();
  float deltaPhi = dimuonVertex->GetDeltaPhi();
  string cutName = "maxDPhi";
  if(category == "DSA") {
    deltaPhi = dimuonVertex->GetOuterDeltaPhi();
    cutName = "maxOuterDR";
  }
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  if(deltaPhi > dimuonVertexCuts[cutName]) return false;
  return true;
}

bool TTAlpsDimuonSelections::PassesDeltaRCut(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  auto category = dimuonVertex->GetVertexCategory();
  float deltaR = dimuonVertex->Get("dR");
  if(category == "DSA") deltaR = dimuonVertex->GetOuterDeltaR();
  if(category == "PatDSA") deltaR = dimuonVertex->Get("dRprox");
  auto dimuonVertexCuts = GetDimuonCategoryMap(dimuonVertex->GetVertexCategory());
  if(deltaR > dimuonVertexCuts["maxDR"]) return false;
  return true;
}

bool TTAlpsDimuonSelections::PassesDeltaPixelHits(shared_ptr<NanoDimuonVertex> dimuonVertex) {
  auto category = dimuonVertex->GetVertexCategory();
  if(category == "DSA" || category == "PatDSA") return true;
  auto dimuonVertexCuts = GetDimuonCategoryMap(category);
  if(dimuonVertex->GetDeltaPixelHits() > dimuonVertexCuts["maxDeltaPixelHits"]) return false;
  return true;
}
