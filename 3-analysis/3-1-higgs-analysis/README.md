# Getting Started: Higgs Analysis with FCCAnalyses

> Original authors: Michele Selvaggi, Benedikt Wach

## Physics goal and learning objectives

We will study Higgs production at a centre-of-mass energy of 240 GeV, targeting

$$
e^+e^- \to ZH \to \mu^+\mu^-b\bar b.
$$

The reconstructed muon pair identifies a Z candidate. We can look for the Higgs through the mass of the system recoiling against that candidate, or reconstruct its decay products as two jets. These observables use different parts of the event and provide complementary information.

Both parts use the same signal and background samples:

| Sample | Role |
|---|---|
| `wzp8_ee_mumuH_Hbb_ecm240` | Signal with a muon pair and a Higgs forced to decay to bottom quarks |
| `p8_ee_ZZ_mumubb_ecm240` | Background with the same muon-pair and bottom-quark final state |
| `p8_ee_WW_mumu_ecm240` | Background with muons and neutrinos from W decays |

**Part I** uses the muons to construct the recoil mass and fills histograms directly from reconstructed events. **Part II** extends the analysis with jets and flavour tagging, saving a reduced ntuple and then applying predefined cuts in a separate stage.

:::{admonition} Learning objectives
:class: objectives

By the end of this tutorial, you should be able to:

- retrieve physics objects from EDM4hep collections and relations;
- distinguish object selection, candidate reconstruction, and event selection;
- build an RDataFrame graph with C++ expressions and helper functions;
- produce histograms directly with `build_graph`;
- organise reconstruction, final selections, and plotting into separate stages;
- interpret recoil mass, dijet mass, flavour scores, and cut flows;
:::

## Prepare the environment and samples

Use an environment with FCCAnalyses and its dependencies available. On a supported system with the Key4hep CVMFS installation, start a fresh shell and run:

```bash
source /cvmfs/sw.hsf.org/key4hep/setup.sh
fccanalysis --help
```

Create a local working directory for the tutorial:

```bash
mkdir -p tutorial/inputs
cd tutorial
```

Run all commands below from this `tutorial` directory.

The input files use the following directory layout. Each directory name matches a sample identifier:

```text
inputs/
├── wzp8_ee_mumuH_Hbb_ecm240/
│   └── wzp8_ee_mumuH_Hbb_ecm240.edm4hep.root
├── p8_ee_ZZ_mumubb_ecm240/
│   └── p8_ee_ZZ_mumubb_ecm240.edm4hep.root
└── p8_ee_WW_mumu_ecm240/
    └── p8_ee_WW_mumu_ecm240.edm4hep.root
```

Download the required samples into this structure:

```bash
sample_base=https://fccsw.web.cern.ch/tutorials/gen-to-ana/bnl-cern-2026/delphes
for sample in wzp8_ee_mumuH_Hbb_ecm240 p8_ee_ZZ_mumubb_ecm240 p8_ee_WW_mumu_ecm240; do
    mkdir -p "inputs/$sample"
    wget -O "inputs/$sample/$sample.edm4hep.root" \
        "$sample_base/$sample/$sample.edm4hep.root"
done
```

Download the scripts for both parts and their supporting files into the same working directory. They are adapted from the [LiveSoftwareTutorials FCC-ee analysis](https://github.com/HEP-FCC/LiveSoftwareTutorials/tree/main/Analysis/ee), with fixed selections and a common normalisation.

```bash
script_base=https://raw.githubusercontent.com/HEP-FCC/fcc-tutorials/main/3-analysis/3-1-higgs-analysis
for file in histmaker_recoil.py plots_recoil.py treemaker_flavor.py selection_flavor.py plots_flavor.py functions.h; do
    wget -O "$file" "$script_base/$file"
done
```

Below a breakdown of their usage is shown:

| Part | Files | Output |
|---|---|---|
| I: direct histograms | [histmaker_recoil.py](https://raw.githubusercontent.com/HEP-FCC/fcc-tutorials/main/3-analysis/3-1-higgs-analysis/histmaker_recoil.py) | `outputs/recoil/` |
| I: plots | [plots_recoil.py](https://raw.githubusercontent.com/HEP-FCC/fcc-tutorials/main/3-analysis/3-1-higgs-analysis/plots_recoil.py) | `outputs/plots/recoil/` |
| II: reduced ntuple | [treemaker_flavor.py](https://raw.githubusercontent.com/HEP-FCC/fcc-tutorials/main/3-analysis/3-1-higgs-analysis/treemaker_flavor.py) | `outputs/flavor/stage1/` |
| II: selections and histograms | [selection_flavor.py](https://raw.githubusercontent.com/HEP-FCC/fcc-tutorials/main/3-analysis/3-1-higgs-analysis/selection_flavor.py) | `outputs/flavor/stage2/` |
| II: plots | [plots_flavor.py](https://raw.githubusercontent.com/HEP-FCC/fcc-tutorials/main/3-analysis/3-1-higgs-analysis/plots_flavor.py) | `outputs/plots/flavor/` |

The scripts use the accompanying [functions.h](https://raw.githubusercontent.com/HEP-FCC/fcc-tutorials/main/3-analysis/3-1-higgs-analysis/functions.h) for muon isolation and Z-candidate building.

## Part I — Recoil mass with a histmaker

Part I uses two commands.

```text
histmaker_recoil.py: EDM4hep → muon selection → Z candidate → recoil selection → histograms
plots_recoil.py:     histograms → plots
```

[histmaker_recoil.py](https://raw.githubusercontent.com/HEP-FCC/fcc-tutorials/main/3-analysis/3-1-higgs-analysis/histmaker_recoil.py) reconstructs the muons, applies every selection, and writes histograms to `outputs/recoil/`. [plots_recoil.py](https://raw.githubusercontent.com/HEP-FCC/fcc-tutorials/main/3-analysis/3-1-higgs-analysis/plots_recoil.py) then writes PDF plots to `outputs/plots/recoil/`, showing the dimuon mass, dimuon momentum, and recoil mass after all cuts.

The following sections explain the supplied reconstruction steps, cuts, and plotting settings.

### Read the script configuration

Open `histmaker_recoil.py`. The settings above `build_graph` tell FCCAnalyses which samples to read, where to write the results, and how to normalise them. The function below those settings describes what to do with each event.

The first settings, such as `MUON_MOMENTUM_MIN` and `Z_MASS_MIN`, are named selection thresholds. The graph uses them later when selecting muons and events.

#### Select the input samples with `processList`

The histmaker interface reads the top-level Python dictionary `processList`:

```python
processList = {
    "wzp8_ee_mumuH_Hbb_ecm240": {
        "fraction": 1.0,
        "crossSection": 0.00394,
        "kfactor": 1.0,
        "matchingEfficiency": 1.0
    },
    "p8_ee_ZZ_mumubb_ecm240": {
        "fraction": 1.0,
        "crossSection": 0.01404652064,
        "kfactor": 1.0,
        "matchingEfficiency": 1.0
    },
    "p8_ee_WW_mumu_ecm240": {
        "fraction": 1.0,
        "crossSection": 0.25792,
        "kfactor": 1.0,
        "matchingEfficiency": 1.0
    },
}
```

Each key is a process name identifying one simulated sample. Its nested dictionary contains settings for that sample:

- `fraction = 1.0` requests the full available sample.
- `crossSection` gives the effective cross section in pb, including the branching fractions for the generated final state.
- `kfactor` and `matchingEfficiency` are additional multiplicative normalisation factors. Both are `1.0` here, so they leave the cross section unchanged.

The spelling of each process name matters: FCCAnalyses uses it to locate the sample's input files. Listing a process does not download its events; the sample-download commands above create the required files.

Part I uses the histmaker names `processList`, `inputDir`, and `outputDir`. In Part II, the `Analysis` class uses `self.process_list`, `self.input_dir`, and `self.output_dir` for the corresponding stage-1 settings.

#### Locate the input files with `inputDir`

```python
inputDir = "inputs/"
```

`inputDir` is the common parent directory of the samples. With the directory layout used here, FCCAnalyses reads the ROOT files matching:

```text
<inputDir>/<process_name>/*.root
```

For the signal, this becomes:

```text
inputs/wzp8_ee_mumuH_Hbb_ecm240/*.root
```

Our downloaded file is therefore found at:

```text
inputs/wzp8_ee_mumuH_Hbb_ecm240/wzp8_ee_mumuH_Hbb_ecm240.edm4hep.root
```

The subdirectory must match the `processList` key; the files inside it can have any name ending in `.root`. A directory can contain several ROOT files belonging to the same sample.

The relative path `inputs/` is resolved from the directory where you execute the command. That is why all tutorial commands run from the `tutorial` working directory.

#### Choose the output location with `outputDir`

```python
outputDir = "outputs/recoil/"
```

The histmaker creates this directory and writes one histogram ROOT file per process. For example, the signal output is:

```text
outputs/recoil/wzp8_ee_mumuH_Hbb_ecm240.root
```

These files contain the histograms produced by the analysis. `plots_recoil.py` reads them to create the figures; Part I does not write an intermediate event ntuple.

#### Load the additional C++ functions

```python
includePaths = ["functions.h"]
```

FCCAnalyses loads this header into ROOT so the graph can call its C++ helpers, including muon isolation and Z-candidate construction. Relative header paths are resolved against the analysis script's directory, so the downloaded `functions.h` belongs beside `histmaker_recoil.py`.

#### Set processing and normalisation options

```python
procDict = "FCCee_procDict_winter2023_IDEA.json"
nCPUS = -1
doScale = True
intLumi = 10.6e6  # pb^-1 = 10.6 ab^-1
```

`procDict` names the standard sample-metadata dictionary found through the FCCAnalyses environment. The values supplied in `processList` override its normalisation metadata for our three samples.
`nCPUS = -1` allows ROOT to use the available CPU threads. `doScale = True` scales the histograms to the expected yields at `intLumi`.

### How the histmaker works

The `build_graph(df, dataset)` function in `histmaker_recoil.py` defines the muon reconstruction, applies the cuts, and books the histograms in one RDataFrame graph. It returns the histogram handles in `results` and the sum of input event weights in `weightsum`. This tutorial uses unit event weights.

`df` is the ROOT dataframe containing the events for one sample; its columns provide the particle collections and other event data. FCCAnalyses calls `build_graph` for each configured sample, passing its name as `dataset`. The function uses `Define` to add calculated columns and `Filter` to select events. Finally, `results.append(df.Histo1D(...))` books each histogram directly on the dataframe after all cuts.

### Muon reconstruction and selection

Muon identification is represented through indices into the reconstructed-particle collection. The script gives the relation column saved in the edm4hep file a more convenient name and subsequently retrieves the corresponding objects explicitly as a new column called `muons_all`:

```python
df = df.Alias("Muon0", "Muon_objIdx.index")
df = df.Define(
    "muons_all",
    "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)",
)
df = df.Define(
    "muons",
    f"FCCAnalyses::ReconstructedParticle::sel_p({MUON_MOMENTUM_MIN})(muons_all)",
)
```

The alias does not copy the data. `get` retrieves muon candidates, and `sel_p(20)` keeps those with total momentum above 20 GeV. This is an **object selection**: it changes a collection within each event. It does not yet remove any events.

Prompt muons from Z decay are often isolated from other particles. The helper `coneIsolation(0.01, 0.5)` sums particle momenta in an annulus around each muon and divides the sum by that muon's momentum. A smaller value indicates less surrounding activity. `sel_iso(0.25)` selects muons with a relative isolation below 0.25.

The loose event selection requires at least one isolated muon and at least one opposite-sign pair among the momentum-selected muons.

### Z-candidate reconstruction

An event can contain more than one opposite-sign pair. The helper `resonanceBuilder_mass_recoil(91.2, 125, 0.4, 240, false)` ranks pairs using their compatibility with the Z mass and a Higgs recoil mass. Its score combines

$$
0.6\,(m_{\mu\mu}-91.2\,\mathrm{GeV})^2
+0.4\,(m_{\mathrm{recoil}}-125\,\mathrm{GeV})^2.
$$

The pair with the smallest score is retained. The arguments specify the target masses, the relative weight of the recoil term, the collision energy, and the use of reconstructed kinematics. The full call also passes the particle and relation collections required by the helper.

The returned collection contains the composite Z candidate followed by the two muons used to build it. Selecting a pair in this way is distinct from imposing a mass window or performing a kinematic fit.

FCCAnalyses property functions act on collections and often return vectors. For a one-element Z collection, `[0]` extracts the scalar observable:

```python
df = df.Define("zmumu", "Vec_rp{zbuilder_result[0]}")
df = df.Define("m_zmumu", "FCCAnalyses::ReconstructedParticle::get_mass(zmumu)[0]")
df = df.Define("p_zmumu", "FCCAnalyses::ReconstructedParticle::get_p(zmumu)[0]")
```

### Understand the recoil mass

In the centre-of-mass frame, using the nominal collision energy and neglecting radiation, the initial four-momentum is

$$
p_{e^+e^-}=(\sqrt{s},0,0,0).
$$

Subtracting the reconstructed dimuon four-momentum gives the recoiling system:

$$
p_{\mathrm{recoil}}=p_{e^+e^-}-p_{\mu\mu},\qquad
m_{\mathrm{recoil}}^2=s+m_{\mu\mu}^2-2\sqrt{s}\,E_{\mu\mu}.
$$

For a correctly reconstructed ZH event, the recoil mass should peak near the Higgs mass. Detector resolution, initial-state radiation, and beam-energy effects broaden or distort that peak.

```python
df = df.Define(
    "recoil_zmumu", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zmumu)"
)
df = df.Define(
    "m_recoil_zmumu", "FCCAnalyses::ReconstructedParticle::get_mass(recoil_zmumu)[0]"
)
```

The observable uses only the reconstructed Z and the assumed initial state; it does not require identifying the Higgs decay products. Our tutorial sample nevertheless contains only Higgs decays to bottom quarks. Its predicted yield therefore describes that final state, not an inclusive Higgs sample.

### Selections and histogram booking

The histmaker applies the following requirements in order:

| Requirement | Purpose |
|---|---|
| At least one isolated muon and an opposite-sign muon pair | Select events containing a plausible leptonic Z decay |
| $86 < m_{\mu\mu} < 96$ GeV | Retain candidates near the Z mass |
| $20 < p_{\mu\mu} < 70$ GeV | Select the momentum region expected for ZH production at 240 GeV |
| $120 < m_{\mathrm{recoil}} < 140$ GeV | Select a region around the Higgs recoil peak |

The script fills three histograms after all cuts: `m_zmumu`, `p_zmumu`, and `m_recoil_zmumu`.

### Sample normalisation

Raw simulated event counts depend on how many events were generated for each process. For these unweighted samples, the expected selected yield is

$$
N_{\mathrm{expected}}=
\frac{N_{\mathrm{selected}}}{N_{\mathrm{generated}}}
\,\sigma_{\mathrm{eff}}\,\mathcal{L}.
$$

Here $\sigma_{\mathrm{eff}}$ is the cross section for the generated final state and $\mathcal{L}$ is the integrated luminosity. We use the benchmark of $10.6\,\mathrm{ab}^{-1}$. This rescales the predicted yield; it does not increase the number of simulated events or reduce their relative statistical fluctuations.

The histmaker already scales its output to 10.6 ab⁻¹. `plots_recoil.py` uses a scale factor of one and the matching luminosity label, preserving that normalisation.

### Run Part I

From the `tutorial` working directory, run the two supplied scripts in order:

```bash
fccanalysis run histmaker_recoil.py
fccanalysis plots plots_recoil.py
```

### Inspect the plots

Open the PDF files in `outputs/plots/recoil/`. Look for the Z peak near 91 GeV in `m_zmumu` and the Higgs recoil peak near 125 GeV in `m_recoil_zmumu`. Compare the signal and background contributions in these plots and in `p_zmumu`.

## Part II — Jets and flavour tagging in a staged analysis

We now extend the same analysis to reconstruct the Higgs decay products. Jet clustering and especially flavour-tagging inference add work that we do not want to repeat every time we adjust a cut. We therefore save a reduced ntuple after a loose pre-selection:

```text
Stage 1: EDM4hep → muons and Z candidate → jets and tagging → reduced ntuple
Stage 2: reduced ntuple → cumulative selections → histograms
Stage 3: histograms → final plots
```

The signal and backgrounds remain the same as in Part I. Reconstruction of the muons and the recoil observable follows the explanations above. The new ingredients are the jets, their flavour scores, and the separation of reconstruction from final selection.

### Stage 1: reconstruct candidates and save observables

#### The Analysis class interface
[treemaker_flavor.py](https://raw.githubusercontent.com/HEP-FCC/fcc-tutorials/main/3-analysis/) creates an FCCAnalyses `Analysis` object and uses its three methods:

| Method | Role |
|---|---|
| `__init__(self, _)` | Set input samples, directories, model paths, and helper objects. |
| `analyzers(self, df)` | Add reconstructed quantities and loose selections to the event dataframe, then return that dataframe. |
| `output(self)` | Return the names of the columns to save in the reduced ntuple. |

Unlike Part I's `build_graph()`, `analyzers()` returns a dataframe rather than histogram handles. FCCAnalyses writes its selected events to a ROOT tree using the columns named by `output()`.

The constructor uses `self.process_list`, `self.input_dir`, `self.output_dir`, and `self.include_paths` for the settings introduced in Part I. It reuses the same samples, input directory, and C++ header. The new output directory stores the reduced ntuples:

```python
self.input_dir = "./inputs/"
self.output_dir = "./outputs/flavor/stage1/"
```

Luminosity scaling is deferred to stage 2, where the cross sections will enter.

#### Identify and retrieve the flavour-tagging model

The two imported FCCAnalyses helpers handle clustering and neural-network inference:

```python
from addons.FastJet.jetClusteringHelper import ExclusiveJetClusteringHelper
from addons.ONNXRuntime.jetFlavourHelper import JetFlavourHelper
```

`ExclusiveJetClusteringHelper` builds jets from reconstructed particles. `JetFlavourHelper` calculates the inputs needed by a trained flavour classifier and evaluates that classifier with ONNX Runtime. Here, *inference* means applying an already trained network to our jets.

Two matching files describe the network:

- The `.json` file specifies input features, their preprocessing, and output score names.
- The `.onnx` file stores the trained network and its parameters.

The script identifies both files with the same model name and provides an EOS filesystem location and a fallback HTTP location. The returned values are filenames that the inference helper can open. This happens during construction of the analysis object, before event processing.

#### Connect the model to event collections

The helpers need to know which EDM4hep collections provide the required particles, tracks, and detector information. The constructor supplies this mapping:

```python
collections = {
    "GenParticles": "Particle",
    "PFParticles": "ReconstructedParticlesNoMuons",
    "PFTracks": "EFlowTrack",
    "PFPhotons": "EFlowPhoton",
    "PFNeutralHadrons": "EFlowNeutralHadron",
    "TrackState": "_EFlowTrack_trackStates",
    "TrackerHits": "TrackerHits",
    "CalorimeterHits": "CalorimeterHits",
    "dNdx": "EFlowTrack_dNdx",
    "PathLength": "EFlowTrack_L",
    "Bz": "magFieldBz",
}
```

The dictionary keys are names understood by the helpers; the values are collection or column names in the dataframe. In particular, `PFParticles` points to `ReconstructedParticlesNoMuons`. That column is created later in `analyzers()` and contains the particles available for jet clustering after muon removal.

The constructor then configures both helpers:

```python
self.jet_clustering_helper = ExclusiveJetClusteringHelper(
    collections["PFParticles"], 2
)
self.jet_flavour_helper = JetFlavourHelper(
    collections,
    self.jet_clustering_helper.jets,
    self.jet_clustering_helper.constituents,
)
with open(self.weaver_preproc, encoding="utf-8") as preproc_file:
    self.jet_flavour_helper.scores = json.load(preproc_file)["output_names"]
```

The arguments to `ExclusiveJetClusteringHelper` specify the particle collection and the requested number of jets: two. Its `.jets` and `.constituents` attributes identify the columns that clustering will produce. Passing them to `JetFlavourHelper` ensures the tagger uses those same jets and their constituent particles. Reading `output_names` from the preprocessing JSON gives the flavour helper the score names produced by this model.

Creating these Python helper objects only configures the analysis; their `define()` methods add the actual calculations to the dataframe later.

#### Build the event graph and cluster two jets

`analyzers()` begins with the same relation aliases, momentum-selected muons, isolation calculation, and opposite-sign-pair requirement introduced in Part I. It leaves the final mass windows and flavour-score cut to stage 2.

The selected muons are removed from the particles used for clustering:

```python
df = df.Define(
    "ReconstructedParticlesNoMuons",
"FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, muons)",)
```

This prevents those muons from also contributing to the jets.

The graph then clusters and tags the remaining particles:

```python
df = df.Filter("ReconstructedParticlesNoMuons.size() >= 2")
df = self.jet_clustering_helper.define(df)
df = df.Filter("event_njet == 2")
df = self.jet_flavour_helper.define(df)
df = self.jet_flavour_helper.inference(self.weaver_preproc, self.weaver_model, df)
```

The first filter requires at least two particles for clustering. The clustering helper adds jet four-momenta, constituent assignments, and `event_njet`. The next filter requires two jets before the tagger uses them. Asking for two jets encodes our $H \to qq$ hypothesis; background events are clustered in exactly the same way.

`jet_flavour_helper.define(df)` constructs the track and constituent features. `inference(...)` uses the JSON preprocessing configuration and ONNX network to add per-jet flavour scores, including `recojet_isB` and `recojet_isC`.

#### Calculate the saved observables

The Z-candidate builder and the definitions of `m_zmumu`, `p_zmumu`, and `m_recoil_zmumu` follow Part I. The new event discriminant adds the two bottom-tagging scores:

```python
df = df.Define("scoresum_B", "recojet_isB[0] + recojet_isB[1]")
```

Each score measures how strongly a jet resembles a bottom jet according to the classifier.

The jet four-momenta give the dijet invariant mass:

```python
df = df.Define(
    "p4_jets",
    "JetConstituentsUtils::compute_tlv_jets("
    f"{self.jet_clustering_helper.jets})",)

df = df.Define("m_jj", "JetConstituentsUtils::InvariantMass(p4_jets[0], p4_jets[1])")
```

`compute_tlv_jets` converts the reconstructed jets to four-vectors, and `InvariantMass` calculates the mass of their sum. For signal, `m_jj` should peak near the Higgs mass. It uses the Higgs decay products directly, while `m_recoil_zmumu` uses the reconstructed Z and the known initial state.

#### Choose which columns are written

The supplied `output()` method is:

```python
def output(self):
    """Columns persisted in the stage-1 output ROOT file."""
    branch_list = [
        "m_zmumu",
        "p_zmumu",
        "m_recoil_zmumu",
        "m_jj",
        "scoresum_B",
    ]
    # Add the output branches from the jet flavour helper.
    branch_list += self.jet_flavour_helper.outputBranches()
    return branch_list
```
Stage 2 can only use columns written here. With FCCAnalyses v0.13.1, the output files are grouped in a directory for each sample. For the default single chunk, for example:

```text
outputs/flavor/stage1/wzp8_ee_mumuH_Hbb_ecm240/wzp8_ee_mumuH_Hbb_ecm240-chunk-0.root
```

FCCAnalyses also writes the processed-event metadata needed to preserve the loose-selection efficiency when normalising later. The final step discovers the ROOT files inside each sample directory; its `inputDir` remains `outputs/flavor/stage1/`.

### Stage 2: apply selections and fill histograms

Open [selection_flavor.py](https://raw.githubusercontent.com/HEP-FCC/fcc-tutorials/main/3-analysis/3-1-higgs-analysis/selection_flavor.py). `fccanalysis final` reads its configuration to select events from the saved ntuples and fill histograms. It reuses the reconstructed quantities, so it does not rerun clustering or the network.

#### Apply the supplied cumulative cuts

The script defines cut thresholds at the top, as in Part I. It uses the same dimuon and recoil windows, then adds `BTAG_SUM_MIN = 1.0`.

The first three `cutList` entries illustrate how the selections are written, if we want to impose selection requirements in multiple steps:

```python
cutList = {
    "sel0_baseline": "true",
    "sel1_zmass": (
        f"m_zmumu > {Z_MASS_MIN} && m_zmumu < {Z_MASS_MAX}"
    ),
    "sel2_zmomentum": (
        f"m_zmumu > {Z_MASS_MIN} && m_zmumu < {Z_MASS_MAX}"
        f" && p_zmumu > {Z_MOMENTUM_MIN}"
        f" && p_zmumu < {Z_MOMENTUM_MAX}"
    ),
    # ...
}
```

The keys label the selection stages. The values are C++ boolean expressions evaluated on each ntuple entry. Python f-strings insert the numerical constants into those expressions, and `&&` means that both requirements must hold. `"true"` accepts every event in the stage-1 ntuple.

FCCAnalyses evaluates each entry independently on that ntuple. Consequently, `sel2_zmomentum` repeats the Z-mass cut before adding the momentum cut. The remaining entries repeat the earlier cuts and add the recoil window and then `scoresum_B > 1.0`. This produces a cumulative cut flow:

| Selection | Additional requirement |
|---|---|
| `sel0_baseline` | All events saved by stage 1 |
| `sel1_zmass` | 86 < dimuon mass < 96 GeV |
| `sel2_zmomentum` | 20 < dimuon momentum < 70 GeV |
| `sel3_recoil` | 120 < recoil mass < 140 GeV |
| `sel4_btag` | `scoresum_B > 1.0` |

#### Preserve the stage-1 efficiency when normalising

FCCAnalyses uses the processed-event metadata saved by stage 1 as the normalisation denominator. Using only the surviving ntuple entries would discard the loose-selection efficiency. `doScale = True` enables the scaling.

With `saveJSON = True`, `fccanalysis final` also writes `outputs/flavor/stage2/results.json`. This file contains the numerical cut flow for each sample, so you can compare the event yields after successive selections.

#### Specify the histograms with `histoList`

FCCAnalyses fills every `histoList` entry for every `cutList` selection and every process. Thus the five observables are available both at baseline and after each additional cut. Histogram files are written to `outputs/flavor/stage2/`, with names such as:

```text
wzp8_ee_mumuH_Hbb_ecm240_sel4_btag_histo.root
```

### Stage 3: produce the plots

[plots_flavor.py](https://raw.githubusercontent.com/HEP-FCC/fcc-tutorials/main/3-analysis/3-1-higgs-analysis/plots_flavor.py) connects the histogram outputs to the plotting command:

```python
inputDir = "outputs/flavor/stage2/"
outdir = "outputs/plots/flavor/"
formats = ["pdf"]

variables = [
    "m_zmumu", "p_zmumu", "m_recoil_zmumu", "m_jj", "scoresum_B",
]
```

`variables` lists histogram keys from `histoList`. The `selections` dictionary lists the matching `cutList` keys, and `plots` groups the sample names into signal and backgrounds.

The result is a PDF for each observable and selection, showing how the expected signal and background distributions change as the cuts accumulate.
Note: FCCAnalyses uses different plotting configuration conventions for the histmaker and staged workflows. This explains the structural differences between the plotting scripts in Parts I and II, even though both read ROOT histograms.

### Run Part II

From the same `tutorial` working directory, run these three commands in order:

```bash
fccanalysis run treemaker_flavor.py
fccanalysis final selection_flavor.py
fccanalysis plots plots_flavor.py
```

## Understand the completed results

After running both workflows, open the plots in `outputs/plots/flavor/`. Follow the distributions from the baseline to the final selection. Look for the Z peak in `m_zmumu` and Higgs-compatible structures in `m_recoil_zmumu` and `m_jj`. Open `outputs/flavor/stage2/results.json` for the numerical cut flow. Use these yields to identify which requirements reject each background and how much signal is lost. The statistical fluctuations reflect the available simulated events even when the histograms are scaled to a much larger expected dataset.

## Further exercises

The supplied workflow is complete. The exercises below explore changes to it. A final-cut change requires rerunning `selection_flavor.py` and `plots_flavor.py`; a change to reconstruction or saved columns also requires rerunning `treemaker_flavor.py`.

:::{admonition} Optional exercise: explain the Z-momentum selection
:class: challenge

For $e^+e^-\to AB$, the outgoing momentum in the centre-of-mass frame is

$$
p=\frac{\sqrt{[s-(m_A+m_B)^2][s-(m_A-m_B)^2]}}{2\sqrt{s}}.
$$

Calculate the Z momentum for ZH and ZZ production at 240 GeV. Use your results to explain the different peaks and the momentum window. Then change one selection boundary and inspect how the signal and background yields respond.
:::


:::{admonition} Optional exercise: explore detector performance
:class: challenge

As an extension, investigate how changes to neutral-hadron momentum resolution affect the dijet mass. Such a change belongs in the reconstruction stage and requires rebuilding the ntuple. The FCCAnalyses [jet-smearing example](https://github.com/HEP-FCC/FCCAnalyses/blob/master/examples/FCCee/smearing/smear_jets.py) provides a starting point.
:::

## Beyond this tutorial

This exercise takes reconstructed events through candidate building, selection, normalisation, and plotting. It demonstrates a subset of the backgrounds and does not constitute a complete Higgs measurement. A full analysis would validate the modelling, include all relevant processes, estimate systematic uncertainties and their correlations, and construct a statistical model. That model could then be used to extract a cross section, signal strength, or Higgs mass.
