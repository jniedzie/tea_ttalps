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
cms_colors_8 = [ROOT.TColor.GetColor(color) for color in color_palette_petroff_8]
cms_colors_10 = [ROOT.TColor.GetColor(color) for color in color_palette_petroff_10]

# samples will appear in the stack in the order they are defined here
# legend_row is counted from the top
# legend_column is counted from the right

samples_params = {
    # ------------------------------------------------------------------------------
    # Data
    # ------------------------------------------------------------------------------
    "SingleMuon"        : {"color": ROOT.kBlack    , "legend_column": 1, "legend_row": 0, "legend_title": "SingleMuon {}"         },
    "Muon"              : {"color": ROOT.kBlack    , "legend_column": 1, "legend_row": 0, "legend_title": "Muon {}"               },

    # ------------------------------------------------------------------------------
    # Backgrounds for paper WIP
    # ------------------------------------------------------------------------------

    "TTToSemiLeptonic"  : {"color": cms_colors_10[0] , "legend_column": 1, "legend_row": 1, "legend_title": "t#bar{t}"               },
    "TTtoLNu2Q"         : {"color": cms_colors_10[0] , "legend_column": 1, "legend_row": 1, "legend_title": "t#bar{t}"               },

    "TTTo2L2Nu"         : {"color": cms_colors_10[0] , "legend_column": 1, "legend_row": 1, "legend_title": "t#bar{t}"               },
    "TTto2L2Nu"         : {"color": cms_colors_10[0] , "legend_column": 1, "legend_row": 1, "legend_title": "t#bar{t}"               },
        
    "ST_t"              : {"color": cms_colors_10[9] , "legend_column": 1, "legend_row": 2, "legend_title": "Single top"             },
    "TWminustoLNu2Q"    : {"color": cms_colors_10[9] , "legend_column": 1, "legend_row": 2, "legend_title": "Single top"             },
    "TbarWplustoLNu2Q"  : {"color": cms_colors_10[9] , "legend_column": 1, "legend_row": 2, "legend_title": "Single top"             },
    "TBbarQ"            : {"color": cms_colors_10[9] , "legend_column": 1, "legend_row": 2, "legend_title": "Single top"             },
    "TbarBQ"            : {"color": cms_colors_10[9] , "legend_column": 1, "legend_row": 2, "legend_title": "Single top"             },

    "TTZTo"             : {"color": cms_colors_10[7] , "legend_column": 1, "legend_row": 3, "legend_title": "t#bar{t}X"              },
    "TTLL"              : {"color": cms_colors_10[7] , "legend_column": 1, "legend_row": 3, "legend_title": "t#bar{t}X"              },
    
    "ttH"               : {"color": cms_colors_10[7] , "legend_column": 1, "legend_row": 3, "legend_title": "t#bar{t}X"              },
    "TTH"               : {"color": cms_colors_10[7] , "legend_column": 1, "legend_row": 3, "legend_title": "t#bar{t}X"              },

    "TTW"               : {"color": cms_colors_10[7] , "legend_column": 1, "legend_row": 3, "legend_title": "t#bar{t}X"              },
    
    "QCD"               : {"color": cms_colors_10[3] , "legend_column": 0, "legend_row": 1, "legend_title": "QCD"                    },
    
    "TTToHadronic"      : {"color": cms_colors_10[0] , "legend_column": 1, "legend_row": 1, "legend_title": "t#bar{t}"               },
    "TTto4Q"            : {"color": cms_colors_10[0] , "legend_column": 1, "legend_row": 1, "legend_title": "t#bar{t}"               },
    
    "WJets"             : {"color": cms_colors_10[8] , "legend_column": 0, "legend_row": 2, "legend_title": "W+jets"                 },
    "W1Jets"            : {"color": cms_colors_10[8] , "legend_column": 0, "legend_row": 2, "legend_title": "W+jets"                 },
    "W2Jets"            : {"color": cms_colors_10[8] , "legend_column": 0, "legend_row": 2, "legend_title": "W+jets"                 },
    "W3Jets"            : {"color": cms_colors_10[8] , "legend_column": 0, "legend_row": 2, "legend_title": "W+jets"                 },
    "W4Jets"            : {"color": cms_colors_10[8] , "legend_column": 0, "legend_row": 2, "legend_title": "W+jets"                 },
    "WtoLNu"            : {"color": cms_colors_10[8] , "legend_column": 0, "legend_row": 2, "legend_title": "W+jets"                 },
    
    
    "TTTT"              : {"color": cms_colors_10[5] , "legend_column": 0, "legend_row": 3, "legend_title": "t#bar{t}t#bar{t}"       },
    "TTZZ"              : {"color": cms_colors_10[7] , "legend_column": 1, "legend_row": 3, "legend_title": "t#bar{t}X"              },
    "TTZH"              : {"color": cms_colors_10[7] , "legend_column": 1, "legend_row": 3, "legend_title": "t#bar{t}X"              },
    "DYJets"            : {"color": cms_colors_10[6] , "legend_column": 0, "legend_row": 4, "legend_title": "DY+jets"                },
   
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
        "line_style": 1,
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
