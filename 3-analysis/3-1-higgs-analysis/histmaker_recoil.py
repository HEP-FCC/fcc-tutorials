"""Part I: reconstruct muons, select recoil candidates and fill histograms.

Run with: fccanalysis run histmaker_recoil.py
Muon reconstruction is adapted from LiveSoftwareTutorials/Analysis/ee.
"""

# selection requirements; momenta and masses are in GeV.
MUON_MOMENTUM_MIN = 20.0
MUON_ISOLATION_MAX = 0.25
Z_MASS_MIN = 86.0
Z_MASS_MAX = 96.0
Z_MOMENTUM_MIN = 20.0
Z_MOMENTUM_MAX = 70.0
RECOIL_MASS_MIN = 120.0
RECOIL_MASS_MAX = 140.0

# Effective final-state cross sections in pb; branching fractions are included.
processList = {
    "wzp8_ee_mumuH_Hbb_ecm240": {
        "fraction": 1.0,
        "crossSection": 0.00394,
        "kfactor": 1.0,
        "matchingEfficiency": 1.0
    },
    "p8_ee_ZZ_mumubb_ecm240": {
        "fraction": 1.0,
        "crossSection": 0.01404652064,
        "kfactor": 1.0,
        "matchingEfficiency": 1.0
    },
    "p8_ee_WW_mumu_ecm240": {
        "fraction": 1.0,
        "crossSection": 0.25792,
        "kfactor": 1.0,
        "matchingEfficiency": 1.0
    },
}
# Use the FCCAnalyses standard dictionary, overridden by processList above.
procDict = "FCCee_procDict_winter2023_IDEA.json"
includePaths = ["functions.h"]
inputDir = "inputs/"
outputDir = "outputs/recoil/"
nCPUS = -1
doScale = True
intLumi = 10.6e6  # pb^-1 = 10.6 ab^-1


def build_graph(df, dataset):
    results = []
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")

    df = df.Alias("Particle0", "_Particle_daughters.index")
    df = df.Alias("Particle1", "_Particle_parents.index")
    df = df.Alias("RecoMCLink0", "_RecoMCLink_from.index")
    df = df.Alias("RecoMCLink1", "_RecoMCLink_to.index")
    df = df.Alias("Muon0", "Muon_objIdx.index")
    df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)",)

    df = df.Define(
        "muons",
        f"FCCAnalyses::ReconstructedParticle::sel_p({MUON_MOMENTUM_MIN})(muons_all)",
    )
    df = df.Define("q_muons", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
    df = df.Define("no_muons", "FCCAnalyses::ReconstructedParticle::get_n(muons)")

    df = df.Define(
        "iso_muons",
        "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(muons, ReconstructedParticles)",)
    df = df.Define(
        "muons_sel_iso",
        f"FCCAnalyses::ZHfunctions::sel_iso({MUON_ISOLATION_MAX})(muons, iso_muons)",)
    # Loose preselection: the candidate builder needs an opposite-sign muon pair.
    df = df.Filter("muons_sel_iso.size() > 0")
    df = df.Filter("no_muons >= 2 && abs(Sum(q_muons)) < q_muons.size()")

    df = df.Define(
        "zbuilder_result",
        "FCCAnalyses::ZHfunctions::resonanceBuilder_mass_recoil("
        "91.2, 125, 0.4, 240, false)(muons, RecoMCLink0, RecoMCLink1, "
        "ReconstructedParticles, Particle, Particle0, Particle1)",)

    # Define the observables used by the final selection and histograms.
    df = df.Define("zmumu", "Vec_rp{zbuilder_result[0]}")

    df = df.Define("m_zmumu", "FCCAnalyses::ReconstructedParticle::get_mass(zmumu)[0]")
    df = df.Define("p_zmumu", "FCCAnalyses::ReconstructedParticle::get_p(zmumu)[0]")
    df = df.Define("recoil_zmumu", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zmumu)",)
    df = df.Define("m_recoil_zmumu", "FCCAnalyses::ReconstructedParticle::get_mass(recoil_zmumu)[0]",)

    # Apply the physics cuts to the defined observables.
    df = df.Filter(f"m_zmumu > {Z_MASS_MIN} && m_zmumu < {Z_MASS_MAX}")
    df = df.Filter(f"p_zmumu > {Z_MOMENTUM_MIN} && p_zmumu < {Z_MOMENTUM_MAX}")
    df = df.Filter(f"m_recoil_zmumu > {RECOIL_MASS_MIN} && m_recoil_zmumu < {RECOIL_MASS_MAX}")

    # Final distributions after all cuts.
    results.append(df.Histo1D(
        ("m_zmumu", ";Dimuon mass [GeV];Events", 100, 86, 96),
        "m_zmumu", "weight",
    ))
    results.append(df.Histo1D(
        ("p_zmumu", ";Dimuon momentum [GeV];Events", 100, 20, 70),
        "p_zmumu", "weight",
    ))
    results.append(df.Histo1D(
        ("m_recoil_zmumu", ";Recoil mass [GeV];Events", 200, 120, 140),
        "m_recoil_zmumu", "weight",
    ))
    return results, weightsum
