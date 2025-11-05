##############################################################################
#####     DAS SAMPLES     #####

##################     2016    ##################

from ttalps_samples_list_2016 import dasSamples2016PreVFP, dasData2016PreVFP, dasBackgrounds2016PreVFP, dasSignals2016PreVFP, dasData2016_standard
from ttalps_samples_list_2016 import dasSamples2016PostVFP, dasData2016PostVFP, dasBackgrounds2016PostVFP, dasSignals2016PostVFP

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
    dasBackgrounds2016PreVFP,
    dasBackgrounds2016PostVFP,
    dasBackgrounds2018,
    dasBackgrounds2017,
    dasSamples2022preEE,
    dasSamples2022postEE,
    dasSamples2023preBPix,
    dasSamples2023postBPix)
    for key, value in d.items()
}

dasSignals = {key: value for d in (
    dasSignals2016PreVFP,
    dasSignals2016PostVFP,
    dasSignals2018,
    dasSignals2017,
    dasSignals2022preEE,
    dasSignals2022postEE,
    dasSignals2023preBPix,
    dasSignals2023postBPix)
    for key, value in d.items()
}

dasData = {key: value for d in (
    dasData2016PreVFP,
    dasData2016PostVFP,
    dasData2018,
    dasData2017,
    dasData2022preEE,
    dasData2022postEE,
    dasData2023preBPix,
    dasData2023postBPix)
    for key, value in d.items()
}
