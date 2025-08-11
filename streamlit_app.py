import streamlit as st
import json
import plotly.graph_objects as go

# Title
st.set_page_config(page_title="NeuroCOVID Network Navigator")
st.title("NeuroCOVID Network Navigator")

# Load the exported SVNet JSON
with open("neurocovid_svnet.json") as f:
    fig_dict = json.load(f)

# Mapping from internal codes to human-readable labels
label_map = {
    "com_tme_ty_sepsis": "Septic Encephalopathy",
    "com_neurodeg_ty_othdem": "Other Dementia",
    "com_str_ty_iphivh": "Intracerebral Hemorrhage/IVH",
    "com_neurm_ty_radic": "Radiculopathy",
    "com_sz_typ_focal": "Focal Seizures",
    "com_cnsinfl_vasc": "Vasculitis",
    "com_tbi_ty_enceph": "Encephalopathy (TBI-related)",
    "com_sz_typ_genl": "Generalized Seizures",
    "com_neurodeg_ty_alz": "Alzheimer’s Disease",
    "com_tme_ty_electro": "Electrolyte Encephalopathy",
    "com_tme_ty_hepenc": "Hepatic Encephalopathy",
    "com_neurodeg_ty_nph": "Normal Pressure Hydrocephalus",
    "com_str_ty_isctia": "Ischemic Stroke/TIA",
    "com_tbi_ty_pconcus": "Post-concussive Syndrome",
    "com_mov_ty_myocl": "Myoclonus",
    "com_ha_ty_othprim": "Other Primary Headache",
    "com_tme_ty_hypercarb": "Hypercarbic Encephalopathy",
    "com_str_ty_sah": "Subarachnoid Hemorrhage",
    "com_tbi_ty_subdur": "Subdural Hematoma",
    "com_tme_ty_environ": "Environmental TME",
    "com_tme_ty_drugwith": "Drug-related Encephalopathy",
    # Continue for all codes...
}

# Remap labels and clean axes
for trace in fig_dict["data"]:
    # Remap node labels
    if trace.get("mode") == "markers+text" and "text" in trace:
        trace["text"] = [label_map.get(t, t) for t in trace["text"]]
    # Hide axis lines and ticks
    if trace.get("type") == "scatter3d":
        # No change to trace needed for axis removal
        pass

# Update layout to remove axis titles/ticks
layout = fig_dict["layout"]
scene = layout.get("scene", {})
for axis in ["xaxis", "yaxis", "zaxis"]:
    if axis in scene:
        scene[axis].update(showticklabels=False, showbackground=False, title=None)

# Create Figure and display
fig = go.Figure(fig_dict)
fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))

st.plotly_chart(fig, use_container_width=True)
