import streamlit as st
import json
import plotly.graph_objects as go

# Title
st.set_page_config(page_title="NeuroCOVID Network Navigator")
st.title("NeuroCOVID Network Navigator")

# Load the exported SVNet JSON
with open("neurocovid_svnet.json") as f:
    fig_dict = json.load(f)

# 1) Remove the potentially invalid 'template' key
fig_dict["layout"].pop("template", None)

# 2) Full mapping from internal codes → human labels
label_map = {
    # Comm 1
    "com_tme_ty_sepsis":           "Septic Encephalopathy",
    "com_neurodeg_ty_othdem":      "Other Dementia",
    "com_str_ty_iphivh":           "Intracerebral Hemorrhage/IVH",
    "com_neurm_ty_radic":          "Radiculopathy",
    "com_sz_typ_focal":            "Focal Seizures",
    "com_cnsinfl_vasc":            "Vasculitis",
    "com_tbi_ty_enceph":           "Encephalopathy (TBI-related)",
    "com_sz_typ_genl":             "Generalized Seizures",
    "com_neurodeg_ty_alz":         "Alzheimer’s Disease",
    "com_tme_ty_electro":          "Electrolyte Encephalopathy",
    "com_tme_ty_hepenc":           "Hepatic Encephalopathy",
    "com_neurodeg_ty_nph":         "Normal Pressure Hydrocephalus",
    "com_str_ty_isctia":           "Ischemic Stroke/TIA",
    "com_tbi_ty_pconcus":          "Post-concussive Syndrome",
    "com_mov_ty_myocl":            "Myoclonus",
    "com_ha_ty_othprim":           "Other Primary Headache",
    "com_tme_ty_hypercarb":        "Hypercarbic Encephalopathy",
    "com_str_ty_sah":              "Subarachnoid Hemorrhage",
    "com_tbi_ty_subdur":           "Subdural Hematoma",
    "com_tme_ty_environ":          "Environmental Encephalopathy",
    "com_tme_ty_drugwith":         "Drug-related Encephalopathy",

    # Comm 2
    "com_ha_ty_migr":              "Migraine",
    "com_neurm_ty_cidp":           "CIDP",
    "com_ha_ty_tension":           "Tension-type Headache",
    "com_neurm_ty_gbd":            "Guillain-Barré Syndrome",
    "com_neurodeg_ty_devdelay":    "Developmental Delay",
    "com_sz_typ_unclass":          "Unclassified Seizure",
    "com_tme_ty_toxnutr":          "Toxic/Nutritional Encephalopathy",
    "com_pain_ty_neuropath":       "Neuropathic Pain",
    "com_cnsinfl_ms":              "Multiple Sclerosis",
    "com_str_ty_cvt":              "Cerebral Venous Thrombosis",
    "com_spdz_ty_degen":           "Spinal Degenerative Disease",

    # Comm 3
    "com_pain_ty_fibromy":         "Fibromyalgia",
    "com_dysaut_ty_pots":          "POTS",
    "com_neurps_ty_bipol":         "Bipolar Disorder",
    "com_neurps_ty_depr":          "Depression",
    "com_neurps_ty_schiz":         "Schizophrenia",
    "com_neurps_ty_anx":           "Anxiety",
    "com_mov_ty_restleg":          "Restless Leg Syndrome",
    "com_neurps_ty_ptsd":          "PTSD",

    # Comm 4
    "com_neurodeg_ty_park":        "Parkinson’s Disease",
    "com_mov_ty_park":             "Parkinsonism",
    "com_mov_ty_estrem":           "Essential Tremor",
    "com_cnsinfl_men":             "Meningitis",
    "com_ha_ty_clus":              "Cluster Headache",
    "com_pain_ty_muscsk":          "Musculoskeletal Pain",
    "com_cnsinfl_enc":             "Encephalitis",

    # Comm 5 & 6
    "com_neurm_ty_nmj":            "NMJ Disorder",
    "com_neurm_ty_myop":           "Myopathy",
}

# 3) Remap the text in each 3d‐scatter trace
for trace in fig_dict["data"]:
    if trace.get("mode") == "markers+text" and "text" in trace:
        trace["text"] = [label_map.get(t, t) for t in trace["text"]]

# 4) Hide all 3D axes in the layout.scene
scene = fig_dict["layout"].get("scene", {})
for axis in ("xaxis", "yaxis", "zaxis"):
    if axis in scene:
        scene[axis].update(
            showticklabels=False,
            showbackground=False,
            title_text=""
        )

# Build and render
fig = go.Figure(fig_dict)
fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))

st.plotly_chart(fig, use_container_width=True)
