import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Set up page configurations
st.set_page_config(page_title="FCFF & FCFE Interactive Dashboard", layout="wide")

st.title("AF2007 Free Cash Flow Interactive Valuation Dashboard")
st.markdown("""
This dashboard helps you visualize how operating, investing, and financing decisions 
impact **Free Cash Flow to the Firm (FCFF)** vs. **Free Cash Flow to Equity (FCFE)**.
""")
st.write("Designed by Dr. G. Charles-Cadogan | Module: AF2007 2026-2027 SEM1")

# -------------------------------------------------------------
# SIDEBAR - INPUT SLIDERS
# -------------------------------------------------------------
st.sidebar.header("🔧 Financial Model Inputs")

ebit = st.sidebar.slider("Operating Income (EBIT) (£M)", min_value=0, max_value=2000, value=1000, step=50)
tax_rate = st.sidebar.slider("Corporate Tax Rate (%)", min_value=0, max_value=50, value=20, step=1) / 100.0
depreciation = st.sidebar.slider("Depreciation & Amortization (£M)", min_value=0, max_value=500, value=150, step=10)
capex = st.sidebar.slider("Capital Expenditures (CapEx) (£M)", min_value=0, max_value=500, value=200, step=10)
nwc_change = st.sidebar.slider("Increase in Net Working Capital (£M)", min_value=-100, max_value=300, value=50, step=10)
interest_expense = st.sidebar.slider("Interest Expense (£M)", min_value=0, max_value=300, value=100, step=10)
net_borrowing = st.sidebar.slider("Net Borrowing (£M)", min_value=-200, max_value=400, value=80, step=10)

# -------------------------------------------------------------
# FINANCIAL MATH CALCULATIONS
# -------------------------------------------------------------
ebit_after_tax = ebit * (1 - tax_rate)
fcff = ebit_after_tax + depreciation - capex - nwc_change

after_tax_interest = interest_expense * (1 - tax_rate)
fcfe = fcff - after_tax_interest + net_borrowing

# -------------------------------------------------------------
# MAIN CONTENT LAYOUT
# -------------------------------------------------------------
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📋 Dynamic Summary Table")
    
    # Create structural data frame to mirror the lecture slides
    data = {
        "Line Item": [
            "Operating Income (EBIT)",
            "Tax Rate",
            "EBIT * (1 - Tax Rate)",
            "Depreciation & Amortization (+)",
            "Capital Expenditures (CapEx) (-)",
            "Increase in Net Working Capital (-)",
            "🏆 Free Cash Flow to Firm (FCFF)",
            "Interest Expense (-)",
            "After-Tax Interest Expense (-)",
            "Net Borrowing (+)",
            "👑 Free Cash Flow to Equity (FCFE)"
        ],
        "Value": [
            f"£{ebit:,.0f}M",
            f"{tax_rate*100:.1f}%",
            f"£{ebit_after_tax:,.1f}M",
            f"£{depreciation:,.0f}M",
            f"£{capex:,.0f}M",
            f"£{nwc_change:,.0f}M",
            f"£{fcff:,.1f}M",
            f"£{interest_expense:,.0f}M",
            f"£{after_tax_interest:,.1f}M",
            f"£{net_borrowing:,.0f}M",
            f"£{fcfe:,.1f}M"
        ]
    }
    df = pd.DataFrame(data)
    st.table(df)

with col2:
    st.subheader("📈 Step-by-Step Components Visualizer")
    
    # Constructing a clean component bar chart via Plotly
    fig = go.Figure()
    
    # Left Cluster: FCFF breakdown
    fig.add_trace(go.Bar(name="EBIT after Tax", x=["FCFF (Firm)"], y=[ebit_after_tax], marker_color='#3b82f6'))
    fig.add_trace(go.Bar(name="Depreciation", x=["FCFF (Firm)"], y=[depreciation], marker_color='#f97316'))
    fig.add_trace(go.Bar(name="CapEx", x=["FCFF (Firm)"], y=[-capex], marker_color='#a855f7'))
    fig.add_trace(go.Bar(name="Change in NWC", x=["FCFF (Firm)"], y=[-nwc_change], marker_color='#ec4899'))
    fig.add_trace(go.Bar(name="Base FCFF", x=["FCFF (Firm)", "FCFE (Equity)"], y=[fcff, fcff], marker_color='#032b69'))
    
    # Right Cluster: Moving from FCFF to FCFE
    fig.add_trace(go.Bar(name="After-Tax Interest", x=["FCFE (Equity)"], y=[-after_tax_interest], marker_color='#14b8a6'))
    fig.add_trace(go.Bar(name="Net Borrowing", x=["FCFE (Equity)"], y=[net_borrowing], marker_color='#ea580c'))
    fig.add_trace(go.Bar(name="Final FCFE", x=["FCFE (Equity)"], y=[fcfe], marker_color='#6b7280'))

    fig.update_layout(
        barmode='group',
        yaxis_title="Cash Flow Value (£M)",
        legend_title="Components",
        height=550,
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(family="Arial")
    )
    
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------------
# QUICK INTERACTIVE WALKTHROUGH INSIGHTS FOR THE CLASSROOM
# -------------------------------------------------------------
st.markdown("---")
st.subheader("💡 Key Takeaways:")
st.info(f"""
* **The Leverage Effect:** Notice that changing **Net Borrowing** or **Interest Expense** alters your final **FCFE (£{fcfe:,.1f}M)** but leaves your **FCFF (£{fcff:,.1f}M)** completely unchanged. This visually proves to students that FCFF is *unlevered*.
* **Non-Cash Add-backs:** Increasing **Depreciation** improves both metrics uniformly without altering operational EBIT performance.
""")
