import os

from GaudiKernel.SystemOfUnits import MeV, GeV, tesla

# Input for simulations (momentum is expected in GeV)
pdgCode = 22 # 11 electron, 13 muon, 22 photon, 111 pi0, 211 pi+
momentum = 10
thetaMin = 90
thetaMax = 90
magneticField = False
addNoise = False

from Gaudi.Configuration import *

from Configurables import FCCDataSvc
podioevent  = FCCDataSvc("EventDataSvc")

_pi = 3.14159
################## Particle gun setup
from Configurables import  MomentumRangeParticleGun
pgun = MomentumRangeParticleGun("ParticleGun")
pgun.PdgCodes = [pdgCode]
pgun.MomentumMin = momentum * GeV
pgun.MomentumMax = momentum * GeV
pgun.PhiMin = 0
pgun.PhiMax = 2 * _pi
pgun.ThetaMin = thetaMin * _pi / 180.
pgun.ThetaMax = thetaMax * _pi / 180.

from Configurables import GenAlg
genalg_pgun = GenAlg()
genalg_pgun.SignalProvider = pgun 
genalg_pgun.hepmc.Path = "hepmc"

from Configurables import HepMCToEDMConverter
hepmc_converter = HepMCToEDMConverter()
hepmc_converter.hepmc.Path="hepmc"
hepmc_converter.GenParticles.Path="genParticles"

################## Simulation setup
# Detector geometry
from Configurables import GeoSvc
geoservice = GeoSvc("GeoSvc")
path_to_detector = os.environ.get("FCCDETECTORS", "")
detectors_to_use=[
                    'Detector/DetFCCeeIDEA-LAr/compact/FCCee_DectMaster.xml',
                  ]
# prefix all xmls with path_to_detector
geoservice.detectors = [os.path.join(path_to_detector, _det) for _det in detectors_to_use]
geoservice.OutputLevel = WARNING

# Geant4 service
# Configures the Geant simulation: geometry, physics list and user actions
from Configurables import SimG4Svc
geantservice = SimG4Svc("SimG4Svc", detector='SimG4DD4hepDetector', physicslist="SimG4FtfpBert", actions="SimG4FullSimActions")

# Fixed seed to have reproducible results, change it for each job if you split one production into several jobs
# Mind that if you leave Gaudi handle random seed and some job start within the same second (very likely) you will have duplicates
geantservice.randomNumbersFromGaudi = False
geantservice.seedValue = 1

# Expected range in a given material under which all the particle energy is automatically deposited in the given cell (no further interaction simulated)
geantservice.g4PreInitCommands += ["/run/setCut 0.1 mm"]

# Magnetic field
from Configurables import SimG4ConstantMagneticFieldTool
if magneticField == 1:
    field = SimG4ConstantMagneticFieldTool("SimG4ConstantMagneticFieldTool", FieldComponentZ=-2*tesla, FieldOn=True, IntegratorStepper="ClassicalRK4")
else:
    field = SimG4ConstantMagneticFieldTool("SimG4ConstantMagneticFieldTool", FieldOn=False)

# Geant4 algorithm
# Translates EDM to G4Event, passes the event to G4, writes out outputs via tools
# and a tool that saves the calorimeter hits

# Detector readouts
# ECAL
ecalBarrelReadoutName = "ECalBarrelEta"
ecalBarrelReadoutNamePhiEta = "ECalBarrelPhiEta"

# Configure saving of calorimeter hits
from Configurables import SimG4SaveCalHits
saveecalbarreltool = SimG4SaveCalHits("saveECalBarrelHits", readoutNames = [ecalBarrelReadoutName])
saveecalbarreltool.CaloHits.Path = "ECalBarrelHits"

# next, create the G4 algorithm, giving the list of names of tools ("XX/YY")
from Configurables import SimG4PrimariesFromEdmTool
particle_converter = SimG4PrimariesFromEdmTool("EdmConverter")
particle_converter.GenParticles.Path = "genParticles"

from Configurables import SimG4Alg
geantsim = SimG4Alg("SimG4Alg",
                       outputs= ["SimG4SaveCalHits/saveECalBarrelHits",
                       ],
                       eventProvider=particle_converter,
                       OutputLevel=0)

############## Digitization (Merging hits into cells, EM scale calibration)
# EM scale calibration (sampling fraction)
from Configurables import CalibrateInLayersTool
calibEcalBarrel = CalibrateInLayersTool("CalibrateECalBarrel",
                                   # sampling fraction obtained using SamplingFractionInLayers
                                   samplingFraction = [0.3674030774913384, 0.09847833302358869, 0.12571104392015559, 0.1435269034800326, 0.15562338401911247, 0.16433369501246228, 0.17101382906715829, 0.17706510179843604, 0.18179714100755953, 0.1854827654246184, 0.188358333708253, 0.2118603901819323],
                                   readoutName = ecalBarrelReadoutName,
                                   layerFieldName = "layer")

# Create cells in ECal barrel
# 1. step - merge hits into cells with default Eta segmentation
# 2. step - rewrite the cellId using the Phi-Eta segmentation
from Configurables import CreateCaloCells
createEcalBarrelCellsStep1 = CreateCaloCells("CreateECalBarrelCellsStep1",
                               doCellCalibration=True,
                               calibTool = calibEcalBarrel,
                               addCellNoise=False, filterCellNoise=False,
                               OutputLevel=INFO,
                               hits="ECalBarrelHits",
                               cells="ECalBarrelCellsStep1")

# Use Phi-Eta segmentation in ECal barrel
from Configurables import RedoSegmentation
resegmentEcalBarrel = RedoSegmentation("ReSegmentationEcal",
                             # old bitfield (readout)
                             oldReadoutName = ecalBarrelReadoutName,
                             # specify which fields are going to be altered (deleted/rewritten)
                             oldSegmentationIds = ["module"],
                             # new bitfield (readout), with new segmentation
                             newReadoutName = ecalBarrelReadoutNamePhiEta,
                             OutputLevel = INFO,
                             inhits = "ECalBarrelCellsStep1",
                             outhits = "ECalBarrelCellsStep2")

EcalBarrelCellsName = "ECalBarrelCells"
createEcalBarrelCells = CreateCaloCells("CreateECalBarrelCells",
                               doCellCalibration=False,
                               addCellNoise=False, filterCellNoise=False,
                               OutputLevel=INFO,
                               hits="ECalBarrelCellsStep2",
                               cells=EcalBarrelCellsName)
cell_creator_to_use = createEcalBarrelCells

# generate noise for each cell if required
if addNoise:
    ecalBarrelNoisePath = "/eos/experiment/fcc/ee/tutorial/caloFullSim2022/elecNoise_ecalBarrelFCCee.root"
    ecalBarrelNoiseHistName = "h_elecNoise_fcc_"
    from Configurables import NoiseCaloCellsFromFileTool
    noiseBarrel = NoiseCaloCellsFromFileTool("NoiseBarrel",
                                             readoutName = ecalBarrelReadoutNamePhiEta,
                                             noiseFileName = ecalBarrelNoisePath,
                                             elecNoiseHistoName = ecalBarrelNoiseHistName,
                                             activeFieldName = "layer",
                                             addPileup = False,
                                             filterNoiseThreshold = 0,
                                             scaleFactor = 1/1000.,
                                             numRadialLayers = 12)

    from Configurables import TubeLayerPhiEtaCaloTool
    barrelGeometry = TubeLayerPhiEtaCaloTool("EcalBarrelGeo",
                                             readoutName = ecalBarrelReadoutNamePhiEta,
                                             activeVolumeName = "LAr_sensitive",
                                             activeFieldName = "layer",
                                             activeVolumesNumber = 12,
                                             fieldNames = ["system"],
                                             fieldValues = [4])
    # cells with noise not filtered
    createEcalBarrelCellsNoise = CreateCaloCells("CreateECalBarrelCellsNoise",
                                   doCellCalibration=False,
                                   addCellNoise=True, filterCellNoise=False,
                                   OutputLevel=INFO,
                                   hits="ECalBarrelCellsStep2",
                                   noiseTool = noiseBarrel,
                                   geometryTool = barrelGeometry,
                                   cells=EcalBarrelCellsName)
    cell_creator_to_use = createEcalBarrelCellsNoise

# add position information to these cells
from Configurables import CellPositionsECalBarrelTool
cellPositionEcalBarrelTool = CellPositionsECalBarrelTool("CellPositionsECalBarrel", readoutName = ecalBarrelReadoutNamePhiEta, OutputLevel = INFO)

from Configurables import CreateCaloCellPositionsFCCee
createEcalBarrelPositionedCells = CreateCaloCellPositionsFCCee("ECalBarrelPositionedCells", OutputLevel = INFO)
createEcalBarrelPositionedCells.positionsECalBarrelTool = cellPositionEcalBarrelTool
createEcalBarrelPositionedCells.hits.Path = EcalBarrelCellsName
createEcalBarrelPositionedCells.positionedHits.Path = "ECalBarrelPositionedCells"

###################
# Create Clusters #
###################
# Empty cells for parts of calorimeter not used here
from Configurables import CreateEmptyCaloCellsCollection
createemptycells = CreateEmptyCaloCellsCollection("CreateEmptyCaloCells")
createemptycells.cells.Path = "emptyCaloCells"

# create towers (agregation of cells in the radial direction)
from Configurables import CaloTowerTool
towers = CaloTowerTool("towers",
                               deltaEtaTower = 0.01, deltaPhiTower = 2*_pi/768.,
                               radiusForPosition = 2160 + 40 / 2.0,
                               ecalBarrelReadoutName = ecalBarrelReadoutNamePhiEta,
                               ecalEndcapReadoutName = "",
                               ecalFwdReadoutName = "",
                               hcalBarrelReadoutName = "",
                               hcalExtBarrelReadoutName = "",
                               hcalEndcapReadoutName = "",
                               hcalFwdReadoutName = "",
                               OutputLevel = INFO)
towers.ecalBarrelCells.Path = EcalBarrelCellsName
towers.ecalEndcapCells.Path = "emptyCaloCells"
towers.ecalFwdCells.Path = "emptyCaloCells"
towers.hcalBarrelCells.Path = "emptyCaloCells"
towers.hcalExtBarrelCells.Path = "emptyCaloCells"
towers.hcalEndcapCells.Path = "emptyCaloCells"
towers.hcalFwdCells.Path = "emptyCaloCells"

# Cluster variables
windE = 9
windP = 17
posE = 5
posP = 11
dupE = 7
dupP = 13
finE = 9
finP = 17
# Minimal energy to create a cluster in GeV (FCC-ee detectors have to reconstruct low energy particles)
threshold = 1

from Configurables import CreateCaloClustersSlidingWindow
createClusters = CreateCaloClustersSlidingWindow("CreateClusters",
                                                 towerTool = towers,
                                                 nEtaWindow = windE, nPhiWindow = windP,
                                                 nEtaPosition = posE, nPhiPosition = posP,
                                                 nEtaDuplicates = dupE, nPhiDuplicates = dupP,
                                                 nEtaFinal = finE, nPhiFinal = finP,
                                                 energyThreshold = threshold,
                                                 energySharingCorrection = False,
                                                 attachCells = True,
                                                 OutputLevel = INFO
                                                 )
createClusters.clusters.Path = "CaloClusters"
createClusters.clusterCells.Path = "CaloClusterCells"

# add position to the cells attached to cluster
createEcalBarrelPositionedCaloClusterCells = CreateCaloCellPositionsFCCee("ECalBarrelPositionedCaloClusterCells", OutputLevel = INFO)
createEcalBarrelPositionedCaloClusterCells.positionsECalBarrelTool = cellPositionEcalBarrelTool
createEcalBarrelPositionedCaloClusterCells.hits.Path = "CaloClusterCells"
createEcalBarrelPositionedCaloClusterCells.positionedHits.Path = "PositionedCaloClusterCells"

# Create a new collection of cluster with dead material correction applied
#from Configurables import CorrectCaloClusters
#correctCaloClusters = CorrectCaloClusters("correctCaloClusters",
#                                          inClusters = createClusters.clusters.Path,
#                                          outClusters = "Corrected"+createClusters.clusters.Path,
#                                          numLayers = [12],
#                                          firstLayerIDs = [0],
#                                          lastLayerIDs = [11],
#                                          readoutNames = [ecalBarrelReadoutNamePhiEta],
#                                          upstreamParameters = [[0.09737335230414161, -10.387181371085651, -146.34314022178035, 1.8135025646800507, -1.3729969471683934, -0.6449866228721779]],
#                                          upstreamFormulas = [['[0]+[1]/(x-[2])', '[0]+[1]/(x-[2])']],
#                                          downstreamParameters = [[0.0005295508692700276, 0.005906234225977198, 1.0551521001079711, -1.88609690802949, -0.11356707602430005, 17.525300224679565]],
#                                          downstreamFormulas = [['[0]+[1]*x', '[0]+[1]/sqrt(x)', '[0]+[1]/x']],
#                                          OutputLevel = INFO
#                                          )

################ Output
from Configurables import PodioOutput
out = PodioOutput("out",
                  OutputLevel=INFO)
out.outputCommands = ["drop *", "keep genParticles", "keep ECalBarrelPositionedCells", "keep CaloClusters", "keep PositionedCaloClusterCells"]

import uuid
out.filename = "output_caloFullSim_"+str(momentum)+"GeV_pdgId_"+str(pdgCode)+"_noise"+str(addNoise)+".root"

#CPU information
from Configurables import AuditorSvc, ChronoAuditor
chra = ChronoAuditor()
audsvc = AuditorSvc()
audsvc.Auditors = [chra]
genalg_pgun.AuditExecute = True
hepmc_converter.AuditExecute = True
geantsim.AuditExecute = True
createEcalBarrelCellsStep1.AuditExecute = True
resegmentEcalBarrel.AuditExecute = True
createEcalBarrelCells.AuditExecute = True
createClusters.AuditExecute = True
out.AuditExecute = True

from Configurables import EventCounter
event_counter = EventCounter('event_counter')
event_counter.Frequency = 10

from Configurables import ApplicationMgr
ApplicationMgr(
    TopAlg = [event_counter,
              genalg_pgun,
              hepmc_converter,
              geantsim,
              createEcalBarrelCellsStep1,
              resegmentEcalBarrel,
              cell_creator_to_use,
              createEcalBarrelPositionedCells,
              createemptycells,
              createClusters,
              createEcalBarrelPositionedCaloClusterCells,
              out
              ],
    EvtSel = 'NONE',
    EvtMax   = 200,
    ExtSvc = [geoservice, podioevent, geantservice, audsvc],
    StopOnSignal = True,
 )
