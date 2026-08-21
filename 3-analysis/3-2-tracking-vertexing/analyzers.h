#ifndef FCCANA_ADDITIONAL_ANALYZERS_H
#define FCCANA_ADDITIONAL_ANALYZERS_H

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"

namespace FCCAnalyses :: VtxAna {
  namespace rv = ROOT::VecOps;

  rv::RVec<float> dummy_analyzer(const rv::RVec<edm4hep::ReconstructedParticleData>& parts) {
    rv::RVec<float> output;
    for (size_t i = 0; i < parts.size(); ++i)
      output.emplace_back(parts.at(i).momentum.x);
    return output;
  }
}

#endif /* FCCANA_ADDITIONAL_ANALYZERS_H */
