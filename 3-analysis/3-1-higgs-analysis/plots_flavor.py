# Adapted from https://github.com/HEP-FCC/LiveSoftwareTutorials/blob/main/Analysis/ee/03_plot.py
"""Plot configuration for the ee->Z(mu+mu-)H(bb) tutorial.

Run after ``selection_flavor.py`` with:
    fccanalysis plots plots_flavor.py
"""

import ROOT


intLumi = 10.6e6  # pb^-1 = 10.6 ab^-1
intLumiLabel = "L = 10.6 ab^{-1}"
ana_tex = "e^{+}e^{-} #rightarrow ZH #rightarrow #mu^{+}#mu^{-}b#bar{b}"
energy = 240.0
collider = "FCC-ee"

inputDir = "outputs/flavor/stage2/"
outdir = "outputs/plots/flavor/"

formats = ["pdf"]
# yaxis = ["lin", "log"]
yaxis = ["lin"]
stacksig = ["stack"]
plotStatUnc = True


variables = [
    "m_zmumu",
    "p_zmumu",
    "m_recoil_zmumu",
    "m_jj",
    "scoresum_B",
]

selections = {
    "ZH": [
        "sel0_baseline",
        "sel1_zmass",
        "sel2_zmomentum",
        "sel3_recoil",
        "sel4_btag",
    ],
}

extralabel = {
    "sel0_baseline": "Baseline selection",
    "sel1_zmass": "Z-mass selection",
    "sel2_zmomentum": "Z-mass and Z-momentum selections",
    "sel3_recoil": "Including the recoil-mass selection",
    "sel4_btag": "Final selection including b tagging",
}


colors = {
    "ZH": ROOT.kRed,
    "ZZ": ROOT.kGreen + 2,
    "WW": ROOT.kBlue + 1,
}

plots = {
    "ZH": {
        "signal": {
            "ZH": ["wzp8_ee_mumuH_Hbb_ecm240"],
        },
        "backgrounds": {
            "ZZ": ["p8_ee_ZZ_mumubb_ecm240"],
            "WW": ["p8_ee_WW_mumu_ecm240"],
        },
    },
}

legend = {
    "ZH": "ZH #rightarrow #mu^{+}#mu^{-}b#bar{b}",
    "ZZ": "ZZ #rightarrow #mu^{+}#mu^{-}b#bar{b}",
    "WW": "WW #rightarrow #mu^{+}#mu^{-} + X",
}
