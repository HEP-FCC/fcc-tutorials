'''
Analysis of $\tau \rightarrow 3 \mu$
'''

import ROOT

testFile = "/eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/" \
           "p8_noBES_ee_Ztautau_ecm91_EvtGen_TauMinus2MuMuMu/" \
           "events_189205650.root"

includePaths = ["analyzers_Tau3Mu.h"]


class RDFanalysis():
    '''
    Mandatory class where the user defines the operations on the dataframe.
    '''

    def analysers(df):
        '''
        Mandatory function to define the actual analysers, please make sure
        you return the last dataframe, in this example it is df2.
        '''
        df2 = (
            df
            # Use the "AllMuons" collection, which contains also non-isolated
            # muons (in contrast to the "Muons" collection)
            #
            # Actually, "Muon" or ("AllMuon") just contain pointers (indices)
            # to the RecoParticle collections, hence one needs to first
            # retrieve the RecoParticles corresponding to these muons (for more
            # detail about the subset collections, see:
            # https://github.com/HEP-FCC/FCCAnalyses/tree/master/examples/basics)
            .Alias("Muon0", "AllMuon#0.index")
            .Define("muons",
                    "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
            .Define("n_muons", "ReconstructedParticle::get_n(muons)")
            # -----------------------------------------
            # Add fake muons from pi -> mu
            # This selects the charged hadrons:
            .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
            .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
            .Define("ChargedHadrons",
                    "ReconstructedParticle2MC::selRP_ChargedHadrons(MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
            # Only the ones with p > 2 GeV could be selected as muons:
            .Define("ChargedHadrons_pgt2",
                    "ReconstructedParticle::sel_p(2.)(ChargedHadrons)")
            # Build fake muons based on a flat fake rate (random selection) ---
            # HUGE fake rate used on purpose here:
            .Define("fakeMuons_5em2",
                    ROOT.VtxAna.selRP_Fakes(5e-2, ROOT.VtxAna.MUON_MASS),
                    ["ChargedHadrons_pgt2"])
            # Now we merge the collection of fake muons with the genuine muons:
            .Define("muons_with_fakes",
                    "ReconstructedParticle::merge( muons, fakeMuons_5em2 )")
            # and we use this collection later on, instead of "muons":
            .Define("n_muons_with_fakes",
                    "ReconstructedParticle::get_n(muons_with_fakes)")
            # -----------------------------------------
            # Build triplets of muons.
            # We are interested in tau- -> mu- mu- mu+ (the MC files produced
            # for this tutorial only forced the decay of the tau- , not the
            # tau+). Hence we look for triples of total charge = -1:
            # .Define("triplets_m", "VtxAna::build_triplets(muons, -1.)")
            .Define("triplets_m",
                    "VtxAna::build_triplets(muons_with_fakes, -1.)")
            .Define("n_triplets_m", "return triplets_m.size();")
            # ----------------------------------------------------
            # Considering all triplets:
            .Define("TauVertexObject_allCandidates",
                    "VtxAna::build_AllTauVertexObject(triplets_m, EFlowTrack_1)")
            .Define("TauMass_allCandidates",
                    "VtxAna::build_AllTauMasses(TauVertexObject_allCandidates)")
            # Total visible energy in the event:
            .Define("RecoPartEnergies",
                    "ReconstructedParticle::get_e(ReconstructedParticles)")
            .Define("visible_energy", "Sum(RecoPartEnergies)")
        )

        return df2


    def output():
        '''
        Mandatory output function, please make sure you return the branch list
        (the list of dataframe columns to be saved).
        '''
        branchList = [
            "n_muons",
            "n_triplets_m",
            "TauMass_allCandidates",
            "visible_energy"
        ]

        return branchList
