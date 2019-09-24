
import os
from Gaudi.Configuration import *
from Configurables import GeoSvc
geoservice = GeoSvc("GeoSvc")
geoservice.detectors=[
	os.path.join(os.environ.get("FCC_DETECTORS", ""), 'Detector/DetFCCeeIDEA/compact/FCCee_DectEmptyMaster.xml'),
  os.path.join(os.environ.get("FCC_DETECTORS", ""), 'Detector/DetFCCeeIDEA/compact/FCCee_DectMaster.xml'),
                                         ]

from Configurables import SimG4Svc
geantservice = SimG4Svc("SimG4Svc")

from Configurables import GeoToGdmlDumpSvc
geodumpservice = GeoToGdmlDumpSvc("GeoDump") 
geodumpservice.gdml="FCCee_IDEA.gdml"

from Configurables import ApplicationMgr
ApplicationMgr( TopAlg = [], 
                EvtSel = 'NONE',
                EvtMax   = 1,
                # order is important, as GeoSvc is needed by SimG4Svc
                ExtSvc = [geoservice, geantservice, geodumpservice],
                OutputLevel=DEBUG
 )