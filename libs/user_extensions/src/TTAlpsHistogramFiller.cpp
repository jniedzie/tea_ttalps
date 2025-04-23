#include "TTAlpsHistogramFiller.hpp"

#include "ConfigManager.hpp"
#include "ExtensionsHelpers.hpp"
#include "TTAlpsCuts.hpp"
#include "UserExtensionsHelpers.hpp"

using namespace std;

TTAlpsHistogramFiller::TTAlpsHistogramFiller(shared_ptr<HistogramsHandler> histogramsHandler_) : histogramsHandler(histogramsHandler_) {
  eventProcessor = make_unique<EventProcessor>();
  nanoEventProcessor = make_unique<NanoEventProcessor>();
  auto &config = ConfigManager::GetInstance();

  try {
    config.GetMap("triggerSets", triggerSets);
    for (auto it = triggerSets.begin(); it != triggerSets.end(); ++it) triggerNames.push_back(it->first);
  } catch (const Exception &e) {
    warn() << "Couldn't read triggerSets from config file ";
    warn() << "(which may be fine if you're not trying to apply trigger selection)" << endl;
  }

  try {
    config.GetHistogramsParams(defaultHistVariables, "defaultHistParams");
  } catch (const Exception &e) {
    warn() << "Couldn't read defaultHistParams from config file - no default histograms will be included" << endl;
  }
  try {
    config.GetMap("muonMatchingParams", muonMatchingParams);
  } catch (const Exception &e) {
    warn() << "Couldn't read muonMatchingParams from config file - no muon matching methods will be applied to muon collections" << endl;
  }
  try {
    config.GetPair("muonVertexCollection", muonVertexCollection);
  } catch (const Exception &e) {
    info() << "Couldn't read muonVertexCollection from config file - no muon vertex collection histograms will be filled" << endl;
  }
  try {
    config.GetValue("muonVertexCollectionInput", muonVertexCollectionInput);
  } catch (const Exception &e) {
    warn() << "Couldn't read muonVertexCollectionInput from config file - using first defined muonMatchingParams vertex collection as default" << endl;
    string matchingMethod = muonMatchingParams.begin()->first;
    muonVertexCollectionInput = "LooseMuonsVertex" + matchingMethod + "Match";
  }
  try {
    config.GetValue("year", year);
  } catch (const Exception &e) {
    info() << "Couldn't read year from config file - will assume year 2018" << endl;
    year = "2018";
  }
}

TTAlpsHistogramFiller::~TTAlpsHistogramFiller() {}

/// --------- Help Functions--------- ///

bool TTAlpsHistogramFiller::EndsWithTriggerName(string name) {
  string lastPart = name.substr(name.rfind("_") + 1);
  return find(triggerNames.begin(), triggerNames.end(), lastPart) != triggerNames.end();
}

/// --------- Default Histograms --------- ///
/// ----- flag: runDefaultHistograms ----- ///

void TTAlpsHistogramFiller::FillDefaultVariables(const shared_ptr<Event> event) {
  for (auto &[title, params] : defaultHistVariables) {
    string collectionName = params.collection;
    string branchName = params.variable;

    float value;

    if (collectionName == "Event") {
      if (branchName[0] == 'n') {
        value = event->GetCollection(branchName.substr(1))->size();
      } else {
        value = event->GetAs<float>(branchName);
      }
      histogramsHandler->Fill(title, value);
    } else {
      auto collection = event->GetCollection(collectionName);
      if (branchName == "leadingPt") {
        auto object = eventProcessor->GetMaxPtObject(event, collectionName);
        if (!object) continue;
        value = object->GetAs<float>("pt");
        histogramsHandler->Fill(title, value);
      } else if (branchName == "subleadingPt") {
        auto object = eventProcessor->GetSubleadingPtObject(event, collectionName);
        if (!object) continue;
        value = object->GetAs<float>("pt");
        histogramsHandler->Fill(title, value);
      } else {
        for (auto object : *collection) {
          value = object->GetAs<float>(branchName);
          histogramsHandler->Fill(title, value);
        }
      }
    }
  }
}

/// --------- NormCheck Histogram --------- ///

void TTAlpsHistogramFiller::FillNormCheck() { histogramsHandler->Fill("Event_normCheck", 0.5); }

/// --------- NormCheck Histogram --------- ///

void TTAlpsHistogramFiller::FillDataCheck(const shared_ptr<Event> event) {
  histogramsHandler->Fill("Event_isData", nanoEventProcessor->IsDataEvent(asNanoEvent(event)));
}

/// --------- LooseMuons Histograms --------- ///
/// ----- flag: runLLPNanoAODHistograms ----- ///

void TTAlpsHistogramFiller::FillCustomTTAlpsVariablesForLooseMuons(const shared_ptr<Event> event) {
  if (muonMatchingParams.empty()) return;

  bool muonVertexCollectionInput_filled = false;
  for (auto &[matchingMethod, param] : muonMatchingParams) {
    string muonCollectionName = "LooseMuons" + matchingMethod + "Match";
    FillLooseMuonsHistograms(event, muonCollectionName);

    string muonVertexCollectionName = "LooseMuonsVertex" + matchingMethod + "Match";
    FillMuonVertexHistograms(event, muonVertexCollectionName);
    if (muonVertexCollectionName == muonVertexCollectionInput) muonVertexCollectionInput_filled = true;
  }
  if (!muonVertexCollectionInput_filled) FillMuonVertexHistograms(event, muonVertexCollectionInput);
}

/// --------- Dimuon Vertex Collection Histograms --------- ///
/// ------------ flag: runLLPNanoAODHistograms ------------ ///

void TTAlpsHistogramFiller::FillCustomTTAlpsVariablesForMuonVertexCollections(const shared_ptr<Event> event) {
  if (muonVertexCollection.first.empty() || muonVertexCollection.second.empty()) return;

  string muonVertexCollectionName = muonVertexCollection.first;
  FillMuonVertexHistograms(event, muonVertexCollectionName);
  FillNminus1HistogramsForMuonVertexCollection(event);
}

void TTAlpsHistogramFiller::FillLooseMuonsHistograms(const std::shared_ptr<NanoMuon> muon, std::string name) {
  vector<string> variables = {
      "pt",
      "eta",
      "phi",
      "dxy",
      "ptErr",
      "etaErr",
      "phiErr",
      "dz",
      "vx",
      "vy",
      "vz",
      "chi2",
      "ndof",
      "trkNumPlanes",
      "trkNumHits",
      "trkNumDTHits",
      "trkNumCSCHits",
      "normChi2",
      "outerEta",
      "outerPhi",
      "dzPV",
      "dzPVErr",
      "dxyPVTraj",
      "dxyPVTrajErr",
      "dxyPVSigned",
      "dxyPVSignedErr",
      "ip3DPVSigned",
      "ip3DPVSignedErr",
      "dxyBS",
      "dxyBSErr",
      "dzBS",
      "dzBSErr",
      "dxyBSTraj",
      "dxyBSTrajErr",
      "dxyBSSigned",
      "dxyBSSignedErr",
      "ip3DBSSigned",
      "ip3DBSSignedErr",
      "displacedID",
      "nSegments",
      "nDTSegments",
      "nCSCSegments",

  };

  for (auto variable : variables) {
    try {
      histogramsHandler->Fill(name + "_" + variable, muon->Get(variable, false));
    } catch (const Exception &e) {
      warn() << "Couldn't fill muon histogram for at least one of the variables" << endl;
    }
  }

  int isPATMuon(0), IsTightMuon(0);
  if (!muon->IsDSA()) {
    histogramsHandler->Fill(name + "_pfRelIso04all", muon->Get("pfRelIso04_all"));
    isPATMuon = 1;
    if (muon->IsTight()) IsTightMuon = 1;
  }
  histogramsHandler->Fill(name + "_isPAT", isPATMuon);
  histogramsHandler->Fill(name + "_IsTight", IsTightMuon);
}

void TTAlpsHistogramFiller::FillLooseMuonsHistograms(const shared_ptr<NanoMuons> muons, string collectionName) {
  float size = muons->size();
  histogramsHandler->Fill("Event_n" + collectionName, muons->size());
  for (auto muon : *muons) {
    FillLooseMuonsHistograms(muon, collectionName);
  }
}

void TTAlpsHistogramFiller::FillLooseMuonsHistograms(const shared_ptr<Event> event, string collectionName) {
  auto muons = asNanoMuons(event->GetCollection(collectionName));
  FillLooseMuonsHistograms(muons, collectionName);
}

void TTAlpsHistogramFiller::FillMuonVertexHistograms(const shared_ptr<NanoDimuonVertex> dimuon, string name) {
  vector<string> variables = {
      "isValid",
      "vxy",
      "vxySigma",
      "vxyz",
      "vxyzSigma",
      "chi2",
      "ndof",
      "vx",
      "vy",
      "vz",
      "t",
      "vxErr",
      "vyErr",
      "vzErr",
      "tErr",
      "displacedTrackIso03Muon1",
      "displacedTrackIso04Muon1",
      "displacedTrackIso03Muon2",
      "displacedTrackIso04Muon2",
      "dcaStatus",
      "dcax",
      "dcay",
      "dcaz",
      "missHitsAfterVert1",
      "missHitsAfterVert2",
      "normChi2",
      "dR",
      "dRprox",
      "hitsInFrontOfVert1",
      "hitsInFrontOfVert2",
      "dca",
  };

  for (auto variable : variables) {
    try {
      histogramsHandler->Fill(name + "_" + variable, dimuon->Get(variable));
    } catch (const Exception &e) {
      warn() << "Couldn't fill dimuon histogram for one of the variables" << endl;
    }
  }

  histogramsHandler->Fill(name + "_Lxy", dimuon->GetLxyFromPV());
  histogramsHandler->Fill(name + "_logLxy", log10(dimuon->GetLxyFromPV()));
  histogramsHandler->Fill(name + "_LxySigma", dimuon->GetLxySigmaFromPV());
  histogramsHandler->Fill(name + "_LxySignificance", dimuon->GetLxyFromPV() / dimuon->GetLxySigmaFromPV());
  histogramsHandler->Fill(name + "_outerDR", dimuon->GetOuterDeltaR());
  histogramsHandler->Fill(name + "_maxHitsInFrontOfVert",
                          max(float(dimuon->Get("hitsInFrontOfVert1")), float(dimuon->Get("hitsInFrontOfVert2"))));
  histogramsHandler->Fill(name + "_absCollinearityAngle", abs(dimuon->GetCollinearityAngle()));
  histogramsHandler->Fill(name + "_absPtLxyDPhi1", abs(dimuon->GetDPhiBetweenMuonpTAndLxy(1)));
  histogramsHandler->Fill(name + "_absPtLxyDPhi2", abs(dimuon->GetDPhiBetweenMuonpTAndLxy(2)));
  histogramsHandler->Fill(name + "_invMass", dimuon->GetInvariantMass());
  histogramsHandler->Fill(name + "_logInvMass", log10(dimuon->GetInvariantMass()));
  histogramsHandler->Fill(name + "_pt", dimuon->GetDimuonPt());
  histogramsHandler->Fill(name + "_eta", dimuon->GetDimuonEta());
  histogramsHandler->Fill(name + "_dEta", abs(dimuon->GetDeltaEta()));
  histogramsHandler->Fill(name + "_dPhi", abs(dimuon->GetDeltaPhi()));
  histogramsHandler->Fill(name + "_chargeProduct", dimuon->GetDimuonChargeProduct());

  histogramsHandler->Fill(name + "_3Dangle", dimuon->Get3DOpeningAngle());
  histogramsHandler->Fill(name + "_cos3Dangle", dimuon->GetCosine3DOpeningAngle());
  histogramsHandler->Fill(name + "_nSegments", dimuon->GetTotalNumberOfSegments());

  // Isolations:
  histogramsHandler->Fill(name + "_displacedTrackIso03Dimuon1", dimuon->Get("displacedTrackIso03Dimuon1"));
  histogramsHandler->Fill(name + "_displacedTrackIso04Dimuon1", dimuon->Get("displacedTrackIso04Dimuon1"));
  histogramsHandler->Fill(name + "_displacedTrackIso03Dimuon2", dimuon->Get("displacedTrackIso03Dimuon2"));
  histogramsHandler->Fill(name + "_displacedTrackIso04Dimuon2", dimuon->Get("displacedTrackIso04Dimuon2"));
  float pfRelIso04_all1(0), pfRelIso04_all2(0), nSegments1(0), nSegments2(0);

  double deltaIso03 = dimuon->GetDeltaDisplacedTrackIso03();
  double deltaIso04 = dimuon->GetDeltaDisplacedTrackIso04();
  histogramsHandler->Fill(name + "_deltaIso03", deltaIso03);
  histogramsHandler->Fill(name + "_deltaIso04", deltaIso04);
  histogramsHandler->Fill(name + "_logDeltaIso03", TMath::Log10(deltaIso03));
  histogramsHandler->Fill(name + "_logDeltaIso04", TMath::Log10(deltaIso04));
  histogramsHandler->Fill(name + "_deltaSquaredIso03", pow(deltaIso03, 2));
  histogramsHandler->Fill(name + "_deltaSquaredIso04", pow(deltaIso04, 2));
  histogramsHandler->Fill(name + "_logDeltaSquaredIso03", TMath::Log10(pow(deltaIso03, 2)));
  histogramsHandler->Fill(name + "_logDeltaSquaredIso04", TMath::Log10(pow(deltaIso04, 2)));

  if (name.find("_PatDSA") != string::npos) {
    pfRelIso04_all1 = dimuon->Muon1()->Get("pfRelIso04_all");
    nSegments2 = dimuon->Muon2()->Get("nSegments");
  } else if (name.find("_DSA") != string::npos) {
    nSegments1 = dimuon->Muon1()->Get("nSegments");
    nSegments2 = dimuon->Muon2()->Get("nSegments");
  } else if (name.find("_Pat") != string::npos) {
    pfRelIso04_all1 = dimuon->Muon1()->Get("pfRelIso04_all");
    pfRelIso04_all2 = dimuon->Muon2()->Get("pfRelIso04_all");
  }

  histogramsHandler->Fill(name + "_nSegments1", nSegments1);
  histogramsHandler->Fill(name + "_nSegments2", nSegments2);
  histogramsHandler->Fill(name + "_pfRelIso04all1", pfRelIso04_all1);
  histogramsHandler->Fill(name + "_pfRelIso04all2", pfRelIso04_all2);

  // Muons in vertex variables:
  auto leadingMuon = dimuon->GetLeadingMuon();
  auto subleadingMuon = dimuon->GetSubleadingMuon();
  histogramsHandler->Fill(name + "_leadingPt", leadingMuon->GetPt());
  histogramsHandler->Fill(name + "_subleadingPt", subleadingMuon->GetPt());
  histogramsHandler->Fill(name + "_leadingEta", leadingMuon->GetEta());
  histogramsHandler->Fill(name + "_subleadingEta", subleadingMuon->GetEta());
  histogramsHandler->Fill(name + "_dxyPVTraj1", dimuon->Muon1()->Get("dxyPVTraj"));
  histogramsHandler->Fill(name + "_dxyPVTraj2", dimuon->Muon2()->Get("dxyPVTraj"));
  histogramsHandler->Fill(name + "_dxyPVTrajSig1", (float)dimuon->Muon1()->Get("dxyPVTraj") / (float)dimuon->Muon1()->Get("dxyPVTrajErr"));
  histogramsHandler->Fill(name + "_dxyPVTrajSig2", (float)dimuon->Muon2()->Get("dxyPVTraj") / (float)dimuon->Muon2()->Get("dxyPVTrajErr"));
}

void TTAlpsHistogramFiller::FillMuonVertexHistograms(const shared_ptr<Event> event, const shared_ptr<PhysicsObjects> vertexCollection,
                                                     string vertexName) {
  map<string, int> count = {{"", 0}, {"PatDSA", 0}, {"Pat", 0}, {"DSA", 0}};

  for (auto vertex : *vertexCollection) {
    auto dimuonVertex = asNanoDimuonVertex(vertex, event);
    auto muon1 = dimuonVertex->Muon1();
    auto muon2 = dimuonVertex->Muon2();

    string vertexCategory = dimuonVertex->GetVertexCategory();
    FillMuonVertexHistograms(dimuonVertex, vertexName);
    FillMuonVertexHistograms(dimuonVertex, vertexName + "_" + vertexCategory);

    count[""]++;
    count[vertexCategory]++;
  }
  for (auto &[category, n] : count) {
    histogramsHandler->Fill("Event_n" + vertexName + (category == "" ? "" : "_") + category, n);
  }
}

void TTAlpsHistogramFiller::FillMuonVertexHistograms(const shared_ptr<Event> event, string vertexName) {
  auto vertexCollection = event->GetCollection(vertexName);
  FillMuonVertexHistograms(event, vertexCollection, vertexName);
}

void TTAlpsHistogramFiller::FillNminus1HistogramsForMuonVertexCollection(const shared_ptr<Event> event) {
  string collectionName = muonVertexCollection.first;
  auto collectionCuts = muonVertexCollection.second;

  for (auto cut : collectionCuts) {
    // Skip the BestDimuonVertex cut
    if (cut == "BestDimuonVertex") continue;

    string nminus1CollectionName = collectionName + "Nminus1" + cut;

    auto bestMuonVertex = event->GetCollection(nminus1CollectionName);
    if (bestMuonVertex->size() < 1) continue;
    if (bestMuonVertex->size() > 1) {
      warn() << "More than one vertex in collection: " << collectionName << ". Expected only one but the size is " << bestMuonVertex->size()
             << std::endl;
      continue;
    }
    auto dimuonVertex = asNanoDimuonVertex(bestMuonVertex->at(0), event);
    string nminus1HistogramsName = collectionName + "Nminus1";
    FillDimuonVertexNminus1HistogramForCut(nminus1HistogramsName, cut, dimuonVertex);
    if (dimuonVertex->IsDSAMuon1() && dimuonVertex->IsDSAMuon2())
      nminus1HistogramsName = collectionName + "Nminus1_DSA";
    else if (!dimuonVertex->IsDSAMuon1() && !dimuonVertex->IsDSAMuon2())
      nminus1HistogramsName = collectionName + "Nminus1_Pat";
    else
      nminus1HistogramsName = collectionName + "Nminus1_PatDSA";
    FillDimuonVertexNminus1HistogramForCut(nminus1HistogramsName, cut, dimuonVertex);
  }
}

void TTAlpsHistogramFiller::FillDimuonVertexNminus1HistogramForCut(string collectionName, string cut,
                                                                   shared_ptr<NanoDimuonVertex> dimuonVertex) {
  string histogramName = collectionName + "_" + cut;
  if (cut == "InvariantMassCut") {
    histogramsHandler->Fill(collectionName + "_invMass", dimuonVertex->GetInvariantMass());
    histogramsHandler->Fill(collectionName + "_logInvMass", log10(dimuonVertex->GetInvariantMass()));
  }
  if (cut == "ChargeCut") histogramsHandler->Fill(collectionName + "_chargeProduct", dimuonVertex->GetDimuonChargeProduct());
  if (cut == "HitsInFrontOfVertexCut")
    histogramsHandler->Fill(collectionName + "_maxHitsInFrontOfVert",
                            max(float(dimuonVertex->Get("hitsInFrontOfVert1")), float(dimuonVertex->Get("hitsInFrontOfVert2"))));
  if (cut == "DPhiBetweenMuonpTAndLxyCut") {
    if (!dimuonVertex->IsDSAMuon1())
      histogramsHandler->Fill(collectionName + "_absPtLxyDPhi1", abs(dimuonVertex->GetDPhiBetweenMuonpTAndLxy(1)));
  }
  if (cut == "DCACut") histogramsHandler->Fill(collectionName + "_dca", dimuonVertex->Get("dca"));
  if (cut == "CollinearityAngleCut")
    histogramsHandler->Fill(collectionName + "_absCollinearityAngle", abs(dimuonVertex->GetCollinearityAngle()));
  if (cut == "Chi2Cut") histogramsHandler->Fill(collectionName + "_normChi2", dimuonVertex->Get("normChi2"));
  if (cut == "DisplacedIsolationCut" || cut == "PFRelIsolationCut") {
    histogramsHandler->Fill(collectionName + "_displacedTrackIso03Dimuon1", dimuonVertex->Get("displacedTrackIso03Dimuon1"));
    histogramsHandler->Fill(collectionName + "_displacedTrackIso03Dimuon2", dimuonVertex->Get("displacedTrackIso03Dimuon2"));
    if (!dimuonVertex->IsDSAMuon1()) histogramsHandler->Fill(collectionName + "_pfRelIso1", dimuonVertex->Muon1()->Get("pfRelIso04_all"));
    if (!dimuonVertex->IsDSAMuon2()) histogramsHandler->Fill(collectionName + "_pfRelIso2", dimuonVertex->Muon2()->Get("pfRelIso04_all"));
  }
  if (cut == "LxyCut") histogramsHandler->Fill(collectionName + "_Lxy", dimuonVertex->GetLxyFromPV());
  if (cut == "DeltaEtaCut") {
    histogramsHandler->Fill(collectionName + "_DeltaEta", abs(dimuonVertex->GetDeltaEta()));
    histogramsHandler->Fill(collectionName + "_OuterDeltaEta", abs(dimuonVertex->GetOuterDeltaEta()));
  }
  if (cut == "DeltaPhiCut") {
    histogramsHandler->Fill(collectionName + "_DeltaPhi", abs(dimuonVertex->GetDeltaPhi()));
    histogramsHandler->Fill(collectionName + "_OuterDeltaPhi", abs(dimuonVertex->GetOuterDeltaPhi()));
  }
  if (cut == "DeltaRCut") {
    histogramsHandler->Fill(collectionName + "_DeltaR", dimuonVertex->Get("dR"));
    histogramsHandler->Fill(collectionName + "_OuterDeltaR", dimuonVertex->GetOuterDeltaR());
    histogramsHandler->Fill(collectionName + "_ProxDeltaR", dimuonVertex->Get("dRprox"));
  }
  if (cut == "DeltaPixelHitsCut") histogramsHandler->Fill(collectionName + "_DeltaPixelHits", dimuonVertex->GetDeltaPixelHits());
  if (cut == "BarrelDeltaEtaCut") {
    histogramsHandler->Fill(collectionName + "_dimuonEta", dimuonVertex->GetDimuonEta());
    histogramsHandler->Fill(collectionName + "_DeltaEta", abs(dimuonVertex->GetDeltaEta()));
  }
  if (cut.find("LogLxy") != string::npos) histogramsHandler->Fill(collectionName + "_LogLxy", log(dimuonVertex->GetLxyFromPV()));
}

/// --------- Muon trigger objects and Muon matched to trigger object Histograms --------- ///
/// -------- flag: runMuonTrigObjHistograms --------- ///

void TTAlpsHistogramFiller::FillMuonTriggerObjectsHistograms(const shared_ptr<Event> event) {
  auto tightMuons = event->GetCollection("TightMuons");
  auto triggerMuonMatchCollection = event->GetCollection("TriggerMuonMatch");
  vector<string> muonTriggerCollectionNames = {"MuonTrigObj", "MuonTriggerObjects", "LeadingMuonTriggerObject"};
  for (auto collectionName : muonTriggerCollectionNames) {
    auto muonTrigObjs = event->GetCollection(collectionName);
    histogramsHandler->Fill("Event_n"+collectionName, muonTrigObjs->size());
    for (const auto &muonTrigObj : *muonTrigObjs) {
      histogramsHandler->Fill(collectionName+"_pt", float(muonTrigObj->Get("pt")));
      histogramsHandler->Fill(collectionName+"_eta", float(muonTrigObj->Get("eta")));
      histogramsHandler->Fill(collectionName+"_phi", float(muonTrigObj->Get("phi")));
      histogramsHandler->Fill(collectionName+"_filterBits", int(muonTrigObj->Get("filterBits")));
      histogramsHandler->Fill(collectionName+"_l1iso", int(muonTrigObj->Get("l1iso")));
      histogramsHandler->Fill(collectionName+"_l1pt", float(muonTrigObj->Get("l1pt")));
      histogramsHandler->Fill(collectionName+"_l1pt_2", float(muonTrigObj->Get("l1pt_2")));
      if (int(muonTrigObj->Get("filterBits")) & 2) histogramsHandler->Fill(collectionName+"_hasFilterBits2", 1);
      else histogramsHandler->Fill(collectionName+"_hasFilterBits2", 0);
      TLorentzVector muonTrigObj4Vector;;
      muonTrigObj4Vector.SetPtEtaPhiM(muonTrigObj->Get("pt"), muonTrigObj->Get("eta"), muonTrigObj->Get("phi"), 0.105);
      float minDR = 9999.;
      for (auto tightMuon : *tightMuons) {
        TLorentzVector tightMuon4Vector = asNanoMuon(tightMuon)->GetFourVector();
        float dR = muonTrigObj4Vector.DeltaR(tightMuon4Vector);
        if (dR < minDR) minDR = dR;
      }
      histogramsHandler->Fill(collectionName+"_minDRTightLooseMuon", minDR);
      if (minDR < 0.3) {
        histogramsHandler->Fill(collectionName+"_tightLooseMuonMatch0p3", 1);
        if (minDR < 0.1) {
          histogramsHandler->Fill(collectionName+"_tightLooseMuonMatch0p1", 1);
        }
        else {
          histogramsHandler->Fill(collectionName+"_tightLooseMuonMatch0p1", 0);
        }
      } else {
        histogramsHandler->Fill(collectionName+"_tightLooseMuonMatch0p3", 0);
        histogramsHandler->Fill(collectionName+"_tightLooseMuonMatch0p1", 0);
      }
      if (triggerMuonMatchCollection->size() > 0) {
        auto triggerMuonMatch = asNanoMuon(triggerMuonMatchCollection->at(0));
        auto triggerMuonMatch4Vector = triggerMuonMatch->GetFourVector();
        float triggerMuonMatchDR = muonTrigObj4Vector.DeltaR(triggerMuonMatch4Vector);
        histogramsHandler->Fill(collectionName+"_triggerMuonMatchDR", triggerMuonMatchDR);
      }
    }
  }
}

/// --------- Gen-Level Muon Histograms --------- ///
/// -------- flag: runGenMuonHistograms --------- ///

void TTAlpsHistogramFiller::FillCustomTTAlpsGenMuonVariables(const shared_ptr<Event> event) {
  FillGenALPsHistograms(event);
  FillGenDimuonResonancesHistograms(event);
  FillGenMatchedLooseMuonsHistograms(event);
  FillLooseMuonsFromWsHistograms(event);
}

void TTAlpsHistogramFiller::FillGenALPsHistograms(const shared_ptr<Event> event) {
  auto genALPs = asTTAlpsEvent(event)->GetGenALPs();

  histogramsHandler->Fill("Event_nGenALP", genALPs->size());

  for (int i = 0; i < genALPs->size(); i++) {
    auto genALP = genALPs->at(i);
    int pdgId = genALP->Get("pdgId");
    histogramsHandler->Fill("GenALP_pdgId", pdgId);
    histogramsHandler->Fill("GenALP_pt", genALP->Get("pt"));
    histogramsHandler->Fill("GenALP_mass", genALP->Get("mass"));
    histogramsHandler->Fill("GenALP_eta", genALP->Get("eta"));
    histogramsHandler->Fill("GenALP_phi", genALP->Get("phi"));
  }
}

void TTAlpsHistogramFiller::FillGenDimuonResonancesHistograms(const shared_ptr<Event> event) {
  auto pv_x = event->GetAs<float>("PV_x");
  auto pv_y = event->GetAs<float>("PV_y");
  auto pv_z = event->GetAs<float>("PV_z");

  // Gen Dimuon from ALP
  auto genDimuonFromALP = asTTAlpsEvent(event)->GetGenDimuonFromALP();
  auto genDimuonFromALPindices = asTTAlpsEvent(event)->GetGenMuonIndicesFromALP();
  auto genParticles = event->GetCollection("GenPart");

  if (!asTTAlpsEvent(event)->IsALPDecayWithinCMS()) return;

  if (genDimuonFromALP) {
    histogramsHandler->Fill("GenDimuonFromALP_index1", genDimuonFromALPindices.at(0));
    histogramsHandler->Fill("GenDimuonFromALP_index2", genDimuonFromALPindices.at(1));

    histogramsHandler->Fill("Event_nGenDimuonFromALP", 1);
    auto genMuon1 = genDimuonFromALP->first;
    auto genMuon2 = genDimuonFromALP->second;
    TLorentzVector genMuon1fourVector = asNanoGenParticle(genMuon1)->GetFourVector(muonMass);
    TLorentzVector genMuon2fourVector = asNanoGenParticle(genMuon2)->GetFourVector(muonMass);

    FillGenDimuonHistograms(genDimuonFromALP, "GenDimuonFromALP", event);
  }
  // Not from ALPs
  auto genMuonsNotFromALP = asTTAlpsEvent(event)->GetGenMuonsNotFromALP();
  auto genDimuonResonancesNotFromALP = asTTAlpsEvent(event)->GetGenDimuonsNotFromALP();
  histogramsHandler->Fill("Event_nGenDimuonsNonresonancesNotFromALP", genMuonsNotFromALP->size());
  histogramsHandler->Fill("Event_nGenDimuonResonancesNotFromALP", genDimuonResonancesNotFromALP->size());

  // Muon Pair resonances
  for (auto genDimuon : *genDimuonResonancesNotFromALP) {
    FillGenDimuonHistograms(make_shared<MuonPair>(genDimuon.first, genDimuon.second), "GenDimuonResonancesNotFromALP", event);
  }
  // All muon pair combinations
  for (int i = 0; i < genMuonsNotFromALP->size(); i++) {
    for (int j = i + 1; j < genMuonsNotFromALP->size(); j++) {
      if (j == i) continue;
      auto genMuonPair = make_shared<MuonPair>(genMuonsNotFromALP->at(i), genMuonsNotFromALP->at(j));
      FillGenDimuonHistograms(genMuonPair, "GenDimuonsNonresonancesNotFromALP", event);
    }
  }
}

void TTAlpsHistogramFiller::FillGenMatchedLooseMuonsHistograms(const shared_ptr<Event> event) {
  if (muonMatchingParams.empty()) return;

  auto pv_x = event->GetAs<float>("PV_x");
  auto pv_y = event->GetAs<float>("PV_y");
  auto pv_z = event->GetAs<float>("PV_z");

  auto genDimuonFromALP = asTTAlpsEvent(event)->GetGenDimuonFromALP();
  auto genParticles = event->GetCollection("GenPart");

  if (!asTTAlpsEvent(event)->IsALPDecayWithinCMS()) return;

  auto ttAlpsEvent = asTTAlpsEvent(event);

  string category = ttAlpsEvent->GetTTbarEventCategory();
  bool hmuCategory = category == "hmu";

  for (auto &[matchingMethod, param] : muonMatchingParams) {
    string muonCollectionName = "LooseMuons" + matchingMethod + "Match";
    string muonVertexCollectionName = "LooseMuonsVertex" + matchingMethod + "Match";

    auto looseMuons = asNanoMuons(event->GetCollection(muonCollectionName));
    auto tightMuons = ttAlpsEvent->GetTightMuonsInCollection(looseMuons);

    FillRecoGenMatchedResonanceHistograms(event, looseMuons, muonVertexCollectionName);

    auto looseDimuonFromALP = ttAlpsEvent->GetDimuonMatchedToGenMuonsFromALP(looseMuons);
    // string looseMuonVertexFromALPsName = "LooseMuonsVertex" + matchingMethod + "MatchFromALP";
    string looseMuonFromALPsName = "LooseMuons" + matchingMethod + "MatchFromALP";
    string tightMuonFromALPsName = "TightMuons" + matchingMethod + "MatchFromALP";

    if (!looseDimuonFromALP) continue;

    if (genDimuonFromALP) {
      FillGenMuonMinDRHistograms(genDimuonFromALP->first, looseMuons, "GenDimuonFromALP1", muonCollectionName);
      FillGenMuonMinDRHistograms(genDimuonFromALP->second, looseMuons, "GenDimuonFromALP2", muonCollectionName);
      auto looseDimuonFromALPCollection = make_shared<NanoMuons>();
      looseDimuonFromALPCollection->push_back(looseDimuonFromALP->first);
      FillGenMuonMinDRHistograms(genDimuonFromALP->first, looseDimuonFromALPCollection, "GenDimuonFromALP1", muonCollectionName + "Final");
      looseDimuonFromALPCollection->at(0) = looseDimuonFromALP->second;
      FillGenMuonMinDRHistograms(genDimuonFromALP->second, looseDimuonFromALPCollection, "GenDimuonFromALP2", muonCollectionName + "Final");
    }

    // Tight leading muon from ALP study
    auto looseMuonsFromALPCollection = std::make_shared<NanoMuons>();
    looseMuonsFromALPCollection->push_back(looseDimuonFromALP->first);
    looseMuonsFromALPCollection->push_back(looseDimuonFromALP->second);
    auto tightMuonsFromALP = ttAlpsEvent->GetTightMuonsInCollection(looseMuonsFromALPCollection);
    histogramsHandler->Fill("Event_n" + tightMuonFromALPsName, tightMuonsFromALP->size());
    if (hmuCategory) histogramsHandler->Fill("Event_n" + tightMuonFromALPsName + "_hmu", tightMuonsFromALP->size());
    for (int j = 0; j < tightMuonsFromALP->size(); j++) {
      histogramsHandler->Fill(tightMuonFromALPsName + "_index", tightMuonsFromALP->at(j)->Get("idx"));
      histogramsHandler->Fill(tightMuonFromALPsName + "_pt", tightMuonsFromALP->at(j)->Get("pt"));
      if (hmuCategory) {
        histogramsHandler->Fill(tightMuonFromALPsName + "_hmu_index", tightMuonsFromALP->at(j)->Get("idx"));
        histogramsHandler->Fill(tightMuonFromALPsName + "_hmu_pt", tightMuonsFromALP->at(j)->Get("pt"));
      }
    }
    int leadingLooseMuonFromALP = 0;
    if (ttAlpsEvent->IsLeadingMuonInCollection(looseMuonsFromALPCollection, looseMuons)) leadingLooseMuonFromALP = 1;
    histogramsHandler->Fill(looseMuonFromALPsName + "_hasLeadingMuon", leadingLooseMuonFromALP);
    if (hmuCategory) {
      histogramsHandler->Fill(looseMuonFromALPsName + "_hmu_hasLeadingMuon", leadingLooseMuonFromALP);
    }
    int leadingTightMuonFromALP = 0;
    if (tightMuons->size() > 0 && tightMuonsFromALP->size() > 0) {
      if (ttAlpsEvent->IsLeadingMuonInCollection(tightMuonsFromALP, tightMuons)) leadingTightMuonFromALP = 1;
    }
    histogramsHandler->Fill(tightMuonFromALPsName + "_hasLeadingMuon", leadingTightMuonFromALP);
    if (hmuCategory) histogramsHandler->Fill(tightMuonFromALPsName + "_hmu_hasLeadingMuon", leadingTightMuonFromALP);
  }
}

void TTAlpsHistogramFiller::FillLooseMuonsFromWsHistograms(const shared_ptr<Event> event) {
  auto genMuonsFromW = asTTAlpsEvent(event)->GetGenMuonsFromW();
  auto genMuonsFromW_indices = asTTAlpsEvent(event)->GetGenMuonIndicesFromW();
  auto genParticles = event->GetCollection("GenPart");
  histogramsHandler->Fill("Event_nGenMuonFromW", genMuonsFromW->size());
  if (genMuonsFromW_indices.size() > 0) {
    histogramsHandler->Fill("GenMuonFromW_index1", genMuonsFromW_indices.at(0));
    if (genMuonsFromW_indices.size() > 1) {
      histogramsHandler->Fill("GenMuonFromW_index2", genMuonsFromW_indices.at(1));
      if (genMuonsFromW_indices.size() > 2) histogramsHandler->Fill("GenMuonFromW_index3", genMuonsFromW_indices.at(2));
    }
  }
  auto ttAlpsEvent = asTTAlpsEvent(event);
  string category = ttAlpsEvent->GetTTbarEventCategory();
  bool hmuCategory = category == "hmu";

  for (auto &[matchingMethod, param] : muonMatchingParams) {
    string muonCollectionName = "LooseMuons" + matchingMethod + "Match";
    auto looseMuons = asNanoMuons(event->GetCollection(muonCollectionName));
    auto tightMuons = ttAlpsEvent->GetTightMuonsInCollection(looseMuons);

    auto looseMuonsFromW = ttAlpsEvent->GetLooseMuonsMatchedToGenMuons(genMuonsFromW, looseMuons, 0.01);
    auto tightMuonsFromW = ttAlpsEvent->GetTightMuonsInCollection(looseMuonsFromW);

    string muonFromWsCollectionName = "LooseMuons" + matchingMethod + "MatchFromW";
    string tightMuonFromWsCollectionName = "TightMuons" + matchingMethod + "MatchFromW";

    histogramsHandler->Fill("Event_n" + tightMuonFromWsCollectionName, tightMuonsFromW->size());
    if (hmuCategory) histogramsHandler->Fill("Event_n" + tightMuonFromWsCollectionName + "_hmu", tightMuonsFromW->size());

    int leadingLooseMuonFromW = 0;
    int leadingTightMuonFromW = 0;
    if (looseMuonsFromW->size() > 0) {
      FillLooseMuonsHistograms(looseMuonsFromW, muonFromWsCollectionName);
      auto looseMuonsFromWCollection = make_shared<NanoMuons>();
      looseMuonsFromWCollection->push_back(looseMuonsFromW->at(0));

      FillGenMuonMinDRHistograms(genMuonsFromW->at(0), looseMuonsFromWCollection, "GenMuonFromW1", muonCollectionName + "Final");
      if (looseMuonsFromW->size() > 1) {
        looseMuonsFromWCollection->at(0) = looseMuonsFromW->at(1);
        FillGenMuonMinDRHistograms(genMuonsFromW->at(1), looseMuonsFromWCollection, "GenMuonFromW2", muonCollectionName + "Final");
      }
      if (ttAlpsEvent->IsLeadingMuonInCollection(looseMuonsFromW, looseMuons)) leadingLooseMuonFromW = 1;
      if (tightMuons->size() > 0 && tightMuonsFromW->size() > 0) {
        if (ttAlpsEvent->IsLeadingMuonInCollection(tightMuonsFromW, tightMuons)) leadingTightMuonFromW = 1;
        for (int j = 0; j < tightMuonsFromW->size(); j++) {
          histogramsHandler->Fill(tightMuonFromWsCollectionName + "_index", tightMuonsFromW->at(j)->Get("idx"));
          histogramsHandler->Fill(tightMuonFromWsCollectionName + "_pt", tightMuonsFromW->at(j)->Get("pt"));
          if (hmuCategory) {
            histogramsHandler->Fill(tightMuonFromWsCollectionName + "_hmu_index", tightMuonsFromW->at(j)->Get("idx"));
            histogramsHandler->Fill(tightMuonFromWsCollectionName + "_hmu_pt", tightMuonsFromW->at(j)->Get("pt"));
          }
        }
      }
    }
    histogramsHandler->Fill(muonFromWsCollectionName + "_hasLeadingMuon", leadingLooseMuonFromW);
    histogramsHandler->Fill(tightMuonFromWsCollectionName + "_hasLeadingMuon", leadingTightMuonFromW);
    if (hmuCategory) {
      histogramsHandler->Fill(muonFromWsCollectionName + "_hmu_hasLeadingMuon", leadingLooseMuonFromW);
      histogramsHandler->Fill(tightMuonFromWsCollectionName + "_hmu_hasLeadingMuon", leadingTightMuonFromW);
    }
  }
}

void TTAlpsHistogramFiller::FillGenDimuonHistograms(shared_ptr<MuonPair> muonPair, string collectionName, const shared_ptr<Event> event) {
  auto pv_x = event->GetAs<float>("PV_x");
  auto pv_y = event->GetAs<float>("PV_y");
  auto pv_z = event->GetAs<float>("PV_z");

  auto muon1 = muonPair->first;
  auto muon2 = muonPair->second;
  TLorentzVector muon1fourVector = asNanoGenParticle(muon1)->GetFourVector(muonMass);
  TLorentzVector muon2fourVector = asNanoGenParticle(muon2)->GetFourVector(muonMass);

  histogramsHandler->Fill(collectionName + "_invMass", (muon1fourVector + muon2fourVector).M());
  histogramsHandler->Fill(collectionName + "_logInvMass", log10((muon1fourVector + muon2fourVector).M()));
  histogramsHandler->Fill(collectionName + "_deltaR", muon1fourVector.DeltaR(muon2fourVector));

  float Lx1 = (float)muon1->Get("vx") - pv_x;
  float Ly1 = (float)muon1->Get("vy") - pv_y;
  float Lz1 = (float)muon1->Get("vz") - pv_z;
  float Lxy1 = sqrt(Lx1 * Lx1 + Ly1 * Ly1);
  TVector3 Lxyz1(Lx1, Ly1, Lz1);
  histogramsHandler->Fill(collectionName + "_Lxy", Lxy1);
  histogramsHandler->Fill(collectionName + "_logLxy", log10(Lxy1));

  auto genParticles = event->GetCollection("GenPart");
  auto genMother = asNanoGenParticle(genParticles->at(asNanoGenParticle(muon1)->GetMotherIndex()));
  float boost = float(genMother->GetPt()) / float(genMother->GetMass());
  histogramsHandler->Fill(collectionName + "_properLxy", Lxy1 / boost);

  auto motherIDs1 = asTTAlpsEvent(event)->GetFiveFirstMotherIDsOfParticle(muon1);
  auto motherIDs2 = asTTAlpsEvent(event)->GetFiveFirstMotherIDsOfParticle(muon2);
  for (int j = 0; j < motherIDs1.size(); j++) {
    histogramsHandler->Fill(collectionName + "_motherID1" + to_string(j + 1), motherIDs1[j]);
    histogramsHandler->Fill(collectionName + "_motherID2" + to_string(j + 1), motherIDs2[j]);
  }

  TVector3 ptVector(muon1fourVector.Px() + muon2fourVector.Px(), muon1fourVector.Py() + muon2fourVector.Py(),
                    muon1fourVector.Pz() + muon2fourVector.Pz());
  float absCollinearityAngle = ptVector.DeltaPhi(Lxyz1);
  histogramsHandler->Fill(collectionName + "_absCollinearityAngle", absCollinearityAngle);

  TVector3 pt1Vector(muon1fourVector.Px(), muon1fourVector.Py(), muon1fourVector.Pz());
  TVector3 pt2Vector(muon2fourVector.Px(), muon2fourVector.Py(), muon2fourVector.Pz());
  float ptLxyDPhi1 = pt1Vector.DeltaPhi(Lxyz1);
  float ptLxyDPhi2 = pt2Vector.DeltaPhi(Lxyz1);
  histogramsHandler->Fill(collectionName + "_absPtLxyDPhi1", abs(ptLxyDPhi1));
  histogramsHandler->Fill(collectionName + "_absPtLxyDPhi2", abs(ptLxyDPhi2));
}

void TTAlpsHistogramFiller::FillGenMuonMinDRHistograms(const shared_ptr<PhysicsObject> genMuon, const shared_ptr<NanoMuons> muonCollection,
                                                       string genMuonCollectionName, string looseMuonCollectionName) {
  TLorentzVector genMuonFourVector = asNanoGenParticle(genMuon)->GetFourVector(muonMass);
  float deltaRmin = 9999.;
  float deltaPhimin = 9999.;
  float deltaEtamin = 9999.;
  for (auto muon : *muonCollection) {
    TLorentzVector muonFourVector = muon->GetFourVector();
    if (genMuonFourVector.DeltaR(muonFourVector) < deltaRmin) {
      deltaRmin = genMuonFourVector.DeltaR(muonFourVector);
    }
    if (genMuonFourVector.DeltaPhi(muonFourVector) < deltaPhimin) {
      deltaPhimin = genMuonFourVector.DeltaPhi(muonFourVector);
    }
    float dEta = abs(genMuonFourVector.Eta() - muonFourVector.Eta());
    if (dEta < deltaEtamin) {
      deltaEtamin = dEta;
    }
  }
  if (deltaRmin < 9999.) histogramsHandler->Fill(genMuonCollectionName + "_" + looseMuonCollectionName + "MinDR", deltaRmin);
  if (deltaPhimin < 9999.) histogramsHandler->Fill(genMuonCollectionName + "_" + looseMuonCollectionName + "MinDPhi", deltaPhimin);
  if (deltaEtamin < 9999.) histogramsHandler->Fill(genMuonCollectionName + "_" + looseMuonCollectionName + "MinDEta", deltaEtamin);
}

void TTAlpsHistogramFiller::FillRecoGenMatchedResonanceHistograms(const shared_ptr<Event> event, const shared_ptr<NanoMuons> muonCollection,
                                                                  string collectionName,
                                                                  const shared_ptr<PhysicsObjects> vertexCollection) {
  auto ttAlpsEvent = asTTAlpsEvent(event);

  // Get resonant dimuons for all possible muon combinations in collection
  auto dimuonFromALP = ttAlpsEvent->GetDimuonMatchedToGenMuonsFromALP(muonCollection);
  auto resonantDimuonsNotFromALP = ttAlpsEvent->GetMuonsMatchedToGenDimuonsNotFromALP(muonCollection);
  // Get non-resonant dimuons for alremainingl possible muon combinations in collection
  auto resonantDimuons = make_shared<NanoMuonPairs>(*resonantDimuonsNotFromALP);
  if (dimuonFromALP) resonantDimuons->push_back(*dimuonFromALP);
  auto nonresonantMuons = ttAlpsEvent->GetRemainingNonResonantMuons(muonCollection, resonantDimuons);

  auto resonantDimuonsVertexNotFromALP = make_shared<Collection<shared_ptr<PhysicsObject>>>();
  auto nonresonantMuonsVertex = make_shared<Collection<shared_ptr<PhysicsObject>>>();
  if (vertexCollection) {
    // Make sure the muon combinations are in the vertex collection
    auto allDimuonsVertexsNotFromALP = asNanoEvent(event)->GetVerticesForDimuons(resonantDimuonsNotFromALP);
    for (auto vertex : *allDimuonsVertexsNotFromALP) {
      for (auto v : *vertexCollection) {
        if (vertex == v) {
          resonantDimuonsVertexNotFromALP->push_back(vertex);
          break;
        }
      }
    }
    auto allNonresonantMuonsVertices = asNanoEvent(event)->GetVerticesForMuons(nonresonantMuons);
    for (auto vertex : *allNonresonantMuonsVertices) {
      for (auto v : *vertexCollection) {
        if (vertex == v) {
          nonresonantMuonsVertex->push_back(vertex);
          break;
        }
      }
    }
  } else {
    resonantDimuonsVertexNotFromALP = asNanoEvent(event)->GetVerticesForDimuons(resonantDimuonsNotFromALP);
    nonresonantMuonsVertex = asNanoEvent(event)->GetVerticesForMuons(nonresonantMuons);
  }

  string dimuonFromALPsCollectionName = collectionName + "FromALP";
  string dimuonNotFromALPsVertexCollectionName = collectionName + "ResonancesNotFromALP";
  string muonNotFromALPsVertexCollectionName = collectionName + "NonresonancesNotFromALP";

  if (dimuonFromALP) {
    auto dimuonVertexFromALP = asNanoEvent(event)->GetVertexForDimuon(dimuonFromALP->first, dimuonFromALP->second);
    if (dimuonVertexFromALP) {
      auto dimuonVertexFromALPCollection = make_shared<Collection<shared_ptr<PhysicsObject>>>();
      dimuonVertexFromALPCollection->push_back(dimuonVertexFromALP);
      FillMuonVertexHistograms(event, dimuonVertexFromALPCollection, dimuonFromALPsCollectionName);

      string category = asNanoDimuonVertex(dimuonVertexFromALP, event)->GetVertexCategory();
      histogramsHandler->Fill("Event_n" + dimuonFromALPsCollectionName + "_" + category, 1);
    }
  }
  map<string, int> nResonantMuonsVerticesNotFromALP = {{"Pat", 0}, {"PatDSA", 0}, {"DSA", 0}};
  map<string, int> nNonresonantMuonsVertices = {{"Pat", 0}, {"PatDSA", 0}, {"DSA", 0}};
  FillMuonVertexHistograms(event, resonantDimuonsVertexNotFromALP, dimuonNotFromALPsVertexCollectionName);
  for (int i = 0; i < resonantDimuonsVertexNotFromALP->size(); i++) {
    nResonantMuonsVerticesNotFromALP[asNanoDimuonVertex(resonantDimuonsVertexNotFromALP->at(i), event)->GetVertexCategory()]++;
  }

  FillMuonVertexHistograms(event, nonresonantMuonsVertex, muonNotFromALPsVertexCollectionName);
  for (int i = 0; i < nonresonantMuonsVertex->size(); i++) {
    nNonresonantMuonsVertices[asNanoDimuonVertex(nonresonantMuonsVertex->at(i), event)->GetVertexCategory()]++;
  }
  for (const auto &[category, count] : nResonantMuonsVerticesNotFromALP) {
    histogramsHandler->Fill("Event_n" + dimuonNotFromALPsVertexCollectionName + "_" + category, count);
    histogramsHandler->Fill("Event_n" + muonNotFromALPsVertexCollectionName + "_" + category, nNonresonantMuonsVertices.at(category));
  }
}

/// --------- Gen-Level Dimuon Vertex Collection Histograms --------- ///
/// ---------- flag: runGenMuonVertexCollectionHistograms ----------- ///

void TTAlpsHistogramFiller::FillCustomTTAlpsGenMuonVertexCollectionsVariables(const shared_ptr<Event> event) {
  if (muonVertexCollection.first.empty() || muonVertexCollection.second.empty()) return;

  string collectionName = muonVertexCollection.first;
  auto vertexCollection = event->GetCollection(collectionName);
  auto muonCollection = asTTAlpsEvent(event)->GetMuonsInVertexCollection(vertexCollection);
  FillRecoGenMatchedResonanceHistograms(event, muonCollection, collectionName, vertexCollection);

  FillMuonCollectionFromALPsNminus1Histograms(event);
}

void TTAlpsHistogramFiller::FillMuonCollectionFromALPsNminus1Histograms(const shared_ptr<Event> event) {
  // Gen-level muon vertex collection from ALP is given for both "Best" and "Good" collections
  string bestMuonVertexCollectionName = muonVertexCollection.first;
  auto muonVertexCollectionCuts = muonVertexCollection.second;
  string goodMuonVertexCollectionName = bestMuonVertexCollectionName;
  goodMuonVertexCollectionName.replace(0, 4, "Good");
  vector<string> muonVertexNminus1CollectionNames = {bestMuonVertexCollectionName, goodMuonVertexCollectionName};

  for (auto collectionName : muonVertexNminus1CollectionNames) {
    for (auto cut : muonVertexCollectionCuts) {
      // Skip the BestDimuonVertex cut
      if (cut == "BestDimuonVertex") continue;

      string nminus1CollectionName = collectionName + "Nminus1" + cut;

      auto looseMuonVertices = event->GetCollection(nminus1CollectionName);
      auto looseMuons = asTTAlpsEvent(event)->GetMuonsInVertexCollection(looseMuonVertices);
      auto looseMuonsFromALP = asTTAlpsEvent(event)->GetDimuonMatchedToGenMuonsFromALP(looseMuons);
      if (!looseMuonsFromALP) continue;
      auto dimuonVertex = asNanoEvent(event)->GetVertexForDimuon(looseMuonsFromALP->first, looseMuonsFromALP->second);
      if (!dimuonVertex) continue;
      string muonFromALPsCollectionName = collectionName + "FromALPNminus1";
      // n minus 1 collection name given as collectionName + "Nminus1" + cut
      FillDimuonVertexNminus1HistogramForCut(muonFromALPsCollectionName, cut, asNanoDimuonVertex(dimuonVertex, event));
      if (looseMuonsFromALP->first->IsDSA() && looseMuonsFromALP->second->IsDSA()) {
        muonFromALPsCollectionName = collectionName + "FromALPNminus1_DSA";
      } else if (!looseMuonsFromALP->first->IsDSA() && !looseMuonsFromALP->second->IsDSA()) {
        muonFromALPsCollectionName = collectionName + "FromALPNminus1_Pat";
      } else {
        muonFromALPsCollectionName = collectionName + "FromALPNminus1_PatDSA";
      }
    }
  }
}

/// --------- Muon Matching Histograms --------- ///
/// ----- flag: runMuonMatchingHistograms ------ ///

void TTAlpsHistogramFiller::FillCustomTTAlpsMuonMatchingVariables(const shared_ptr<Event> event) {
  FillMatchingHistograms(event, "LoosePATMuons", "LooseDSAMuons");
}

void TTAlpsHistogramFiller::FillMatchingHistograms(const shared_ptr<Event> event, string patMuonCollection, string dsaMuonCollection) {
  auto looseMuons = asNanoMuons(event->GetCollection(patMuonCollection));
  auto looseDsaMuons = asNanoMuons(event->GetCollection(dsaMuonCollection));

  float matchingMinDeltaR = 0.1;

  // Segment-based matching
  float nSegmentMatched = 0;
  float nSegmentDRMatched = 0;
  float nSegmentOuterDRMatched = 0;
  for (auto dsaMuon : *looseDsaMuons) {
    float nSegments = dsaMuon->Get("nSegments");
    float minRatio = float(2) / float(3);

    histogramsHandler->Fill(dsaMuonCollection + "_nSegments", nSegments);
    histogramsHandler->Fill(dsaMuonCollection + "_muonMatch1", dsaMuon->Get("muonMatch1"));
    float ratio1 = float(dsaMuon->Get("muonMatch1")) / nSegments;
    histogramsHandler->Fill(dsaMuonCollection + "_matchRatio1", ratio1);
    histogramsHandler->Fill(dsaMuonCollection + "_muonMatch2", dsaMuon->Get("muonMatch2"));
    float ratio2 = float(dsaMuon->Get("muonMatch2")) / nSegments;
    histogramsHandler->Fill(dsaMuonCollection + "_matchRatio2", ratio2);
    histogramsHandler->Fill(dsaMuonCollection + "_muonMatch1_nSegments", dsaMuon->Get("muonMatch1"), nSegments);
    histogramsHandler->Fill(dsaMuonCollection + "_muonMatch2_nSegments", dsaMuon->Get("muonMatch2"), nSegments);

    float matchFound = false;
    float muon_idx = -1;
    float maxMatches = -1;
    float ratio = -1;
    for (int i = 1; i <= 5; i++) {
      float ratio_tmp = dsaMuon->GetMatchesForNthBestMatch(i) / nSegments;
      if (!matchFound && ratio_tmp >= minRatio) {
        if (asNanoEvent(event)->PATMuonIndexExist(looseMuons, dsaMuon->GetMatchIdxForNthBestMatch(i))) {
          matchFound = true;
          muon_idx = dsaMuon->GetMatchIdxForNthBestMatch(i);
          maxMatches = dsaMuon->GetMatchesForNthBestMatch(i);
          ratio = ratio_tmp;
        }
      }
    }
    if (matchFound) {
      nSegmentMatched++;
      pair<float, int> dsaGenMinDR = asNanoEvent(event)->GetDeltaRandIndexOfClosestGenMuon(dsaMuon);
      float dsaMinDR = dsaGenMinDR.first;
      float dsaMinDR_genidx = dsaGenMinDR.second;
      auto muon = asNanoEvent(event)->GetPATMuonWithIndex(muon_idx, patMuonCollection);
      pair<float, int> patGenMinDR = asNanoEvent(event)->GetDeltaRandIndexOfClosestGenMuon(muon);
      float patMinDR = patGenMinDR.first;
      float patMinDR_genidx = patGenMinDR.second;

      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_" + dsaMuonCollection + "_genMinDR", patMinDR, dsaMinDR);
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_" + dsaMuonCollection + "_genMinDRidx", patMinDR_genidx,
                              dsaMinDR_genidx);

      FillMatchedMuonHistograms(muon, "SegmentMatch" + patMuonCollection);
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_nSegments", nSegments);
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_matchingRatio", ratio);
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_maxMatches", maxMatches);
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_muonMatchIdx", muon_idx);

      FillMatchedMuonHistograms(muon, "SegmentMatch" + dsaMuonCollection);

      histogramsHandler->Fill("SegmentMatch" + dsaMuonCollection + "_eta_outerEta", dsaMuon->Get("eta"), dsaMuon->Get("outerEta"));
      histogramsHandler->Fill("SegmentMatch" + dsaMuonCollection + "_phi_outerPhi", dsaMuon->Get("phi"), dsaMuon->Get("outerPhi"));
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_eta_outerEta", muon->Get("eta"), muon->Get("outerEta"));
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_phi_outerPhi", muon->Get("phi"), muon->Get("outerPhi"));
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_" + dsaMuonCollection + "_eta", muon->Get("eta"), dsaMuon->Get("eta"));
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_" + dsaMuonCollection + "_phi", muon->Get("phi"), dsaMuon->Get("phi"));
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_" + dsaMuonCollection + "_outerEta", muon->Get("outerEta"),
                              dsaMuon->Get("outerEta"));
      histogramsHandler->Fill("SegmentMatch" + patMuonCollection + "_" + dsaMuonCollection + "_outerPhi", muon->Get("outerPhi"),
                              dsaMuon->Get("outerPhi"));

      // Segment-based + DR matching
      auto dsaMuonP4 = dsaMuon->GetFourVector();
      auto muonP4 = muon->GetFourVector();
      if (muonP4.DeltaR(dsaMuonP4) < matchingMinDeltaR) {
        nSegmentDRMatched++;
        FillMatchedMuonHistograms(muon, "SegmentDRMatch" + patMuonCollection);
        histogramsHandler->Fill("SegmentDRMatch" + patMuonCollection + "_nSegments", nSegments);
        histogramsHandler->Fill("SegmentDRMatch" + patMuonCollection + "_matchingRatio", ratio);
        histogramsHandler->Fill("SegmentDRMatch" + patMuonCollection + "_maxMatches", maxMatches);
        histogramsHandler->Fill("SegmentDRMatch" + patMuonCollection + "_muonMatchIdx", muon_idx);
      }

      // Segment-based + Outer DR matching
      float eta1 = dsaMuon->Get("outerEta");
      float phi1 = dsaMuon->Get("outerPhi");
      float eta2 = muon->Get("outerEta");
      float phi2 = muon->Get("outerPhi");
      if (asNanoEvent(event)->DeltaR(eta1, phi1, eta2, phi2) < matchingMinDeltaR) {
        nSegmentOuterDRMatched++;
        FillMatchedMuonHistograms(muon, "SegmentOuterDRMatch" + patMuonCollection);
        histogramsHandler->Fill("SegmentOuterDRMatch" + patMuonCollection + "_nSegments", nSegments);
        histogramsHandler->Fill("SegmentOuterDRMatch" + patMuonCollection + "_matchingRatio", ratio);
        histogramsHandler->Fill("SegmentOuterDRMatch" + patMuonCollection + "_maxMatches", maxMatches);
        histogramsHandler->Fill("SegmentOuterDRMatch" + patMuonCollection + "_muonMatchIdx", muon_idx);
      }
    }
  }
  histogramsHandler->Fill("Event_nSegmentMatch" + patMuonCollection, nSegmentMatched);
  histogramsHandler->Fill("Event_nSegmentMatch" + dsaMuonCollection, nSegmentMatched);
  histogramsHandler->Fill("Event_nSegmentDRMatch" + patMuonCollection, nSegmentDRMatched);
  histogramsHandler->Fill("Event_nSegmentOuterDRMatch" + patMuonCollection, nSegmentOuterDRMatched);

  // Delta R matching values
  for (auto dsaMuon : *looseDsaMuons) {
    auto dsaMuonP4 = dsaMuon->GetFourVector();
    for (auto patMuon : *looseMuons) {
      auto patMuonP4 = patMuon->GetFourVector();
      float outerDeltaR = dsaMuon->OuterDeltaRtoMuon(patMuon);
      float deltaR = dsaMuonP4.DeltaR(patMuonP4);
      histogramsHandler->Fill(dsaMuonCollection + "_PATDR", deltaR);
      histogramsHandler->Fill(dsaMuonCollection + "_PATOuterDR", outerDeltaR);

      auto vertex = asNanoEvent(event)->GetVertexForDimuon(dsaMuon, patMuon);
      if (vertex) {
        float proxDR = vertex->Get("dRprox");
        histogramsHandler->Fill(dsaMuonCollection + "_PATProxDR", proxDR);
      }
    }
  }
}

void TTAlpsHistogramFiller::FillMatchedMuonHistograms(const shared_ptr<NanoMuon> muon, string muonCollectionName) {
  histogramsHandler->Fill(muonCollectionName + "_pt", muon->Get("pt"));
  histogramsHandler->Fill(muonCollectionName + "_eta", muon->Get("eta"));
  histogramsHandler->Fill(muonCollectionName + "_phi", muon->Get("phi"));
  histogramsHandler->Fill(muonCollectionName + "_dxyPVTraj", muon->Get("dxyPVTraj"));
  float dxyPVTrajSig = abs(float(muon->Get("dxyPVTraj")) / float(muon->Get("dxyPVTrajErr")));
  histogramsHandler->Fill(muonCollectionName + "_dxyPVTrajSig", dxyPVTrajSig);
  histogramsHandler->Fill(muonCollectionName + "_ip3DPVSigned", muon->Get("ip3DPVSigned"));
  float ip3DPVSignedSig = abs(float(muon->Get("ip3DPVSigned")) / float(muon->Get("ip3DPVSignedErr")));
  histogramsHandler->Fill(muonCollectionName + "_ip3DPVSignedSig", ip3DPVSignedSig);
}

/// --------- Trigger study Histograms --------- ///
/// ------ flag: runLLPTriggerHistograms ------ ///

void TTAlpsHistogramFiller::FillTriggerStudyHistograms(const shared_ptr<Event> event, string triggerName) {
  auto genMuonsFromALP = asTTAlpsEvent(event)->GetGenDimuonFromALP();
  string muonCollectionName = triggerName + "GenMuonFromALP";

  int nGenMuonsFromALP = 0;
  if (genMuonsFromALP) nGenMuonsFromALP = 1;
  histogramsHandler->Fill("Event_n" + muonCollectionName, nGenMuonsFromALP);

  if (genMuonsFromALP) {
    auto genMuon1 = genMuonsFromALP->first;
    auto genMuon2 = genMuonsFromALP->second;
    histogramsHandler->Fill(muonCollectionName + "_pt1", genMuon1->Get("pt"));
    histogramsHandler->Fill(muonCollectionName + "_pt2", genMuon2->Get("pt"));
    float leadingPt = max((float)genMuon1->Get("pt"), (float)genMuon2->Get("pt"));
    float subleadingPt = min((float)genMuon1->Get("pt"), (float)genMuon2->Get("pt"));
    histogramsHandler->Fill(muonCollectionName + "_leadingPt", leadingPt);
    histogramsHandler->Fill(muonCollectionName + "_subleadingPt", subleadingPt);
  }
}

/// --------- Dimuon Cutflow Histograms --------- ///

void TTAlpsHistogramFiller::FillDimuonCutFlows(const shared_ptr<CutFlowManager> cutFlowManager, string dimuonCategory) {
  if (muonVertexCollection.first.empty() || muonVertexCollection.second.empty()) return;

  string collectionName = muonVertexCollection.first;
  if (dimuonCategory != "") collectionName = collectionName + "_" + dimuonCategory;
  int cutFlowLength = cutFlowManager->GetCutFlow(collectionName).size();
  string cutFlowName = "dimuonCutFlow_" + collectionName;
  string rawEventsCutFlowName = "rawEventsDimuonCutFlow_" + collectionName;
  auto cutFlowHist = new TH1D(cutFlowName.c_str(), cutFlowName.c_str(), cutFlowLength, 0, cutFlowLength);
  auto rawEventsCutFlowHist = new TH1D(rawEventsCutFlowName.c_str(), rawEventsCutFlowName.c_str(), cutFlowLength, 0, cutFlowLength);

  map<int, pair<string, float>> sortedWeightsAfterCuts;
  map<int, pair<string, float>> sortedRawEventsAfterCuts;
  auto cutFlow = cutFlowManager->GetCutFlow(collectionName);
  auto rawEventsCutFlow = cutFlowManager->GetRawEventsCutFlow(collectionName);
  for (auto &[cutName, sumOfWeights] : cutFlowManager->GetCutFlow(collectionName)) {
    string number = cutName.substr(0, cutName.find("_"));
    int index = stoi(number);
    sortedWeightsAfterCuts[index] = {cutName, sumOfWeights};
    sortedRawEventsAfterCuts[index] = {cutName, rawEventsCutFlow[cutName]};
  }

  int bin = 1;
  for (auto &[index, values] : sortedWeightsAfterCuts) {
    cutFlowHist->SetBinContent(bin, get<1>(values));
    rawEventsCutFlowHist->SetBinContent(bin, get<1>(sortedRawEventsAfterCuts[index]));
    cutFlowHist->GetXaxis()->SetBinLabel(bin, get<0>(values).c_str());
    rawEventsCutFlowHist->GetXaxis()->SetBinLabel(bin, get<0>(sortedRawEventsAfterCuts[index]).c_str());
    bin++;
  }
  histogramsHandler->SetHistogram1D(make_pair(cutFlowName.c_str(), ""), cutFlowHist);
  histogramsHandler->SetHistogram1D(make_pair(rawEventsCutFlowName.c_str(), ""), rawEventsCutFlowHist);
}

/// --------- ABCD Histograms --------- ///
/// ----- flag: runABCDHistograms ----- ///

void TTAlpsHistogramFiller::FillABCDHistograms(const shared_ptr<Event> event) {
  if (muonVertexCollection.first.empty() || muonVertexCollection.second.empty()) return;

  string collectionName = muonVertexCollection.first;
  auto collection = event->GetCollection(collectionName);
  if (collection->size() < 1) return;

  for (auto vertex : *collection) {
    auto dimuon = asNanoDimuonVertex(vertex, event);
    auto muon1 = dimuon->Muon1();
    auto muon2 = dimuon->Muon2();

    map<string, double> variables = {
        {"absCollinearityAngle", dimuon->GetCollinearityAngle()},
        {"3Dangle", dimuon->Get3DOpeningAngle()},

        {"logLxy", TMath::Log10(dimuon->GetLxyFromPV())},
        {"logLxySignificance", TMath::Log10(dimuon->GetLxyFromPV() / dimuon->GetLxySigmaFromPV())},
        {"logAbsCollinearityAngle", TMath::Log10(dimuon->GetCollinearityAngle())},
        {"log3Dangle", TMath::Log10(dimuon->Get3DOpeningAngle())},

        {"outerDR", dimuon->GetOuterDeltaR()},
        {"maxHitsInFrontOfVert", max(float(dimuon->Get("hitsInFrontOfVert1")), float(dimuon->Get("hitsInFrontOfVert2")))},

        {"absPtLxyDPhi1", abs(dimuon->GetDPhiBetweenMuonpTAndLxy(1))},
        {"absPtLxyDPhi2", abs(dimuon->GetDPhiBetweenMuonpTAndLxy(2))},

        {"logAbsPtLxyDPhi1", TMath::Log10(abs(dimuon->GetDPhiBetweenMuonpTAndLxy(1)))},
        {"logAbsPtLxyDPhi2", TMath::Log10(abs(dimuon->GetDPhiBetweenMuonpTAndLxy(2)))},

        {"invMass", dimuon->GetInvariantMass()},
        {"logInvMass", log10(dimuon->GetInvariantMass())},
        {"pt", dimuon->GetDimuonPt()},
        {"logPt", TMath::Log10(dimuon->GetDimuonPt())},
        {"eta", dimuon->GetDimuonEta()},
        {"dEta", abs(dimuon->GetDeltaEta())},
        {"dPhi", abs(dimuon->GetDeltaPhi())},

        {"nSegments", dimuon->GetTotalNumberOfSegments()},
        {"logDisplacedTrackIso03Dimuon1", TMath::Log10(dimuon->Get("displacedTrackIso03Dimuon1"))},
        {"logDisplacedTrackIso04Dimuon1", TMath::Log10(dimuon->Get("displacedTrackIso04Dimuon1"))},
        {"logDisplacedTrackIso03Dimuon2", TMath::Log10(dimuon->Get("displacedTrackIso03Dimuon2"))},
        {"logDisplacedTrackIso04Dimuon2", TMath::Log10(dimuon->Get("displacedTrackIso04Dimuon2"))},
        {"leadingPt", dimuon->GetLeadingMuonPt()},
        {"logDxyPVTraj1", TMath::Log10(dimuon->Muon1()->Get("dxyPVTraj"))},
        {"logDxyPVTraj2", TMath::Log10(dimuon->Muon2()->Get("dxyPVTraj"))},
        {"logDxyPVTrajSig1", TMath::Log10((float)dimuon->Muon1()->Get("dxyPVTraj") / (float)dimuon->Muon1()->Get("dxyPVTrajErr"))},
        {"logDxyPVTrajSig2", TMath::Log10((float)dimuon->Muon2()->Get("dxyPVTraj") / (float)dimuon->Muon2()->Get("dxyPVTrajErr"))},

        {"deltaIso03", dimuon->GetDeltaDisplacedTrackIso03()},
        {"deltaIso04", dimuon->GetDeltaDisplacedTrackIso04()},
        {"logDeltaIso03", TMath::Log10(dimuon->GetDeltaDisplacedTrackIso03())},
        {"logDeltaIso04", TMath::Log10(dimuon->GetDeltaDisplacedTrackIso04())},
        {"deltaSquaredIso03", pow(dimuon->GetDeltaDisplacedTrackIso03(), 2)},
        {"deltaSquaredIso04", pow(dimuon->GetDeltaDisplacedTrackIso04(), 2)},
        {"logDeltaSquaredIso03", TMath::Log10(pow(dimuon->GetDeltaDisplacedTrackIso03(), 2))},
        {"logDeltaSquaredIso04", TMath::Log10(pow(dimuon->GetDeltaDisplacedTrackIso04(), 2))},
    };

    string category = dimuon->GetVertexCategory();

    float deltaEta = dimuon->GetDeltaEta();

    for (auto &[varName_1, varValue_1] : variables) {
      for (auto &[varName_2, varValue_2] : variables) {
        if (varName_1 == varName_2) continue;
        histogramsHandler->Fill(collectionName + "_" + varName_2 + "_vs_" + varName_1, varValue_1, varValue_2);
        histogramsHandler->Fill(collectionName + "_" + varName_2 + "_vs_" + varName_1 + "_" + category, varValue_1, varValue_2);
      }
    }
  }
}

/// --------- ABCD mothers Histograms --------- ///
/// ----- flag: runABCDMothersHistograms ----- ///

void TTAlpsHistogramFiller::FillABCDMothersHistograms(const shared_ptr<Event> event, bool runFakesHistograms) {
  if (muonVertexCollection.first.empty() || muonVertexCollection.second.empty()) return;

  auto genMuons = event->GetCollection("GenPart");

  string collectionName = muonVertexCollection.first;
  auto collection = event->GetCollection(collectionName);

  if (collection->size() < 1) return;

  for (auto vertex : *collection) {
    auto dimuon = asNanoDimuonVertex(vertex, event);
    auto muon1 = dimuon->Muon1();
    auto muon2 = dimuon->Muon2();

    string category = dimuon->GetVertexCategory();

    float deltaR = 0.5;
    auto genMuon1 = muon1->GetGenMuon(genMuons, deltaR);
    auto genMuon2 = muon2->GetGenMuon(genMuons, deltaR);

    int mother1_pid = 0;
    int mother2_pid = 0;
    if (!genMuon1)
      mother1_pid = muon1->IsDSA() ? 91 : 90;
    else {
      mother1_pid = genMuons->at(genMuon1->GetMotherIndex())->Get("pdgId");
    }
    if (!genMuon2)
      mother2_pid = muon2->IsDSA() ? 91 : 90;
    else {
      mother2_pid = genMuons->at(genMuon2->GetMotherIndex())->Get("pdgId");
    }

    histogramsHandler->Fill(collectionName + "_motherPid1_vs_motherPid2", mother1_pid, mother2_pid);

    if ((mother1_pid == 24 && mother2_pid == 24) || (mother1_pid == -24 && mother2_pid == -24)) {
      // Same sign WW
      histogramsHandler->Fill(collectionName + "_deltaR_WW", dimuon->GetDeltaR());
      histogramsHandler->Fill(collectionName + "_logDeltaR_WW", log10(dimuon->GetDeltaR()));
    } else if ((mother1_pid == 24 && mother2_pid == 15) || (mother1_pid == -24 && mother2_pid == -15)) {
      // Same sign Wτ
      histogramsHandler->Fill(collectionName + "_deltaR_Wtau", dimuon->GetDeltaR());
      histogramsHandler->Fill(collectionName + "_logDeltaR_Wtau", log10(dimuon->GetDeltaR()));
    } else {
      histogramsHandler->Fill(collectionName + "_deltaR_OS", dimuon->GetDeltaR());
      histogramsHandler->Fill(collectionName + "_logDeltaR_OS", log10(dimuon->GetDeltaR()));
    }

    float lxySignificance = TMath::Log10(dimuon->GetLxyFromPV() / dimuon->GetLxySigmaFromPV());
    float angle3D = TMath::Log10(dimuon->Get3DOpeningAngle());
    float logInvMass = log10(dimuon->GetInvariantMass());
    float logDeltaIso03 = TMath::Log10(dimuon->GetDeltaDisplacedTrackIso03());

    if (logInvMass > 1.6 && logInvMass < 1.9 && logDeltaIso03 > -1.6 && logDeltaIso03 < -1.0) {
      histogramsHandler->Fill(collectionName + "_motherPid1_vs_motherPid2_mysteriousBlob", mother1_pid, mother2_pid);
      if (runFakesHistograms) {
        FillMuonVertexHistograms(dimuon, collectionName + "_" + category + "_fakes");

        if (muon1->IsDSA())
          FillLooseMuonsHistograms(muon1, "LooseDSAMuonsSegmentMatch_fakes");
        else
          FillLooseMuonsHistograms(muon1, "LoosePATMuonsSegmentMatch_fakes");

        if (muon2->IsDSA())
          FillLooseMuonsHistograms(muon2, "LooseDSAMuonsSegmentMatch_fakes");
        else
          FillLooseMuonsHistograms(muon2, "LoosePATMuonsSegmentMatch_fakes");
      }

    } else {
      if (runFakesHistograms) {
        FillMuonVertexHistograms(dimuon, collectionName + "_" + category + "_nonFakes");
        if (muon1->IsDSA())
          FillLooseMuonsHistograms(muon1, "LooseDSAMuonsSegmentMatch_nonFakes");
        else
          FillLooseMuonsHistograms(muon1, "LoosePATMuonsSegmentMatch_nonFakes");

        if (muon2->IsDSA())
          FillLooseMuonsHistograms(muon2, "LooseDSAMuonsSegmentMatch_nonFakes");
        else
          FillLooseMuonsHistograms(muon2, "LoosePATMuonsSegmentMatch_nonFakes");
      }
    }

    if (lxySignificance > -2.0 && lxySignificance < -1.0 && angle3D > -1.5 && angle3D < -1.0) {
      histogramsHandler->Fill(collectionName + "_motherPid1_vs_motherPid2_lowBlob", mother1_pid, mother2_pid);
    }
    if (lxySignificance > -0.5 && lxySignificance < 0.5 && angle3D > 0.0 && angle3D < 0.4) {
      histogramsHandler->Fill(collectionName + "_motherPid1_vs_motherPid2_rightBlob", mother1_pid, mother2_pid);

      if (lxySignificance > -0.5 && lxySignificance < 0.5 && angle3D > -1.5 && angle3D < -1.0) {
        histogramsHandler->Fill(collectionName + "_motherPid1_vs_motherPid2_centralBlob", mother1_pid, mother2_pid);
      }
      if (lxySignificance > -2.0 && lxySignificance < -1.8 && angle3D > -0.5 && angle3D < 0.2) {
        histogramsHandler->Fill(collectionName + "_motherPid1_vs_motherPid2_lowLine", mother1_pid, mother2_pid);
      }
      if (lxySignificance > -2.0 && lxySignificance < -1.0 && angle3D > 0.2 && angle3D < 0.4) {
        histogramsHandler->Fill(collectionName + "_motherPid1_vs_motherPid2_rightLine", mother1_pid, mother2_pid);
      }
    }
  }
}
/// --------- Fakes Histograms --------- ///
/// ----- flag: runFakesHistograms ----- ///

void TTAlpsHistogramFiller::FillFakesHistograms(const shared_ptr<Event> event) {
  if (muonVertexCollection.first.empty() || muonVertexCollection.second.empty()) return;

  string collectionName = muonVertexCollection.first;
  auto collection = event->GetCollection(collectionName);

  if (collection->size() < 1) return;

  auto genMuons = event->GetCollection("GenPart");

  for (auto vertex : *collection) {
    auto dimuon = asNanoDimuonVertex(vertex, event);
    auto muon1 = dimuon->Muon1();
    auto muon2 = dimuon->Muon2();
    string category = dimuon->GetVertexCategory();

    float deltaR = 0.5;
    auto genMuon1 = muon1->GetGenMuon(genMuons, deltaR);
    auto genMuon2 = muon2->GetGenMuon(genMuons, deltaR);

    int mother1_pid = 0;
    int mother2_pid = 0;
    if (!genMuon1)
      mother1_pid = muon1->IsDSA() ? 91 : 90;
    else {
      mother1_pid = genMuons->at(genMuon1->GetMotherIndex())->Get("pdgId");
    }
    if (!genMuon2)
      mother2_pid = muon2->IsDSA() ? 91 : 90;
    else {
      mother2_pid = genMuons->at(genMuon2->GetMotherIndex())->Get("pdgId");
    }

    if (mother1_pid == 90) {
      FillMuonVertexHistograms(dimuon, collectionName + "_" + category + "_fakes");
      FillLooseMuonsHistograms(muon1, "LoosePATMuonsSegmentMatch_fakes");
    } else if (mother1_pid == 91) {
      FillMuonVertexHistograms(dimuon, collectionName + "_" + category + "_fakes");
      FillLooseMuonsHistograms(muon1, "LooseDSAMuonsSegmentMatch_fakes");
    } else if (muon1->IsDSA()) {
      FillMuonVertexHistograms(dimuon, collectionName + "_" + category + "_nonFakes");
      FillLooseMuonsHistograms(muon1, "LooseDSAMuonsSegmentMatch_nonFakes");
    } else if (!muon1->IsDSA()) {
      FillMuonVertexHistograms(dimuon, collectionName + "_" + category + "_nonFakes");
      FillLooseMuonsHistograms(muon1, "LoosePATMuonsSegmentMatch_nonFakes");
    }

    if (mother2_pid == 90) {
      FillMuonVertexHistograms(dimuon, collectionName + "_" + category + "_fakes");
      FillLooseMuonsHistograms(muon2, "LoosePATMuonsSegmentMatch_fakes");
    } else if (mother2_pid == 91) {
      FillMuonVertexHistograms(dimuon, collectionName + "_" + category + "_fakes");
      FillLooseMuonsHistograms(muon2, "LooseDSAMuonsSegmentMatch_fakes");
    } else if (muon2->IsDSA()) {
      FillMuonVertexHistograms(dimuon, collectionName + "_" + category + "_nonFakes");
      FillLooseMuonsHistograms(muon2, "LooseDSAMuonsSegmentMatch_nonFakes");
    } else if (!muon2->IsDSA()) {
      FillMuonVertexHistograms(dimuon, collectionName + "_" + category + "_nonFakes");
      FillLooseMuonsHistograms(muon2, "LoosePATMuonsSegmentMatch_nonFakes");
    }
  }
}