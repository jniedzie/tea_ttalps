import copy

regionA_collection = {
    "regionA_Pat": {
        "inputCollections": ("BestPFIsoDimuonVertex_Pat",),
        "logDxyPVTraj2": (-1.68, 9999.),
        "logPt": (1.40, 9999.),
    },

    "regionA_PatDSA": {
        "inputCollections": ("BestPFIsoDimuonVertex_PatDSA",),
        "logAbsCollinearityAngle": (-9999., -0.6),
        "logDxyPVTraj1": (-2.4, 9999.),
    },

    "regionA_DSA": {
        "inputCollections": ("BestPFIsoDimuonvertex_DSA",),
        "logAbsCollinearityAngle": (-9999., -1),
        "logPt": (1.24, 9999.),
    },
}

regionB_collection = {
    "regionB_Pat": {
        "inputCollections": ("BestPFIsoDimuonVertex_Pat",),
        "logDxyPVTraj2": (-9999., -1.68),
        "logPt": (1.40, 9999.),
    },

    "regionB_PatDSA": {
        "inputCollections": ("BestPFIsoDimuonVertex_PatDSA",),
        "logAbsCollinearityAngle": (-9999., -0.6),
        "logDxyPVTraj1": (-9999., -2.4),
    },

    "regionB_DSA": {
        "inputCollections": ("BestPFIsoDimuonvertex_DSA",),
        "logAbsCollinearityAngle": (-1., 9999.),
        "logPt": (1.24, 9999.),
    },
}

regionC_collection = {
    "regionC_Pat": {
        "inputCollections": ("BestPFIsoDimuonVertex_Pat",),
        "logDxyPVTraj2": (-1.68, 9999.),
        "logPt": (-9999., 1.40),
    },

    "regionC_PatDSA": {
        "inputCollections": ("BestPFIsoDimuonVertex_PatDSA",),
        "logAbsCollinearityAngle": (-0.6, 9999.),
        "logDxyPVTraj1": (-2.4, 9999.),
    },

    "regionC_DSA": {
        "inputCollections": ("BestPFIsoDimuonvertex_DSA",),
        "logAbsCollinearityAngle": (-9999., -1),
        "logPt": (-9999., 1.24),
    },
}

regionD_collection = {
    "regionD_Pat": {
        "inputCollections": ("BestPFIsoDimuonVertex_Pat",),
        # "logAbsCollinearityAngle": (-2., 9999.),
        # "logPt": (-9999., 1.56),
        "logDxyPVTraj2": (-9999., -1.68),
        "logPt": (-9999., 1.40),
    },

    "regionD_PatDSA": {
        "inputCollections": ("BestPFIsoDimuonVertex_PatDSA",),
        "logAbsCollinearityAngle": (-0.6, 9999.),
        "logDxyPVTraj1": (-9999., -2.4),
    },

    "regionD_DSA": {
        "inputCollections": ("BestPFIsoDimuonvertex_DSA",),
        "logAbsCollinearityAngle": (-1., 9999.),
        "logPt": (-9999., 1.24),
    },
}


def get_abcd_region_d_collection():
  return regionD_collection

def get_abcd_regions_collections():  
  return {**regionA_collection, **regionB_collection, **regionC_collection, **regionD_collection}
