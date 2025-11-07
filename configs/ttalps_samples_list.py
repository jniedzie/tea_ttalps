##############################################################################
#####     DAS SAMPLES     #####

##################     2016    ##################

from ttalps_samples_list_2016 import dasSamples2016preVFP, dasData2016preVFP, dasBackgrounds2016preVFP, dasSignals2016preVFP, dasData2016_standard
from ttalps_samples_list_2016 import dasSamples2016postVFP, dasData2016postVFP, dasBackgrounds2016postVFP, dasSignals2016postVFP

##################     2017    ##################
from ttalps_samples_list_2017 import dasSamples2017, dasData2017, dasBackgrounds2017, dasSignals2017, dasData2017_standard

##################     2018    ##################
from ttalps_samples_list_2018 import dasSamples2018, dasData2018, dasBackgrounds2018, dasSignals2018, dasData2018_standard
from ttalps_samples_list_2018 import dasBackgrounds2018Devel, dasData2018Devel, dasSamples2018Devel

##################     2022    ##################
from ttalps_samples_list_2022 import dasSamples2022preEE, dasData2022preEE, dasBackgrounds2022preEE, dasSignals2022preEE, dasData2022_standard
from ttalps_samples_list_2022 import dasSamples2022postEE, dasData2022postEE, dasBackgrounds2022postEE, dasSignals2022postEE

##################     2023    ##################
from ttalps_samples_list_2023 import dasSamples2023preBPix, dasData2023preBPix, dasBackgrounds2023preBPix, dasSignals2023preBPix, dasData2023_standard
from ttalps_samples_list_2023 import dasSamples2023postBPix, dasData2023postBPix, dasBackgrounds2023postBPix, dasSignals2023postBPix

##################     All years    ##################
dasBackgrounds = {key: value for d in (
    dasBackgrounds2016preVFP,
    dasBackgrounds2016postVFP,
    dasBackgrounds2018,
    dasBackgrounds2017,
    dasBackgrounds2022preEE,
    dasBackgrounds2022postEE,
    dasBackgrounds2023preBPix,
    dasBackgrounds2023postBPix)
    for key, value in d.items()
}

dasSignals = {key: value for d in (
    dasSignals2016preVFP,
    dasSignals2016postVFP,
    dasSignals2018,
    dasSignals2017,
    dasSignals2022preEE,
    dasSignals2022postEE,
    dasSignals2023preBPix,
    dasSignals2023postBPix)
    for key, value in d.items()
}

dasData = {key: value for d in (
    dasData2016preVFP,
    dasData2016postVFP,
    dasData2018,
    dasData2017,
    dasData2022preEE,
    dasData2022postEE,
    dasData2023preBPix,
    dasData2023postBPix)
    for key, value in d.items()
}
