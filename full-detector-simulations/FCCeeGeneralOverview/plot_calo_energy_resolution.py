import sys
import ROOT

# prevent ROOT to display anything
ROOT.gROOT.SetBatch(ROOT.kTRUE)

f = ROOT.TFile(sys.argv[1])
events = f.Get("events")

# raw clusters
c = ROOT.TCanvas("c_clusterEnergyResolution", "")
h = ROOT.TH1F("h_clusterEnergyResolution", ";ECal Barrel Cluster Energy [GeV]; Number of Clusters", 100, 5, 15)
events.Draw("CaloClusters.energy >> h_clusterEnergyResolution")
fit_range_min = h.GetXaxis().GetBinCenter(h.GetMaximumBin()) - 3 * h.GetRMS()
fit_range_max = h.GetXaxis().GetBinCenter(h.GetMaximumBin()) + 3 * h.GetRMS()
fit_result = h.Fit("gaus", "SQ", "", fit_range_min, fit_range_max)
mean = str(round(fit_result.Get().Parameter(1), 2))
resolution = str(round(fit_result.Get().Parameter(2), 2))
legend = ROOT.TLegend(0.47, 0.65, 0.8, 0.8)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.AddEntry(ROOT.nullptr, "#color[2]{#mu: %s GeV}"%mean, "")
legend.AddEntry(ROOT.nullptr, "#color[2]{#sigma = %s GeV}"%resolution, "")
legend.Draw()
c.Print(sys.argv[1].replace(".root", "_clusterEnergyResolution.png"))

# MVA calibrated clusters
c = ROOT.TCanvas("c_calibratedClusterEnergyResolution", "")
h = ROOT.TH1F("h_calibratedClusterEnergyResolution", ";ECal Barrel Calibrated Cluster Energy [GeV]; Number of Clusters", 100, 5, 15)
events.Draw("CalibratedCaloClusters.energy >> h_calibratedClusterEnergyResolution")
fit_range_min = h.GetXaxis().GetBinCenter(h.GetMaximumBin()) - 3 * h.GetRMS()
fit_range_max = h.GetXaxis().GetBinCenter(h.GetMaximumBin()) + 3 * h.GetRMS()
fit_result = h.Fit("gaus", "SQ", "", fit_range_min, fit_range_max)
mean = str(round(fit_result.Get().Parameter(1), 2))
resolution = str(round(fit_result.Get().Parameter(2), 2))
legend = ROOT.TLegend(0.47, 0.65, 0.8, 0.8)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.AddEntry(ROOT.nullptr, "#color[2]{#mu: %s GeV}"%mean, "")
legend.AddEntry(ROOT.nullptr, "#color[2]{#sigma = %s GeV}"%resolution, "")
legend.Draw()
c.Print(sys.argv[1].replace(".root", "_calibratedClusterEnergyResolution.png"))

