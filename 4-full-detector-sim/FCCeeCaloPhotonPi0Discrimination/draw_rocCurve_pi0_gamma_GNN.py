import os
import ROOT
import sys
from rocCurveFacility import *

ROOT.gROOT.SetBatch(ROOT.kTRUE)

#Where your files are
input_file_path = ""
#name of your files
pi0_file = os.path.join(input_file_path, "")
photon_file = os.path.join(input_file_path, "")
#output name
output_string_suffix = ""

# Retrive the MVA score data as TH1 and draw them
pi0_rootfile = ROOT.TFile(pi0_file)
pi0_events = pi0_rootfile.Get("events")
pi0_th1 = ROOT.TH1F("pi0_score", "PI0 MVA score", 200, 0, 1)
pi0_events.Draw("Cluster_isPhoton >> pi0_score")
pi0_th1.SetLineColor(ROOT.kRed)

photon_rootfile = ROOT.TFile(photon_file)
photon_events = photon_rootfile.Get("events")
photon_th1 = ROOT.TH1F("photon_score", "Photon MVA score", 200, 0, 1)
photon_events.Draw("Cluster_isPhoton >> photon_score")

score_canvas = ROOT.TCanvas("MVA score", "MVA score")
score_canvas.SetLogy()
pi0_th1.Draw()
photon_th1.Draw("same")
legend = ROOT.TLegend(0.47, 0.65, 0.8, 0.8)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.AddEntry(pi0_th1, "#pi^{0}")
legend.AddEntry(photon_th1, "#gamma")
legend.Draw()
score_canvas.Print("MVA_score" + output_string_suffix + ".png")

# Draw ROC curve to asses the MVA performance
pi0_efficiency_vs_cut = drawEffVsCutCurve(pi0_th1)
photon_efficiency_vs_cut = drawEffVsCutCurve(photon_th1)
roc = drawROCfromEffVsCutCurves(photon_efficiency_vs_cut, pi0_efficiency_vs_cut)
drawTGraph([roc], "ROC" + output_string_suffix, "#pi^{0} Efficiency", "#gamma Efficiency")#, None, "Sample X%s %s"%(spin_sig, mass_sig), "", ["pdf", "png", "root"], outFileDir)
