import streamlit as st
import json
import plotly.graph_objects as go

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1) Page & global CSS
st.set_page_config(
    page_title="NeuroCOVID Network Navigator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    /* Animated vertical gradient */
    @keyframes gradientBG {
      0%   { background-position: 0%   0%; }
      50%  { background-position: 0% 100%; }
      100% { background-position: 0%   0%; }
    }
    div[data-testid="stAppViewContainer"] {
      background: linear-gradient(0deg, #b9f5fd 0%, #cff9fe 50%, #e6fcff 100%);
      background-size: 100% 400%;
      animation: gradientBG 30s ease infinite;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    }
    /* Transparent Streamlit chrome */
    header, footer, div[data-testid="stToolbar"] {
      background: transparent !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("NeuroCOVID Network Navigator")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2) Zoom slider
zoom = st.sidebar.slider("Zoom level", min_value=0.5, max_value=2.0, value=1.0, step=0.05,
                         help="Use this to zoom into the network")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3) Load & prep figure
with open("neurocovid_svnet.json") as f:
    fig_dict = json.load(f)
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

for trace in fig_dict["data"]:
    mode = trace.get("mode")
    if mode == "markers+text":
        trace["text"] = [label_map.get(t, t) for t in trace["text"]]
        trace["marker"].update(size=10, line=dict(width=1, color="#111"))
        tf = trace.setdefault("textfont", {})
        tf.update(color="#111", size=11)
    elif mode == "lines":
        trace["line"].update(width=2.5, color="rgba(30,30,30,0.7)")

# hide axes & grid
scene = fig_dict["layout"].get("scene", {})
for ax in ("xaxis","yaxis","zaxis"):
    scene.get(ax, {}).update(
        showgrid=False, zeroline=False,
        showticklabels=False, title_text=""
    )

# adjust camera distance by zoom
base_eye = dict(x=1.5, y=1.5, z=1.2)
scene.update(
    bgcolor="rgba(0,0,0,0)",
    camera=dict(
        eye={k: base_eye[k] / zoom for k in base_eye}
    )
)

# legend & background transparency
layout = fig_dict["layout"]
layout.update(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    legend=dict(
        bgcolor="rgba(255,255,255,0.6)",
        bordercolor="#CCC",
        borderwidth=1,
        x=0.02, y=0.98
    ),
    margin=dict(l=0, r=0, t=60, b=0),
    title=dict(
        text="Interactive SVNet of Neurological Comorbidities",
        x=0.5, xanchor="center",
        font=dict(size=20, color="#111")
    )
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4) Render
fig = go.Figure(fig_dict)
st.plotly_chart(fig, use_container_width=True, theme=None)
