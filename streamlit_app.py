import streamlit as st
import json
import plotly.graph_objects as go

# ————————————————————————————————
# Streamlit page setup
st.set_page_config(
    page_title="NeuroCOVID Network Navigator",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown(
    """
    <style>
      /* make the background pure white */
      .reportview-container, .main .block-container {
        background-color: #FFFFFF;
      }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("NeuroCOVID Network Navigator")

# ————————————————————————————————
# Load the SVNet JSON
with open("neurocovid_svnet.json") as f:
    fig_dict = json.load(f)

# drop the old template
fig_dict["layout"].pop("template", None)

# 2) Full mapping from internal codes → human labels
label_map = {
    # Comm 1
    "com_tme_ty_sepsis":      "Septic Encephalopathy",
    "com_neurodeg_ty_othdem": "Other Dementia",
    "com_str_ty_iphivh":      "Intracerebral Hemorrhage/IVH",
    "com_neurm_ty_radic":     "Radiculopathy",
    "com_sz_typ_focal":       "Focal Seizures",
    "com_cnsinfl_vasc":       "Vasculitis",
    "com_tbi_ty_enceph":      "Encephalopathy (TBI)",
    "com_sz_typ_genl":        "Generalized Seizures",
    "com_neurodeg_ty_alz":    "Alzheimer’s Disease",
    "com_tme_ty_electro":     "Electrolyte Encephalopathy",
    "com_tme_ty_hepenc":      "Hepatic Encephalopathy",
    "com_neurodeg_ty_nph":    "Normal Pressure Hydrocephalus",
    "com_str_ty_isctia":      "Ischemic Stroke/TIA",
    "com_tbi_ty_pconcus":     "Post-concussive Syndrome",
    "com_mov_ty_myocl":       "Myoclonus",
    "com_ha_ty_othprim":      "Other Headache",
    "com_tme_ty_hypercarb":   "Hypercarbic Encephalopathy",
    "com_str_ty_sah":         "Subarachnoid Hemorrhage",
    "com_tbi_ty_subdur":      "Subdural Hematoma",
    "com_tme_ty_environ":     "Environmental Encephalopathy",
    "com_tme_ty_drugwith":    "Drug-related Encephalopathy",

    # Comm 2
    "com_ha_ty_migr":         "Migraine",
    "com_neurm_ty_cidp":      "CIDP",
    "com_ha_ty_tension":      "Tension-type Headache",
    "com_neurm_ty_gbd":       "Guillain-Barré",
    "com_neurodeg_ty_devdelay":"Developmental Delay",
    "com_sz_typ_unclass":     "Unclassified Seizure",
    "com_tme_ty_toxnutr":     "Toxic/Nutritional Encephalopathy",
    "com_pain_ty_neuropath":  "Neuropathic Pain",
    "com_cnsinfl_ms":         "Multiple Sclerosis",
    "com_str_ty_cvt":         "Cerebral Venous Thrombosis",
    "com_spdz_ty_degen":      "Spinal Degenerative Disease",

    # Comm 3
    "com_pain_ty_fibromy":    "Fibromyalgia",
    "com_dysaut_ty_pots":     "POTS",
    "com_neurps_ty_bipol":    "Bipolar Disorder",
    "com_neurps_ty_depr":     "Depression",
    "com_neurps_ty_schiz":    "Schizophrenia",
    "com_neurps_ty_anx":      "Anxiety",
    "com_mov_ty_restleg":     "Restless Leg Syndrome",
    "com_neurps_ty_ptsd":     "PTSD",

    # Comm 4
    "com_neurodeg_ty_park":   "Parkinson’s Disease",
    "com_mov_ty_park":        "Parkinsonism",
    "com_mov_ty_estrem":      "Essential Tremor",
    "com_cnsinfl_men":        "Meningitis",
    "com_ha_ty_clus":         "Cluster Headache",
    "com_pain_ty_muscsk":     "Musculoskeletal Pain",
    "com_cnsinfl_enc":        "Encephalitis",

    # Comm 5 & 6
    "com_neurm_ty_nmj":       "NMJ Disorder",
    "com_neurm_ty_myop":      "Myopathy",
}

# relabel nodes and strengthen edges
for trace in fig_dict["data"]:
    if trace.get("mode") == "markers+text":
        trace["text"] = [label_map.get(t, t) for t in trace["text"]]
        # make the markers slightly larger and darker border
        trace["marker"].update(size=10, line=dict(width=1, color="#222"))
        trace["textfont"].update(color="#111", size=10)
    elif trace.get("mode") == "lines":
        trace["line"].update(width=1.5, color="rgba(50,50,50,0.3)")

# ————————————————————————————————
# Tidy up axes + scene background gradient
scene = fig_dict["layout"].get("scene", {})
for ax in ("xaxis","yaxis","zaxis"):
    if ax in scene:
        scene[ax].update(
            showgrid=False, zeroline=False,
            showticklabels=False, title_text=""
        )

# apply a light vertical gradient from white→paleblue
scene.update(
    bgcolor="rgba(245, 252, 255, 1)",
    camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
)

# ————————————————————————————————
# Modernize legend: semi-opaque white box floating over the graph
layout = fig_dict["layout"]
layout.update(
    paper_bgcolor="white",
    plot_bgcolor="rgba(0,0,0,0)",  # transparent, let scene show
    legend=dict(
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="#DDD",
        borderwidth=1,
        x=0.02, y=0.98
    ),
    margin=dict(l=0,r=0,t=60,b=0),
    title=dict(
        text="Interactive SVNet of Neurological Comorbidities",
        x=0.5,
        xanchor="center",
        font=dict(size=18, color="#222")
    )
)

# ————————————————————————————————
# Render
fig = go.Figure(fig_dict)
st.plotly_chart(fig, use_container_width=True)