#!/bin/env python
import sys, ROOT, uproot3 as uproot
from ROOT import TFile, TTree
ROOT.gROOT.SetBatch(True)
if len(sys.argv) < 2:
  print("Please specify input file"); sys.exit(1)
inputFile = sys.argv[1]; print("Reading:", inputFile)
tfile = ROOT.TFile.Open(inputFile)
myTree = tfile.Get("events")
myTree.Draw("ECalEndcapCollection.position.z>>zHist(100, 2300, 2510)",
"ECalEndcapCollection.position.z > 0")
myTree.Draw("ECalEndcapCollection.energy>>eHist(30, 0, 0.002)")
zHist = tfile.Get("zHist")
eHist = tfile.Get("eHist")
oFile = ROOT.TFile.Open("temp.root", "RECREATE")
eHist.Write(); zHist.Write(); oFile.Close()
uFile = uproot.open("temp.root")
uFile["zHist"].show()
uFile["eHist"].show()
