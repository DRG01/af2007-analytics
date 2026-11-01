import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AF2007 Portfolio Analytics Tool", layout="wide")

st.title("AF2007 Principles of Investment and Portfolio Management Dashboard")
st.markdown("### Markowitz Efficient Frontier & Capital Market Line Simulator")
st.write("Designed by Dr. G. Charles-Cadogan | Module: AF2007 2026-2027 SEM1")

# Sidebar Configuration for Portfolio Parameters
st.sidebar.header("Asset Calibration Parameters")
rf = st.sidebar.slider("Risk-Free Rate (%)", 0.0, 10.0, 4.5, 0.1) / 100

st.sidebar.subheader("Asset 1 (High-Growth Tech)")
r1 = st.sidebar.slider("Expected Return Asset 1 (%)", 0.0, 25.0, 14.0, 0.5) / 100
sd1 = st.sidebar.slider("Volatility Asset 1 (%)", 1.0, 40.0, 20.0, 0.5) / 100

st.sidebar.subheader("Asset 2 (Defensive Consumer Staple)")
r2 = st.sidebar.slider("Expected Return Asset 2 (%)", 0.0, 25.0, 8.0, 0.5) / 100
sd2 = st.sidebar.slider("Volatility Asset 2 (%)", 1.0, 40.0, 12.0, 0.5) / 100

st.sidebar.subheader("Correlation Interface")
rho = st.sidebar.slider("Correlation Coefficient (ρ12)", -1.0, 1.0, 0.1, 0.05)

# Portfolio Math Engine
weights = np.linspace(0, 1, 100)
p_returns = []
p_vols = []

for w in weights:
    w1 = w
    w2 = 1 - w
    ret = w1 * r1 + w2 * r2
    var = (w1**2)*(sd1**2) + (w2**2)*(sd2**2) + 2*w1*w2*sd1*sd2*rho
    vol = np.sqrt(var)
    p_returns.append(ret)
    p_vols.append(vol)

df = pd.DataFrame({'Weight1': weights, 'Weight2': 1-weights, 'Return': p_returns, 'Volatility': p_vols})

# Locate Minimum Variance Portfolio (MVP)
mvp_idx = df['Volatility'].idxmin()
mvp = df.iloc[mvp_idx]

# Tangency Portfolio Approximation (Optimal Risky Portfolio)
df['Sharpe'] = (df['Return'] - rf) / df['Volatility']
tang_idx = df['Sharpe'].idxmax()
tangency = df.iloc[tang_idx]

# Plotting Geometry
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['Volatility']*100, df['Return']*100, color='#2b5c8f', linewidth=2.5, label='Feasible Frontier')
ax.scatter([sd1*100, sd2*100], [r1*100, r2*100], color='black', s=50, zorder=5)
ax.text(sd1*100+0.5, r1*100, "Asset 1", fontsize=10, weight='semibold')
ax.text(sd2*100+0.5, r2*100, "Asset 2", fontsize=10, weight='semibold')

# Highlight MVP and Tangency Points
ax.scatter(mvp['Volatility']*100, mvp['Return']*100, color='#d9534f', s=100, marker='*', zorder=6, label='Minimum Variance Portfolio')
ax.scatter(tangency['Volatility']*100, tangency['Return']*100, color='#f0ad4e', s=80, marker='o', zorder=6, label='Tangency Portfolio')

# Draw Capital Market Line (CML)
cml_vols = np.linspace(0, max(df['Volatility'])*1.2, 100)
cml_rets = rf + tangency['Sharpe'] * cml_vols
ax.plot(cml_vols*100, cml_rets*100, color='green', linestyle='--', linewidth=1.8, label='Capital Market Line (CML)')
ax.scatter(0, rf*100, color='green', s=60, label='Risk-Free Asset')

ax.set_xlabel('Portfolio Volatility / Standard Deviation (%)', fontsize=11)
ax.set_ylabel('Expected Portfolio Return (%)', fontsize=11)
ax.set_xlim(0, max(df['Volatility'])*120)
ax.set_ylim(0, max(df['Return'])*130)
ax.legend(loc='upper left', frameon=True, facecolor='white')
ax.set_title('Markowitz Efficient Frontier & Separation Theorem Interface', fontsize=13, weight='bold', pad=10)

# Layout Configurations
col1, col2 = st.columns([2, 1])
with col1:
    st.pyplot(fig)

with col2:
    st.markdown("### Forensic Allocation Audit")
    st.metric("Risk-Free Rate Baseline", f"{rf*100:.2f}%")
    st.metric("Tangency Portfolio Return", f"{tangency['Return']*100:.2f}%")
    st.metric("Optimal Weight Asset 1", f"{tangency['Weight1']*100:.1f}%")
    st.metric("Optimal Weight Asset 2", f"{tangency['Weight2']*100:.1f}%")
    st.metric("Maximized Sharpe Ratio", f"{tangency['Sharpe']:.4f}")
