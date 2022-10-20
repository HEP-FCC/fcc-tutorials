import ROOT
import numpy as np
import math
import os

def drawEffVsCutCurve(myTH1, total = 0):
    """ Create and return eff. vs. cut TGraph, from a one-dimensional histogram.
    The efficiencies are computed relative to the histogram's integral,
    or relative to 'total' if it is given. """

    discrV = [ myTH1.GetBinLowEdge(1) ]
    integral = myTH1.Integral()
    totintegral = myTH1.Integral()
    effV = [ integral/totintegral ]

    for i in range(2, myTH1.GetNbinsX()):
        discrV.append(myTH1.GetBinLowEdge(i))
        integral -= myTH1.GetBinContent(i-1)
        effV.append(integral/totintegral)

    # We may want the max. efficiency to be correctly normalised,
    # if the TH1 passed as argument doesn't cover the whole range.
    if total != 0:
        if total < integral:
            print("Warning in createEffVsCutCurve: total number specified to be *smaller* than the histograms's integral. Something might be wrong.")
        integral = total
    #if integral != 0 :
    #    effV = [ x/integral for x in effV ]
    #print len(discrV), discrV, effV
    return ROOT.TGraph(len(discrV), np.array(discrV), np.array(effV))

def drawROCfromEffVsCutCurves(sigGraph, bkgGraph):
    """ Return ROC curve drawn from the "efficiency vs. discriminant" cut curves of signal and background.
    For now, assume the range and binning of the discriminants is the same for both signal and background.
    This might have to be refined. """

    nPoints = sigGraph.GetN()

    if nPoints != bkgGraph.GetN():
        print("Background and signal curves must have the same number of entries!")
        print("Entries signal:     {}".format(nPoints))
        print("Entries background: {}".format(bkgGraph.GetN()))
        sys.exit(1)

    sigEff = []
    sigEffErrXLow = []
    sigEffErrXUp = []
    bkgEff = []
    bkgEffErrYLow = []
    bkgEffErrYUp = []

    for i in range(nPoints):
        sigValX = sigGraph.GetPointX(i)
        sigValY = sigGraph.GetPointY(i)
        bkgValX = bkgGraph.GetPointX(i)
        bkgValY = bkgGraph.GetPointY(i)

        #sigGraph.GetPoint(i, sigValX, sigValY)
        #bkgGraph.GetPoint(i, bkgValX, bkgValY)

        sigEff.append(sigValY)
        sigEffErrXLow.append(sigGraph.GetErrorXlow(i))
        sigEffErrXUp.append(sigGraph.GetErrorXhigh(i))

        bkgEff.append(bkgValY)
        bkgEffErrYLow.append(bkgGraph.GetErrorYlow(i))
        bkgEffErrYUp.append(bkgGraph.GetErrorYhigh(i))

    #return ROOT.TGraphAsymmErrors(nPoints, np.array(sigEff), np.array(bkgEff), np.array(sigEffErrXLow), np.array(sigEffErrXUp), np.array(bkgEffErrYLow), np.array(bkgEffErrYUp))
    return ROOT.TGraphAsymmErrors(nPoints, np.array(bkgEff), np.array(sigEff), np.array(bkgEffErrYLow), np.array(bkgEffErrYUp), np.array(sigEffErrXLow), np.array(sigEffErrXUp))

def drawFigMeritVsCutCurve(bkgTH1, sigTH1, total = 0): # Not implemented
    """ Create and return 2 x (sqrt(S+B)-sqrt(B)) vs. cut TGraph, from two one-dimensional histograms. """

    discrV = [ ]
    effV = [ ]

    for i in range(1, bkgTH1.GetNbinsX() + 1):
        discrV.append(bkgTH1.GetBinLowEdge(i))
        nBkg = bkgTH1.Integral(i, bkgTH1.GetNbinsX() + 1)
        if nBkg < 0:
            nBkg = 0
        nSig = sigTH1.Integral(i, sigTH1.GetNbinsX() + 1)
        effV.append(2*(math.sqrt(nSig+nBkg) - math.sqrt(nBkg)))

    return ROOT.TGraph(len(discrV), np.array(discrV), np.array(effV))

def printCanvas(canvas, name, formats, directory):
    for format in formats:
        outFile = os.path.join(directory, name + "." + format)
        canvas.Print(outFile)

def drawTGraph(graphs, name, xLabel="", yLabel="", legend=None, leftText="", rightText="", formats=["png"], dir=".", style="L", range=None, doLogX=False, logRange=None, ratio=None):
    """Draw and print a set of TGraphs on a canvas."""

    #gStyle()

    pads = {}

    if ratio is not None:
        pads["canvas"] = ROOT.TCanvas(name, name, 550, 450)
        pads["base"] = ROOT.TPad("base", "", 0, 0, 1, 1)
        pads["base"].Draw()
        pads["base"].cd()
        pads["hist"] = ROOT.TPad("hist", name, 0, 0.2, 1, 1)
    else:
        pads["canvas"] = ROOT.TCanvas(name, name, 550, 400)
        pads["base"] = ROOT.TPad("base", "", 0, 0, 1, 1)
        pads["base"].Draw()
        pads["base"].cd()
        pads["hist"] = ROOT.TPad("hist", name, 0, 0, 1, 1)
    pads["hist"].SetGrid()
    pads["hist"].Draw()
    pads["hist"].cd()

    Tleft = ROOT.TLatex(0.125, 0.92, leftText)
    Tleft.SetNDC(ROOT.kTRUE)
    Tleft.SetTextSize(0.048)
    font = Tleft.GetTextFont()
    Tright = ROOT.TLatex(0.8, 0.85, rightText)
    Tright.SetNDC(ROOT.kTRUE)
    Tright.SetTextSize(0.048)
    Tright.SetTextFont(font)

    mg = ROOT.TMultiGraph()
    colors = [ ROOT.TColor.GetColor(hex) for hex in [
            "#1f77b4",
            "#ff7f0e",
            "#2ca02c",
            "#d62728",
            "#9467bd",
            "#8c564b",
            "#e377c2",
            "#7f7f7f",
            "#bcbd22",
            "#17becf",
        ] ]
    markers = [20, 21, 22, 23, 29, 33, 34]

    for i, graph in enumerate(graphs):
        graph.SetMarkerColor(colors[i])
        graph.SetLineColor(colors[i])
        graph.SetLineWidth(2)
        graph.SetMarkerStyle(markers[i])
        mg.Add(graph)

    mg.Draw("A" + style)
    mg.GetXaxis().SetTitle(xLabel)
    mg.GetXaxis().SetTitleFont(font)
    if range:
        mg.GetXaxis().SetRangeUser(range[0][0], range[0][1])
        mg.GetYaxis().SetRangeUser(range[1][0], range[1][1])
    mg.GetYaxis().SetTitle(yLabel)
    mg.GetYaxis().SetTitleFont(font)
    mg.SetTitle("")

    if legend is not None:
        legend.SetTextFont(font)
        legend.SetFillColor(10)
        legend.SetFillStyle(0)
        legend.SetLineColor(0)
        legend.SetTextSize(0.035)
        legend.Draw()

    Tleft.Draw()
    Tright.Draw()

    pads["base"].cd()

    if ratio is not None:
        pads["ratio"] = ROOT.TPad("ratio", "", 0, 0, 1, 0.2)
        pads["ratio"].Draw()
        pads["ratio"].cd()
        pads["ratio"].SetGrid()

        tmp_h = ROOT.TH1F(name + "tmp_ratio", "", 1, mg.GetXaxis().GetXmin(), mg.GetXaxis().GetXmax())
        tmp_h.GetYaxis().SetTitleSize(0.2)
        tmp_h.GetYaxis().SetTitleOffset(0.2)
        tmp_h.GetYaxis().CenterTitle()
        tmp_h.GetYaxis().SetNdivisions(6, 2, 0)
        tmp_h.GetYaxis().SetLabelSize(0.15)
        tmp_h.GetXaxis().SetNdivisions(5, 5, 0, 0)
        tmp_h.GetXaxis().SetLabelSize(0.0)
        tmp_h.SetDirectory(0)

        ratio = createRatioFromGraph(graphs[ratio[0]], graphs[ratio[1]])
        min, max = getGraphMinMax(ratio)
        tmp_h.GetYaxis().SetRangeUser(0.9*min, 1.1*max)
        tmp_h.Draw()
        ratio.Draw(style)

        unity = ROOT.TF1("unity", "1", -1000, 1000)
        unity.SetLineColor(8)
        unity.SetLineWidth(1)
        unity.SetLineStyle(1)
        unity.Draw("same")

    printCanvas(pads["canvas"], name, formats, dir)

    if doLogX:
        if logRange:
            mg.GetXaxis().SetRangeUser(logRange[0][0], logRange[0][1])
            mg.GetYaxis().SetRangeUser(logRange[1][0], logRange[1][1])
        pads["hist"].SetLogx()
        printCanvas(pads["canvas"], name + "_logX", formats, dir)
