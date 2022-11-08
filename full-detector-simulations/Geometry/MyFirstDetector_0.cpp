#include "DD4hep/DetFactoryHelper.h"
#include "XML/Layering.h"
#include "XML/Utilities.h"
#include "DDRec/DetectorData.h"
static dd4hep::Ref_t create_detector(
dd4hep::Detector& theDetector,
xml_h entities,
dd4hep::SensitiveDetector sens) {
// XML Detector Element (confusingly also XML::DetElement)
xml_det_t x_det = entities;
// DetElement of our detector instance, attach additional information, sub-elements...
// uses name of detector and ID number as defined in the XML detector tag
std::string detName = x_det.nameStr();
sens.setType("calorimeter");
dd4hep::DetElement sdet (detName, x_det.id());
//get the dimensions tag
xml_dim_t dim = x_det.dimensions();
//read its attributes
double rmin = dim.rmin();
double rmax = dim.rmax();
double zmax = dim.zmax();
//Make a Cylinder
dd4hep::Tube envelope(rmin, rmax, zmax);
dd4hep::Material air = theDetector.air();
dd4hep::Volume envelopeVol(detName+"_envelope",
envelope,
air);
dd4hep::PlacedVolume physvol =
theDetector.pickMotherVolume(sdet).placeVolume(envelopeVol);
// add system ID and identify as barrel (as opposed to endcap +/-1)
physvol.addPhysVolID("system", sdet.id()).addPhysVolID(_U(side),0);
sdet.setPlacement(physvol);
return sdet;
}
DECLARE_DETELEMENT(MyFirstDetector,create_detector)