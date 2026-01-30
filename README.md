# Advanced CDC-Standard Transmission Model
### Developed by [Marco Waisman-Garzon](https://www.linkedin.com/in/marco-waisman-garzon/)
## https://pathogen-sim.streamlit.app/

An interactive epidemiological dashboard built with a modular Python architecture. This simulator implements a stochastic SVIPR model to project disease dynamics based on vaccination rates, waning immunity, and super-spreader events.

## Key Features
- **Modular Engine:** Separates mathematical simulation (`engine.py`) from the UI (`app.py`).
- **Stochastic Modeling:** Uses Poisson distributions to account for real-world uncertainty.
- **CDC Alignment:** Implements stratified compartments for Vaccinated (V) and Partially Immune (P) populations.

## Installation & Usage
1. Clone the repo: `git clone https://github.com/YOUR_USERNAME/pathogen-sim`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the dashboard: `streamlit run app.py`

## Methodology
This model follows the CDC’s Transmission Model Explainer, moving beyond basic SIR logic by incorporating:
- **Vaccine Efficacy:** Adjustable multipliers for reduced susceptibility.
- **Waning Immunity:** A time-decay function from fully protected to partial immunity.
- **Super-spreader Events:** Probability-based spikes in the base R0 value.
