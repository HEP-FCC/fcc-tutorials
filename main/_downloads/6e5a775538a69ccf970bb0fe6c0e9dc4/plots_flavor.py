import ROOT

# global parameters
intLumi = 1
intLumiLabel = "L = 5 ab^{-1}"
ana_tex = "e^{+}e^{-} #rightarrow ZH #rightarrow #mu^{+}#mu^{-} b b"
delphesVersion = "3.4.2"
energy = 240.0
collider = "FCC-ee"
formats = ["png", "pdf"]

outdir         = './outputs/plots/flavor/' 
inputDir       = './outputs/histmaker/flavor/' 

plotStatUnc = True

colors = {}
colors["ZH"] = ROOT.kRed
colors["ZZ"] = ROOT.kGreen + 2

procs = {}
procs["signal"] = {"ZH": ["p8_ee_ZH_Zmumu_ecm240"]}
procs["backgrounds"] = {"ZZ": ["p8_ee_ZZ_mumubb_ecm240"]}

legend = {}
legend["ZH"] = "ZH"
legend["ZZ"] = "ZZ"

hists = {}

hists["zmumu_recoil_m"] = {
    "output": "zmumu_recoil_m",
    "logy": False,
    "stack": True,
    "rebin": 100,
    "xmin": 120,
    "xmax": 140,
    "ymin": 0,
    "ymax": 2000,
    "xtitle": "Recoil (GeV)",
    "ytitle": "Events / 100 MeV",
}

hists["jj_m"] = {
    "output": "jj_m",
    "logy": False,
    "stack": True,
    "rebin": 2,
    "xmin": 50,
    "xmax": 150,
    "ymin": 0,
    "ymax": 4000,
    "xtitle": "m_{jj} (GeV)",
    "ytitle": "Events / 2 GeV",
}

hists["scoresum_B"] = {
    "output": "scoresum_B",
    "logy": True,
    "stack": True,
    "rebin": 1,
    "xmin": 0,
    "xmax": 2.0,
    "ymin": 1,
    "ymax": 100000,
    "xtitle": "p_{1}(B) + p_{2}(B)",
    "ytitle": "Events",
}