#ifndef FCCANA_ADDITIONAL_ANALYZERS_H
#define FCCANA_ADDITIONAL_ANALYZERS_H

// C++ standard library
#include <cmath>
#include <random>
#include <chrono>

// ROOT
#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"

// EDM4hep
#include "edm4hep/ReconstructedParticleData.h"

// FCCAnalyses
#include "FCCAnalyses/VertexingUtils.h"
#include "FCCAnalyses/ReconstructedParticle2Track.h"
#include "FCCAnalyses/VertexFitterSimple.h"

namespace FCCAnalyses :: VtxAna {
  const double MUON_MASS = 0.1056;  // GeV

  double tau3mu_vertex_mass(const VertexingUtils::FCCAnalysesVertex& vertex) {
    TLorentzVector tau;
    ROOT::VecOps::RVec<TVector3> momenta = vertex.updated_track_momentum_at_vertex;
    int n = momenta.size();
    for (int ileg=0; ileg < n; ileg++) {
      TVector3 track_momentum = momenta[ileg];
      TLorentzVector leg;
      leg.SetXYZM(track_momentum[0], track_momentum[1], track_momentum[2], MUON_MASS) ;
      tau += leg;
    }

    return tau.M();
  }

  double tau3mu_raw_mass(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& legs) {
    TLorentzVector tau;
    int n = legs.size();
    for (int ileg=0; ileg < n; ileg++) {
      TLorentzVector leg;
      leg.SetXYZM(legs[ileg].momentum.x, legs[ileg].momentum.y, legs[ileg].momentum.z, MUON_MASS);
      tau += leg;
    }

    return tau.M();
  }

  ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>>
  build_triplets(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& inParticles,
                 float total_charge) {
    ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>> result;

    int n = inParticles.size();
    if (n < 3) {
      return result;
    }

    for (int i = 0; i < n; ++i) {
      edm4hep::ReconstructedParticleData pi = inParticles[i];

      for (int j = i + 1; j < n; ++j) {
        edm4hep::ReconstructedParticleData pj = inParticles[j];

        for (int k=j+1; k < n; ++k) {
          edm4hep::ReconstructedParticleData pk = inParticles[k];
          float charge_tot = pi.charge + pj.charge + pk.charge;

          if (charge_tot == total_charge) {
            ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> a_triplet = {pi, pj, pk};
            result.push_back(a_triplet);
          }
        }  // end of the loop over k
      }  // end of the loop over j
    }  // end of the loop over i

    return result;
  }

  ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex>
  build_AllTauVertexObject(const ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>>& triplets,
                           const ROOT::VecOps::RVec<edm4hep::TrackState>& allTracks) {
    ROOT::VecOps::RVec< VertexingUtils::FCCAnalysesVertex> results;
    int ntriplets = triplets.size();
    for (int i=0; i < ntriplets; i++) {
      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs = triplets[i];

      ROOT::VecOps::RVec<edm4hep::TrackState> the_tracks = ReconstructedParticle2Track::getRP2TRK(legs, allTracks);
      VertexingUtils::FCCAnalysesVertex vertex = VertexFitterSimple::VertexFitter_Tk(2, the_tracks);
      results.push_back(vertex);
    }

    return results;
  }

  ROOT::VecOps::RVec<double>
  build_AllTauMasses(const ROOT::VecOps::RVec<VertexingUtils::FCCAnalysesVertex>& vertices) {
    ROOT::VecOps::RVec<double> results;
    for (const auto& v: vertices) {
      double mass = tau3mu_vertex_mass(v);
      results.push_back(mass);
    }

    return results;
  }

  struct selRP_Fakes {
    selRP_Fakes(float arg_fakeRate, float arg_mass);

    float m_fakeRate = 1e-3;  // fake rate
    float m_mass = MUON_MASS;  // particle mass
    std::default_random_engine m_generator;
    std::uniform_real_distribution<float> m_flat;

    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
    operator() (const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& inParticles);
  };

  selRP_Fakes::selRP_Fakes(float arg_fakeRate, float arg_mass): m_fakeRate(arg_fakeRate),
                                                                m_mass(arg_mass) {
    auto seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::default_random_engine generator(seed);
    m_generator = generator;
    std::uniform_real_distribution<float> flatdis(0., 1.);
    m_flat.param(flatdis.param());
  };

  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
  selRP_Fakes::operator() (const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& inParticles) {
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
    for (const auto& p: inParticles) {
      float arandom = m_flat(m_generator);
      if (arandom <= m_fakeRate) {
        edm4hep::ReconstructedParticleData reso = p;
        // overwrite the mass:
        reso.mass = m_mass;
        result.push_back(reso);
      }
    }

    return result;
  }
}

#endif /* FCCANA_ADDITIONAL_ANALYZERS_H */
