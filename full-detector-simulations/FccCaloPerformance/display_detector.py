import ROOT
import dd4hep
import os
fcc_det_path = os.path.join(os.environ.get("FCCDETECTORS"), "Detector/DetFCCeeIDEA-LAr/compact/FCCee_DectMaster.xml")
print(fcc_det_path)
description = dd4hep.Detector.getInstance()
description.fromXML(fcc_det_path)
c = ROOT.TCanvas("c_detector_display", "", 600,600)
description.manager().SetVisLevel(6)
description.manager().SetVisOption(1)
vol = description.manager().GetTopVolume()
vol.Draw()
wait = input("Press enter to quit the program")
