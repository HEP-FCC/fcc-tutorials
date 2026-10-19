# Adapted from https://github.com/HEP-FCC/LiveSoftwareTutorials/blob/main/Analysis/ee/solutions/02_selection_and_hist.py
"""Final selections and histograms for the Z(mu+mu-)H(bb) tutorial.

Run after ``treemaker_flavor.py`` with:
    fccanalysis final selection_flavor.py

Stage 1 has already constructed the physics objects and written the relevant
observables to flat ntuples.  This script applies cumulative physics selections
to those ntuples and produces histograms after every selection step.
"""


# Fixed tutorial selections; optional exercises can vary these values.
Z_MASS_MIN = 86.0
Z_MASS_MAX = 96.0
Z_MOMENTUM_MIN = 20.0
Z_MOMENTUM_MAX = 70.0
RECOIL_MASS_MIN = 120.0
RECOIL_MASS_MAX = 140.0
BTAG_SUM_MIN = 1.0


# Input ntuples written by treemaker_flavor.py.
inputDir = "outputs/flavor/stage1/"
outputDir = "outputs/flavor/stage2/"


processList = {
    "wzp8_ee_mumuH_Hbb_ecm240": {},
    "p8_ee_ZZ_mumubb_ecm240": {},
    "p8_ee_WW_mumu_ecm240": {},
}

# Override the FCCAnalyses standard dictionary for these tutorial samples.
procDict = "FCCee_procDict_winter2023_IDEA.json"

# Effective final-state cross sections in pb, matching Part I.
# Branching fractions are already included.
procDictAdd = {
    "wzp8_ee_mumuH_Hbb_ecm240": {
        "crossSection": 0.00394,
        "kfactor": 1.0,
        "matchingEfficiency": 1.0
    },
    "p8_ee_ZZ_mumubb_ecm240": {
        "crossSection": 0.01404652064,
        "kfactor": 1.0,
        "matchingEfficiency": 1.0
    },
    "p8_ee_WW_mumu_ecm240": {
        "crossSection": 0.25792,
        "kfactor": 1.0,
        "matchingEfficiency": 1.0
    }
}

intLumi = 10.6e6  # pb^-1 = 10.6 ab^-1
doScale = True
saveJSON = True


# Each selection contains all preceding requirements.  This makes the entries
# cumulative and allows the effect of every additional cut to be compared.
cutList = {
    "sel0_baseline": "true",
    "sel1_zmass": (
        f"m_zmumu > {Z_MASS_MIN} && m_zmumu < {Z_MASS_MAX}"
    ),
    "sel2_zmomentum": (
        f"m_zmumu > {Z_MASS_MIN} && m_zmumu < {Z_MASS_MAX}"
        f" && p_zmumu > {Z_MOMENTUM_MIN}"
        f" && p_zmumu < {Z_MOMENTUM_MAX}"
    ),
    "sel3_recoil": (
        f"m_zmumu > {Z_MASS_MIN} && m_zmumu < {Z_MASS_MAX}"
        f" && p_zmumu > {Z_MOMENTUM_MIN}"
        f" && p_zmumu < {Z_MOMENTUM_MAX}"
        f" && m_recoil_zmumu > {RECOIL_MASS_MIN}"
        f" && m_recoil_zmumu < {RECOIL_MASS_MAX}"
    ),
    "sel4_btag": (
        f"m_zmumu > {Z_MASS_MIN} && m_zmumu < {Z_MASS_MAX}"
        f" && p_zmumu > {Z_MOMENTUM_MIN}"
        f" && p_zmumu < {Z_MOMENTUM_MAX}"
        f" && m_recoil_zmumu > {RECOIL_MASS_MIN}"
        f" && m_recoil_zmumu < {RECOIL_MASS_MAX}"
        f" && scoresum_B > {BTAG_SUM_MIN}"
    ),
}


cutLabels = {
    "sel0_baseline": "Baseline selection",
    "sel1_zmass": "Z-mass selection",
    "sel2_zmomentum": "Z-mass and Z-momentum selections",
    "sel3_recoil": "Z-mass, Z-momentum and recoil-mass selections",
    "sel4_btag": "Final selection including b tagging",
}


# Every histogram is produced separately for every entry in cutList.
histoList = {
    "m_zmumu": {
        "name": "m_zmumu",
        "title": "m_{#mu#mu} [GeV]",
        "bin": 200,
        "xmin": 0.0,
        "xmax": 200.0,
    },
    "p_zmumu": {
        "name": "p_zmumu",
        "title": "p_{#mu#mu} [GeV]",
        "bin": 150,
        "xmin": 0.0,
        "xmax": 150.0,
    },
    "m_recoil_zmumu": {
        "name": "m_recoil_zmumu",
        "title": "m_{recoil} [GeV]",
        "bin": 100,
        "xmin": 50.0,
        "xmax": 150.0,
    },
    "m_jj": {
        "name": "m_jj",
        "title": "m_{jj} [GeV]",
        "bin": 100,
        "xmin": 50.0,
        "xmax": 150.0,
    },
    "scoresum_B": {
        "name": "scoresum_B",
        "title": "Sum of the two jet b-tag scores",
        "bin": 50,
        "xmin": 0.0,
        "xmax": 2.0,
    },
}
