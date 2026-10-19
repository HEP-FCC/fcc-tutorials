"""Part I plots: fccanalysis plots plots_recoil.py."""

import ROOT

# The histmaker already scales the histograms to 10.6 ab^-1.
# This plotting interface multiplies by intLumi, so use a factor of one.
intLumi = 1.0
intLumiLabel = "L = 10.6 ab^{-1}"
ana_tex = "e^{+}e^{-} #rightarrow ZH #rightarrow #mu^{+}#mu^{-}b#bar{b}"
energy = 240.0
collider = "FCC-ee"
formats = ["pdf"]
inputDir = "outputs/recoil/"
outdir = "outputs/plots/recoil/"
plotStatUnc = True

colors = {"ZH": ROOT.kRed, "ZZ": ROOT.kGreen + 2, "WW": ROOT.kBlue + 1}
legend = {"ZH": "ZH", "ZZ": "ZZ", "WW": "WW"}
procs = {
    "signal": {"ZH": ["wzp8_ee_mumuH_Hbb_ecm240"]},
    "backgrounds": {
        "ZZ": ["p8_ee_ZZ_mumubb_ecm240"],
        "WW": ["p8_ee_WW_mumu_ecm240"],
    },
}

hists = {}
for name, title, xmin, xmax in [
    ("m_zmumu", "m_{#mu#mu} [GeV]", 86, 96),
    ("p_zmumu", "p_{#mu#mu} [GeV]", 20, 70),
    ("m_recoil_zmumu", "Recoil mass [GeV]", 120, 140),
]:
    hists[name] = {
        "output": name, "logy": False, "stack": True,
        "xmin": xmin, "xmax": xmax, "ymin": 0,
        "xtitle": title, "ytitle": "Events / bin",
    }
