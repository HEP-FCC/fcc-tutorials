from podio import root_io
import ROOT
ROOT.gROOT.SetBatch(True)

input_file_path = "./wzp6_ee_mumuH_ecm240_CLD_RECO_moreStat.root"
podio_reader = root_io.Reader(input_file_path)

th1_recoil = ROOT.TH1F("Recoil Mass", "Recoil Mass", 100, 110, 160)

p_cm = ROOT.Math.LorentzVector('ROOT::Math::PxPyPzE4D<double>')(0, 0, 0, 240)
for event in podio_reader.get("events"):
    pfos = event.get("TightSelectedPandoraPFOs")
    n_good_muons = 0
    p_mumu = ROOT.Math.LorentzVector('ROOT::Math::PxPyPzE4D<double>')()
    for pfo in pfos:
        if abs(pfo.getPDG()) == 13 and pfo.getEnergy() > 20:
            n_good_muons += 1
            p_mumu += ROOT.Math.LorentzVector('ROOT::Math::PxPyPzE4D<double>')(pfo.getMomentum().x, pfo.getMomentum().y, pfo.getMomentum().z, pfo.getEnergy())
    if n_good_muons == 2:
        th1_recoil.Fill((p_cm - p_mumu).M())

canvas_recoil = ROOT.TCanvas("Recoil Mass", "Recoil Mass")
th1_recoil.Draw()
canvas_recoil.Print("recoil_mass.png")


