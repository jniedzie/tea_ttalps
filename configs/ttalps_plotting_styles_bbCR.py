import ROOT

from Sample import SampleType

color_palette_wong = (
    ROOT.TColor.GetColor(230, 159, 0),
    ROOT.TColor.GetColor(86, 180, 233),
    ROOT.TColor.GetColor(0, 158, 115),
    ROOT.TColor.GetColor(0, 114, 178),
    ROOT.TColor.GetColor(213, 94, 0),
)

color_palette_petroff_6 = ["#5790fc", "#f89c20", "#e42536", "#964a8b", "#9c9ca1", "#7a21dd"]
color_palette_petroff_8 = ["#1845fb", "#ff5e02", "#c91f16", "#c849a9", "#adad7d", "#86c8dd", "#578dff", "#656364"]
color_palette_petroff_10 = ["#3f90da", "#ffa90e", "#bd1f01", "#94a4a2", "#832db6", "#a96b59", "#e76300", "#b9ac70", "#717581", "#92dadd"]

cms_colors = [ROOT.TColor.GetColor(color) for color in color_palette_petroff_10 + color_palette_petroff_8]

# samples will appear in the stack in the order they are defined here
# legend_row is counted from the top
# legend_column is counted from the right

samples_params = {
    # ------------------------------------------------------------------------------
    # Data
    # ------------------------------------------------------------------------------

    "SingleMuon"        : {"color": ROOT.kBlack    , "legend_column": 2, "legend_row": 0, "legend_title": "SingleMuon 2018"        },
    "MuonC"             : {"color": ROOT.kBlack    , "legend_column": 2, "legend_row": 0, "legend_title": "Muon era C 2023"        },

    # ------------------------------------------------------------------------------
    # Backgrounds
    # ------------------------------------------------------------------------------

    

    "TTTo2L2Nu"         : {"color": cms_colors[4] , "legend_column": 2, "legend_row": 1, "legend_title": "t#bar{t} leptonic"      },
    "TTto2L2Nu"         : {"color": cms_colors[4] , "legend_column": 2, "legend_row": 1, "legend_title": "t#bar{t} leptonic"      },
    "TTToSemiLeptonic"  : {"color": cms_colors[0] , "legend_column": 2, "legend_row": 2, "legend_title": "t#bar{t} semi-leptonic" },
    "TTtoLNu2Q"         : {"color": cms_colors[0] , "legend_column": 2, "legend_row": 2, "legend_title": "t#bar{t} semi-leptonic" },
    "ST_t"              : {"color": cms_colors[3] , "legend_column": 2, "legend_row": 3, "legend_title": "Single top"             },
    "TWminustoLNu2Q"    : {"color": cms_colors[3] , "legend_column": 2, "legend_row": 3, "legend_title": "Single top"             },
    "TbarWplustoLNu2Q"  : {"color": cms_colors[3] , "legend_column": 2, "legend_row": 3, "legend_title": "Single top"             },
    "WJets"             : {"color": cms_colors[2] , "legend_column": 2, "legend_row": 4, "legend_title": "W+jets"                 },
    "WtoLNu"            : {"color": cms_colors[2] , "legend_column": 2, "legend_row": 4, "legend_title": "W+jets"                 },
    
    "TTZToLL"           : {"color": cms_colors[6] , "legend_column": 1, "legend_row": 1, "legend_title": "t#bar{t}Z"              },
    "TTLL"              : {"color": cms_colors[6] , "legend_column": 1, "legend_row": 1, "legend_title": "t#bar{t}Z"              },
    "ttH"               : {"color": cms_colors[7] , "legend_column": 1, "legend_row": 2, "legend_title": "t#bar{t}H"              },
    "TTH"               : {"color": cms_colors[7] , "legend_column": 1, "legend_row": 2, "legend_title": "t#bar{t}H"              },
    "TTTT"              : {"color": cms_colors[8] , "legend_column": 1, "legend_row": 3, "legend_title": "t#bar{t}t#bar{t}"       },
    "DYJets"            : {"color": cms_colors[3] , "legend_column": 1, "legend_row": 4, "legend_title": "DY+jets"                },
    "QCD"               : {"color": cms_colors[1] , "legend_column": 1, "legend_row": 5, "legend_title": "QCD"                    },
    "TTToHadronic"      : {"color": cms_colors[5] , "legend_column": 1, "legend_row": 6, "legend_title": "t#bar{t} hadronic"      },
    "TTto4Q"            : {"color": cms_colors[5] , "legend_column": 1, "legend_row": 6, "legend_title": "t#bar{t} hadronic"      },
    "TTZZ"              : {"color": cms_colors[9] , "legend_column": 1, "legend_row": 7, "legend_title": "t#bar{t}ZZ"             },
    "TTZH"              : {"color": cms_colors[0] , "legend_column": 1, "legend_row": 8, "legend_title": "t#bar{t}ZH"             },

    # ------------------------------------------------------------------------------
    # Signals
    # ------------------------------------------------------------------------------

    "tta_mAlp-0p35GeV_ctau-1e2mm": {"color": ROOT.kGreen+1, "legend_column": 0, "legend_row": 1, "legend_title": "0.35 GeV, 1e5 mm"},
    "tta_mAlp-0p35GeV_ctau-1e3mm": {"color": ROOT.kRed+1  , "legend_column": 0, "legend_row": 2, "legend_title": "0.35 GeV, 1e3 mm"},
    "tta_mAlp-0p35GeV_ctau-1e5mm": {"color": ROOT.kRed+3  , "legend_column": 0, "legend_row": 3, "legend_title": "0.35 GeV, 1e5 mm"}
}


samples_styles = {
    SampleType.background: {
        "line_alpha": 0,
        "line_style": 1,
        "fill_alpha": 0.7,
        "marker_size": 0,
        "marker_style": 0,
        "legend_style": "f",
    },
    SampleType.signal: {
        "line_alpha": 1,
        "line_style": 2,
        "fill_alpha": 0,
        "marker_size": 0,
        "marker_style": 0,
        "legend_style": "l",
    },
    SampleType.data: {
        "line_style": 1,
        "line_alpha": 1,
        "fill_alpha": 0,
        "marker_size": 0.7,
        "marker_style": 20,
        "legend_style": "pe",
    }
}
