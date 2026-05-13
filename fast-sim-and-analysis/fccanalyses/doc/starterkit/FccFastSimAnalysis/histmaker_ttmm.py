
# list of processes (mandatory)
processList = {
    'p8_tautau_ecm91':    {'fraction':1},
    'wz_tautau_ecm91':    {'fraction':1},
    'kk_tautau_ecm91':    {'fraction':1},
}
# Link to the dictonary that contains all the cross section informations etc...
# Mandatory but anyone is good for local files
procDict = "FCCee_procDict_winter2023_IDEA.json"

# Define the input dir (optional)
inputDir    = "gen/"

#Optional: output directory, default is local running directory
outputDir   = "outputs"

# optional: ncpus, default is 4, -1 uses all cores available
nCPUS       = -1

# scale the histograms with the cross-section and integrated luminosity
doScale = False
# doScale = True
# intLumi = 1000000 # 1 /ab

# define some binning for various histograms
bins_p_l = (100, 0, 50) # 0.5 GeV bins
bins_cosTheta = (50, -1, 1)
bins_acol = (50, -1, -.9)

# build_graph function that contains the analysis logic, cuts and histograms (mandatory)
def build_graph(df, dataset):
    import ROOT
    ROOT.gInterpreter.Declare("""

       #ifndef funDone
       #define funDone
    
       float cosTheta(const edm4hep::Vector3d& in){
          return (in.z/sqrt(pow(in.x,2)+pow(in.y,2)+pow(in.z,2)));
       };
    
       float scalarProductNorm(const edm4hep::Vector3d& in1, const edm4hep::Vector3d& in2 ){
          return ((in1.x*in2.x + in1.y*in2.y + in1.z*in2.z)/sqrt(pow(in1.x,2)+pow(in1.y,2)+pow(in1.z,2))/sqrt(pow(in2.x,2)+pow(in2.y,2)+pow(in2.z,2) ));
       };

       float momP(const edm4hep::Vector3d& in ){
          return (sqrt(pow(in.x,2)+pow(in.y,2)+pow(in.z,2)));
       };

       #endif
    """)

    results = []
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")

    # Connect to taus
    df = df.Define("tauplusvec", ROOT.MCParticle.sel_pdgID(-15, 0),["MCParticles"])
    df = df.Define("tauminusvec", ROOT.MCParticle.sel_pdgID(15, 0),["MCParticles"])
    df = df.Define("tauplus", "tauplusvec[0]")
    df = df.Define("tauminus", "tauminusvec[0]")
 
    # Connect to muons
    df = df.Define("muplusvec", ROOT.MCParticle.sel_pdgID(-13, 0),["MCParticles"])
    df = df.Define("muminusvec", ROOT.MCParticle.sel_pdgID(13, 0),["MCParticles"])
    df = df.Define("muplus", "muplusvec[0]")
    df = df.Define("muminus", "muminusvec[0]")

    # CosThetas
    df = df.Define("cthetaup", "cosTheta(tauplusvec[0].momentum)")
    df = df.Define("cthetaum", "cosTheta(tauminusvec[0].momentum)")
    df = df.Define("cthemup", "cosTheta(muplusvec[0].momentum)")
    df = df.Define("cthemun", "cosTheta(muminusvec[0].momentum)")

    # Acollinearities
    df = df.Define("acoltau", "scalarProductNorm(tauminusvec[0].momentum, tauplusvec[0].momentum)")
    df = df.Define("acolmu", "scalarProductNorm(muminusvec[0].momentum, muplusvec[0].momentum)")

    # Muon momenta
    df = df.Define("muplus_p", "momP(muplusvec[0].momentum)")
    df = df.Define("muminus_p", "momP(muminusvec[0].momentum)")
        
    # baseline histograms, before any selection cuts (store with _cut0)
    results.append(df.Histo1D(("P_mup", "", *bins_p_l), "muplus_p"))
    results.append(df.Histo1D(("P_mum", "", *bins_p_l), "muminus_p"))
    results.append(df.Histo1D(("CosTheta_taup", "", *bins_cosTheta), "cthetaup"))
    results.append(df.Histo1D(("CosTheta_mup", "", *bins_cosTheta), "cthemup"))
    results.append(df.Histo1D(("AcolTau", "", *bins_acol), "acoltau"))
    results.append(df.Histo1D(("AcolMu", "", *bins_acol), "acolmu"))

    return results, weightsum

