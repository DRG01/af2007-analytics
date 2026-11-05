import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

# 1. Page Configuration okay
st.set_page_config(page_title="RegTech Penalty Supervisor", layout="wide")
st.title("The Penalised Regulator: Supervisory Risk Triage Dashboard")
st.markdown("### Data-Driven Early-Warning & Penalty Threshold Simulator")
st.caption("Based on the 2026 RegTech Model by Dr. G. Charles-Cadogan")

# 2. Main Parameters Driving the Model (The Four Key Variables)
st.markdown("---")
col_var1, col_var2 = st.columns(2)

with col_var1:
    L = st.slider("Firm Leverage Ratio (D/V)", 0.10, 0.95, 0.50, 0.01)
    alpha = st.slider("Compensation Convexity (Vega Incentive)", 0.0, 1.0, 0.40, 0.05)

with col_var2:
    sigma = st.slider("Asset Volatility (σ)", 0.05, 1.00, 0.60, 0.01)
    enforcement = st.slider("Regulatory Enforcement Intensity (ϱ_env)", 0.05, 1.00, 0.45, 0.01)

# 3. Mathematical Operations & Predictive Engine
r = 0.045  # Fixed Baseline Risk-Free Rate
T = 1.0    # 1-Year Default Horizon

# Merton Structural Formulation
d1 = (np.log(1.0 / L) + (r + (sigma ** 2) / 2.0) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# Outputs
default_prob = 1.0 - float(np.clip(d2 / 3.0, 0.0, 1.0)) # Scaled approximation for probability presentation
distance_to_default = max(0.1, float(d2))

# Charles-Cadogan High-Dimensional Supervisory Score Mechanics
supervisory_score = 1.5 * L + 1.2 * sigma + 0.8 * (alpha * 1.5) - 1.4 * enforcement
supervisory_score = float(np.clip(supervisory_score, 0.0, 1.0))

# Structural Penalty Threshold (ϱ*) Proposition 2.1
rho_star = (L * 0.5) * ((sigma * 0.15 * alpha) * (sigma * T + d2)) + (0.05 * alpha)
rho_star = float(np.clip(rho_star, 0.0, 1.0))

# 4. Triage Escalation Logic
if supervisory_score < 0.35:
    tier_label = "Safe Tier"
    tier_color = "#2e7d32" # Green
elif supervisory_score < 0.65:
    tier_label = "Warning Tier"
    tier_color = "#fbc02d" # Yellow
else:
    tier_label = "Intervention Tier"
    tier_color = "#c62828" # Red

# 5. Top Highlights Panel (Displays Metrics exactly like the image)
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric(label="Default Probability Representation", value=f"{default_prob * 100:.2f}%")
    st.markdown(f"<span style='background-color:{tier_color}33; color:{tier_color}; padding:3px 8px; border-radius:4px; font-weight:bold;'>{tier_label}</span>", unsafe_allow_html=True)
with col_m2:
    st.metric(label="Supervisory Score (ŝ)", value=f"{supervisory_score:.3f}")
with col_m3:
    st.metric(label="Structural Penalty Threshold (ϱ*)", value=f"{rho_star:.3f}")
with col_m4:
    st.metric(label="Merton Distance to Default", value=f"{distance_to_default:.2f}")

st.markdown("<br>", unsafe_allow_html=True)

# 6. Matplotlib Matrix Mapping Engine
vol_axis = np.linspace(0.05, 1.0, 100)
boundary_curve = 0.15 + (vol_axis ** 1.8) * (L * 0.8) + (alpha * 0.1)

fig, ax = plt.subplots(figsize=(10, 5), facecolor='#fafafa')
ax.set_facecolor('#fafafa')

# Draw the background zone structures
ax.fill_between(vol_axis, 0, boundary_curve, color='#e8f5e9', alpha=0.6, label='Stabilized Capital Base (Safe Zone)')
ax.fill_between(vol_axis, boundary_curve, boundary_curve + 0.25, color='#fffde7', alpha=0.6, label='Warning Zone')
ax.fill_between(vol_axis, boundary_curve + 0.25, 1.2, color='#ffebee', alpha=0.6, label='ϱ* Penalty Threshold Exceeded Area')

# Draw the operational boundary line
ax.plot(vol_axis, boundary_curve, color='#2979ff', linewidth=3, zorder=2)

# Position the dynamic firm asset indicator marker
current_y_position = boundary_curve[int((sigma - 0.05) / 0.95 * 99)] + (supervisory_score * 0.2)
current_y_position = min(1.1, current_y_position)

# Outer glowing indicator ring and core point
ax.scatter(sigma, current_y_position, color='#fbc02d', s=250, alpha=0.4, zorder=4)
ax.scatter(sigma, current_y_position, color='#f57f17', s=90, edgecolors='white', linewidth=1.5, zorder=5)

# Text and labels configuration
ax.text(0.08, 0.1, "Stabilized Capital Base", color='#2e7d32', fontsize=11, alpha=0.8, weight='semibold')
ax.text(0.08, 0.95, "ϱ* Penalty Threshold Exceeded Area", color='#c62828', fontsize=11, alpha=0.8, weight='semibold')

ax.set_xlabel("Asset Volatility & Systemic Stress Profile (σ)", fontsize=10, color='#555555', labelpad=8)
ax.set_ylabel("Supervisory Threat Matrix", fontsize=10, color='#555555', labelpad=8)
ax.set_xlim(0.05, 1.0)
ax.set_ylim(0.0, 1.1)

# Clean up axes ticks to look modern and clean
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')
ax.get_xaxis().set_ticks([])
ax.get_yaxis().set_ticks([])

# 7. Render Plot
st.pyplot(fig)
