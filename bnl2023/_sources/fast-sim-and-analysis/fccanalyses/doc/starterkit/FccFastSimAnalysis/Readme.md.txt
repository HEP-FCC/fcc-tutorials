
# FCC: Analysing simulated events

Let's first clone and build ```FCCAnalyses```. 

```bash
git clone https://github.com/HEP-FCC/FCCAnalyses.git
cd FCCAnalyses
source ./setup.sh
mkdir build install && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install -j 20
cd ..
mkdir tutorial && cd tutorial
```

Copy the necessary files, either from the web or from some location where the files were produced locally

```bash
mkdir localSamples && cd localSamples
mkdir  p8_ee_WW_mumu_ecm240 && cd p8_ee_WW_mumu_ecm240
wget https://fccsw.web.cern.ch/tutorials/apr2023/tutorial2/p8_ee_WW_mumu_ecm240_edm4hep.root
cd ..
mkdir p8_ee_ZZ_mumubb_ecm240 && cd p8_ee_ZZ_mumubb_ecm240
wget https://fccsw.web.cern.ch/tutorials/apr2023/tutorial2/p8_ee_ZZ_mumubb_ecm240_edm4hep.root
cd ..
mkdir p8_ee_ZH_Zmumu_ecm240  && cd p8_ee_ZH_Zmumu_ecm240
wget https://fccsw.web.cern.ch//tutorials/apr2023/tutorial2/p8_ee_ZH_Zmumu_ecm240_edm4hep.root
cd ../..
```

This tutorial consists in two parts. Both parts will make use of ee->ZH (Z->mumu)events, with its relevant backgrounds ee->WW and ee->ZZ:

- in **Part I** you will construct the recoil mass observable and apply a list of pre-selection cuts.
- in **Part II** you will learn how to run an exclusive jet clustering algorithm. evaluate the various jet flavor probabilities and use them to select H->bb events.

:::{admonition} Learning Objectives
:class: objectives

In this first example, you will learn how to: 

-   read the **edm4hep** data format and construct physics observable (such as the recoil mass)
-  define C++ helper functions in a separate that will be compiled at run time 
-   apply an **event selection** and **fill histograms** in a single iteration using the **histmaker** option.
-   produce **flat ntuples** with observables of interest with **FCCAnalyses**
-   produce plots with the **plot** option. 
:::

## Part I: Analyse events with histmaker

Create a file called `functions.h`. This contains C++ helper functions that you will need to compute observables with RDataframe

```cpp
#ifndef ZHfunctions_H
#define ZHfunctions_H

#include <cmath>
#include <vector>
#include <math.h>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"
#include "ReconstructedParticle2MC.h"


namespace FCCAnalyses { namespace ZHfunctions {


// build the Z resonance based on the available leptons. Returns the best lepton pair compatible with the Z mass and recoil at 125 GeV
// technically, it returns a ReconstructedParticleData object with index 0 the di-lepton system, index and 2 the leptons of the pair
struct resonanceBuilder_mass_recoil {
    float m_resonance_mass;
    float m_recoil_mass;
    float chi2_recoil_frac;
    float ecm;
    bool m_use_MC_Kinematics;
    resonanceBuilder_mass_recoil(float arg_resonance_mass, float arg_recoil_mass, float arg_chi2_recoil_frac, float arg_ecm, bool arg_use_MC_Kinematics);
    Vec_rp operator()(Vec_rp legs, Vec_i recind, Vec_i mcind, Vec_rp reco, Vec_mc mc, Vec_i parents, Vec_i daugthers) ;
};

resonanceBuilder_mass_recoil::resonanceBuilder_mass_recoil(float arg_resonance_mass, float arg_recoil_mass, float arg_chi2_recoil_frac, float arg_ecm, bool arg_use_MC_Kinematics) {m_resonance_mass = arg_resonance_mass, m_recoil_mass = arg_recoil_mass, chi2_recoil_frac = arg_chi2_recoil_frac, ecm = arg_ecm, m_use_MC_Kinematics = arg_use_MC_Kinematics;}

Vec_rp resonanceBuilder_mass_recoil::resonanceBuilder_mass_recoil::operator()(Vec_rp legs, Vec_i recind, Vec_i mcind, Vec_rp reco, Vec_mc mc, Vec_i parents, Vec_i daugthers) {

    Vec_rp result;
    result.reserve(3);
    std::vector<std::vector<int>> pairs; // for each permutation, add the indices of the muons
    int n = legs.size();
  
    if(n > 1) {
        ROOT::VecOps::RVec<bool> v(n);
        std::fill(v.end() - 2, v.end(), true); // helper variable for permutations
        do {
            std::vector<int> pair;
            rp reso;
            reso.charge = 0;
            TLorentzVector reso_lv; 
            for(int i = 0; i < n; ++i) {
                if(v[i]) {
                    pair.push_back(i);
                    reso.charge += legs[i].charge;
                    TLorentzVector leg_lv;

                    if(m_use_MC_Kinematics) { // MC kinematics
                        int track_index = legs[i].tracks_begin;   // index in the Track array
                        int mc_index = ReconstructedParticle2MC::getTrack2MC_index(track_index, recind, mcind, reco);
                        if (mc_index >= 0 && mc_index < mc.size()) {
                            leg_lv.SetXYZM(mc.at(mc_index).momentum.x, mc.at(mc_index).momentum.y, mc.at(mc_index).momentum.z, mc.at(mc_index).mass);
                        }
                    }
                    else { // reco kinematics
                         leg_lv.SetXYZM(legs[i].momentum.x, legs[i].momentum.y, legs[i].momentum.z, legs[i].mass);
                    }

                    reso_lv += leg_lv;
                }
            }

            if(reso.charge != 0) continue; // neglect non-zero charge pairs
            reso.momentum.x = reso_lv.Px();
            reso.momentum.y = reso_lv.Py();
            reso.momentum.z = reso_lv.Pz();
            reso.mass = reso_lv.M();
            result.emplace_back(reso);
            pairs.push_back(pair);

        } while(std::next_permutation(v.begin(), v.end()));
    }
    else {
        std::cout << "ERROR: resonanceBuilder_mass_recoil, at least two leptons required." << std::endl;
        exit(1);
    }
  
    if(result.size() > 1) {
  
        Vec_rp bestReso;
        
        int idx_min = -1;
        float d_min = 9e9;
        for (int i = 0; i < result.size(); ++i) {
            
            // calculate recoil
            auto recoil_p4 = TLorentzVector(0, 0, 0, ecm);
            TLorentzVector tv1;
            tv1.SetXYZM(result.at(i).momentum.x, result.at(i).momentum.y, result.at(i).momentum.z, result.at(i).mass);
            recoil_p4 -= tv1;
      
            auto recoil_fcc = edm4hep::ReconstructedParticleData();
            recoil_fcc.momentum.x = recoil_p4.Px();
            recoil_fcc.momentum.y = recoil_p4.Py();
            recoil_fcc.momentum.z = recoil_p4.Pz();
            recoil_fcc.mass = recoil_p4.M();
            
            TLorentzVector tg;
            tg.SetXYZM(result.at(i).momentum.x, result.at(i).momentum.y, result.at(i).momentum.z, result.at(i).mass);
        
            float boost = tg.P();
            float mass = std::pow(result.at(i).mass - m_resonance_mass, 2); // mass
            float rec = std::pow(recoil_fcc.mass - m_recoil_mass, 2); // recoil
            float d = (1.0-chi2_recoil_frac)*mass + chi2_recoil_frac*rec;
            
            if(d < d_min) {
                d_min = d;
                idx_min = i;
            }

     
        }
        if(idx_min > -1) { 
            bestReso.push_back(result.at(idx_min));
            auto & l1 = legs[pairs[idx_min][0]];
            auto & l2 = legs[pairs[idx_min][1]];
            bestReso.emplace_back(l1);
            bestReso.emplace_back(l2);
        }
        else {
            std::cout << "ERROR: resonanceBuilder_mass_recoil, no mininum found." << std::endl;
            exit(1);
        }
        return bestReso;
    }
    else {
        auto & l1 = legs[0];
        auto & l2 = legs[1];
        result.emplace_back(l1);
        result.emplace_back(l2);
        return result;
    }
}    




struct sel_iso {
    sel_iso(float arg_max_iso);
    float m_max_iso = .25;
    Vec_rp operator() (Vec_rp in, Vec_f iso);
  };

sel_iso::sel_iso(float arg_max_iso) : m_max_iso(arg_max_iso) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  sel_iso::operator() (Vec_rp in, Vec_f iso) {
    Vec_rp result;
    result.reserve(in.size());
    for (size_t i = 0; i < in.size(); ++i) {
        auto & p = in[i];
        if (iso[i] < m_max_iso) {
            result.emplace_back(p);
        }
    }
    return result;
}

 
// compute the cone isolation for reco particles
struct coneIsolation {

    coneIsolation(float arg_dr_min, float arg_dr_max);
    double deltaR(double eta1, double phi1, double eta2, double phi2) { return TMath::Sqrt(TMath::Power(eta1-eta2, 2) + (TMath::Power(phi1-phi2, 2))); };

    float dr_min = 0;
    float dr_max = 0.4;
    Vec_f operator() (Vec_rp in, Vec_rp rps) ;
};

coneIsolation::coneIsolation(float arg_dr_min, float arg_dr_max) : dr_min(arg_dr_min), dr_max( arg_dr_max ) { };
Vec_f coneIsolation::coneIsolation::operator() (Vec_rp in, Vec_rp rps) {
  
    Vec_f result;
    result.reserve(in.size());

    std::vector<ROOT::Math::PxPyPzEVector> lv_reco;
    std::vector<ROOT::Math::PxPyPzEVector> lv_charged;
    std::vector<ROOT::Math::PxPyPzEVector> lv_neutral;

    for(size_t i = 0; i < rps.size(); ++i) {

        ROOT::Math::PxPyPzEVector tlv;
        tlv.SetPxPyPzE(rps.at(i).momentum.x, rps.at(i).momentum.y, rps.at(i).momentum.z, rps.at(i).energy);
        
        if(rps.at(i).charge == 0) lv_neutral.push_back(tlv);
        else lv_charged.push_back(tlv);
    }
    
    for(size_t i = 0; i < in.size(); ++i) {

        ROOT::Math::PxPyPzEVector tlv;
        tlv.SetPxPyPzE(in.at(i).momentum.x, in.at(i).momentum.y, in.at(i).momentum.z, in.at(i).energy);
        lv_reco.push_back(tlv);
    }

    
    // compute the isolation (see https://github.com/delphes/delphes/blob/master/modules/Isolation.cc#L154) 
    for (auto & lv_reco_ : lv_reco) {
    
        double sumNeutral = 0.0;
        double sumCharged = 0.0;
    
        // charged
        for (auto & lv_charged_ : lv_charged) {
    
            double dr = coneIsolation::deltaR(lv_reco_.Eta(), lv_reco_.Phi(), lv_charged_.Eta(), lv_charged_.Phi());
            if(dr > dr_min && dr < dr_max) sumCharged += lv_charged_.P();
        }
        
        // neutral
        for (auto & lv_neutral_ : lv_neutral) {
    
            double dr = coneIsolation::deltaR(lv_reco_.Eta(), lv_reco_.Phi(), lv_neutral_.Eta(), lv_neutral_.Phi());
            if(dr > dr_min && dr < dr_max) sumNeutral += lv_neutral_.P();
        }
        
        double sum = sumCharged + sumNeutral;
        double ratio= sum / lv_reco_.P();
        result.emplace_back(ratio);
    }
    return result;
}
 
 
 
// returns missing energy vector, based on reco particles
Vec_rp missingEnergy(float ecm, Vec_rp in, float p_cutoff = 0.0) {
    float px = 0, py = 0, pz = 0, e = 0;
    for(auto &p : in) {
        if (std::sqrt(p.momentum.x * p.momentum.x + p.momentum.y*p.momentum.y) < p_cutoff) continue;
        px += -p.momentum.x;
        py += -p.momentum.y;
        pz += -p.momentum.z;
        e += p.energy;
    }
    
    Vec_rp ret;
    rp res;
    res.momentum.x = px;
    res.momentum.y = py;
    res.momentum.z = pz;
    res.energy = ecm-e;
    ret.emplace_back(res);
    return ret;
}

// calculate the cosine(theta) of the missing energy vector
float get_cosTheta_miss(Vec_rp met){
    
    float costheta = 0.;
    if(met.size() > 0) {
        
        TLorentzVector lv_met;
        lv_met.SetPxPyPzE(met[0].momentum.x, met[0].momentum.y, met[0].momentum.z, met[0].energy);
        costheta = fabs(std::cos(lv_met.Theta()));
    }
    return costheta;
}

 
 

}}

#endif
```

Create a file called `histmaker_recoil.py` containing the following. Make sure to modify the ```inputDir``` and point to where the samples previously produced are located. 


```python
# list of processes (mandatory)
processList = {
    #'p8_ee_ZZ_ecm240':{'fraction':1},
    #'p8_ee_WW_ecm240':{'fraction':1}, 
    #'wzp6_ee_mumuH_ecm240':{'fraction':1},
    'p8_ee_WW_mumu_ecm240':    {'fraction':1, 'crossSection': 0.25792}, 
    'p8_ee_ZZ_mumubb_ecm240':  {'fraction':1, 'crossSection': 2 * 1.35899 * 0.034 * 0.152},
    'p8_ee_ZH_Zmumu_ecm240':   {'fraction':1, 'crossSection': 0.201868 * 0.034},
}

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
#prodTag     = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# additional/custom C++ functions, defined in header files (optional)
includePaths = ["functions.h"]

# Define the input dir (optional)
#inputDir    = "outputs/FCCee/higgs/mH-recoil/mumu/stage1"
inputDir    = "./localSamples/"

#Optional: output directory, default is local running directory
outputDir   = "./outputs/histmaker/recoil/"


# optional: ncpus, default is 4, -1 uses all cores available
nCPUS       = -1

# scale the histograms with the cross-section and integrated luminosity
doScale = True
intLumi = 5000000 # 5 /ab


# define some binning for various histograms
bins_p_mu = (2000, 0, 200) # 100 MeV bins
bins_m_ll = (2000, 0, 200) # 100 MeV bins
bins_p_ll = (2000, 0, 200) # 100 MeV bins
bins_recoil = (200000, 0, 200) # 1 MeV bins 
bins_cosThetaMiss = (10000, 0, 1)

bins_theta = (500, -5, 5)
bins_eta = (600, -3, 3)
bins_phi = (500, -5, 5)

bins_count = (50, 0, 50)
bins_charge = (10, -5, 5)
bins_iso = (500, 0, 5)



# build_graph function that contains the analysis logic, cuts and histograms (mandatory)
def build_graph(df, dataset):

    results = []
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    
    # define some aliases to be used later on
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    df = df.Alias("Muon0", "Muon#0.index")


    # get all the leptons from the collection
    df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")

    
    # select leptons with momentum > 20 GeV
    df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::sel_p(20)(muons_all)")
    
    
    df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
    df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
    df = df.Define("muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
    df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
    df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")
    
    # compute the muon isolation and store muons with an isolation cut of 0.25 in a separate column muons_sel_iso
    df = df.Define("muons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(muons, ReconstructedParticles)")
    df = df.Define("muons_sel_iso", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(muons, muons_iso)")
    
        
    # baseline histograms, before any selection cuts (store with _cut0)
    results.append(df.Histo1D(("muons_p_cut0", "", *bins_p_mu), "muons_p"))
    results.append(df.Histo1D(("muons_theta_cut0", "", *bins_theta), "muons_theta"))
    results.append(df.Histo1D(("muons_phi_cut0", "", *bins_phi), "muons_phi"))
    results.append(df.Histo1D(("muons_q_cut0", "", *bins_charge), "muons_q"))
    results.append(df.Histo1D(("muons_no_cut0", "", *bins_count), "muons_no"))
    results.append(df.Histo1D(("muons_iso_cut0", "", *bins_iso), "muons_iso"))
    

    #########
    ### CUT 0: all events
    #########
    df = df.Define("cut0", "0")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut0"))


    #########
    ### CUT 1: at least 1 muon with at least one isolated one
    #########
    df = df.Filter("muons_no >= 1 && muons_sel_iso.size() > 0")
    df = df.Define("cut1", "1")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut1"))

    
    #########
    ### CUT 2 :at least 2 opposite-sign (OS) leptons
    #########
    df = df.Filter("muons_no >= 2 && abs(Sum(muons_q)) < muons_q.size()")
    df = df.Define("cut2", "2")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut2"))
    
    # now we build the Z resonance based on the available leptons.
    # the function resonanceBuilder_mass_recoil returns the best lepton pair compatible with the Z mass (91.2 GeV) and recoil at 125 GeV
    # the argument 0.4 gives a weight to the Z mass and the recoil mass in the chi2 minimization
    # technically, it returns a ReconstructedParticleData object with index 0 the di-lepton system, index and 2 the leptons of the pair
    df = df.Define("zbuilder_result", "FCCAnalyses::ZHfunctions::resonanceBuilder_mass_recoil(91.2, 125, 0.4, 240, false)(muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    df = df.Define("zmumu", "Vec_rp{zbuilder_result[0]}") # the Z
    df = df.Define("zmumu_muons", "Vec_rp{zbuilder_result[1],zbuilder_result[2]}") # the leptons 
    df = df.Define("zmumu_m", "FCCAnalyses::ReconstructedParticle::get_mass(zmumu)[0]") # Z mass
    df = df.Define("zmumu_p", "FCCAnalyses::ReconstructedParticle::get_p(zmumu)[0]") # momentum of the Z
    df = df.Define("zmumu_recoil", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zmumu)") # compute the recoil based on the reconstructed Z
    df = df.Define("zmumu_recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(zmumu_recoil)[0]") # recoil mass
    df = df.Define("zmumu_muons_p", "FCCAnalyses::ReconstructedParticle::get_p(zmumu_muons)") # get the momentum of the 2 muons from the Z resonance
     


    #########
    ### CUT 3: Z mass window
    #########  
    df = df.Filter("zmumu_m > 86 && zmumu_m < 96")
    df = df.Define("cut3", "3")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut3"))

    
    #########
    ### CUT 4: Z momentum
    #########  
    df = df.Filter("zmumu_p > 20 && zmumu_p < 70")
    df = df.Define("cut4", "4")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut4"))

    
    #########
    ### CUT 5: cosThetaMiss
    #########  
    df = df.Define("missingEnergy", "FCCAnalyses::ZHfunctions::missingEnergy(240., ReconstructedParticles)")
    #df = df.Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss(missingEnergy)")
    df = df.Define("cosTheta_miss", "FCCAnalyses::ZHfunctions::get_cosTheta_miss(MissingET)")
    results.append(df.Histo1D(("cosThetaMiss_cut4", "", *bins_cosThetaMiss), "cosTheta_miss")) # plot it before the cut

    df = df.Filter("cosTheta_miss < 0.98")
    df = df.Define("cut5", "5")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut5"))


    #########
    ### CUT 6: recoil mass window
    #########  
    df = df.Filter("zmumu_recoil_m < 140 && zmumu_recoil_m > 120")
    df = df.Define("cut6", "6")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut6"))
    

    ########################
    # Final histograms
    ########################
    results.append(df.Histo1D(("zmumu_m", "", *bins_m_ll), "zmumu_m"))
    results.append(df.Histo1D(("zmumu_recoil_m", "", *bins_recoil), "zmumu_recoil_m"))
    results.append(df.Histo1D(("zmumu_p", "", *bins_p_ll), "zmumu_p"))
    results.append(df.Histo1D(("zmumu_muons_p", "", *bins_p_mu), "zmumu_muons_p"))
    

    return results, weightsum
```

This script first defines the ```inputDir``` and ```outputDir```. Then the scaling and binning for the various histograms are defined. In the ```build_graph``` function the ```muon``` collection is defined and isolated muons with ```p > 20 GeV``` are selected. Then successive cuts that aim at forming the Z mass candidate and reject the backgrounds.  

Now run the **histmaker** script on previously produced samples, to produce a root file containing TH1 histograms:

```bash
fccanalysis run histmaker_recoil.py
```

Now produce the plotting script `plots_recoil.py` run the plotting script with the command:

```python
import ROOT

# global parameters
intLumi        = 1.
intLumiLabel   = "L = 5 ab^{-1}"
ana_tex        = 'e^{+}e^{-} #rightarrow ZH #rightarrow #mu^{+}#mu^{-} + X'
delphesVersion = '3.4.2'
energy         = 240.0
collider       = 'FCC-ee'
formats        = ['png','pdf']

outdir         = './outputs/plots/recoil/' 
inputDir       = './outputs/histmaker/recoil/' 

plotStatUnc    = True

colors = {}
colors['ZH'] = ROOT.kRed
colors['WW'] = ROOT.kBlue+1
colors['ZZ'] = ROOT.kGreen+2

#procs = {}
#procs['signal'] = {'ZH':['wzp6_ee_mumuH_ecm240']}
#procs['backgrounds'] =  {'WW':['p8_ee_WW_ecm240'], 'ZZ':['p8_ee_ZZ_ecm240']}
procs = {}
procs['signal'] = {'ZH':['p8_ee_ZH_Zmumu_ecm240']}
#procs['backgrounds'] =  {'WW':['p8_ee_WW_mumu_ecm240'], 'ZZ':['p8_ee_ZZ_mumubb_ecm240']}
procs['backgrounds'] =  {'ZZ':['p8_ee_ZZ_mumubb_ecm240']}


legend = {}
legend['ZH'] = 'ZH'
legend['WW'] = 'WW'
legend['ZZ'] = 'ZZ'



hists = {}

hists["zmumu_recoil_m"] = {
    "output":   "zmumu_recoil_m",
    "logy":     False,
    "stack":    True,
    "rebin":    100,
    "xmin":     120,
    "xmax":     140,
    "ymin":     0,
    "ymax":     2500,
    "xtitle":   "Recoil (GeV)",
    "ytitle":   "Events / 100 MeV",
}

hists["zmumu_p"] = {
    "output":   "zmumu_p",
    "logy":     False,
    "stack":    True,
    "rebin":    2,
    "xmin":     0,
    "xmax":     80,
    "ymin":     0,
    "ymax":     2000,
    "xtitle":   "p(#mu^{#plus}#mu^{#minus}) (GeV)",
    "ytitle":   "Events ",
}

hists["zmumu_m"] = {
    "output":   "zmumu_m",
    "logy":     False,
    "stack":    True,
    "rebin":    2,
    "xmin":     86,
    "xmax":     96,
    "ymin":     0,
    "ymax":     3000,
    "xtitle":   "m(#mu^{#plus}#mu^{#minus}) (GeV)",
    "ytitle":   "Events ",
}

hists["cosThetaMiss_cut4"] = {
    "output":   "cosThetaMiss_cut4",
    "logy":     True,
    "stack":    True,
    "rebin":    10,
    "xmin":     0,
    "xmax":     1,
    "ymin":     10,
    "ymax":     100000,
    "xtitle":   "cos(#theta_{miss})",
    "ytitle":   "Events ",
    "extralab": "Before cos(#theta_{miss}) cut",
}


hists["cutFlow"] = {
    "output":   "cutFlow",
    "logy":     True,
    "stack":    True,
    "xmin":     0,
    "xmax":     6,
    "ymin":     1e4,
    "ymax":     1e11,
    "xtitle":   ["All events", "#geq 1 #mu^{#pm} + ISO", "#geq 2 #mu^{#pm} + OS", "86 < m_{#mu^{+}#mu^{#minus}} < 96", "20 < p_{#mu^{+}#mu^{#minus}} < 70", "|cos#theta_{miss}| < 0.98", "120 < m_{rec} < 140"],
    "ytitle":   "Events ",
    "scaleSig": 10
}
```

and the 


```bash
fccanalysis plots plots_recoil.py
```

and look at them in `plots/`.

Please note that the event statistics is not great because we only produced on 10 000 events in the `k4SimDelphes` step.


## Part II: Produce a flat tree and analyse events

:::{admonition} Learning Objectives
:class: objectives

In this second example, you will learn how to: 

-  read the **edm4hep** data format, produce jet collections and evaluate the ParticleNet jet tagger score and apply an an event **preselection**
-  produce **flat ntuples** with observables of interest with **FCCAnalyses**
-  apply an **event selection** and **fill histograms** in a single iteration using the **histmaker** option.
-   produce plots with the **plot** option. 
:::


This first analysis stage usually runs on large samples on batch, and the idea is to produce small ntuples with less variables. Also, jet inference of the jet tagger is pretty slow, and usually has to be performed only once. We can then run thr **histmaker** in a second stage. 

Create a file called `treemaker_flavor.py`

```python
import os, copy

# list of processes
processList = {
    "p8_ee_ZH_Zmumu_ecm240": {
        "fraction": 1,
        "crossSection": 0.201868 * 0.034,
    },
    "p8_ee_ZZ_mumubb_ecm240": {
        "fraction": 1,
        "crossSection": 2 * 1.35899 * 0.034 * 0.152,
    },
}

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
#prodTag     = "FCCee/winter2023/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "./outputs/treemaker/flavor/"

# Define the input dir (optional)
inputDir    = "./localSamples/"

# additional/costom C++ functions, defined in header files (optional)
includePaths = ["functions.h"]

## latest particle transformer model, trained on 9M jets in winter2023 samples
model_name = "fccee_flavtagging_edm4hep_wc_v1"

## model files needed for unit testing in CI
url_model_dir = "https://fccsw.web.cern.ch/fccsw/testsamples/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
url_preproc = "{}/{}.json".format(url_model_dir, model_name)
url_model = "{}/{}.onnx".format(url_model_dir, model_name)

## model files locally stored on /eos
model_dir = (
    "/eos/experiment/fcc/ee/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
)
local_preproc = "{}/{}.json".format(model_dir, model_name)
local_model = "{}/{}.onnx".format(model_dir, model_name)

## get local file, else download from url
def get_file_path(url, filename):
    if os.path.exists(filename):
        return os.path.abspath(filename)
    else:
        urllib.request.urlretrieve(url, os.path.basename(url))
        return os.path.basename(url)


weaver_preproc = get_file_path(url_preproc, local_preproc)
weaver_model = get_file_path(url_model, local_model)

from addons.ONNXRuntime.python.jetFlavourHelper import JetFlavourHelper
from addons.FastJet.python.jetClusteringHelper import (
    ExclusiveJetClusteringHelper,
)

jetFlavourHelper = None
jetClusteringHelper = None


# Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis:

    # __________________________________________________________
    # Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):

        # __________________________________________________________
        # Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2

        # define some aliases to be used later on
        df = df.Alias("Particle0", "Particle#0.index")
        df = df.Alias("Particle1", "Particle#1.index")
        df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
        df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
        df = df.Alias("Muon0", "Muon#0.index")
        # get all the leptons from the collection
        df = df.Define(
            "muons_all",
            "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)",
        )
        # select leptons with momentum > 20 GeV
        df = df.Define(
            "muons",
            "FCCAnalyses::ReconstructedParticle::sel_p(20)(muons_all)",
        )
        df = df.Define(
            "muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)"
        )
        df = df.Define(
            "muons_theta",
            "FCCAnalyses::ReconstructedParticle::get_theta(muons)",
        )
        df = df.Define(
            "muons_phi",
            "FCCAnalyses::ReconstructedParticle::get_phi(muons)",
        )
        df = df.Define(
            "muons_q",
            "FCCAnalyses::ReconstructedParticle::get_charge(muons)",
        )
        df = df.Define(
            "muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)"
        )
        # compute the muon isolation and store muons with an isolation cut of 0df = df.25 in a separate column muons_sel_iso
        df = df.Define(
            "muons_iso",
            "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(muons, ReconstructedParticles)",
        )
        df = df.Define(
            "muons_sel_iso",
            "FCCAnalyses::ZHfunctions::sel_iso(0.25)(muons, muons_iso)",
        )

        #########
        ### CUT 1: at least 1 muon with at least one isolated one
        #########
        df = df.Filter("muons_no >= 1 && muons_sel_iso.size() > 0")
        #########
        ### CUT 2 :at least 2 opposite-sign (OS) leptons
        #########
        df = df.Filter("muons_no >= 2 && abs(Sum(muons_q)) < muons_q.size()")
        # now we build the Z resonance based on the available leptons.
        # the function resonanceBuilder_mass_recoil returns the best lepton pair compatible with the Z mass (91.2 GeV) and recoil at 125 GeV
        # the argument 0.4 gives a weight to the Z mass and the recoil mass in the chi2 minimization
        # technically, it returns a ReconstructedParticleData object with index 0 the di-lepton system, index and 2 the leptons of the pair

        ## here cluster jets in the events but first remove muons from the list of
        ## reconstructed particles

        ## create a new collection of reconstructed particles removing muons with p>20
        df = df.Define(
            "ReconstructedParticlesNoMuons",
            "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles,muons)",
        )

        ## perform N=2 jet clustering
        global jetClusteringHelper
        global jetFlavourHelper

        ## define jet and run clustering parameters
        ## name of collections in EDM root files
        collections = {
            "GenParticles": "Particle",
            "PFParticles": "ReconstructedParticles",
            "PFTracks": "EFlowTrack",
            "PFPhotons": "EFlowPhoton",
            "PFNeutralHadrons": "EFlowNeutralHadron",
            "TrackState": "EFlowTrack_1",
            "TrackerHits": "TrackerHits",
            "CalorimeterHits": "CalorimeterHits",
            "dNdx": "EFlowTrack_2",
            "PathLength": "EFlowTrack_L",
            "Bz": "magFieldBz",
        }

        collections_nomuons = copy.deepcopy(collections)
        collections_nomuons["PFParticles"] = "ReconstructedParticlesNoMuons"

        jetClusteringHelper = ExclusiveJetClusteringHelper(
            collections_nomuons["PFParticles"], 2
        )
        df = jetClusteringHelper.define(df)

        ## define jet flavour tagging parameters

        jetFlavourHelper = JetFlavourHelper(
            collections_nomuons,
            jetClusteringHelper.jets,
            jetClusteringHelper.constituents,
        )

        ## define observables for tagger
        df = jetFlavourHelper.define(df)

        ## tagger inference
        df = jetFlavourHelper.inference(weaver_preproc, weaver_model, df)

        df = df.Define(
            "zbuilder_result",
            "FCCAnalyses::ZHfunctions::resonanceBuilder_mass_recoil(91.2, 125, 0.4, 240, false)(muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)",
        )
        df = df.Define("zmumu", "Vec_rp{zbuilder_result[0]}")  # the Z
        df = df.Define(
            "zmumu_muons", "Vec_rp{zbuilder_result[1],zbuilder_result[2]}"
        )  # the leptons
        df = df.Define(
            "zmumu_m",
            "FCCAnalyses::ReconstructedParticle::get_mass(zmumu)[0]",
        )  # Z mass
        df = df.Define(
            "zmumu_p", "FCCAnalyses::ReconstructedParticle::get_p(zmumu)[0]"
        )  # momentum of the Z
        df = df.Define(
            "zmumu_recoil",
            "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zmumu)",
        )  # compute the recoil based on the reconstructed Z
        df = df.Define(
            "zmumu_recoil_m",
            "FCCAnalyses::ReconstructedParticle::get_mass(zmumu_recoil)[0]",
        )  # recoil mass
        df = df.Define(
            "zmumu_muons_p",
            "FCCAnalyses::ReconstructedParticle::get_p(zmumu_muons)",
        )  # get the momentum of the 2 muons from the Z resonance

        df = df.Define(
            "missingEnergy",
            "FCCAnalyses::ZHfunctions::missingEnergy(240., ReconstructedParticles)",
        )
        # .Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss(missingEnergy)")
        df = df.Define(
            "cosTheta_miss",
            "FCCAnalyses::ZHfunctions::get_cosTheta_miss(MissingET)",
        )

        df = df.Define(
            "missing_p",
            "FCCAnalyses::ReconstructedParticle::get_p(MissingET)",
        )

        #########
        ### CUT 3: Njets = 2
        #########
        df = df.Filter("event_njet > 1")

        df = df.Define(
            "jets_p4",
            "JetConstituentsUtils::compute_tlv_jets({})".format(
                jetClusteringHelper.jets
            ),
        )
        df = df.Define(
            "jj_m",
            "JetConstituentsUtils::InvariantMass(jets_p4[0], jets_p4[1])",
        )

        return df

    # __________________________________________________________
    # Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
            "zmumu_m",
            "zmumu_p",
            "zmumu_recoil_m",
            "cosTheta_miss",
            "missing_p",
            "jj_m",
        ]

        ##  outputs jet properties
        # branchList += jetClusteringHelper.outputBranches()

        ## outputs jet scores and constituent breakdown
        branchList += jetFlavourHelper.outputBranches()

        return branchList
```



and run

```bash
fccanalysis run treemaker_flavor.py
```

this will produce a root file for every process containing a flat tree `events` containning high-level variables. In addition to selecting muons as done in the previous example, this script create a new collection of `ReconstructedParticles` without the two high energy muons, and runs the jet clustering algorithm in exclusive N=2 mode of the new collection. In such a way, the two clustered jets form the H->jj jet candidates. The jet flavour algorithm is then evaluated on these two jets and the relevant scores are stored in the output tree.   

Now we can produce a **histmaker** script, that runs this time on a flat ntuple format instead of the edm4hep format `histmaker_flavor.py`:


```python
# list of processes (mandatory)
processList = {
    "p8_ee_ZH_Zmumu_ecm240": {
        "fraction": 1,
        "crossSection": 0.201868 * 0.034,
    },
    "p8_ee_ZZ_mumubb_ecm240": {
        "fraction": 1,
        "crossSection": 2 * 1.35899 * 0.034 * 0.152,
    },
}

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
#prodTag = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# Define the input dir (optional)
inputDir    = "./outputs/treemaker/flavor/"

# Optional: output directory, default is local running directory
outputDir = "./outputs/histmaker/flavor/"


# optional: ncpus, default is 4, -1 uses all cores available
nCPUS = -1

# scale the histograms with the cross-section and integrated luminosity
doScale = True
intLumi = 5000000  # 5 /ab


# define some binning for various histograms
bins_p_mu = (2000, 0, 200)  # 100 MeV bins
bins_m_ll = (2000, 0, 200)  # 100 MeV bins
bins_p_ll = (2000, 0, 200)  # 100 MeV bins
bins_recoil = (200000, 0, 200)  # 1 MeV bins
bins_cosThetaMiss = (10000, 0, 1)

bins_m_jj = (100, 50, 150)  # 1 GeV bins
bins_score = (50, 0, 2.0)  #

bins_theta = (500, -5, 5)
bins_eta = (600, -3, 3)
bins_phi = (500, -5, 5)

bins_count = (50, 0, 50)
bins_charge = (10, -5, 5)
bins_iso = (500, 0, 5)


# build_graph function that contains the analysis logic, cuts and histograms (mandatory)
def build_graph(df, dataset):

    results = []
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")

    #########
    ### CUT 4: Z mass window
    #########
    df = df.Filter("zmumu_m > 86 && zmumu_m < 96")

    #########
    ### CUT 5: Z momentum
    #########
    df = df.Filter("zmumu_p > 20 && zmumu_p < 70")

    #########
    ### CUT 6: recoil mass window
    #########
    df = df.Filter("zmumu_recoil_m < 140 && zmumu_recoil_m > 120")

    #########
    ### CUT 7: cut on the jet tagging score to select H->bb events
    #########
    df = df.Define("scoresum_B", "recojet_isB[0] + recojet_isB[1]")
    results.append(df.Histo1D(("scoresum_B", "", *bins_score), "scoresum_B"))

    df = df.Filter("scoresum_B > 1.0")

    results.append(df.Histo1D(("zmumu_m", "", *bins_m_ll), "zmumu_m"))
    results.append(
        df.Histo1D(("zmumu_recoil_m", "", *bins_recoil), "zmumu_recoil_m")
    )
    results.append(df.Histo1D(("zmumu_p", "", *bins_p_ll), "zmumu_p"))
    results.append(df.Histo1D(("jj_m", "", *bins_m_jj), "jj_m"))

    return results, weightsum
```


and run it: 
```bash
fccanalysis run histmaker_flavor.py
```

This script takes the ntuples produced in the **run** stage, applies a similar selection as in the previous examples, but requires the jets to have a high probability to be B-like. 

Now we can write the code to produce plots, in `plots_flavor.py`:

```python
import ROOT

# global parameters
intLumi = 1
intLumiLabel = "L = 5 ab^{-1}"
ana_tex = "e^{+}e^{-} #rightarrow ZH #rightarrow #mu^{+}#mu^{-} b b"
delphesVersion = "3.4.2"
energy = 240.0
collider = "FCC-ee"
formats = ["png", "pdf"]

outdir         = './outputs/plots/flavor/' 
inputDir       = './outputs/histmaker/flavor/' 

plotStatUnc = True

colors = {}
colors["ZH"] = ROOT.kRed
colors["ZZ"] = ROOT.kGreen + 2

procs = {}
procs["signal"] = {"ZH": ["p8_ee_ZH_Zmumu_ecm240"]}
procs["backgrounds"] = {"ZZ": ["p8_ee_ZZ_mumubb_ecm240"]}

legend = {}
legend["ZH"] = "ZH"
legend["ZZ"] = "ZZ"

hists = {}

hists["zmumu_recoil_m"] = {
    "output": "zmumu_recoil_m",
    "logy": False,
    "stack": True,
    "rebin": 100,
    "xmin": 120,
    "xmax": 140,
    "ymin": 0,
    "ymax": 2000,
    "xtitle": "Recoil (GeV)",
    "ytitle": "Events / 100 MeV",
}

hists["jj_m"] = {
    "output": "jj_m",
    "logy": False,
    "stack": True,
    "rebin": 2,
    "xmin": 50,
    "xmax": 150,
    "ymin": 0,
    "ymax": 4000,
    "xtitle": "m_{jj} (GeV)",
    "ytitle": "Events / 2 GeV",
}

hists["scoresum_B"] = {
    "output": "scoresum_B",
    "logy": True,
    "stack": True,
    "rebin": 1,
    "xmin": 0,
    "xmax": 2.0,
    "ymin": 1,
    "ymax": 100000,
    "xtitle": "p_{1}(B) + p_{2}(B)",
    "ytitle": "Events",
}
```

```bash
fccanalysis plots plots_flavor.py
```

:::{admonition} Exercises
:class: challenge

## Simple

1) Modify `histmaker_flavor.py` to require the two jets individually to be B-like, i.e requiring the B score is greater 0.5 for each jet. 

2) Selecting gluon-like jets instead. You will need to modify both the  `treemaker_flavor.py` and `histmaker_flavor.py` for this.)

3) Produce plots with larger statistics by re-running `DelphesPythia8_EDM4HEP` with more events. In particular produce a ZZ inclusive sample using to include all Z decays. Rerun all the examples above.

## Advanced

1) To evaluate the impact of detector performance, smear the neutral hadron resolution in the `ReconstructedParticlesNoMuons` collection and check the impact on the dijet invariant mass resolution. An example can be found [here] (https://github.com/HEP-FCC/FCCAnalyses/blob/master/examples/FCCee/smearing/smear_jets.py): 

2) Now smear the impact parameter resolution and evaluate the imapct on the efficiency of selecting two B-tagged jets or two C-tagged jets. 

3) **This part can only be on lxplus and for people having the access rights to eos and the analysis dictonary**
In order to produce plots with more statistics using centrally produced samples, we could use already processed large statistics samples.
To do so we re-run the pre-selection over 10 percent of the total statistics [here](http://fcc-physics-events.web.cern.ch/fcc-physics-events/Delphesevents_spring2021_IDEA.php).
Add to your a `analysis_stage1.py` file

```python
processList = {
    'p8_ee_ZZ_ecm240':{'fraction':0.1},
    'p8_ee_WW_ecm240':{'fraction':0.1},
    'p8_ee_ZH_ecm240':{'fraction':0.1}
}
prodTag     = "FCCee/winter2023/IDEA/"
:::
