# Guide to the Transition of FCCSW to EDM4hep

For the studies of the Conceptual Design Report, FCC software used its own datamodel, [FCCEDM](https://github.com/hep-fcc/fccedm).
The technical implementation was based on a novel library called [PODIO](https://github.com/aidasoft/podio), and tries to use "Plain Old Data" to achieve thread safety and general ease of use.

While FCCEDM has served its purpose, continued use has revealed some minor issues, inconsistencies and impracticalities (see [here](https://github.com/HEP-FCC/fcc-edm/issues?q=is%3Aissue+) and [here](https://fccsw-forum.web.cern.ch/t/event-data-model-discussion/32)).
Since then, FCC has joined a common software effort with other Future Collider Communities, and decided to base the common software ([Key4HEP](https://cern.ch/key4hep)) on a new, common datamodel ([EDM4HEP](https://github.com/key4hep/edm4hep)). 

The types defined by EDM4HEP are somewhat closer to [LCIO](https://github.com/ilcsoft/lcio), but like FCCEDM it is implemented with PODIO.
In any case, the transition, while time-intensive, is no major technical challenge, and provides the basis for a common experiment software beyond FCC.


This document should guide users and developers through the transition.

EDM4HEP and FCCEDM can coexist, but for a frictionless transition, FCCEDM should be replaced completely as soon as possible.


The following sections focus on the Gaudi-based framework FCCSW and explain how to transition the components of the datamodel.
The latest developments can be found on [this branch](https://github.com/HEP-FCC/FCCSW/tree/edm4hep) (PRs welcome).



## Technical Information

### Build System

EDM4HEP ships a CMake configuration (in uppercase: `EDM4HEPConfig.cmake`) that defines CMake Targets (in lowercase: `EDM4HEP::edm4hep`).
To include and link edm4hep, it is sufficient to add the following to the `CMakeLists.txt` of an example project:




```

find_package(EDM4HEP)

 gaudi_add_module(ExampleModule
                  src/components/*.cpp
                  INCLUDE_DIRS # nothing needs to be added here, the target defines the includes
                  LINK_LIBRARIES EDM4HEP::edm4hep)
```


### Component source Code  

The code now can be adapted changing any mention of `datamodel` to `edm4hep` and converting the types: 

#### Generation / MCParticles

FCCEDM had several types to describe particles at the Generator Level: `GenParticle`, `GenVertex` and `GenJet`. 
The mother/daughter relationship was encoded in the vertices; A particle and its decay product were supposed to share one vertex object (the mother particle as its endvertex, the daughter particle as its startvertex). A library for creating directed acyclic graphs was supposed to help deal with this slightly cumbersome system, but was not really used in practice.

EDM4HEP replaces this by the single type `MCParticle`. This contains the vertex information, and Jets are generally treated as particles in EDM4hep.

The correspondence is fairly direct:

| | |
|----|----|
| EDM4HEP | FCCEDM |
| MCParticle | MCParticle/GenVertex/GenJet |
| PDG | core.pdgId |
| generatorStatus | core.status |
| charge | charge |
| time |  startVertex.ctau # Note the unit differences! |
| vertex | startVertex.position |
| endpoint | endVertex.position |
| momentum, mass | core.p4 |
| momentumAtEndpoint ||
| spin | |
| colorFlow | |



### Job options

As the GenVertex type is no longer an independent type in edm4hep, any components that used to write GenParticles and GenVertices need to be adapted (the opportunity was used to also update the spelling from `genparticles` to `GenParticles` for the Gaudi data property):

```diff
- hepmc_converter.genparticles.Path="allGenParticles"
- hepmc_converter.genvertices.Path="allGenVertices"
+ hepmc_converter.GenParticles.Path="allGenParticles"
```

The configuration for the SimG4SaveSmearedParticles tool needs to be adapted in the following way:

```diff
- from Configurables import SimG4SaveSmearedParticles
- saveparticlestool = SimG4SaveSmearedParticles("saveSmearedParticles")
- saveparticlestool.particles.Path = "smearedParticles"
- saveparticlestool.particlesMCparticles.Path = "particleMCparticleAssociation"
+ saveparticlestool.RecParticles.Path = "smearedParticles"
+ saveparticlestool.MCRecoParticleAssoc.Path = "particleMCparticleAssociation"

```

```diff

- particle_converter = SimG4PrimariesFromEdmTool("EdmConverter")
- particle_converter.genParticles.Path = "allGenParticles"
+ particle_converter.GenParticles.Path = "allGenParticles"
```
