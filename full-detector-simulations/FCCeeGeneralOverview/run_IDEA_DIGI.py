import os

from Gaudi.Configuration import INFO, DEBUG

# input
from Configurables import k4DataSvc, PodioInput
evtsvc = k4DataSvc('EventDataSvc')
evtsvc.input = "electron_gun_10GeV_IDEA_SIM.root"

# Detector geometry (needed for the digitizer because we need to go in local coordinates)
from Configurables import GeoSvc
geoservice = GeoSvc("GeoSvc")
path_to_detector = os.environ.get("K4GEO", "")
print(path_to_detector)
detectors_to_use=[
                    'FCCee/IDEA/compact/IDEA_o1_v02/IDEA_o1_v02.xml'
                  ]
# prefix all xmls with path_to_detector
geoservice.detectors = [os.path.join(path_to_detector, _det) for _det in detectors_to_use]
geoservice.OutputLevel = INFO

# Digitize drift chamber sim hits
from Configurables import DCHsimpleDigitizerExtendedEdm
dch_digitizer = DCHsimpleDigitizerExtendedEdm("DCHsimpleDigitizerExtendedEdm",
    inputSimHits = "",
    outputDigiHits = savetrackertool.SimTrackHits.Path.replace("sim", "digi"),
    outputSimDigiAssociation = "DC_simDigiAssociation",
    readoutName = "CDCHHits",
    xyResolution = 0.1, # mm
    zResolution = 1, # mm
    debugMode = False,
    OutputLevel = INFO
)


# Output
from Configurables import PodioOutput
out = PodioOutput("out",
                  OutputLevel=INFO)
out.outputCommands = ["keep *"]
out.filename = "output_simplifiedDriftChamber_MagneticField_"+str(magneticField)+"_pMin_"+str(momentum*1000)+"_MeV"+"_ThetaMinMax_"+str(thetaMin)+"_"+str(thetaMax)+"_pdgId_"+str(pdgCode)+"_stepLength_default.root"

#CPU information
from Configurables import AuditorSvc, ChronoAuditor
chra = ChronoAuditor()
audsvc = AuditorSvc()
audsvc.Auditors = [chra]
genAlg.AuditExecute = True
hepmc_converter.AuditExecute = True
out.AuditExecute = True

from Configurables import EventCounter
event_counter = EventCounter('event_counter')
event_counter.Frequency = 1

from Configurables import ApplicationMgr
ApplicationMgr(
    TopAlg = [
              event_counter,
              dch_digitizer,
              out
              ],
    EvtSel = 'NONE',
    EvtMax   = 100,
    ExtSvc = [geoservice, podioevent, , audsvc],
    StopOnSignal = True,
 )
