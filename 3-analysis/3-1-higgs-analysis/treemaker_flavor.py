# Adapted from https://github.com/HEP-FCC/LiveSoftwareTutorials/blob/main/Analysis/ee/solutions/01_basic_selection.py
""" Stage-1 analysis: ee->Z(->mu+mu-)H(->bb) """

import json
import os
from pathlib import Path
import urllib.request

from addons.FastJet.jetClusteringHelper import ExclusiveJetClusteringHelper
from addons.ONNXRuntime.jetFlavourHelper import JetFlavourHelper

# Model files for the flavour tagging inference.
MODEL_NAME = "fccee_flavtagging_edm4hep_wc_v1"
MODEL_URL_DIR = (
    "https://fccsw.web.cern.ch/fccsw/testsamples/jet_flavour_tagging/"
    "winter2023/wc_pt_13_01_2022"
)
MODEL_EOS_DIR = (
    "/eos/experiment/fcc/ee/jet_flavour_tagging/winter2023/"
    "wc_pt_13_01_2022"
)

# Small helper function to download the model files if they are not already present.
def get_file_path(url, filename):
    """Use a local model when available; otherwise download the test model."""
    if os.path.exists(filename):
        return os.path.abspath(filename)
    local_path = Path("models") / os.path.basename(url)
    local_path.parent.mkdir(exist_ok=True)
    if not local_path.is_file():
        temporary_path = local_path.with_suffix(local_path.suffix + ".part")
        urllib.request.urlretrieve(url, temporary_path)
        temporary_path.replace(local_path)
    return str(local_path.resolve())


class Analysis:
    """Select ee->Z(->mu+mu-)H(->bb) candidates and run flavour tagging on two jets."""

    def __init__(self, _):

        self.process_list = {
            "wzp8_ee_mumuH_Hbb_ecm240": {
                "fraction": 1.0,
            },
            "p8_ee_ZZ_mumubb_ecm240": {
                "fraction": 1.0,
            },
            "p8_ee_WW_mumu_ecm240": {
                "fraction": 1.0,
            },
        }

        # The input and output directories are relative to the current working directory.
        self.input_dir = "./inputs/"
        self.output_dir = "./outputs/flavor/stage1/"
        # The include paths are needed for the C++ helper functions used in the analysis.
        self.include_paths = [str(Path(__file__).with_name("functions.h"))]

        # Download the pre-processing and model files for the jet-flavour inference.
        preproc_url = f"{MODEL_URL_DIR}/{MODEL_NAME}.json"
        model_url = f"{MODEL_URL_DIR}/{MODEL_NAME}.onnx"
        self.weaver_preproc = get_file_path(
            preproc_url, f"{MODEL_EOS_DIR}/{MODEL_NAME}.json"
        )
        self.weaver_model = get_file_path(
            model_url, f"{MODEL_EOS_DIR}/{MODEL_NAME}.onnx"
        )

        # Dictionary mapping the EDM4hep collection names to the names used by the flavour tagger and jet clustering helpers.
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


    def analyzers(self, df):
        """Define the Z(mu+mu-)H(bb) reconstruction graph."""
        df = df.Alias("Particle0", "_Particle_daughters.index")
        df = df.Alias("Particle1", "_Particle_parents.index")
        df = df.Alias("RecoMCLink0", "_RecoMCLink_from.index")
        df = df.Alias("RecoMCLink1", "_RecoMCLink_to.index")
        df = df.Alias("Muon0", "Muon_objIdx.index")
        df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)",)

        df = df.Define(
            "muons",
            "FCCAnalyses::ReconstructedParticle::sel_p(20)(muons_all)",
        )
        df = df.Define("q_muons", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
        df = df.Define("no_muons", "FCCAnalyses::ReconstructedParticle::get_n(muons)")

        df = df.Define(
            "iso_muons",
            "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(muons, ReconstructedParticles)",)
        df = df.Define(
            "muons_sel_iso",
            "FCCAnalyses::ZHfunctions::sel_iso(0.25)(muons, iso_muons)",)
        # At least one isolated muon and an opposite-sign muon pair.
        df = df.Filter("muons_sel_iso.size() > 0")
        df = df.Filter("no_muons >= 2 && abs(Sum(q_muons)) < q_muons.size()")

        # Remove the selected muons from the list of reconstructed particles to avoid double-counting them in the jet clustering.
        df = df.Define(
            "ReconstructedParticlesNoMuons",
            "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, muons)",)

        # Run the jet clustering and flavour tagging inference.
        df = df.Filter("ReconstructedParticlesNoMuons.size() >= 2")
        df = self.jet_clustering_helper.define(df)
        df = df.Filter("event_njet == 2")
        df = self.jet_flavour_helper.define(df)
        df = self.jet_flavour_helper.inference(self.weaver_preproc, self.weaver_model, df)

        df = df.Define(
            "zbuilder_result",
            "FCCAnalyses::ZHfunctions::resonanceBuilder_mass_recoil("
            "91.2, 125, 0.4, 240, false)(muons, RecoMCLink0, RecoMCLink1, "
            "ReconstructedParticles, Particle, Particle0, Particle1)",)

        df = df.Define("zmumu", "Vec_rp{zbuilder_result[0]}")

        df = df.Define("m_zmumu", "FCCAnalyses::ReconstructedParticle::get_mass(zmumu)[0]")
        df = df.Define("p_zmumu", "FCCAnalyses::ReconstructedParticle::get_p(zmumu)[0]")
        df = df.Define("recoil_zmumu", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zmumu)",)
        df = df.Define("m_recoil_zmumu", "FCCAnalyses::ReconstructedParticle::get_mass(recoil_zmumu)[0]",)

        # Compute the sum of the two leading jets' b-tagging scores and store it in a new column called "scoresum_B".
        df = df.Define("scoresum_B", "recojet_isB[0] + recojet_isB[1]")

        df = df.Define(
            "p4_jets",
            "JetConstituentsUtils::compute_tlv_jets("
            f"{self.jet_clustering_helper.jets})",)

        df = df.Define("m_jj", "JetConstituentsUtils::InvariantMass(p4_jets[0], p4_jets[1])")

        return df

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
