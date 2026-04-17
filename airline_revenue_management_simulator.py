import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Airline Revenue Management",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --blue:       #1e88e5;
    --blue-dark:  #1565c0;
    --blue-light: #e3f2fd;
    --navy:       #1e3a8a;
    --text:       #1e293b;
    --subtext:    #475569;
    --muted:      #94a3b8;
    --border:     #e2e8f0;
    --bg:         #f0f2f6;
    --card:       #ffffff;
    --red:        #ef4444;
    --green:      #22c55e;
    --amber:      #f59e0b;
    --purple:     #8b5cf6;
}

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}
.stApp { background: var(--bg); }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { display: none; }

/* ── Header ── */
.header-container {
    display: flex; align-items: center; gap: 20px;
    margin-bottom: 28px;
    background: linear-gradient(90deg, #1e3a8a 0%, #1e88e5 100%);
    padding: 30px 36px; border-radius: 15px; color: white;
}
.header-text h1 {
    font-size: 28px; font-weight: 800; color: white !important;
    margin: 0 0 6px 0; letter-spacing: -0.02em;
}
.header-text p { font-size: 13px; opacity: 0.88; margin: 0; line-height: 1.5; }

/* ── st.metric blue-border style ── */
[data-testid="stMetric"] {
    background: white !important; padding: 18px 16px !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
    border-left: 5px solid var(--blue) !important;
}
[data-testid="stMetricLabel"] {
    font-size: 12px !important; font-weight: 700 !important;
    color: var(--subtext) !important; text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}
[data-testid="stMetricValue"] {
    font-size: 26px !important; font-weight: 800 !important;
    color: var(--navy) !important; font-family: 'Outfit', sans-serif !important;
}
[data-testid="stMetricDelta"] { font-size: 12px !important; font-weight: 600 !important; }

/* ── Panel cards ── */
.panel {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 12px; padding: 20px 22px; margin-bottom: 14px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.04);
}
.panel-title {
    font-size: 12px; font-weight: 700; color: var(--navy);
    margin-bottom: 14px; text-transform: uppercase; letter-spacing: 0.07em;
    border-bottom: 2px solid var(--blue-light); padding-bottom: 9px;
}

/* ── Fare class chips ── */
.chip {
    display: inline-block; padding: 3px 12px; border-radius: 20px;
    font-size: 11px; font-weight: 700; letter-spacing: 0.05em;
}
.chip-f1 { background:#eff6ff; color:#1d4ed8; border:1px solid #93c5fd; }
.chip-f2 { background:#f0fdf4; color:#166534; border:1px solid #86efac; }

/* ── Rec banners ── */
.rec-banner {
    background: #eff6ff; border: 1.5px solid var(--blue);
    border-left: 5px solid var(--blue);
    border-radius: 10px; padding: 16px 20px; margin-bottom: 20px;
}
.rec-banner.green { background:#f0fdf4; border-color:var(--green); border-left-color:var(--green); }
.rec-banner.amber { background:#fffbeb; border-color:var(--amber); border-left-color:var(--amber); }
.rec-title { font-size: 15px; font-weight: 700; color: var(--navy); margin-bottom: 5px; }
.rec-body  { font-size: 13px; color: var(--subtext); line-height: 1.6; }

/* ── Alerts ── */
.alert-info { background:var(--blue-light); border:1px solid #90caf9; border-radius:8px; padding:9px 13px; font-size:12px; color:#1565c0; font-weight:600; margin-top:8px; }

/* ── Section label ── */
.sec-lbl {
    font-size: 11px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.1em; color: var(--muted); margin: 0 0 8px 0;
}

/* ── Breakdown rows ── */
.brow {
    display: flex; justify-content: space-between; align-items: center;
    padding: 9px 14px; border-radius: 8px; margin: 3px 0;
    background: #f8fafc; font-size: 13px; font-weight: 500;
    border: 1px solid var(--border);
}

hr { border: none; border-top: 1px solid var(--border); margin: 16px 0; }

/* ── Buttons ── */
div.stButton > button {
    border-radius: 8px !important; font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important; font-size: 14px !important;
    padding: 10px 0 !important; transition: all 0.15s !important;
}
div.stButton > button[kind="primary"] {
    background: var(--blue) !important; border-color: var(--blue) !important; color: white !important;
}
div.stButton > button[kind="primary"]:hover {
    background: var(--blue-dark) !important; border-color: var(--blue-dark) !important;
}

/* ── Inputs ── */
div[data-testid="stNumberInput"] input {
    background: white !important; border: 1.5px solid var(--border) !important;
    border-radius: 8px !important; color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important; font-weight: 500 !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px rgba(30,136,229,0.12) !important;
}
label {
    font-size: 11px !important; font-weight: 700 !important;
    color: var(--subtext) !important; letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}
.stSlider > div > div > div { background: var(--blue) !important; }
.stProgress > div > div { background: var(--blue) !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 3px; background: #f0f2f6;
    border-radius: 10px; padding: 4px; border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px !important; font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important; font-size: 12px !important;
    color: var(--subtext) !important; padding: 7px 14px !important;
}
.stTabs [aria-selected="true"] { background: var(--blue) !important; color: white !important; }
[data-testid="stDataFrame"] { border-radius: 10px !important; }
</style>
"""

# ═══════════════════════════════════════════════════════════════════
# SIMULATION ENGINE
# ═══════════════════════════════════════════════════════════════════

def simulate_one(
    capacity, total_tickets, booking_limit_leisure,
    f1_price, f2_price,
    f1_demand_mean, f1_demand_std,
    f2_demand_mean, f2_demand_std,
    f1_noshow_prob, f2_noshow_prob,
    f1_refund, f2_refund,
    vol_prob, vdb_voucher, idb_cost,
    n_sim, seed=None,
):
    """
    Full simulation of two-fare-class revenue management.

    Returns dict of arrays (length n_sim) and scalar summaries.
    """
    if seed is not None:
        np.random.seed(seed)

    reservation_level = total_tickets - booking_limit_leisure  # max F1 tickets

    # ── Sample demand ──────────────────────────────────────────────
    f2_demand_raw = np.random.normal(f2_demand_mean, f2_demand_std, n_sim)
    f2_demand     = np.clip(np.round(f2_demand_raw).astype(int), 0, None)

    f1_demand_raw = np.random.normal(f1_demand_mean, f1_demand_std, n_sim)
    f1_demand     = np.clip(np.round(f1_demand_raw).astype(int), 0, None)

    # ── Tickets sold ───────────────────────────────────────────────
    # Leisure books first up to booking_limit_leisure
    f2_sold = np.minimum(f2_demand, booking_limit_leisure)
    # Remaining capacity for F1 = min(reservation_level, total_tickets - f2_sold)
    f1_capacity = np.minimum(reservation_level, total_tickets - f2_sold)
    f1_sold     = np.minimum(f1_demand, f1_capacity)
    total_sold  = f1_sold + f2_sold

    # ── Revenue from ticket sales ──────────────────────────────────
    ticket_revenue = f1_sold * f1_price + f2_sold * f2_price

    # ── No-shows ──────────────────────────────────────────────────
    f1_noshow = np.random.binomial(f1_sold, f1_noshow_prob)
    f2_noshow = np.random.binomial(f2_sold, f2_noshow_prob)

    # F1 no-shows get refund, F2 do not
    refund_cost = f1_noshow * f1_price * f1_refund  # f1_refund=1 → full refund

    f1_showed = f1_sold - f1_noshow
    f2_showed = f2_sold - f2_noshow
    total_showed = f1_showed + f2_showed

    # ── Oversell situation ────────────────────────────────────────
    oversell = np.maximum(0, total_showed - capacity)

    # Voluntary denied boardings — only leisure pax volunteer
    # Each leisure pax who showed has vol_prob chance of volunteering
    # We need min(oversell, volunteers) to resolve voluntarily
    max_volunteers = np.random.binomial(f2_showed, vol_prob)
    vdb = np.minimum(oversell, max_volunteers)

    # Involuntary denied boardings (what remains after volunteers)
    idb = oversell - vdb

    # ── Costs ─────────────────────────────────────────────────────
    vdb_cost = vdb * vdb_voucher   # airline keeps ticket revenue, just pays voucher
    idb_total_cost = idb * idb_cost

    # ── Net profit ────────────────────────────────────────────────
    profit = ticket_revenue - refund_cost - vdb_cost - idb_total_cost

    return {
        # Arrays
        "profit":          profit,
        "ticket_revenue":  ticket_revenue,
        "refund_cost":     refund_cost,
        "vdb_cost":        vdb_cost,
        "idb_cost":        idb_total_cost,
        "f1_sold":         f1_sold,
        "f2_sold":         f2_sold,
        "total_sold":      total_sold,
        "f1_showed":       f1_showed,
        "f2_showed":       f2_showed,
        "total_showed":    total_showed,
        "oversell":        oversell,
        "vdb":             vdb,
        "idb":             idb,
        "f1_noshow":       f1_noshow,
        "f2_noshow":       f2_noshow,
        # Scalars
        "mean_profit":     float(profit.mean()),
        "std_profit":      float(profit.std()),
        "p5_profit":       float(np.percentile(profit, 5)),
        "p95_profit":      float(np.percentile(profit, 95)),
        "prob_oversell":   float((oversell > 0).mean()),
        "prob_idb":        float((idb > 0).mean()),
        "mean_vdb":        float(vdb.mean()),
        "mean_idb":        float(idb.mean()),
        "mean_f1_sold":    float(f1_sold.mean()),
        "mean_f2_sold":    float(f2_sold.mean()),
        "mean_revenue":    float(ticket_revenue.mean()),
        "mean_refund":     float(refund_cost.mean()),
        "load_factor":     float((f1_showed + f2_showed).mean() / capacity * 100),
    }


def scan_grid(
    capacity, total_tickets_range, booking_limit_range,
    f1_price, f2_price,
    f1_demand_mean, f1_demand_std,
    f2_demand_mean, f2_demand_std,
    f1_noshow_prob, f2_noshow_prob,
    f1_refund, f2_refund,
    vol_prob, vdb_voucher, idb_cost,
    n_sim, seed=None,
):
    """Scan a grid of (total_tickets, booking_limit_leisure) pairs."""
    rows = []
    for tt in total_tickets_range:
        for bl in booking_limit_range:
            if bl > tt:
                continue  # booking limit can't exceed total
            rl = tt - bl  # reservation level for F1
            r = simulate_one(
                capacity, tt, bl,
                f1_price, f2_price,
                f1_demand_mean, f1_demand_std,
                f2_demand_mean, f2_demand_std,
                f1_noshow_prob, f2_noshow_prob,
                f1_refund, f2_refund,
                vol_prob, vdb_voucher, idb_cost,
                n_sim, seed,
            )
            rows.append({
                "Total Tickets": tt,
                "Booking Limit (F2)": bl,
                "Reservation Level (F1)": rl,
                "Mean Profit":    round(r["mean_profit"], 0),
                "Std Dev":        round(r["std_profit"], 0),
                "P5 Profit":      round(r["p5_profit"], 0),
                "P95 Profit":     round(r["p95_profit"], 0),
                "Prob Oversell":  round(r["prob_oversell"] * 100, 1),
                "Prob IDB":       round(r["prob_idb"] * 100, 1),
                "Avg VDB":        round(r["mean_vdb"], 2),
                "Avg IDB":        round(r["mean_idb"], 2),
                "Avg F1 Sold":    round(r["mean_f1_sold"], 1),
                "Avg F2 Sold":    round(r["mean_f2_sold"], 1),
                "Load Factor":    round(r["load_factor"], 1),
            })
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════════
# APP
# ═══════════════════════════════════════════════════════════════════
st.markdown(CSS, unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
    <div style="font-size:52px;line-height:1">✈️</div>
    <div class="header-text">
        <h1>Airline Revenue Management</h1>
        <p>Two-fare-class simulation · Space reservation · Overbooking · Voluntary & Involuntary Denied Boardings<br>
        Optimise <strong>total tickets to sell</strong> and <strong>booking limit for leisure fares</strong> to maximise expected profit.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Layout: narrow inputs | wide results ─────────────────────────
left, right = st.columns([1, 2], gap="large")

with left:
    # ── Fare class parameters ──
    st.markdown('<div class="panel-title">💼 Business Fare — F1 <span class="chip chip-f1">HIGH YIELD</span></div>', unsafe_allow_html=True)
    f1_price      = st.number_input("F1 Ticket Price ($)",       min_value=0.0, value=1500.0, step=50.0)
    f1_dem_mean   = st.number_input("F1 Demand Mean",            min_value=0.0, value=20.0,   step=1.0)
    f1_dem_std    = st.number_input("F1 Demand Std Dev",         min_value=0.0, value=5.0,    step=0.5)
    f1_noshow_pct = st.number_input("F1 No-Show Rate (%)", min_value=0.0, max_value=100.0, value=15.0, step=0.1, format="%.1f")
    f1_refund     = st.checkbox("F1 No-Shows Get Full Refund", value=True)
    st.divider()
    st.markdown('<div class="panel-title">🏖 Leisure Fare — F2 <span class="chip chip-f2">PRICE SENSITIVE</span></div>', unsafe_allow_html=True)
    f2_price      = st.number_input("F2 Ticket Price ($)",       min_value=0.0, value=500.0,  step=25.0)
    f2_dem_mean   = st.number_input("F2 Demand Mean",            min_value=0.0, value=200.0,  step=5.0)
    f2_dem_std    = st.number_input("F2 Demand Std Dev",         min_value=0.0, value=20.0,   step=1.0)
    f2_noshow_pct = st.number_input("F2 No-Show Rate (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1, format="%.1f")
    f2_refund     = st.checkbox("F2 No-Shows Get Full Refund", value=False)
    st.divider()
    st.markdown('<div class="panel-title">✈️ Flight & Oversell Policy</div>', unsafe_allow_html=True)
    capacity    = st.number_input("Aircraft Capacity (Seats)", min_value=1, max_value=1000, value=150, step=1)
    vol_pct     = st.number_input("Leisure Volunteer Prob. (%)", min_value=0.0, max_value=100.0, value=1.5, step=0.1, format="%.1f",
                                   help="Each leisure pax who shows up has this chance of volunteering for a voucher.")
    vdb_voucher = st.number_input("Voluntary Denied Boarding Voucher — VDB ($)", min_value=0.0, value=800.0, step=50.0,
                                  help="Voucher given to passengers who voluntarily give up their seat.")
    idb_cost    = st.number_input("Involuntary Denied Boarding Cost — IDB ($)", min_value=0.0, value=3000.0, step=100.0,
                                  help="Total cost per passenger forcibly denied boarding (higher voucher + estimated goodwill loss).")
    st.divider()

    st.markdown('<div class="panel-title">⚙️ Simulation Settings</div>', unsafe_allow_html=True)
    n_sim    = st.number_input("Monte Carlo Iterations", min_value=100, max_value=100000, value=10000, step=1000)
    use_seed = st.checkbox("Fix random seed")
    seed_val = st.number_input("Seed", min_value=0, value=42, step=1, disabled=not use_seed)

    run = st.button("▶  Run Simulation", type="primary", use_container_width=True)

# ── Results ───────────────────────────────────────────────────────
with right:
    if not run and "rm_res" not in st.session_state:
        st.markdown("""
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                    height:460px;background:white;border:2px dashed #e2e8f0;border-radius:15px;">
            <div style="font-size:64px;margin-bottom:16px">✈️</div>
            <div style="font-size:20px;font-weight:800;color:#1e3a8a;margin-bottom:8px;font-family:'Outfit',sans-serif">
                Ready for Analysis</div>
            <div style="font-size:14px;color:#64748b;text-align:center;max-width:320px;line-height:1.6">
                Configure parameters on the left and click <strong>Run Simulation</strong>.</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        if run:
            seed = int(seed_val) if use_seed else None
            f1_np = f1_noshow_pct / 100
            f2_np = f2_noshow_pct / 100
            vp    = vol_pct / 100

            with st.spinner("Running optimizer scan..."):
                tt_range = range(int(capacity), int(capacity) + 31, 1)
                bl_range = range(max(0, int(capacity) - 30), int(capacity) + 1, 1)
                grid_df  = scan_grid(
                    int(capacity), tt_range, bl_range,
                    float(f1_price), float(f2_price),
                    float(f1_dem_mean), float(f1_dem_std),
                    float(f2_dem_mean), float(f2_dem_std),
                    f1_np, f2_np,
                    float(f1_refund), float(f2_refund),
                    vp, float(vdb_voucher), float(idb_cost),
                    int(n_sim), seed,
                )
                # Run detailed simulation at the optimal point
                best_idx_run = grid_df["Mean Profit"].idxmax()
                opt_tt = int(grid_df.loc[best_idx_run, "Total Tickets"])
                opt_bl = int(grid_df.loc[best_idx_run, "Booking Limit (F2)"])
                res = simulate_one(
                    int(capacity), opt_tt, opt_bl,
                    float(f1_price), float(f2_price),
                    float(f1_dem_mean), float(f1_dem_std),
                    float(f2_dem_mean), float(f2_dem_std),
                    f1_np, f2_np,
                    float(f1_refund), float(f2_refund),
                    vp, float(vdb_voucher), float(idb_cost),
                    int(n_sim), seed,
                )

            st.session_state.rm_res   = res
            st.session_state.grid_df  = grid_df
            st.session_state.rm_params = dict(
                capacity=capacity,
                total_tickets=opt_tt,
                booking_limit=opt_bl,
                reservation_lvl=opt_tt - opt_bl,
                f1_price=f1_price, f2_price=f2_price, n_sim=n_sim,
                vdb_voucher=vdb_voucher, idb_cost=idb_cost,
            )

        res     = st.session_state.rm_res
        grid_df = st.session_state.grid_df
        params  = st.session_state.rm_params

        # ── Find optimal ───────────────────────────────────────────
        best_idx  = grid_df["Mean Profit"].idxmax()
        best_row  = grid_df.loc[best_idx]
        best_tt   = int(best_row["Total Tickets"])
        best_bl   = int(best_row["Booking Limit (F2)"])
        best_rl   = int(best_row["Reservation Level (F1)"])
        best_prof = float(best_row["Mean Profit"])
        cur_prof  = res["mean_profit"]
        gain      = best_prof - cur_prof

        # ── Recommendation banner ──────────────────────────────────
        st.markdown(f"""
        <div class="rec-banner green">
            <div class="rec-title">✅ Optimal Settings Found</div>
            <div class="rec-body">Sell <strong>{best_tt}</strong> total tickets with a leisure booking limit of
            <strong>{best_bl}</strong> (F1 reservation level: <strong>{best_rl}</strong>).
            Expected profit: <strong>${best_prof:,.0f}</strong> per flight.</div>
        </div>""", unsafe_allow_html=True)

        # ── Key metrics ────────────────────────────────────────────
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Exp. Profit",      f"${res['mean_profit']:,.0f}",
                  delta=f"±${res['std_profit']:,.0f} std dev")
        c2.metric("Avg F1 Sold",      f"{res['mean_f1_sold']:.1f}",
                  delta=f"of {params['reservation_lvl']} reserved", delta_color="off")
        c3.metric("Oversell Prob.",   f"{res['prob_oversell']*100:.1f}%",
                  delta=f"IDB: {res['prob_idb']*100:.1f}%", delta_color="inverse")
        c4.metric("Avg IDB / Flight", f"{res['mean_idb']:.2f}",
                  delta=f"Avg VDB: {res['mean_vdb']:.2f}", delta_color="off")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Shared plot style ──────────────────────────────────────
        PLOT = dict(paper_bgcolor="white", plot_bgcolor="white",
                    font=dict(family="Outfit", color="#475569", size=12),
                    margin=dict(l=10, r=10, t=28, b=40))
        GRID = dict(showgrid=True, gridcolor="#f1f5f9")
        TICK = dict(tickfont=dict(family="JetBrains Mono", size=11, color="#475569"))
        NGRID = dict(showgrid=False)

        # ── Tabs ──────────────────────────────────────────────────
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📈 Profit Distribution",
            "🔍 Optimizer Grid",
            "👥 Denied Boardings",
            "💰 Revenue Breakdown",
            "📊 Demand & Load",
            "📋 Full Scan Table",
        ])

        # ── TAB 1: Profit Distribution ─────────────────────────────
        with tab1:
            profit = res["profit"]
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=profit, nbinsx=60,
                marker=dict(color="#1e88e5", opacity=0.8, line=dict(color="white", width=0.4)),
                hovertemplate="Profit: $%{x:,.0f}<br>Count: %{y}<extra></extra>",
            ))
            fig.add_vline(x=res["mean_profit"], line=dict(color="#1e3a8a", width=2, dash="dash"),
                          annotation_text=f" Mean = ${res['mean_profit']:,.0f}",
                          annotation_font=dict(color="#1e3a8a", size=12, family="Outfit"))
            fig.update_layout(**PLOT, height=300,
                title=dict(text="Profit Distribution per Flight (at Optimal Settings)", font=dict(size=14, color="#1e3a8a")),
                xaxis=dict(title="Profit ($)", tickprefix="$", **NGRID, **TICK),
                yaxis=dict(title="Number of Flights", **GRID, **TICK),
                showlegend=False, bargap=0.03)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            p95_profit = float(np.percentile(profit, 95))
            p99_profit = float(np.percentile(profit, 99))

            for lbl, val, note, fg in [
                ("Mean expected profit",          f"${res['mean_profit']:,.0f}", "",                                                           "#1e3a8a"),
                ("95th percentile profit",        f"${p95_profit:,.0f}",        "Only 5% of flights earn more than this",                      "#22c55e"),
                ("99th percentile profit",        f"${p99_profit:,.0f}",        "Only 1% of flights earn more than this",                      "#16a34a"),
                ("Optimal total tickets to sell", f"{best_tt} tickets",         "",                                                            "#1e88e5"),
                ("Optimal leisure booking limit", f"{best_bl} (F1 reserve: {best_rl})", "",                                                    "#1e88e5"),
            ]:
                st.markdown(f"""
                <div class="brow">
                    <div>
                        <div>{lbl}</div>
                        {"<div style='font-size:11px;color:#94a3b8;margin-top:2px'>" + note + "</div>" if note else ""}
                    </div>
                    <span style="color:{fg};font-family:'JetBrains Mono',monospace;
                                 font-weight:700;font-size:14px">{val}</span>
                </div>""", unsafe_allow_html=True)

        # ── TAB 2: Optimizer Grid ──────────────────────────────────
        with tab2:
            if grid_df.empty:
                st.info("No valid combinations found in scan range.")
            else:
                # Heatmap of mean profit
                pivot = grid_df.pivot_table(
                    index="Total Tickets", columns="Booking Limit (F2)", values="Mean Profit"
                )
                fig_h = go.Figure(go.Heatmap(
                    z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
                    colorscale="Blues", colorbar=dict(title="Mean Profit ($)"),
                    hovertemplate="Total: %{y}<br>BL(F2): %{x}<br>Profit: $%{z:,.0f}<extra></extra>",
                ))
                # Mark best
                fig_h.add_trace(go.Scatter(
                    x=[best_bl], y=[best_tt], mode="markers",
                    marker=dict(symbol="star", size=18, color="#ef4444",
                                line=dict(color="white", width=1.5)),
                    name="Optimal", showlegend=True,
                    hovertemplate=f"Optimal: TT={best_tt}, BL={best_bl}<extra></extra>",
                ))
                fig_h.update_layout(**{**PLOT, "margin": dict(l=10, r=10, t=10, b=40)},
                    height=380,
                    xaxis=dict(title="Booking Limit for Leisure (F2)", **TICK),
                    yaxis=dict(title="Total Tickets to Sell", **TICK),
                    legend=dict(font=dict(size=12)))
                st.markdown('<div class="sec-lbl">Mean Profit Heatmap — Total Tickets × Booking Limit &nbsp; ⭐ = Optimal</div>', unsafe_allow_html=True)
                st.plotly_chart(fig_h, use_container_width=True, config={"displayModeBar": False})

                # Profit line for best total_tickets level
                best_tt_slice = grid_df[grid_df["Total Tickets"] == best_tt].sort_values("Booking Limit (F2)")
                if not best_tt_slice.empty:
                    fig2 = go.Figure()
                    fig2.add_trace(go.Scatter(
                        x=best_tt_slice["Booking Limit (F2)"], y=best_tt_slice["P95 Profit"],
                        mode="lines", line=dict(width=0), showlegend=False, hoverinfo="skip"))
                    fig2.add_trace(go.Scatter(
                        x=best_tt_slice["Booking Limit (F2)"], y=best_tt_slice["P5 Profit"],
                        mode="lines", line=dict(width=0),
                        fill="tonexty", fillcolor="rgba(30,136,229,0.08)",
                        name="P5–P95 range", hoverinfo="skip"))
                    fig2.add_trace(go.Scatter(
                        x=best_tt_slice["Booking Limit (F2)"], y=best_tt_slice["Mean Profit"],
                        mode="lines+markers", line=dict(color="#1e88e5", width=3),
                        marker=dict(size=6, color="#1e88e5"), name="Mean Profit",
                        hovertemplate="BL=%{x}<br>Profit=$%{y:,.0f}<extra></extra>"))
                    fig2.add_vline(x=best_bl, line=dict(color="#22c55e", width=2),
                                   annotation_text=f" Optimal BL={best_bl}",
                                   annotation_font=dict(color="#22c55e", size=12, family="Outfit"))
                    fig2.add_vline(x=params["booking_limit"], line=dict(color="#f59e0b", width=2, dash="dash"),
                                   annotation_text=f" Current ({params['booking_limit']})",
                                   annotation_font=dict(color="#f59e0b", size=12, family="Outfit"))
                    fig2.update_layout(**{**PLOT, "margin": dict(l=10, r=10, t=10, b=40)}, height=240,
                        xaxis=dict(title="Booking Limit for Leisure (F2)", **NGRID, **TICK),
                        yaxis=dict(title="Expected Profit ($)", tickprefix="$", **GRID, **TICK),
                        legend=dict(font=dict(size=11)))
                    st.markdown(f'<div class="sec-lbl">Profit vs Booking Limit at Total Tickets = {best_tt}</div>', unsafe_allow_html=True)
                    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

        # ── TAB 3: Denied Boardings ────────────────────────────────
        with tab3:
            c1, c2 = st.columns(2)

            with c1:
                # VDB distribution
                vdb_arr = res["vdb"]
                uv, cv = np.unique(vdb_arr, return_counts=True)
                fig3 = go.Figure()
                fig3.add_trace(go.Bar(
                    x=uv, y=cv / len(vdb_arr) * 100,
                    marker_color="#f59e0b", marker_opacity=0.85,
                    hovertemplate="%{x} VDB: %{y:.1f}% of flights<extra></extra>",
                ))
                fig3.update_layout(**PLOT, height=260,
                    title=dict(text="Voluntary Denied Boardings (VDB)",
                               font=dict(size=13, color="#1e3a8a")),
                    xaxis=dict(title="VDB Count", **NGRID, **TICK),
                    yaxis=dict(title="% of Flights", **GRID, **TICK),
                    showlegend=False)
                st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

            with c2:
                # IDB distribution
                idb_arr = res["idb"]
                ui, ci2 = np.unique(idb_arr, return_counts=True)
                fig4 = go.Figure()
                fig4.add_trace(go.Bar(
                    x=ui, y=ci2 / len(idb_arr) * 100,
                    marker_color="#ef4444", marker_opacity=0.85,
                    hovertemplate="%{x} IDB: %{y:.1f}% of flights<extra></extra>",
                ))
                fig4.update_layout(**PLOT, height=260,
                    title=dict(text="Involuntary Denied Boardings (IDB)",
                               font=dict(size=13, color="#1e3a8a")),
                    xaxis=dict(title="IDB Count", **NGRID, **TICK),
                    yaxis=dict(title="% of Flights", **GRID, **TICK),
                    showlegend=False)
                st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

            # Summary rows
            st.markdown("<hr>", unsafe_allow_html=True)
            for lbl, val, fg in [
                ("No oversell (0 VDB, 0 IDB)",  f"{(res['oversell']==0).mean()*100:.1f}% of flights",            "#22c55e"),
                ("Oversold — resolved by VDB",  f"{((res['oversell']>0)&(res['idb']==0)).mean()*100:.1f}% of flights", "#f59e0b"),
                ("Required IDB (≥1)",            f"{(res['idb']>=1).mean()*100:.1f}% of flights",                 "#ef4444"),
                ("Required IDB (≥3)",            f"{(res['idb']>=3).mean()*100:.1f}% of flights",                 "#dc2626"),
            ]:
                st.markdown(f"""
                <div class="brow">
                    <span>{lbl}</span>
                    <span style="color:{fg};font-family:'JetBrains Mono',monospace;
                                 font-weight:700;font-size:14px">{val}</span>
                </div>""", unsafe_allow_html=True)

            # Worst case
            st.markdown("<br>", unsafe_allow_html=True)
            worst_idb_cost = int(idb_arr.max()) * float(idb_cost)
            st.markdown(f"""
            <div style="background:#fef2f2;border:1.5px solid #fca5a5;border-left:5px solid #ef4444;
                        border-radius:10px;padding:16px 18px;">
                <div style="font-size:11px;font-weight:700;color:#991b1b;text-transform:uppercase;
                            letter-spacing:0.08em;margin-bottom:6px">Worst-Case IDB Exposure (single flight)</div>
                <div style="font-size:26px;font-weight:800;color:#dc2626;font-family:'Outfit',sans-serif">
                    ${worst_idb_cost:,.0f}</div>
                <div style="font-size:12px;color:#ef4444;margin-top:4px">
                    {int(idb_arr.max())} IDB × ${float(idb_cost):,.0f} per passenger</div>
            </div>
            """, unsafe_allow_html=True)

        # ── TAB 4: Revenue Breakdown ───────────────────────────────
        with tab4:
            # Stacked waterfall of average profit components
            rev_mean    = float(res["ticket_revenue"].mean())
            refund_mean = float(res["refund_cost"].mean())
            vdb_mean    = float(res["vdb_cost"].mean())
            idb_mean    = float(res["idb_cost"].mean())
            profit_mean = res["mean_profit"]

            fig5 = go.Figure(go.Waterfall(
                name="Profit Bridge",
                orientation="v",
                measure=["absolute", "relative", "relative", "relative", "total"],
                x=["Ticket Revenue", "F1 Refunds", "VDB Vouchers", "IDB Costs", "Net Profit"],
                y=[rev_mean, -refund_mean, -vdb_mean, -idb_mean, profit_mean],
                text=[f"${rev_mean:,.0f}", f"-${refund_mean:,.0f}",
                      f"-${vdb_mean:,.0f}", f"-${idb_mean:,.0f}", f"${profit_mean:,.0f}"],
                textposition="outside",
                connector=dict(line=dict(color="#e2e8f0")),
                increasing=dict(marker=dict(color="#22c55e")),
                decreasing=dict(marker=dict(color="#ef4444")),
                totals=dict(marker=dict(color="#1e88e5")),
            ))
            fig5.update_layout(**PLOT, height=360,
                title=dict(text="Average Profit Bridge (per Flight)", font=dict(size=14, color="#1e3a8a")),
                xaxis=dict(showgrid=False, **TICK),
                yaxis=dict(title="$ per Flight", tickprefix="$", **GRID, **TICK),
                showlegend=False)
            st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})

            # F1 vs F2 revenue split
            f1_rev_mean = float((res["f1_sold"] * float(f1_price)).mean())
            f2_rev_mean = float((res["f2_sold"] * float(f2_price)).mean())
            col1, col2 = st.columns(2)
            with col1:
                fig6 = go.Figure(go.Pie(
                    labels=["F1 Business", "F2 Leisure"],
                    values=[f1_rev_mean, f2_rev_mean],
                    marker_colors=["#1e88e5", "#22c55e"],
                    textinfo="label+percent",
                    hovertemplate="%{label}: $%{value:,.0f}<extra></extra>",
                    hole=0.45,
                ))
                fig6.update_layout(**PLOT, height=280,
                    title=dict(text="Revenue Mix by Fare Class", font=dict(size=13, color="#1e3a8a")))
                st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                for lbl, val, fg in [
                    ("Avg ticket revenue",  f"${rev_mean:,.0f}",    "#1e3a8a"),
                    ("Avg F1 refunds paid", f"-${refund_mean:,.0f}","#ef4444"),
                    ("Avg VDB vouchers",    f"-${vdb_mean:,.0f}",   "#f59e0b"),
                    ("Avg IDB costs",       f"-${idb_mean:,.0f}",   "#dc2626"),
                    ("Avg net profit",      f"${profit_mean:,.0f}", "#22c55e"),
                ]:
                    st.markdown(f"""
                    <div class="brow">
                        <span style="font-weight:600">{lbl}</span>
                        <span style="color:{fg};font-family:'JetBrains Mono',monospace;
                                     font-weight:700;font-size:14px">{val}</span>
                    </div>""", unsafe_allow_html=True)

        # ── TAB 5: Demand & Load Factor ────────────────────────────
        with tab5:
            c1, c2 = st.columns(2)

            with c1:
                st.markdown('<div class="sec-lbl">F1 Business Tickets Sold</div>', unsafe_allow_html=True)
                fig7a = go.Figure()
                fig7a.add_trace(go.Histogram(
                    x=res["f1_sold"], nbinsx=25, name="F1 Sold",
                    marker=dict(color="#1e88e5", opacity=0.82,
                                line=dict(color="white", width=0.4))))
                fig7a.update_layout(**{**PLOT, "margin": dict(l=10, r=10, t=10, b=40)}, height=240,
                    xaxis=dict(title="F1 Tickets Sold", **NGRID, **TICK),
                    yaxis=dict(title="Frequency", **GRID, **TICK),
                    showlegend=False)
                st.plotly_chart(fig7a, use_container_width=True, config={"displayModeBar": False})

            with c2:
                st.markdown('<div class="sec-lbl">F2 Leisure Tickets Sold</div>', unsafe_allow_html=True)
                fig7b = go.Figure()
                fig7b.add_trace(go.Histogram(
                    x=res["f2_sold"], nbinsx=25, name="F2 Sold",
                    marker=dict(color="#22c55e", opacity=0.82,
                                line=dict(color="white", width=0.4))))
                fig7b.update_layout(**{**PLOT, "margin": dict(l=10, r=10, t=10, b=40)}, height=240,
                    xaxis=dict(title="F2 Tickets Sold", **NGRID, **TICK),
                    yaxis=dict(title="Frequency", **GRID, **TICK),
                    showlegend=False)
                st.plotly_chart(fig7b, use_container_width=True, config={"displayModeBar": False})

            with c2:
                # Load factor distribution
                lf = (res["f1_showed"] + res["f2_showed"]) / int(capacity) * 100
                fig8 = go.Figure()
                fig8.add_trace(go.Histogram(
                    x=lf, nbinsx=40,
                    marker=dict(color="#8b5cf6", opacity=0.8,
                                line=dict(color="white", width=0.3)),
                    hovertemplate="Load Factor: %{x:.1f}%<br>Count: %{y}<extra></extra>",
                ))
                fig8.add_vline(x=100, line=dict(color="#ef4444", width=2, dash="dash"),
                               annotation_text=" 100% capacity",
                               annotation_font=dict(color="#ef4444", size=11, family="Outfit"))
                fig8.update_layout(**{**PLOT, "margin": dict(l=10, r=10, t=10, b=40)}, height=240,
                    xaxis=dict(title="Load Factor (%)", ticksuffix="%", **NGRID, **TICK),
                    yaxis=dict(title="Frequency", **GRID, **TICK),
                    showlegend=False)
                st.markdown('<div class="sec-lbl">Load Factor Distribution (% Seats Filled)</div>', unsafe_allow_html=True)
                st.plotly_chart(fig8, use_container_width=True, config={"displayModeBar": False})

            # Showed-up vs capacity
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown('<div class="sec-lbl">Total Show-Ups vs Aircraft Capacity</div>', unsafe_allow_html=True)
            fig9 = go.Figure()
            fig9.add_trace(go.Histogram(
                x=res["total_showed"], nbinsx=45,
                marker=dict(color="#f59e0b", opacity=0.8,
                            line=dict(color="white", width=0.3)),
                hovertemplate="Show-ups: %{x}<br>Count: %{y}<extra></extra>",
            ))
            fig9.add_vline(x=int(capacity), line=dict(color="#ef4444", width=2, dash="dash"),
                           annotation_text=f" Capacity ({int(capacity)})",
                           annotation_font=dict(color="#ef4444", size=12, family="Outfit"))
            fig9.update_layout(**{**PLOT, "margin": dict(l=10, r=10, t=10, b=40)}, height=220,
                xaxis=dict(title="Total Passengers Who Showed Up", **NGRID, **TICK),
                yaxis=dict(title="Frequency", **GRID, **TICK),
                showlegend=False)
            st.plotly_chart(fig9, use_container_width=True, config={"displayModeBar": False})
            st.caption(f"Flights where show-ups exceed {int(capacity)} seats trigger denied boarding procedures.")

        # ── TAB 6: Full Scan Table ─────────────────────────────────
        with tab6:
            st.markdown('<div class="sec-lbl">Full Optimizer Scan Results</div>', unsafe_allow_html=True)
            st.dataframe(
                grid_df.sort_values("Mean Profit", ascending=False),
                use_container_width=True, hide_index=True,
            )
            st.download_button("⬇ Download as CSV",
                               data=grid_df.to_csv(index=False),
                               file_name="rm_optimizer_scan.csv",
                               mime="text/csv",
                               use_container_width=True)

        st.markdown("---")
        st.caption(
            f"Model: Normal demand · Binomial no-show/volunteer sampling · "
            f"{int(n_sim):,} Monte Carlo iterations · "
            f"F1 ${float(f1_price):,.0f} | F2 ${float(f2_price):,.0f} · "
            f"Capacity {int(capacity)} seats"
        )
