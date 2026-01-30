import streamlit as st
import plotly.express as px
from engine import CDCEngine

st.set_page_config(layout="wide", page_title="Epidemiological Command Center")

# Branding
st.title("Advanced CDC-Standard Transmission Model")
st.markdown("Developed by **[Marco Waisman-Garzon](https://www.linkedin.com/in/marco-waisman-garzon/)**")

# Sidebar
with st.sidebar:
    st.header("Parameters")
    pop = st.number_input("Population", value=10000)
    r0 = st.slider("R0", 0.5, 5.0, 2.5)
    v_rate = st.slider("Vax Coverage", 0.0, 1.0, 0.6)
    v_eff = st.slider("Vax Efficacy", 0.0, 1.0, 0.9)
    days = st.slider("Days", 30, 365, 150)

# Execute Engine
engine = CDCEngine(pop, r0, v_rate, v_eff)
data = engine.run_simulation(days, ss_prob=0.05, partial_prot=0.4)

# Plotting
fig = px.area(data, x="Day", y=["I", "P", "V", "S"], 
              title="Stochastic Outbreak Projection",
              color_discrete_map={"I": "#EF553B", "P": "#FECB52", "V": "#00CC96", "S": "#636EFA"})
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)
