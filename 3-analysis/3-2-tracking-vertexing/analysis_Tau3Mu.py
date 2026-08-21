'''
Analysis of $\tau \rightarrow 3 \mu$
'''

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
            # Build triplets of muons.
            # We are interested in tau- -> mu- mu- mu+ (the MC files produced
            # for this tutorial only forced the decay of the tau- , not the
            # tau+). Hence we look for triples of total charge = -1:
            .Define("triplets_m", "VtxAna::build_triplets(muons, -1.)")
            .Define("n_triplets_m", "return triplets_m.size();")
            # ----------------------------------------------------
            # Considering all triplets:
            .Define("TauVertexObject_allCandidates",
                    "VtxAna::build_AllTauVertexObject(triplets_m, EFlowTrack_1)")
            .Define("TauMass_allCandidates",
                    "VtxAna::build_AllTauMasses(TauVertexObject_allCandidates)")
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
            "TauMass_allCandidates"
        ]

        return branchList
