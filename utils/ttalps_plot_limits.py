import ROOT
from ttalps_cross_sections import cross_sections

year = "2018"
cross_sections = get_cross_sections(year)

y_min = 1e-3
y_max = 1e4

########  Signal Limits Summary Lxy Significance  ########
####  PAT-PAT  ####
    # ("tta_mAlp-0p35GeV_ctau-1e-5mm", 0.35): (53.9981,27.3901,37.3454,53.9375,79.0922,110.6069,),
    # ("tta_mAlp-0p35GeV_ctau-1e0mm", 0.35): (12.4943,5.5664,8.1123,12.5000,19.4756,28.8879,),
    # ("tta_mAlp-0p35GeV_ctau-1e1mm", 0.35): (55.5908,21.5596,33.5796,55.7500,91.7499,140.9686,),
    # ("tta_mAlp-0p35GeV_ctau-1e2mm", 0.35): (558.9079,218.3594,338.1158,559.0000,919.9681,1425.6646),
    # ("tta_mAlp-0p35GeV_ctau-1e3mm", 0.35): (4200.2824,1593.7500,2514.8926,4000.0000,7156.9458,11733.1719,),
    # ("tta_mAlp-1GeV_ctau-1e-5mm", 1): (180.8130,101.6719,133.1796,180.7500,244.8725,317.4915,),
    # ("tta_mAlp-1GeV_ctau-1e0mm", 1): (8.4522,3.7712,5.4961,8.4688,13.1609,19.5058,),
    # ("tta_mAlp-1GeV_ctau-1e1mm", 1): (21.1509,7.9688,12.6379,21.2500,35.6496,55.3392,),
    # ("tta_mAlp-1GeV_ctau-1e2mm", 1): (36.2018,13.5938,21.4703,36.2500,61.1030,95.2623,),
    # ("tta_mAlp-1GeV_ctau-1e3mm", 1): (1344.4657,447.5781,750.0636,1348.0000,2422.6372,3981.1968,),
    # ("tta_mAlp-2GeV_ctau-1e-5mm", 2): (162.8830,91.5469,119.9169,162.7500,220.4868,285.8741,),
    # ("tta_mAlp-2GeV_ctau-1e0mm", 2): (8.3411,3.8604,5.5181,8.3750,12.8817,18.9778,),
    # ("tta_mAlp-2GeV_ctau-1e1mm", 2): (12.7533,4.9048,7.6848,12.8125,21.1882,32.7127,),
    # ("tta_mAlp-2GeV_ctau-1e2mm", 2): (78.5575,27.9932,45.4408,78.7500,135.8800,216.8075,),
    # ("tta_mAlp-2GeV_ctau-1e3mm", 2): (570.3231,198.8594,324.2113,572.0000,1014.3232,1665.7311,),
    # ("tta_mAlp-12GeV_ctau-1e0mm", 12): (47.9084,24.6855,33.5628,47.8750,69.0573,95.6612,),
    # ("tta_mAlp-12GeV_ctau-1e1mm", 12): (12.5246,5.3489,7.9413,12.5625,19.9736,30.0839,),
    # ("tta_mAlp-12GeV_ctau-1e2mm", 12): (24.1039,8.2930,13.6115,24.1250,42.9730,70.2744,),
    # ("tta_mAlp-12GeV_ctau-1e3mm", 12): (),
    # ("tta_mAlp-30GeV_ctau-1e0mm", 30): (),
    # ("tta_mAlp-30GeV_ctau-1e1mm", 30): (),
    # ("tta_mAlp-30GeV_ctau-1e2mm", 30): (),
    # ("tta_mAlp-30GeV_ctau-1e3mm", 30): (),
    # ("tta_mAlp-60GeV_ctau-1e0mm", 60): (82.0796,46.1250,60.4189,82.0000,111.0901,144.0349,),
    # ("tta_mAlp-60GeV_ctau-1e1mm", 60): (),
    # ("tta_mAlp-60GeV_ctau-1e2mm", 60): (32.2887,12.0142,19.0927,32.3750,54.8294,86.5208,),
    # ("tta_mAlp-60GeV_ctau-1e3mm", 60): (),
    # ("tta_mAlp-70GeV_ctau-1e0mm", 70): (150.7006,84.0684,110.5372,150.5000,203.8911,264.3567,),
####  PAT-DSA  ####
    # ("tta_mAlp-0p35GeV_ctau-1e-5mm", 0.35): (1318.7859,695.5664,943.9657,1319.0000,1839.5015,2441.7214,),
    # ("tta_mAlp-0p35GeV_ctau-1e0mm", 0.35): (1020.1974,485.1406,684.9629,1018.0000,1513.0505,2125.0479,),
    # ("tta_mAlp-0p35GeV_ctau-1e1mm", 0.35): (1425.6414,657.2969,939.5551,1426.0000,2193.3530,3197.8396,),
    # ("tta_mAlp-0p35GeV_ctau-1e2mm", 0.35): (5883.9139,2562.5000,3752.9297,4000.0000,8049.8193,12131.2783,),
    # # ("tta_mAlp-0p35GeV_ctau-1e3mm", 0.35): (),
    # ("tta_mAlp-1GeV_ctau-1e-5mm", 1): (2112.2057,1113.7500,1511.4902,2112.0000,2945.4338,3909.7163,),
    # ("tta_mAlp-1GeV_ctau-1e0mm", 1): (1309.1825,658.6055,906.8190,1307.0000,1885.2831,2578.9338,),
    # ("tta_mAlp-1GeV_ctau-1e1mm", 1): (1105.7227,479.1211,708.9360,1105.0000,1721.6409,2508.8901,),
    # ("tta_mAlp-1GeV_ctau-1e2mm", 1): (1534.3782,699.7148,1004.9524,1531.0000,2354.8552,3424.3176,),
    # # ("tta_mAlp-1GeV_ctau-1e3mm", 1): (),
    # ("tta_mAlp-2GeV_ctau-1e-5mm", 2): (1938.2185,1080.8789,1421.1927,1935.0000,2636.8823,3448.6748,),
    # ("tta_mAlp-2GeV_ctau-1e0mm", 2): (1395.9691,740.0312,995.0972,1393.0000,1953.8083,2604.5637,),
    # ("tta_mAlp-2GeV_ctau-1e1mm", 2): (967.6095,459.8828,649.3018,965.0000,1453.5095,2072.4856,),
    # ("tta_mAlp-2GeV_ctau-1e2mm", 2): (1420.8936,609.2969,906.2426,1418.0000,2265.8313,3400.7771,),
    # ("tta_mAlp-2GeV_ctau-1e3mm", 2): (5093.8495,2000.0000,3062.5000,4000.0000,8049.8193,12131.2783,),
    # ("tta_mAlp-12GeV_ctau-1e0mm", 12): (1215.7429,678.1328,891.6424,1214.0000,1654.3541,2155.7068,),
    # ("tta_mAlp-12GeV_ctau-1e1mm", 12): (529.9263,252.5781,354.4440,530.0000,810.9761,1195.6761,),
    # ("tta_mAlp-12GeV_ctau-1e2mm", 12): (196.7520,90.5742,129.4688,196.5000,306.9393,463.5847,),
    # # ("tta_mAlp-12GeV_ctau-1e3mm", 12): (),
    # # ("tta_mAlp-30GeV_ctau-1e0mm", 30): (),
    # # ("tta_mAlp-30GeV_ctau-1e1mm", 30): (),
    # # ("tta_mAlp-30GeV_ctau-1e2mm", 30): (),
    # # ("tta_mAlp-30GeV_ctau-1e3mm", 30): (),
    # ("tta_mAlp-60GeV_ctau-1e0mm", 60): (1594.6398,883.0625,1165.5298,1592.0000,2169.4661,2847.7952,),
    # # ("tta_mAlp-60GeV_ctau-1e1mm", 60): (),
    # ("tta_mAlp-60GeV_ctau-1e2mm", 60): (85.4885,38.7422,55.5458,85.5000,135.5986,206.5423,),
    # # ("tta_mAlp-60GeV_ctau-1e3mm", 60): (),
    # ("tta_mAlp-70GeV_ctau-1e0mm", 70): (1739.8951,963.4922,1271.6868,1737.0000,2367.0618,3095.7871,),
####  DSA-DSA  ####
    # ("tta_mAlp-0p35GeV_ctau-1e-5mm", 0.35): (2532.6318,1296.1836,1759.9897,2533.0000,3724.4043,5324.9595,),
    # ("tta_mAlp-0p35GeV_ctau-1e0mm", 0.35): (334.7197,160.7168,224.5278,334.5000,507.8331,740.6140,),
    # ("tta_mAlp-0p35GeV_ctau-1e1mm", 0.35): (157.5546,73.3291,103.6679,157.7500,245.7818,368.2206,),
    # ("tta_mAlp-0p35GeV_ctau-1e2mm", 0.35): (497.1847,227.6016,324.7760,498.0000,789.8022,1203.0182,),
    # ("tta_mAlp-0p35GeV_ctau-1e3mm", 0.35): (3008.5804,1339.9453,1939.7618,3009.0000,4904.0522,7856.2637,),
    # ("tta_mAlp-1GeV_ctau-1e-5mm", 1): (3448.1629,1681.1523,2328.0808,3443.0000,5213.3892,7656.7339,),
    # ("tta_mAlp-1GeV_ctau-1e0mm", 1): (897.9670,431.4609,602.7682,898.0000,1363.3307,1988.2551,),
    # ("tta_mAlp-1GeV_ctau-1e1mm", 1): (139.3591,65.3906,92.0237,139.5000,216.7914,322.9258,),
    # ("tta_mAlp-1GeV_ctau-1e2mm", 1): (162.9257,75.1328,107.3965,163.0000,255.9107,385.1501,),
    # ("tta_mAlp-1GeV_ctau-1e3mm", 1): (1032.7060,468.9844,672.3962,1035.0000,1653.8331,2552.2371,),
    # ("tta_mAlp-2GeV_ctau-1e-5mm", 2): (5100.1304,2625.0000,3548.8281,4000.0000,7539.6060,11043.5869,),
    # ("tta_mAlp-2GeV_ctau-1e0mm", 2): (2072.9825,1043.5898,1428.8687,2071.0000,3086.3767,4503.8345,),
    # ("tta_mAlp-2GeV_ctau-1e1mm", 2): (161.2911,75.7031,106.5364,161.5000,250.3369,371.6579,),
    # ("tta_mAlp-2GeV_ctau-1e2mm", 2): (112.2028,51.8555,73.6496,112.5000,177.0739,268.6096,),
    # ("tta_mAlp-2GeV_ctau-1e3mm", 2): (506.5927,231.7148,330.6454,507.0000,804.0758,1236.2850,),
    # ("tta_mAlp-12GeV_ctau-1e0mm", 12): (2224.4465,1153.3594,1561.6827,2220.0000,3219.9387,4502.5967,),
    # ("tta_mAlp-12GeV_ctau-1e1mm", 12): (661.8437,312.8984,441.0842,662.0000,1020.8714,1513.0826,),
    # ("tta_mAlp-12GeV_ctau-1e2mm", 12): (26.9653,10.3359,16.1944,27.0000,45.7264,72.7247,),
    # # ("tta_mAlp-12GeV_ctau-1e3mm", 12): (),
    # # ("tta_mAlp-30GeV_ctau-1e0mm", 30): (),
    # # ("tta_mAlp-30GeV_ctau-1e1mm", 30): (),
    # # ("tta_mAlp-30GeV_ctau-1e2mm", 30): (),
    # # ("tta_mAlp-30GeV_ctau-1e3mm", 30): (),
    # ("tta_mAlp-60GeV_ctau-1e0mm", 60): (4482.2508,2328.1250,3151.0010,4000.0000,6519.1792,9297.2021,),
    # # ("tta_mAlp-60GeV_ctau-1e1mm", 60): (),
    # ("tta_mAlp-60GeV_ctau-1e2mm", 60): (84.2631,32.3477,50.6825,84.5000,142.4332,225.6384,),
    # # ("tta_mAlp-60GeV_ctau-1e3mm", 60): (),
    # ("tta_mAlp-70GeV_ctau-1e0mm", 70): (4813.0378,2484.3750,3360.5957,4000.0000,7029.3926,10077.7188,),



#########  OVER MASS  #########
x_min = 0.1
x_max = 1e2
x_title = "m_{a} [GeV]"
####  1 mm ALP  ####
# output_name = "BestPFIsoDimuonVertex_PAT_LxySignificance_1e0mm_mass"
# cross_section_limits = {
#     ("tta_mAlp-0p35GeV_ctau-1e0mm", 0.35): (12.4943,5.5664,8.1123,12.5000,19.4756,28.8879,),
# # #     ("tta_mAlp-1GeV_ctau-1e0mm", 1): (8.4522,3.7712,5.4961,8.4688,13.1609,19.5058,),
#     ("tta_mAlp-2GeV_ctau-1e0mm", 2): (8.3411,3.8604,5.5181,8.3750,12.8817,18.9778,),
#     ("tta_mAlp-12GeV_ctau-1e0mm", 12): (47.9084,24.6855,33.5628,47.8750,69.0573,95.6612,),
#     # ("tta_mAlp-30GeV_ctau-1e0mm", 30): (),
#     ("tta_mAlp-60GeV_ctau-1e0mm", 60): (82.0796,46.1250,60.4189,82.0000,111.0901,144.0349,),
# # #     ("tta_mAlp-70GeV_ctau-1e0mm", 70): (150.7006,84.0684,110.5372,150.5000,203.8911,264.3567,),
# }
# output_name = "BestPFIsoDimuonVertex_PATDSA_LxySignificance_1e0mm_mass"
# cross_section_limits = {
    # ("tta_mAlp-0p35GeV_ctau-1e0mm", 0.35): (1020.1974,485.1406,684.9629,1018.0000,1513.0505,2125.0479,),
    # # # ("tta_mAlp-1GeV_ctau-1e0mm", 1): (1309.1825,658.6055,906.8190,1307.0000,1885.2831,2578.9338,),
    # ("tta_mAlp-2GeV_ctau-1e0mm", 2): (1395.9691,740.0312,995.0972,1393.0000,1953.8083,2604.5637,),
    # ("tta_mAlp-12GeV_ctau-1e0mm", 12): (1215.7429,678.1328,891.6424,1214.0000,1654.3541,2155.7068,),
    # # ("tta_mAlp-30GeV_ctau-1e0mm", 30): (),
    # ("tta_mAlp-60GeV_ctau-1e0mm", 60): (1594.6398,883.0625,1165.5298,1592.0000,2169.4661,2847.7952,),
    # # # ("tta_mAlp-70GeV_ctau-1e0mm", 70): (1739.8951,963.4922,1271.6868,1737.0000,2367.0618,3095.7871,),
# }
output_name = "BestPFIsoDimuonVertex_DSA_LxySignificance_1e0mm_mass"
cross_section_limits = {
    ("tta_mAlp-0p35GeV_ctau-1e0mm", 0.35): (334.7197,160.7168,224.5278,334.5000,507.8331,740.6140,),
# #     ("tta_mAlp-1GeV_ctau-1e0mm", 1): (897.9670,431.4609,602.7682,898.0000,1363.3307,1988.2551,),
    ("tta_mAlp-2GeV_ctau-1e0mm", 2): (2072.9825,1043.5898,1428.8687,2071.0000,3086.3767,4503.8345,),
    ("tta_mAlp-12GeV_ctau-1e0mm", 12): (2224.4465,1153.3594,1561.6827,2220.0000,3219.9387,4502.5967,),
    # ("tta_mAlp-30GeV_ctau-1e0mm", 30): (),
    ("tta_mAlp-60GeV_ctau-1e0mm", 60): (4482.2508,2328.1250,3151.0010,4000.0000,6519.1792,9297.2021,),
# #     ("tta_mAlp-70GeV_ctau-1e0mm", 70): (4813.0378,2484.3750,3360.5957,4000.0000,7029.3926,10077.7188,),
}
####  10 cm ALP  ####
# output_name = "BestPFIsoDimuonVertex_PAT_LxySignificance_1e2mm_mass"
# cross_section_limits = {
#     ("tta_mAlp-0p35GeV_ctau-1e2mm", 0.35): (558.9079,218.3594,338.1158,559.0000,919.9681,1425.6646),
# # #     ("tta_mAlp-1GeV_ctau-1e2mm", 1): (36.2018,13.5938,21.4703,36.2500,61.1030,95.2623,),
#     ("tta_mAlp-2GeV_ctau-1e2mm", 2): (78.5575,27.9932,45.4408,78.7500,135.8800,216.8075,),
#     ("tta_mAlp-12GeV_ctau-1e2mm", 12): (24.1039,8.2930,13.6115,24.1250,42.9730,70.2744,),
#     # ("tta_mAlp-30GeV_ctau-1e2mm", 30): (),
#     ("tta_mAlp-60GeV_ctau-1e2mm", 60): (32.2887,12.0142,19.0927,32.3750,54.8294,86.5208,),
# }
# output_name = "BestPFIsoDimuonVertex_PATDSA_LxySignificance_1e2mm_mass"
# cross_section_limits = {
#     ("tta_mAlp-0p35GeV_ctau-1e2mm", 0.35): (5883.9139,2562.5000,3752.9297,4000.0000,8049.8193,12131.2783,),
# # #     ("tta_mAlp-1GeV_ctau-1e2mm", 1): (1534.3782,699.7148,1004.9524,1531.0000,2354.8552,3424.3176,),
#     ("tta_mAlp-2GeV_ctau-1e2mm", 2): (1420.8936,609.2969,906.2426,1418.0000,2265.8313,3400.7771,),
#     ("tta_mAlp-12GeV_ctau-1e2mm", 12): (196.7520,90.5742,129.4688,196.5000,306.9393,463.5847,),
#     # ("tta_mAlp-30GeV_ctau-1e2mm", 30): (),
#     ("tta_mAlp-60GeV_ctau-1e2mm", 60): (85.4885,38.7422,55.5458,85.5000,135.5986,206.5423,),
# }
# output_name = "BestPFIsoDimuonVertex_DSA_LxySignificance_1e2mm_mass"
# cross_section_limits = {
#     ("tta_mAlp-0p35GeV_ctau-1e2mm", 0.35): (497.1847,227.6016,324.7760,498.0000,789.8022,1203.0182,),
# # #     ("tta_mAlp-1GeV_ctau-1e2mm", 1): (162.9257,75.1328,107.3965,163.0000,255.9107,385.1501,),
#     ("tta_mAlp-2GeV_ctau-1e2mm", 2): (112.2028,51.8555,73.6496,112.5000,177.0739,268.6096,),
#     ("tta_mAlp-12GeV_ctau-1e2mm", 12): (26.9653,10.3359,16.1944,27.0000,45.7264,72.7247,),
#     # ("tta_mAlp-30GeV_ctau-1e2mm", 30): (),
#     ("tta_mAlp-60GeV_ctau-1e2mm", 60): (84.2631,32.3477,50.6825,84.5000,142.4332,225.6384,),
# }

#########  OVER CTAU  #########
# x_min = 1e-5 * 1e-3
# x_max = 1e5 * 1e-3
# x_title = "c#tau [m]"
####  2 GeV ALP  ####
# output_name = "BestPFIsoDimuonVertex_PAT_LxySignificance_2GeV_ctau"
# cross_section_limits = {
# ("tta_mAlp-2GeV_ctau-1e-5mm", 1e-5*1e-3): (162.8830,91.5469,119.9169,162.7500,220.4868,285.8741,),
#     ("tta_mAlp-2GeV_ctau-1e0mm", 1e0*1e-3): (8.3411,3.8604,5.5181,8.3750,12.8817,18.9778,),
#     ("tta_mAlp-2GeV_ctau-1e1mm", 1e1*1e-3): (12.7533,4.9048,7.6848,12.8125,21.1882,32.7127,),
#     ("tta_mAlp-2GeV_ctau-1e2mm", 1e2*1e-3): (78.5575,27.9932,45.4408,78.7500,135.8800,216.8075,),
#     ("tta_mAlp-2GeV_ctau-1e3mm", 1e3*1e-3): (570.3231,198.8594,324.2113,572.0000,1014.3232,1665.7311,),
# }
# output_name = "BestPFIsoDimuonVertex_PATDSA_LxySignificance_2GeV_ctau"
# cross_section_limits = {
# ("tta_mAlp-2GeV_ctau-1e-5mm", 1e-5*1e-3): (1938.2185,1080.8789,1421.1927,1935.0000,2636.8823,3448.6748,),
#     ("tta_mAlp-2GeV_ctau-1e0mm", 1e0*1e-3): (1395.9691,740.0312,995.0972,1393.0000,1953.8083,2604.5637,),
#     ("tta_mAlp-2GeV_ctau-1e1mm", 1e1*1e-3): (967.6095,459.8828,649.3018,965.0000,1453.5095,2072.4856,),
#     ("tta_mAlp-2GeV_ctau-1e2mm", 1e2*1e-3): (1420.8936,609.2969,906.2426,1418.0000,2265.8313,3400.7771,),
#     ("tta_mAlp-2GeV_ctau-1e3mm", 1e3*1e-3): (5093.8495,2000.0000,3062.5000,4000.0000,8049.8193,12131.2783,),
# }
# output_name = "BestPFIsoDimuonVertex_DSA_LxySignificance_2GeV_ctau"
# cross_section_limits = {
#     ("tta_mAlp-2GeV_ctau-1e-5mm", 1e-5*1e-3): (5100.1304,2625.0000,3548.8281,4000.0000,7539.6060,11043.5869,),
#     ("tta_mAlp-2GeV_ctau-1e0mm", 1e0*1e-3): (2072.9825,1043.5898,1428.8687,2071.0000,3086.3767,4503.8345,),
#     ("tta_mAlp-2GeV_ctau-1e1mm", 1e1*1e-3): (161.2911,75.7031,106.5364,161.5000,250.3369,371.6579,),
#     ("tta_mAlp-2GeV_ctau-1e2mm", 1e2*1e-3): (112.2028,51.8555,73.6496,112.5000,177.0739,268.6096,),
#     ("tta_mAlp-2GeV_ctau-1e3mm", 1e3*1e-3): (506.5927,231.7148,330.6454,507.0000,804.0758,1236.2850,),
# }
####  12 GeV ALP  ####
# output_name = "BestPFIsoDimuonVertex_PAT_LxySignificance_12GeV_ctau"
# cross_section_limits = {
#     ("tta_mAlp-12GeV_ctau-1e0mm", 1e0*1e-3): (47.9084,24.6855,33.5628,47.8750,69.0573,95.6612,),
#     ("tta_mAlp-12GeV_ctau-1e1mm", 1e1*1e-3): (12.5246,5.3489,7.9413,12.5625,19.9736,30.0839,),
#     ("tta_mAlp-12GeV_ctau-1e2mm", 1e2*1e-3): (24.1039,8.2930,13.6115,24.1250,42.9730,70.2744,),
# }
# output_name = "BestPFIsoDimuonVertex_PATDSA_LxySignificance_12GeV_ctau"
# cross_section_limits = {
#     ("tta_mAlp-12GeV_ctau-1e0mm", 1e0*1e-3): (1215.7429,678.1328,891.6424,1214.0000,1654.3541,2155.7068,),
#     ("tta_mAlp-12GeV_ctau-1e1mm", 1e1*1e-3): (529.9263,252.5781,354.4440,530.0000,810.9761,1195.6761,),
#     ("tta_mAlp-12GeV_ctau-1e2mm", 1e2*1e-3): (196.7520,90.5742,129.4688,196.5000,306.9393,463.5847,),
# }
# output_name = "BestPFIsoDimuonVertex_DSA_LxySignificance_12GeV_ctau"
# cross_section_limits = {
#     ("tta_mAlp-12GeV_ctau-1e0mm", 1e0*1e-3): (2224.4465,1153.3594,1561.6827,2220.0000,3219.9387,4502.5967,),
#     ("tta_mAlp-12GeV_ctau-1e1mm", 1e1*1e-3): (661.8437,312.8984,441.0842,662.0000,1020.8714,1513.0826,),
#     ("tta_mAlp-12GeV_ctau-1e2mm", 1e2*1e-3): (26.9653,10.3359,16.1944,27.0000,45.7264,72.7247,),
# }


def main():
    ROOT.gROOT.SetBatch(True)
    
    obs_graph = ROOT.TGraph()
    obs_graph.SetLineColor(ROOT.kBlack)
    obs_graph.SetLineWidth(2)
    obs_graph.SetLineStyle(1)

    exp_graph = ROOT.TGraphAsymmErrors()
    exp_graph.SetLineColor(ROOT.kBlack)
    exp_graph.SetLineWidth(2)
    exp_graph.SetLineStyle(2)

    exp_graph_1sigma = ROOT.TGraphAsymmErrors()
    exp_graph_1sigma.SetLineWidth(0)
    exp_graph_1sigma.SetFillColorAlpha(ROOT.kGreen+1, 1.0)

    exp_graph_2sigma = ROOT.TGraphAsymmErrors()
    exp_graph_2sigma.SetLineWidth(0)
    exp_graph_2sigma.SetFillColorAlpha(ROOT.kYellow+1, 1.0)

    for i, (name, ctau) in enumerate(cross_section_limits):
        
        scale = cross_sections[name]
        limits = cross_section_limits[(name, ctau)]
        
        obs_graph.SetPoint(i, ctau, limits[0]*scale)
        exp_graph.SetPoint(i, ctau, limits[3]*scale)

        exp_graph_1sigma.SetPoint(i, ctau, limits[3]*scale)
        exp_graph_1sigma.SetPointError(i, 0, 0, (limits[3] - limits[2])*scale, (limits[4] - limits[3])*scale)

        exp_graph_2sigma.SetPoint(i, ctau, limits[3]*scale)
        exp_graph_2sigma.SetPointError(i, 0, 0, (limits[3] - limits[1])*scale, (limits[5] - limits[3])*scale)

    canvas = ROOT.TCanvas("canvas", "", 800, 600)
    canvas.cd()
    canvas.SetLogx()
    canvas.SetLogy()


    exp_graph_2sigma.Draw("A3")
    exp_graph_1sigma.Draw("3same")
    exp_graph.Draw("Lsame")
    obs_graph.Draw("Lsame")

    exp_graph_2sigma.GetXaxis().SetTitleSize(0.05)
    exp_graph_2sigma.GetYaxis().SetTitleSize(0.05)
    exp_graph_2sigma.GetXaxis().SetLabelSize(0.04)
    exp_graph_2sigma.GetYaxis().SetLabelSize(0.04)
    exp_graph_2sigma.GetXaxis().SetTitleOffset(1.1)
    exp_graph_2sigma.GetYaxis().SetTitleOffset(1.1)
    
    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetBottomMargin(0.15)

    exp_graph_2sigma.GetXaxis().SetTitle(x_title)
    exp_graph_2sigma.GetYaxis().SetTitle(
        "#sigma_{pp #rightarrow a #rightarrow #mu #mu} [pb]")

    # exp_graph_2sigma.GetXaxis().SetMoreLogLabels()

    # set x and y axes limits
    exp_graph_2sigma.GetXaxis().SetLimits(x_min, x_max)
    exp_graph_2sigma.SetMinimum(y_min)
    exp_graph_2sigma.SetMaximum(y_max)

    legend = ROOT.TLegend(0.20, 0.65, 0.45, 0.9)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.04)
    legend.AddEntry(obs_graph, "Observed", "L")
    legend.AddEntry(exp_graph, "Expected", "L")
    legend.AddEntry(exp_graph_1sigma, "Expected #pm 1 #sigma", "F")
    legend.AddEntry(exp_graph_2sigma, "Expected #pm 2 #sigma", "F")
    legend.Draw()

    tex = ROOT.TLatex(0.15, 0.92, "#bf{CMS} #it{Preliminary}")
    # tex = ROOT.TLatex(0.15, 0.92, "#bf{CMS}")
    tex.SetNDC()
    tex.SetTextFont(42)
    tex.SetTextSize(0.045)
    tex.SetLineWidth(2)
    tex.Draw()

    tex2 = ROOT.TLatex(0.60, 0.92, "#scale[0.8]{pp, 60 fb^{-1} (#sqrt{s} = 13 TeV)}")
    tex2.SetNDC()
    tex2.SetTextFont(42)
    tex2.SetTextSize(0.045)
    tex2.SetLineWidth(2)
    tex2.Draw()

    canvas.Update()
    canvas.SaveAs(f"../plots/limits_cross_section_{output_name}.pdf")
    

if __name__ == "__main__":
    main()
