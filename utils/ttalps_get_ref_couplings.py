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
cross_section_unc_for_mass_Run2 = {
    0.35: 2.935e-05,
    1.0:  3.1e-05,
    2.0:  3.199e-05,
    12.0: 3.065e-05,
    30.0: 2.162e-05,
    60.0: 1.323e-05,
    70.0: 1.888e-05,
}

cross_section_for_mass_Run3 = {
    0.35: 0.0044,   
    2.0: 0.00480,  
    12.0: 0.00455,  
    30.0: 0.00395,  
    60.0: 0.00304,  
  }
cross_section_unc_for_mass_Run3 = {
    0.35: 0.04e-3,   
    2.0:  0.05e-3,  
    12.0: 0.09e-3,  
    30.0: 0.04e-3,  
    60.0: 0.06e-3,  
}


REFERENCE_CTT = 0.1

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
def get_cross_section(mass, ctt, unc = False):
    sigma_ref = cross_section_for_mass_Run3[mass]
    if unc:
        sigma_ref = cross_section_unc_for_mass_Run3[mass]
    return sigma_ref * (ctt / REFERENCE_CTT) ** 2


# ------------------------------------------------------------
# Main scan
# ------------------------------------------------------------
def main():
    masses = [0.35, 2, 12, 30, 60]  # GeV
    # ctau_values = [1e-9, 3e-9, 1e-8, 1e-5, 1e-3, 1e-1, 1e0, 1e1, 1e2, 1e3]  # mm
    ctau_values = [1e-5, 1e0, 1e1, 1e2, 1e3]  # mm

    boost = False

    print("\n=== Derived ctt values and cross sections ===\n")
    print(f"{'mass [GeV]':>10}  {'ctau [mm]':>12}  {'ctt':>12}  {'sigma [pb]':>12}")
    print("-" * 55)

    for m in masses:
        for ctau in ctau_values:
            ctt = derive_ctt(m, ctau, boost=boost)
            sigma = get_cross_section(m, ctt)
            sigma_unc = get_cross_section(m, ctt, unc=True)
            print(f"{m:10.2f}  {ctau:12.3e}  {ctt:12.5e}  {sigma:12.2e} \\pm {sigma_unc:12.2e}")
            # print(f"{get_cross_section_for_theory_coupling(m, ctau)}")

        print("-" * 55)

    print(f"lifetimes for ctt=1: {[reference_ctau(m, boost=boost) for m in masses]} mm")

    eta_masses = [0.5, 0.75, 1, 1.5, 2, 3, 4]
    eta_prime_masses = [0.85, 1, 1.5, 2, 3, 4]
    print("\n\nLifetimes for coupling=1:")
    for mass in eta_masses:
        print(f"eta mass {mass}: {find_lifetime_for_mass(mass, 1.0, False):12.3e}")
    for mass in eta_prime_masses:
        print(f"eta prime mass {mass}: {find_lifetime_for_mass(mass, 1.0, False):12.3e}")
    
    phi_masses = [15, 20, 25, 30, 40, 50, 60]
    print("\n\nLifetimes for coupling=0.1:")
    for mass in phi_masses:
        print(f"phi mass {mass}: {find_lifetime_for_mass(mass, 0.1, False):12.3e}")

    phi_masses_couplings2 = [
        (15,  21.54),
        (20,  16.74),
        (25,  11.83),
        (30,  7.93),
        (40,  3.35),
        (50,  2.39),
        (60,  1.90),
    ]
    lumi_scale = sqrt(138/200)
    print("\n\nLifetimes for phi coupling limits:")
    for (mass, coupling2) in phi_masses_couplings2:
        coupling = sqrt(coupling2)
        coupling2_scaled = coupling2*lumi_scale
        coupling_scaled = sqrt(coupling2_scaled)
        print(f"phi mass {mass}, coupling {coupling}: {find_lifetime_for_mass(mass, coupling, False):12.3e}, scaled coupling {coupling_scaled}: {find_lifetime_for_mass(mass, coupling_scaled, False):12.3e}")

    atlas_masses = [15, 60]
    altas_coupling = 0.7
    for mass in atlas_masses:
        print(f"altas mass {mass}: {find_lifetime_for_mass(mass, altas_coupling, False):12.3e}")

    cms_dm_mass = 50
    cms_dm_coupling1 = 1.0
    print(f"cms dm mass {cms_dm_mass}: {find_lifetime_for_mass(cms_dm_mass, cms_dm_coupling1, False):12.3e}")
    cms_dm_limit = 33.38
    print(f"cms dm mass {cms_dm_mass}: {find_lifetime_for_mass(cms_dm_mass, cms_dm_limit, False):12.3e}")



# ------------------------------------------------------------
if __name__ == "__main__":
    main()

# Run 3
# 0.35\GeV & $(5.84 \pm 0.05)\times10^{3}$ & $(5.84 \pm 0.05)\times10^{-2}$ & $(5.84 \pm 0.05)\times10^{-3}$ & $(5.84 \pm 0.05)\times10^{-4}$ & $(5.84 \pm 0.05)\times10^{-5}$ \\ 
# 2\GeV    & $(1.85 \pm 0.02)\times10^{2}$ & $(1.85 \pm 0.02)\times10^{-3}$ & $(1.85 \pm 0.02)\times10^{-4}$ & $(1.85 \pm 0.02)\times10^{-5}$ & $(1.85 \pm 0.02)\times10^{-6}$ \\ 
# 12\GeV   & $(4.26 \pm 0.08)\times10^{-4}$ & $(4.26 \pm 0.08)\times10^{-9}$ & $(4.26 \pm 0.08)\times10^{-10}$ & $(4.26 \pm 0.08)\times10^{-11}$ & $(4.26 \pm 0.08)\times10^{-12}$ \\ 
# 30\GeV   & $(1.09 \pm 0.01)\times10^{-4}$ & $(1.09 \pm 0.01)\times10^{-9}$ & $(1.09 \pm 0.01)\times10^{-10}$ & $(1.09 \pm 0.01)\times10^{-11}$ & $(1.09 \pm 0.01)\times10^{-12}$ \\ 
# 60\GeV   & $(3.93 \pm 0.08)\times10^{-5}$ & $(3.93 \pm 0.08)\times10^{-10}$ & $(3.93 \pm 0.08)\times10^{-11}$ & $(3.93 \pm 0.08)\times10^{-12}$ & $(3.93 \pm 0.08)\times10^{-13}$ 


# Run 2
# 0.35\GeV & $(5.19 \pm 0.04)\times10^{3}$ & $(5.19 \pm 0.04)\times10^{-2}$ & $(5.19 \pm 0.04)\times10^{-3}$ & $(5.19 \pm 0.04)\times10^{-4}$ & $(5.19 \pm 0.04)\times10^{-5}$ \\ 
# 2\GeV    & $(1.63 \pm 0.01)\times10^{2}$ & $(1.63 \pm 0.01)\times10^{-3}$ & $(1.63 \pm 0.01)\times10^{-4}$ & $(1.63 \pm 0.01)\times10^{-5}$ & $(1.63 \pm 0.01)\times10^{-6}$ \\ 
# 12\GeV   & $(3.76 \pm 0.03)\times10^{-4}$ & $(3.76 \pm 0.03)\times10^{-9}$ & $(3.76 \pm 0.03)\times10^{-10}$ & $(3.76 \pm 0.03)\times10^{-11}$ & $(3.76 \pm 0.03)\times10^{-12}$ \\ 
# 30\GeV   & $(9.65 \pm 0.06)\times10^{-5}$ & $(9.65 \pm 0.06)\times10^{-10}$ & $(9.65 \pm 0.06)\times10^{-11}$ & $(9.65 \pm 0.06)\times10^{-12}$ & $(9.65 \pm 0.06)\times10^{-13}$ \\ 
# 60\GeV   & $(3.46 \pm 0.02)\times10^{-5}$ & $(3.46 \pm 0.02)\times10^{-10}$ & $(3.46 \pm 0.02)\times10^{-11}$ & $(3.46 \pm 0.02)\times10^{-12}$ & $(3.46 \pm 0.02)\times10^{-13}$ \\
