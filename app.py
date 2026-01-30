import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# --- THE ENGINE ---
def run_stochastic_sir(N, r0, recovery_rate, days):
    beta = r0 * recovery_rate
    gamma = recovery_rate
    
    # Starting conditions: 1 infected, rest susceptible
    S, I, R = [N-1], [1], [0]
    
    for _ in range(days):
        s_curr, i_curr, r_curr = S[-1], I[-1], R[-1]
        
        # Stochastic transitions using Poisson distribution
        new_infections = np.random.poisson(beta * s_curr * i_curr / N)
        new_recoveries = np.random.poisson(gamma * i_curr)
        
        # Guardrails
        new_infections = min(new_infections, s_curr)
        new_recoveries = min(new_recoveries, i_curr)
        
        S.append(s_curr - new_infections)
        I.append(i_curr + new_infections - new_recoveries)
        R.append(r_curr + new_recoveries)
        
    return pd.DataFrame({"Day": range(days + 1), "Susceptible": S, "Infected": I, "Recovered": R})

# --- THE COCKPIT (Streamlit UI) ---
st.set_page_config(layout="wide", page_title="CDC-Style Pro Model")
st.title("Advanced Transmission Model (CDC Explainer Style)")
st.markdown(
    """
    Developed by **[Marco Waisman-Garzon](https://www.linkedin.com/in/marco-waisman-garzon/)** *Stochastic Engine | Epidemiological Data Systems*
    """, 
    unsafe_allow_html=True
)

# Sidebar Controls
st.sidebar.header("Simulation Parameters")
pop = st.sidebar.number_input("Population Size", value=10000, step=1000)
r0_val = st.sidebar.slider("R0 (Contagiousness)", 0.5, 5.0, 2.5)
rec_rate = st.sidebar.slider("Recovery Rate (1/Days)", 0.05, 0.5, 0.1)
days_to_sim = st.sidebar.slider("Days to Simulate", 30, 365, 150)

# Run Engine
df = run_stochastic_sir(pop, r0_val, rec_rate, days_to_sim)

# Show Results (Visuals)
col1, col2 = st.columns([3, 1])

with col1:
    fig = px.line(df, x="Day", y=["Susceptible", "Infected", "Recovered"], 
                  title="Epidemic Curve", color_discrete_sequence=["#636EFA", "#EF553B", "#00CC96"])
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.metric("Peak Infections", int(df["Infected"].max()))
    st.metric("Final Recovered", int(df["Recovered"].iloc[-1]))
    if st.button("Rerun Simulation"):
        st.rerun()
