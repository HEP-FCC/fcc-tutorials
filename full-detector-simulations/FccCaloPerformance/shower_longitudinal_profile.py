import sys
import ROOT
from math import sqrt

# prevent ROOT to display anything
ROOT.gROOT.SetBatch(ROOT.kTRUE)


f = ROOT.TFile(sys.argv[1])
events = f.Get("events")

tprof_energy_vs_depth = ROOT.TProfile("tprof_energy_vs_depth", "tprof_energy_vs_depth", 20, 2150, 2550)
for event in events:
    dict_radius_energy = {}
    for cell in event.PositionedCaloClusterCells:
        radius = str(round(sqrt(cell.position.x * cell.position.x + cell.position.y * cell.position.y)))
        if radius in dict_radius_energy.keys():
            dict_radius_energy[radius] += cell.energy
        else:
            dict_radius_energy[radius] = cell.energy
    for radius in dict_radius_energy.keys():
        tprof_energy_vs_depth.Fill(float(radius), dict_radius_energy[radius])

canvas = ROOT.TCanvas('energy_vs_depth', 'energy_vs_depth')
tprof_energy_vs_depth.Scale(1/tprof_energy_vs_depth.Integral())
tprof_energy_vs_depth.SetLineWidth(3)
tprof_energy_vs_depth.GetXaxis().SetTitle("Radial depth (mm)")
tprof_energy_vs_depth.GetYaxis().SetTitle("Average energy deposit (a.u.)")
tprof_energy_vs_depth.Draw()
canvas.Print(sys.argv[1].replace(".root", "_energyLongitudinalProfile.png"))
