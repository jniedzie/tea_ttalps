#!/usr/bin/env python3

from math import sqrt, pi
import physics 


def get_cross_section_for_theory_coupling(mass, ctau):

  cross_section_for_mass_and_lifetime_Run2 = {
    # (mass [GeV], ctau [mm]):  sigma [pb], 
    ( 0.35, 1.0e-05):  5.19231e+03, # ctt = 1.15208e+02
    ( 0.35, 1.0e+00):  5.19231e-02, # ctt = 3.64318e-01
    ( 0.35, 1.0e+01):  5.19231e-03, # ctt = 1.15208e-01
    ( 0.35, 1.0e+02):  5.19231e-04, # ctt = 3.64318e-02
    ( 0.35, 1.0e+03):  5.19231e-05, # ctt = 1.15208e-02
    ( 2.00, 1.0e-05):  1.63141e+02, # ctt = 1.96317e+01
    ( 2.00, 1.0e+00):  1.63141e-03, # ctt = 6.20807e-02
    ( 2.00, 1.0e+01):  1.63141e-04, # ctt = 1.96317e-02
    ( 2.00, 1.0e+02):  1.63141e-05, # ctt = 6.20807e-03
    ( 2.00, 1.0e+03):  1.63141e-06, # ctt = 1.96317e-03
    (12.00, 1.0e-05):  3.76066e-04, # ctt = 3.05896e-02
    (12.00, 1.0e+00):  3.76066e-09, # ctt = 9.67327e-05
    (12.00, 1.0e+01):  3.76066e-10, # ctt = 3.05896e-05
    (12.00, 1.0e+02):  3.76066e-11, # ctt = 9.67327e-06
    (12.00, 1.0e+03):  3.76066e-12, # ctt = 3.05896e-06
    (30.00, 1.0e-05):  9.64833e-05, # ctt = 1.65937e-02
    (30.00, 1.0e+00):  9.64833e-10, # ctt = 5.24740e-05
    (30.00, 1.0e+01):  9.64833e-11, # ctt = 1.65937e-05
    (30.00, 1.0e+02):  9.64833e-12, # ctt = 5.24740e-06
    (30.00, 1.0e+03):  9.64833e-13, # ctt = 1.65937e-06
    (60.00, 1.0e-05):  3.46190e-05, # ctt = 1.13677e-02
    (60.00, 1.0e+00):  3.46190e-10, # ctt = 3.59477e-05
    (60.00, 1.0e+01):  3.46190e-11, # ctt = 1.13677e-05
    (60.00, 1.0e+02):  3.46190e-12, # ctt = 3.59477e-06
    (60.00, 1.0e+03):  3.46190e-13, # ctt = 1.13677e-06
  }
  return cross_section_for_mass_and_lifetime_Run2[(mass, ctau)]

# ------------------------------------------------------------
# Cross sections at reference coupling ctt = 0.1
# ------------------------------------------------------------
cross_section_for_mass_Run2 = {
    0.35: 0.003912,  # +- 2.935e-05 pb
    1.0:  0.004088,  # +- 3.1e-05 pb
    2.0:  0.004233,  # +- 3.199e-05 pb
    12.0: 0.004019,  # +- 3.065e-05 pb
    30.0: 0.003504,  # +- 2.162e-05 pb
    60.0: 0.002679,  # +- 1.323e-05 pb
    70.0: 0.002438,  # +- 1.888e-05 pb
}

cross_section_for_mass_Run3 = {
      0.35: 0.0044,   
      2.0: 0.00480,  
      12.0: 0.00455,  
      30.0: 0.00395,  
      60.0: 0.00304,  
  }

REFERENCE_CTT = 0.1

def find_BRs_for_mass(mass, coupling, Lambda=4*pi*1000):

    mu = 1 if mass < 1 else mass
    lscs = physics.getLSfromctt(coupling,0, Lambda, mu)
    br_to_mumu = physics.Gammaatoll(mass,physics.readCmumu(lscs),physics.sm['mmu'],Lambda)
    
    br_to_ee = physics.Gammaatoll(mass,physics.readCee(lscs),physics.sm['me'],Lambda)
    ctautau = 0
    try: 
        ctautau = physics.readCtautau(lscs)
    except IndexError:
        ctautau = 0
    br_to_tautau = physics.Gammaatoll(mass,ctautau,physics.sm['mtau'],Lambda)
    ccc = 0
    try:
        ccc = physics.readCcc(lscs)
    except IndexError:
        ccc = 0
    br_to_cc = physics.Gammaatoqq(mass,ccc,physics.sm['mc'],Lambda)
    cbb = 0
    try:
        cbb = physics.readCbb(lscs)
    except IndexError:
        cbb = 0
    br_to_bb = physics.Gammaatoqq(mass,cbb,physics.sm['mb'],Lambda)
    br_to_gammagamma = physics.Gammaatogamgam(mass,lscs,Lambda)
    br_to_had = physics.Gammaatohad(mass,lscs,Lambda)
    br_to_3pi000 = physics.Gammaato3pi000(mass,lscs,Lambda)
    br_to_3pi0pm = physics.Gammaato3pi0pm(mass,lscs,Lambda)

    br_tot = br_to_mumu + br_to_ee + br_to_tautau + br_to_cc + br_to_bb + br_to_gammagamma + br_to_had + br_to_3pi000 + br_to_3pi0pm
    br_mumu_final = br_to_mumu / br_tot
    br_3pi000_final = br_to_3pi000 / br_tot
    br_3pi0pm_final = br_to_3pi0pm / br_tot
    return br_mumu_final, br_3pi000_final, br_3pi0pm_final


# ------------------------------------------------------------
# Lifetime function
# ------------------------------------------------------------
def find_lifetime_for_mass(mass, coupling, boost=True, Lambda=4*pi*1000):
    ctau = physics.ctaua(mass, coupling, 0, Lambda)  # cm

    if boost:
        boost_factor = 1.0 / mass
        if mass < 3:
            boost_factor *= 223
        elif mass < 20:
            boost_factor *= 230
        elif mass < 30:
            boost_factor *= 240
        elif mass < 50:
            boost_factor *= 260
        else:
            boost_factor *= 296
        ctau *= boost_factor

    return ctau * 10.0  # mm


# ------------------------------------------------------------
# Reference lifetime (ctt = 1)
# ------------------------------------------------------------
def reference_ctau(mass, boost=True, Lambda=4*pi*1000):
    return find_lifetime_for_mass(mass=mass, coupling=1.0, boost=boost, Lambda=Lambda)


# ------------------------------------------------------------
# Invert using exact scaling: ctau ∝ 1/ctt^2
# ------------------------------------------------------------
def derive_ctt(mass, ctau_target, boost=True, Lambda=4*pi*1000):
    ctau_ref = reference_ctau(mass, boost, Lambda)
    return sqrt(ctau_ref / ctau_target)


# ------------------------------------------------------------
# Cross section scaling: sigma ∝ ctt^2
# ------------------------------------------------------------
def get_cross_section(mass, ctt):
    sigma_ref = cross_section_for_mass_Run3[mass]
    return sigma_ref * (ctt / REFERENCE_CTT) ** 2


# ------------------------------------------------------------
# Main scan
# ------------------------------------------------------------
def main():
    masses = [0.35, 2, 12, 30, 60]  # GeV
    couplings = [0.1, 1.0]

    print("\n=== Derived branching ratios ===\n")
    print(f"{'mass [GeV]':>10} \t {'coupling':>10} \t BR(a -> mumu) \t BR(a -> pi0pi0pi0) \t BR(a -> pi0pi+pi-)")
    print("-" * 55)

    for m in masses:
        for c in couplings:
            brs = find_BRs_for_mass(m, c)
            print(f"{m:10.2f}  {c:10.2f}  {brs[0]:12.5e}  {brs[1]:12.5e}  {brs[2]:12.5e}")
            # print(f"{get_cross_section_for_theory_coupling(m, ctau)}")

        print("-" * 55)


# ------------------------------------------------------------
if __name__ == "__main__":
    main()
