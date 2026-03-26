from Logger import error

lxy_uncertainty_for_mass_and_ctau_Pat = {
    0.35: {
        1e-05: 1.0751775472965923,
        1.0: 1.6580155398904233,
        10: 1.7744752267281945,
        100: 1.7886358524233423,
        1000: 1.7382818795907822,
    },
    2: {
        1e-05: 1.018757792582629,
        1.0: 1.304656885050331,
        10: 1.759043017118202,
        100: 1.8332521485089148,
        1000: 1.8562650668689364,
    },
    12: {
        1e-05: 1.0176318167632186,
        1.0: 1.0299748247239688,
        10: 1.5460552294580743,
        100: 1.8118591872907945,
        1000: 1.8342275618571864,
    },
    30: {
        1e-05: 1.0152587843531362,
        1.0: 1.0052241906710704,
        10: 1.3216429786813042,
        100: 1.6832780722730405,
        1000: 1.7809811221509861,
    },
    60: {
        1e-05: 1.0183238432047126,
        1.0: 1.0009631738366698,
        10: 1.1586674819003944,
        100: 1.5730473781309178,
        1000: 1.672553381331284,
    },
}
lxy_uncertainty_for_mass_and_ctau_PatDSA = {
    0.35: {
        1e-05: 1.0016921625614084,
        1.0: 1.0098381347549619,
        10: 1.011597850083839,
        100: 1.0168581196986548,
        1000: 1.0359203901353742,
    },
    2: {
        1e-05: 1.0304667599722164,
        1.0: 1.0135249032541358,
        10: 1.0145903439852426,
        100: 1.0026839343072587,
        1000: 1.028031837824204,
    },
    12: {
        1e-05: 1.0,
        1.0: 1.0032610677037601,
        10: 1.005505435653981,
        100: 1.0012123585126405,
        1000: 1.037412454600737,
    },
    30: {
        1e-05: 1.0,
        1.0: 1.0,
        10: 1.0,
        100: 1.0058444156645938,
        1000: 1.0148049501248515,
    },
    60: {
        1e-05: 1.0,
        1.0: 1.0270577276699955,
        10: 1.0123758166943433,
        100: 1.0,
        1000: 1.0043655785674208,
    },
}
lxy_uncertainty_for_mass_and_ctau_DSA = {
    0.35: {
        1e-05: 1.0,
        1.0: 1.0240768066656263,
        10: 1.0489703320404307,
        100: 1.1143883198840958,
        1000: 1.1098091416392566,
    },
    2: {
        1e-05: 1.0,
        1.0: 1.063088358150207,
        10: 1.0295855833787686,
        100: 1.1217019648537516,
        1000: 1.1948926819260401,
    },
    12: {
        1e-05: 1.1513429489775904,
        1.0: 1.038000506692032,
        10: 1.004543068700814,
        100: 1.0616404176318504,
        1000: 1.2257503771183138,
    },
    30: {
        1e-05: 1.0787618120576519,
        1.0: 1.0,
        10: 1.0,
        100: 1.021447076974441,
        1000: 1.2146874909006804,
    },
    60: {
        1e-05: 1.0,
        1.0: 1.0,
        10: 1.0656276624327379,
        100: 1.0069841472142111,
        1000: 1.157920149555634,
    },
}

lxy_uncertainty_for_signal_name_Pat = {
    "tta_mAlp-0p35GeV_ctau-1e-5mm": 1.0751775472965923,
    "tta_mAlp-0p35GeV_ctau-1e0mm": 1.6580155398904233,
    "tta_mAlp-0p35GeV_ctau-1e1mm": 1.7744752267281945,
    "tta_mAlp-0p35GeV_ctau-1e2mm": 1.7886358524233423,
    "tta_mAlp-0p35GeV_ctau-1e3mm": 1.7382818795907822,
    "tta_mAlp-2GeV_ctau-1e-5mm": 1.018757792582629,
    "tta_mAlp-2GeV_ctau-1e0mm": 1.304656885050331,
    "tta_mAlp-2GeV_ctau-1e1mm": 1.759043017118202,
    "tta_mAlp-2GeV_ctau-1e2mm": 1.8332521485089148,
    "tta_mAlp-2GeV_ctau-1e3mm": 1.8562650668689364,
    "tta_mAlp-12GeV_ctau-1e-5mm": 1.0176318167632186,
    "tta_mAlp-12GeV_ctau-1e0mm": 1.0299748247239688,
    "tta_mAlp-12GeV_ctau-1e1mm": 1.5460552294580743,
    "tta_mAlp-12GeV_ctau-1e2mm": 1.8118591872907945,
    "tta_mAlp-12GeV_ctau-1e3mm": 1.8342275618571864,
    "tta_mAlp-30GeV_ctau-1e-5mm": 1.0152587843531362,
    "tta_mAlp-30GeV_ctau-1e0mm": 1.0052241906710704,
    "tta_mAlp-30GeV_ctau-1e1mm": 1.3216429786813042,
    "tta_mAlp-30GeV_ctau-1e2mm": 1.6832780722730405,
    "tta_mAlp-30GeV_ctau-1e3mm": 1.7809811221509861,
    "tta_mAlp-60GeV_ctau-1e-5mm": 1.0183238432047126,
    "tta_mAlp-60GeV_ctau-1e0mm": 1.0009631738366698,
    "tta_mAlp-60GeV_ctau-1e1mm": 1.1586674819003944,
    "tta_mAlp-60GeV_ctau-1e2mm": 1.5730473781309178,
    "tta_mAlp-60GeV_ctau-1e3mm": 1.672553381331284,
}
lxy_uncertainty_for_signal_name_PatDSA = {
    "tta_mAlp-0p35GeV_ctau-1e-5mm": 1.0016921625614084,
    "tta_mAlp-0p35GeV_ctau-1e0mm": 1.0098381347549619,
    "tta_mAlp-0p35GeV_ctau-1e1mm": 1.011597850083839,
    "tta_mAlp-0p35GeV_ctau-1e2mm": 1.0168581196986548,
    "tta_mAlp-0p35GeV_ctau-1e3mm": 1.0359203901353742,
    "tta_mAlp-2GeV_ctau-1e-5mm": 1.0304667599722164,
    "tta_mAlp-2GeV_ctau-1e0mm": 1.0135249032541358,
    "tta_mAlp-2GeV_ctau-1e1mm": 1.0145903439852426,
    "tta_mAlp-2GeV_ctau-1e2mm": 1.0026839343072587,
    "tta_mAlp-2GeV_ctau-1e3mm": 1.028031837824204,
    "tta_mAlp-12GeV_ctau-1e-5mm": 1.0,
    "tta_mAlp-12GeV_ctau-1e0mm": 1.0032610677037601,
    "tta_mAlp-12GeV_ctau-1e1mm": 1.005505435653981,
    "tta_mAlp-12GeV_ctau-1e2mm": 1.0012123585126405,
    "tta_mAlp-12GeV_ctau-1e3mm": 1.037412454600737,
    "tta_mAlp-30GeV_ctau-1e-5mm": 1.0,
    "tta_mAlp-30GeV_ctau-1e0mm": 1.0,
    "tta_mAlp-30GeV_ctau-1e1mm": 1.0,
    "tta_mAlp-30GeV_ctau-1e2mm": 1.0058444156645938,
    "tta_mAlp-30GeV_ctau-1e3mm": 1.0148049501248515,
    "tta_mAlp-60GeV_ctau-1e-5mm": 1.0,
    "tta_mAlp-60GeV_ctau-1e0mm": 1.0270577276699955,
    "tta_mAlp-60GeV_ctau-1e1mm": 1.0123758166943433,
    "tta_mAlp-60GeV_ctau-1e2mm": 1.0,
    "tta_mAlp-60GeV_ctau-1e3mm": 1.0043655785674208,
}
lxy_uncertainty_for_signal_name_DSA = {
    "tta_mAlp-0p35GeV_ctau-1e-5mm": 1.0,
    "tta_mAlp-0p35GeV_ctau-1e0mm": 1.0240768066656263,
    "tta_mAlp-0p35GeV_ctau-1e1mm": 1.0489703320404307,
    "tta_mAlp-0p35GeV_ctau-1e2mm": 1.1143883198840958,
    "tta_mAlp-0p35GeV_ctau-1e3mm": 1.1098091416392566,
    "tta_mAlp-2GeV_ctau-1e-5mm": 1.0,
    "tta_mAlp-2GeV_ctau-1e0mm": 1.063088358150207,
    "tta_mAlp-2GeV_ctau-1e1mm": 1.0295855833787686,
    "tta_mAlp-2GeV_ctau-1e2mm": 1.1217019648537516,
    "tta_mAlp-2GeV_ctau-1e3mm": 1.1948926819260401,
    "tta_mAlp-12GeV_ctau-1e-5mm": 1.1513429489775904,
    "tta_mAlp-12GeV_ctau-1e0mm": 1.038000506692032,
    "tta_mAlp-12GeV_ctau-1e1mm": 1.004543068700814,
    "tta_mAlp-12GeV_ctau-1e2mm": 1.0616404176318504,
    "tta_mAlp-12GeV_ctau-1e3mm": 1.2257503771183138,
    "tta_mAlp-30GeV_ctau-1e-5mm": 1.0787618120576519,
    "tta_mAlp-30GeV_ctau-1e0mm": 1.0,
    "tta_mAlp-30GeV_ctau-1e1mm": 1.0,
    "tta_mAlp-30GeV_ctau-1e2mm": 1.021447076974441,
    "tta_mAlp-30GeV_ctau-1e3mm": 1.2146874909006804,
    "tta_mAlp-60GeV_ctau-1e-5mm": 1.0,
    "tta_mAlp-60GeV_ctau-1e0mm": 1.0,
    "tta_mAlp-60GeV_ctau-1e1mm": 1.0656276624327379,
    "tta_mAlp-60GeV_ctau-1e2mm": 1.0069841472142111,
    "tta_mAlp-60GeV_ctau-1e3mm": 1.157920149555634,
}

def get_lxy_uncertainty_for_mass_ctau(mass, ctau, category):
    if category == "Pat" or category == "_Pat":
        return lxy_uncertainty_for_mass_and_ctau_Pat[mass][ctau]
    if category == "PatDSA" or category == "_PatDSA":
        return lxy_uncertainty_for_mass_and_ctau_PatDSA[mass][ctau]
    if category == "DSA" or category == "_DSA":
        return lxy_uncertainty_for_mass_and_ctau_DSA[mass][ctau]
    error(f"Unknown category {category} for Lxy uncertainty")

def get_lxy_uncertainty_for_name(name, category):
    if category == "Pat" or category == "_Pat":
        return lxy_uncertainty_for_signal_name_Pat[name]
    if category == "PatDSA" or category == "_PatDSA":
        return lxy_uncertainty_for_signal_name_PatDSA[name]
    if category == "DSA" or category == "_DSA":
        return lxy_uncertainty_for_signal_name_DSA[name]
    error(f"Unknown category {category} for Lxy uncertainty")
