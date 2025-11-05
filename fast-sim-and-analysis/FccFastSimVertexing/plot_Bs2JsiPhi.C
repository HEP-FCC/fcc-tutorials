#include "TChain.h"
#include "TCanvas.h"

void plot_Bs2JsiPhi() {
  gSystem->mkdir("plots_Bs2JPsiPhi");

  TChain events = TChain("events", "events");
  events.Add("Bs2JpsiPhi_MCseeded.root");

  TString cut0 = "BsMCDecayVertex.position.z < 1e10" ;   // a Bs -> mumuKK has been found in MCParticle


  //
  // Number of tracks
  //
  TCanvas c0 = TCanvas("Ntracks", "Ntracks");
  TH1F h_ntr = TH1F("h_ntr", ";N( Bs tracks ); a.u.", 5, -0.5, 4.5);
  events.Draw("n_BsTracks >> h_ntr", cut0);
  gStyle->SetOptStat(10);   // Entries only
  h_ntr.Draw();
  gStyle->SetOptStat(10);
  TLatex tt;
  tt.SetTextSize(0.04);
  tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow J/#psi #phi #rightarrow #mu#muKK");
  gPad->SetLogy(1);

  c0.Print("plots_Bs2JPsiPhi/Bs2JPsiPhi_n_tracks.png");
  c0.Print("plots_Bs2JPsiPhi/Bs2JPsiPhi_n_tracks.pdf");


  //
  // Chi2 of the vertex fit
  //
  gStyle->SetOptStat(1110);
  TCanvas c1 = TCanvas("chi2", "chi2");
  TH1F h_chi2 = TH1F("h_chi2", ";#chi^{2}/n.d.f.; a.u.", 100, 0., 10.);
  gStyle->SetOptStat(1110);
  events.Draw("BsVertex.chi2 >> hchi2", cut0 + " && BsVertex.chi2 > 0");
  tt.DrawLatexNDC(0.2, 0.96, "B_{s} #rightarrow J/#psi #phi #rightarrow #mu#muKK");
  gPad->SetLogy(1);

  c1.SaveAs("plots_Bs2JPsiPhi/Bs2JPsiPhi_vtx_chi2.png");
  c1.SaveAs("plots_Bs2JPsiPhi/Bs2JPsiPhi_vtx_chi2.pdf");


  //
  // Pulls of the vertex in x, y, z
  //
  TCanvas c2 = TCanvas("pulls", "pulls");
  c2.Divide(2, 2);

  TString cut = cut0 + " && BsVertex.chi2 < 10";

  c2.cd(1);
  TH1F h_px = TH1F("h_px", ";Pull x_{vtx}; a.u.", 100, -5., 5.);
  events.Draw("(BsVertex.position.x - BsMCDecayVertex.x[0]) / TMath::Sqrt(BsVertex.covMatrix[0]) >> h_px", cut);
  h_px.Draw();
  h_px.Fit("gaus");

  c2.cd(2);
  TH1F h_py = TH1F("h_py", ";Pull y_{vtx}; a.u.", 100, -5., 5.);
  events.Draw("(BsVertex.position.y - BsMCDecayVertex.y[0]) / TMath::Sqrt(BsVertex.covMatrix[2]) >> h_py", cut);
  h_py.Draw();
  h_py.Fit("gaus");

  c2.cd(3);
  TH1F h_pz = TH1F("h_pz", ";Pull z_{vtx}; a.u.", 100, -5., 5.);
  events.Draw("(BsVertex.position.z - BsMCDecayVertex.z[0]) / TMath::Sqrt(BsVertex.covMatrix[5]) >> h_pz", cut);
  h_pz.Draw();
  h_pz.Fit("gaus");
  tt.DrawLatexNDC(0.2, 0.96, "B_{s} #rightarrow J/#psi #phi #rightarrow #mu#muKK");

  c2.SaveAs("plots_Bs2JPsiPhi/Bs2JPsiPhi_vtx_pulls.png");
  c2.SaveAs("plots_Bs2JPsiPhi/Bs2JPsiPhi_vtx_pulls.pdf");


  //
  // resolutions on the Bs decay vertex:
  //
  TCanvas c2r = TCanvas("reso", "reso");
  c2r.Divide(2, 2);

  TF1 ff = TF1("ff", "gaus(0)+gaus(3)", -40., 40.);
  ff.SetParameter(1, -5e-2);
  ff.SetParameter(2, 6);
  ff.SetParameter(3, 500);
  ff.SetParameter(4, 1e-2);
  ff.SetParameter(5, 15);

  c2r.cd(1);
  TH1F h_x = TH1F("h_x", ";(vtx_{reco} - vtx_{gen}).x (#mum); Events", 100, -40., 40.);
  events.Draw("1e3 * (BsVertex.position.x - BsMCDecayVertex.x[0]) >> h_x", cut);
  h_x.Fit("ff", "l");

  c2r.cd(2);
  TH1F h_y = TH1F("h_y", ";(vtx_{reco} - vtx_{gen}).y (#mum); Events", 100, -40., 40.);
  events.Draw("1e3 * (BsVertex.position.y - BsMCDecayVertex.y[0]) >> h_y", cut);
  h_y.Fit("ff", "l");

  c2r.cd(3);
  TH1F h_z = TH1F("h_z", ";(vtx_{reco} - vtx_{gen}).z (#mum); Events", 100, -40., 40.);
  events.Draw("1e3 * (BsVertex.position.z - BsMCDecayVertex.z[0]) >> h_z", cut);
  h_z.Fit("ff", "l");

  c2r.SaveAs("plots_Bs2JPsiPhi/Bs2JPsiPhi_vtx_res.png");
  c2r.SaveAs("plots_Bs2JPsiPhi/Bs2JPsiPhi_vtx_res.pdf");


  //
  // Resolution on flight distance:
  //
  TCanvas c3 = TCanvas("fd", "fd");

  TString fld = "TMath::Sqrt(pow(1e3 * BsVertex.position.x, 2) + pow(1e3 * BsVertex.position.y, 2) + pow(1e3 * BsVertex.position.z, 2))";
  TString fld_gen = "TMath::Sqrt(pow(1e3 * BsMCDecayVertex.x[0], 2) + pow(1e3 * BsMCDecayVertex.y[0], 2) + pow(1e3 * BsMCDecayVertex.z[0], 2))";
  TString fld_res = fld + " - " + fld_gen;

  TH1F h_fld = TH1F("h_fld", "; flight distance (rec-true) (#mum); Events", 100, -70., 70.);
  events.Draw(fld_res + " >> h_fld", cut);
  h_fld.Fit("gaus");
  tt.DrawLatexNDC(0.2, 0.96, "B_{s} #rightarrow J/#psi #phi #rightarrow #mu#muKK");

  c3.SaveAs("plots_Bs2JPsiPhi/Bs2JPsiPhi_fd_res.png");
  c3.SaveAs("plots_Bs2JPsiPhi/Bs2JPsiPhi_fd_res.pdf");


  //
  // Pull of the flight distance:
  //
  TCanvas c4 = TCanvas("pull_fd", "pull_fd");

  TString fld_mm = "TMath::Sqrt(pow(BsVertex.position.x, 2) + pow(BsVertex.position.y,2) + pow(BsVertex.position.z,2))";
  TString fld_gen_mm = "TMath::Sqrt(pow(BsMCDecayVertex.x[0], 2) + pow(BsMCDecayVertex.y[0], 2) + pow(BsMCDecayVertex.z[0], 2))";
  TString fld_res_mm = fld_mm + " - " + fld_gen_mm;

  TString term1 = " BsVertex.position.x * (BsVertex.covMatrix[0] * BsVertex.position.x + BsVertex.covMatrix[1] * BsVertex.position.y + BsVertex.covMatrix[3] * BsVertex.position.z) " ;
  TString term2 = " BsVertex.position.y * (BsVertex.covMatrix[1] * BsVertex.position.x + BsVertex.covMatrix[2] * BsVertex.position.y + BsVertex.covMatrix[4] * BsVertex.position.z) " ;
  TString term3 = " BsVertex.position.z * (BsVertex.covMatrix[3] * BsVertex.position.x + BsVertex.covMatrix[4] * BsVertex.position.y + BsVertex.covMatrix[5] * BsVertex.position.z) ";
  TString tsum = term1 + " + " + term2 + " + " + term3;

  TString fld_unc = " (TMath::Sqrt(" + tsum + ") / " + fld_mm + " ) ";
  TString fld_pull = "( " + fld_res_mm + " ) / " + fld_unc;

  TH1F h_fld_pull = TH1F("h_fld_pull", "; Pull flight distance; a.u.", 100, -5., 5.);
  events.Draw(fld_pull + " >> h_fld_pull" , cut);
  h_fld_pull.Fit("gaus");

  c4.SaveAs("plots_Bs2JPsiPhi/Bs2JPsiPhi_fd_pull.png");
  c4.SaveAs("plots_Bs2JPsiPhi/Bs2JPsiPhi_fd_pull.pdf");
}
