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
            .Alias("Particle1", "Particle#1.index")
            .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
            .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

            # MC indices of the decay
            # Bs (PDG = 531) -> mu+ (PDG = -13) mu- (PDG = 13) K+ (PDG = 321) K- (PDG = -321)
            # Retrieves a vector of integers which correspond to indices in the
            # Particle block
            # vector[0] = the mother, and then the daughters in the order
            # specified, i.e. here [1] = the mu+, [2] = the mu-, [3] = the K+,
            # [4] = the K-
            #
            # Boolean arguments:
            #   1st: `stableDaughters`, when set to true, the daughters specified
            #        in the list are looked for among the final, stable
            #        particles that come out from the mother, i.e. the decay
            #        tree is explored recursively if needed.
            #   2nd: `chargeConjugateMother`
            #   3rd: `chargeConjugateDaughters`
            #   4th: `inclusiveDecay`, when set to false, if a mother is found,
            #        that decays into the particles specified in the list plus
            #        other particle(s), this decay is not selected.
            # If the event contains more than one such decays, only the first
            # one is kept.
            .Define("Tau3Mu_indices",
                    "MCParticle::get_indices(15, {-13, 13, 13}, true, true, true, false) (Particle, Particle1)")

            # select events for which the requested decay chain has been found:
            .Filter("Tau3Mu_indices.size() > 0")

            # the mu+ (MCParticle) that comes from the Bs decay :
            .Define("MC_Muplus", "return Particle.at(Tau3Mu_indices[1]);")
            # Decay vertex (an `edm4hep::Vector3d`) of the Bs (MC) = production
            # vertex of the muplus:
            .Define("TauMCDecayVertex", "return MC_Muplus.vertex;")

            # Returns the RecoParticles associated with the four Bs decay products.
            # The size of this collection is always 4 provided that
            # Tau3Mu_indices is not empty, possibly including "dummy"
            # particles in case one of the legs did not make a RecoParticle
            # (e.g. because it is outside the tracker acceptance). This is done
            # on purpose, in order to maintain the mapping with the indices ---
            # i.e. the 1st particle in the list BsRecoParticles is the mu+,
            # then the mu-, etc.
            # (selRP_matched_to_list ignores the unstable MC particles that are
            # in the input list of indices hence the mother particle, which is
            # the [0] element of the Tau3Mu_indices vector).
            #
            # The matching between RecoParticles and MCParticles requires 4
            # collections. For more detail, see
            # https://github.com/HEP-FCC/FCCAnalyses/tree/master/examples/basics
            .Define("TauRecoParticles",
                    "ReconstructedParticle2MC::selRP_matched_to_list(Tau3Mu_indices, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")

            # the corresponding tracks --- here, dummy particles, if any, are
            # removed, i.e. one may have < 4 tracks, e.g. if one muon or kaon
            # was emitted outside of the acceptance
            .Define("TauTracks",
                    "ReconstructedParticle2Track::getRP2TRK(BsRecoParticles, EFlowTrack_1)")

            # number of tracks in this BsTracks collection (= the #tracks
            # used to reconstruct the Bs vertex)
            .Define("n_TauTracks",
                    "ReconstructedParticle2Track::getTK_n(BsTracks)")

            # Fit the tracks to a common vertex. That would be a secondary
            # vertex, hence we put a "2" as the first argument of
            # VertexFitter_Tk: First the full object, of type
            # Vertexing::FCCAnalysesVertex
            .Define("TauVertexObject",
                    "VertexFitterSimple::VertexFitter_Tk(2, BsTracks)")
            # from which we extract the edm4hep::VertexData object, which
            # contains the vertex position in mm
            .Define("TauVertex",
                    "VertexingUtils::get_VertexData(BsVertexObject)")
            # The reco'ed tau mass --- from the post-VertxFit momenta, at the
            # tau decay vertex:
            .Define("TauMass", "VtxAna::tau3mu_vertex_mass(TauVertexObject)")
            # The "raw" mass --- using the track momenta at their dca:
            .Define("RawMass", "VtxAna::tau3mu_raw_mass(TauRecoParticles)")
        )

        return df2


    def output():
        '''
        Mandatory output function, please make sure you return the branch list
        (the list of dataframe columns to be saved).
        '''
        branchList = [
            "MC_Muplus",
            "n_BsTracks",
            "BsMCDecayVertex",
            "BsVertex",
            "TauMass",
            "RawMass",
        ]

        return branchList
