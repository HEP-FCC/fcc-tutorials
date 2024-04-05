#include "podio/ROOTFrameReader.h"
#include "podio/Frame.h"

#include "edm4hep/ReconstructedParticleCollection.h"

int plot_recoil_mass(std::string input_file_path) {
  auto reader = podio::ROOTFrameReader();
  reader.openFile(input_file_path);

  TH1* th1_recoil = new TH1F("Recoil Mass", "Recoil Mass", 100, 110., 160.);

  ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<Double32_t>> p_cm(0., 0., 0., 240.);
  for (size_t i = 0; i < reader.getEntries("events"); ++i) {
    auto event = podio::Frame(reader.readNextEntry("events"));
    auto& pfos = event.get<edm4hep::ReconstructedParticleCollection>("TightSelectedPandoraPFOs");
    int n_good_muons = 0;
    ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<Double32_t>> p_mumu;
    for (const auto& pfo : pfos) {
      if (std::abs(pfo.getPDG()) == 13 and pfo.getEnergy() > 20.) {
        n_good_muons++;
        p_mumu += ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<Double32_t>>(pfo.getMomentum().x, pfo.getMomentum().y, pfo.getMomentum().z, pfo.getEnergy());
      }
    }
    if(n_good_muons == 2)
      th1_recoil->Fill((p_cm - p_mumu).M());
  }
  TCanvas* canvas_recoil = new TCanvas("Recoil Mass", "Recoil Mass");
  th1_recoil->Draw();
  canvas_recoil->Print("recoil_mass.png");
  return 0;
}
