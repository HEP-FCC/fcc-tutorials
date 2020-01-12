import os
import copy
import heppy.framework.config as cfg

import logging
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

comp = cfg.Component(
    'example',
    files = ['FCCDelphesOutput.root']
   )
selectedComponents = [comp]

from heppy.analyzers.fcc.Reader import Reader
source = cfg.Analyzer(
    Reader,

    weights = 'mcEventWeights',

    gen_particles = 'skimmedGenParticles',

    electrons = 'electrons',
    electronITags = 'electronITags',
    electronsToMC = 'electronsToMC',

    muons = 'muons',
    muonITags = 'muonITags',
    muonsToMC = 'muonsToMC',
    
)

from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events

#############################
##   Gen Level Analysis    ##
#############################

# select stable electrons and muons
from heppy.analyzers.Selector import Selector
gen_leptons = cfg.Analyzer(
    Selector,
    'gen_leptons',
    output = 'gen_leptons',
    input_objects = 'gen_particles',
    filter_func = lambda ptc: (abs(ptc.pdgid()) == 11 or (abs(ptc.pdgid()) == 13) ) and ptc.status() == 1
)

# produce flat root tree containing information about stable leptons in the event
from heppy.analyzers.examples.hzz4l.HTo4lGenTreeProducer import HTo4lGenTreeProducer
gen_tree = cfg.Analyzer(
    HTo4lGenTreeProducer,
    leptons = 'gen_leptons',
)

#############################
##   Reco Level Analysis   ##
#############################


# select isolated muons with pT > 5 GeV and relIso < 0.4
from heppy.analyzers.Selector import Selector
selected_muons = cfg.Analyzer(
    Selector,
    'selected_muons',
    output = 'selected_muons',
    input_objects = 'muons',
    filter_func = lambda ptc: ptc.pt()>5 and ptc.iso.sumpt/ptc.pt()<0.4
)

# select electrons with pT > 7 GeV and relIso < 0.4
selected_electrons = cfg.Analyzer(
    Selector,
    'selected_electrons',
    output = 'selected_electrons',
    input_objects = 'electrons',
    filter_func = lambda ptc: ptc.pt()>7 and ptc.iso.sumpt/ptc.pt()<0.4
)

# merge electrons and muons into a single lepton collection
from heppy.analyzers.Merger import Merger
selected_leptons = cfg.Analyzer(
      Merger,
      instance_label = 'selected_leptons', 
      inputs = ['selected_electrons','selected_muons'],
      output = 'selected_leptons'
)

# create Z boson candidates with leptons
from heppy.analyzers.LeptonicZedBuilder import LeptonicZedBuilder
zeds = cfg.Analyzer(
      LeptonicZedBuilder,
      output = 'zeds',
      leptons = 'selected_leptons',
)

# create H boson candidates
from heppy.analyzers.ResonanceBuilder import ResonanceBuilder
higgses = cfg.Analyzer(
      ResonanceBuilder,
      output = 'higgses',
      leg_collection = 'zeds',
      pdgid = 25
)

# apply event selection. Defined in "analyzers/examples/hzz4l/selection.py"
from heppy.analyzers.examples.hzz4l.selection import Selection
selection = cfg.Analyzer(
    Selection,
    instance_label='cuts'
)

# store interesting quantities into flat ROOT tree
from heppy.analyzers.examples.hzz4l.HTo4lTreeProducer import HTo4lTreeProducer
reco_tree = cfg.Analyzer(
    HTo4lTreeProducer,
    zeds = 'zeds',
    higgses = 'higgses',
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    gen_leptons,
    gen_tree,
    selected_muons,
    selected_electrons,
    selected_leptons,
    zeds,
    selection,
    higgses,
    reco_tree,
    ] )


config = cfg.Config(
    components = selectedComponents,
    sequence = sequence,
    services = [],
    events_class = Events
)

if __name__ == '__main__':
    import sys
    from heppy.framework.looper import Looper

    def next():
        loop.process(loop.iEvent+1)

    loop = Looper( 'looper', config,
                   nEvents=100,
                   nPrint=0)
    loop.process(6)
    print loop.event
