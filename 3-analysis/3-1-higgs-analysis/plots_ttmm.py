import ROOT

# global parameters
intLumi        = 1.
intLumiLabel   = "L = 7 pb^{-1}"
ana_tex        = 'e^{+}e^{-} #rightarrow Z #rightarrow #tau^{+}#tau^{-}'
delphesVersion = '3.5'
energy         = 91.188
collider       = 'FCC-ee'
inputDir       = './outputs/histmaker/ttmm/' # _after_stage1
formats        = ['png','pdf']
outdir         = './outputs/plots/ttmm/' # _after_stage1
plotStatUnc    = True

colors = {}
colors['kk'] = ROOT.kRed
colors['wz'] = ROOT.kBlue+1
colors['p8'] = ROOT.kGreen+2

procs = {}
procs['signal'] = {'p8':['p8_tautau_ecm91'], 'wz':['wz_tautau_ecm91'], 'kk':['kk_tautau_ecm91']}
procs['backgrounds'] =  {}


legend = {}
legend['p8'] = 'Pythia8'
legend['wz'] = 'Whizard'
legend['kk'] = 'KKMCee'



hists = {}

hists["AcolTau"] = {
    "output":   "AcolTau",
    "logy":     True,
    "stack":    False,
    "rebin":    1,
    "xmin":     -1,
    "xmax":     -.9,
    "ymin":     0.1,
    "ymax":     10000,
    "xtitle":   "Acol",
    "ytitle":   "Events / 0.002",
}

hists["AcolMu"] = {
    "output":   "AcolMu",
    "logy":     True,
    "stack":    False,
    "rebin":    1,
    "xmin":     -1,
    "xmax":     -.9,
    "ymin":     0.1,
    "ymax":     10000,
    "xtitle":   "Acol",
    "ytitle":   "Events / 0.002",
}

hists["CosTheta_taup"] = {
    "output":   "CosTheta_taup",
    "logy":     False,
    "stack":    False,
    "rebin":    1,
    "xmin":     -1,
    "xmax":     1,
    "ymin":     0,
    "ymax":     600,
    "xtitle":   "CosTheta Tau+",
    "ytitle":   "Events / 0.002",
}

hists["CosTheta_mup"] = {
    "output":   "CosTheta_mup",
    "logy":     False,
    "stack":    False,
    "rebin":    1,
    "xmin":     -1,
    "xmax":     1,
    "ymin":     0,
    "ymax":     600,
    "xtitle":   "CosTheta Mu+",
    "ytitle":   "Events / 0.002",
}


hists["P_mup"] = {
    "output":   "P_mup",
    "logy":     False,
    "stack":    False,
    "rebin":    1,
    "xmin":     0,
    "xmax":     50,
    "ymin":     0,
    "ymax":     350,
    "xtitle":   "P Mu+",
    "ytitle":   "Events / 0.5 GeV/c",
}

hists["P_mum"] = {
    "output":   "P_mum",
    "logy":     False,
    "stack":    False,
    "rebin":    1,
    "xmin":     0,
    "xmax":     50,
    "ymin":     0,
    "ymax":     350,
    "xtitle":   "P Mu-",
    "ytitle":   "Events / 0.5 GeV/c",
}


