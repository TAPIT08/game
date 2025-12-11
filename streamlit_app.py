import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time

# Streamlit Color Dice Game
# - Interactive play mode with animated dice
# - Monte Carlo simulation mode with analysis
# - Fair vs Tweaked game modes

st.set_page_config(page_title="Color Dice Game", page_icon="🎲", layout="wide")

# Game configuration
colors = ["Red", "Blue", "Yellow", "Green", "White", "Purple"]
fair_probabilities = [1/6] * 6
tweaked_probabilities = [0.13, 0.174, 0.174, 0.174, 0.174, 0.174]

UNICODE_DICE = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
COLOR_HEX = {
    "Red": "#e74c3c",
    "Blue": "#3b82f6",
    "Yellow": "#facc15",
    "Green": "#10b981",
    "White": "#f8f9fa",
    "Purple": "#9b59b6",
}

# Initialize session state
if 'total_profit' not in st.session_state:
    st.session_state.total_profit = 0.0
if 'plays' not in st.session_state:
    st.session_state.plays = 0
if 'history' not in st.session_state:
    st.session_state.history = []
if 'outcome_history' not in st.session_state:
    st.session_state.outcome_history = []
if 'last_outcome' not in st.session_state:
    st.session_state.last_outcome = None
if 'last_profit' not in st.session_state:
    st.session_state.last_profit = None

# Simulation functions
def simulate_game(mode, plays=20000, bet=1.0, tweak_type="payout"):
    """Run Monte Carlo simulation"""
    chosen_color = "Red"
    chosen_idx = colors.index(chosen_color)
    p_fair = np.array([1/6.0] * 6)
    
    if mode == "fair":
        probs = p_fair
        payout_net = (1 - p_fair[chosen_idx]) / p_fair[chosen_idx]  # Fair payout = 5.0
    elif mode == "tweaked":
        if tweak_type == "payout":
            probs = p_fair
            payout_net = 4.8  # Slightly lower payout
        else:  # prob tweak
            probs = np.array([0.2] + [0.8 / 5.0] * 5)  # Red has 20% chance
            payout_net = (1 - probs[chosen_idx]) / probs[chosen_idx]
    else:
        raise ValueError("Unknown mode")
    
    outcomes = np.random.choice(len(probs), size=plays, p=probs)
    wins = outcomes == chosen_idx
    profits = np.where(wins, payout_net * bet, -bet)
    
    total = profits.sum()
    mean = profits.mean()
    std = profits.std()
    win_rate = (profits > 0).mean()
    house_edge = -mean / bet
    
    return {
        "mode": mode,
        "tweak": tweak_type,
        "plays": plays,
        "bet": bet,
        "profits": profits,
        "total": float(total),
        "mean": float(mean),
        "std": float(std),
        "win_rate": float(win_rate),
        "house_edge": float(house_edge),
    }

def play_round(mode, bet_amount):
    """Play one round and return outcome and profit"""
    probs = fair_probabilities if mode == "Fair" else tweaked_probabilities
    outcome = np.random.choice(colors, p=probs)
    
    if outcome == "Red":
        payout_multiplier = 2.0 if mode == "Fair" else 1.9
        profit = bet_amount * payout_multiplier - bet_amount
    else:
        profit = -bet_amount
    
    return outcome, profit

# Title and tabs
st.title("🎲 Color Dice Game: Perya Simulation")
st.markdown("### Stochastic Game Simulation - Fair vs Tweaked Models")

tab1, tab2, tab3 = st.tabs(["🎮 Interactive Play", "📊 Monte Carlo Simulation", "ℹ️ About"])

# Tab 1: Interactive Play
with tab1:
    st.header("Play the Color Dice Game")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Game Settings")
        play_mode = st.radio("Game Mode:", ["Fair", "Tweaked"], 
                             help="Fair: Equal odds. Tweaked: House edge via reduced payout.")
        bet_amount = st.number_input("Bet Amount:", min_value=1, max_value=1000, value=10, step=5)
        
        if st.button("🎲 Roll Dice", type="primary", use_container_width=True):
            outcome, profit = play_round(play_mode, bet_amount)
            st.session_state.last_outcome = outcome
            st.session_state.last_profit = profit
            st.session_state.total_profit += profit
            st.session_state.plays += 1
            st.session_state.history.append(profit)
            st.session_state.outcome_history.append(outcome)
            st.rerun()
        
        if st.button("🔄 Reset Game", use_container_width=True):
            st.session_state.total_profit = 0.0
            st.session_state.plays = 0
            st.session_state.history = []
            st.session_state.outcome_history = []
            st.session_state.last_outcome = None
            st.session_state.last_profit = None
            st.rerun()
        
        st.divider()
        st.metric("Total Plays", st.session_state.plays)
        st.metric("Total Profit", f"${st.session_state.total_profit:.2f}", 
                 delta=f"${st.session_state.last_profit:.2f}" if st.session_state.last_profit else None)
    
    with col2:
        st.subheader("Dice Result")
        
        if st.session_state.last_outcome:
            outcome = st.session_state.last_outcome
            idx = colors.index(outcome)
            color_bg = COLOR_HEX[outcome]
            
            # Display large dice with color background
            st.markdown(f"""
                <div style="text-align: center; padding: 40px; background-color: {color_bg}; 
                            border-radius: 20px; margin: 20px 0;">
                    <h1 style="font-size: 120px; margin: 0; 
                               color: {'#000' if outcome in ['White', 'Yellow'] else '#fff'};">
                        {UNICODE_DICE[idx]}
                    </h1>
                    <h2 style="margin: 10px 0; 
                               color: {'#000' if outcome in ['White', 'Yellow'] else '#fff'};">
                        {outcome}
                    </h2>
                </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.last_profit > 0:
                st.success(f"🎉 You won ${st.session_state.last_profit:.2f}!")
            else:
                st.error(f"😢 You lost ${abs(st.session_state.last_profit):.2f}")
        else:
            st.info("Click 'Roll Dice' to start playing!")
        
        # Show history charts if available
        if len(st.session_state.history) > 1:
            st.subheader("Your Game History")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                # Cumulative profit chart
                fig, ax = plt.subplots(figsize=(5, 3))
                ax.plot(np.cumsum(st.session_state.history), linewidth=2)
                ax.set_title("Cumulative Profit", fontsize=10)
                ax.set_xlabel("Play Number", fontsize=9)
                ax.set_ylabel("Total Profit ($)", fontsize=9)
                ax.grid(alpha=0.3)
                st.pyplot(fig)
                plt.close()
            
            with col_b:
                # Profit distribution
                fig, ax = plt.subplots(figsize=(5, 3))
                ax.hist(st.session_state.history, bins=12, alpha=0.7, color='steelblue')
                ax.set_title("Profit Distribution", fontsize=10)
                ax.set_xlabel("Profit per Play ($)", fontsize=9)
                ax.set_ylabel("Frequency", fontsize=9)
                ax.grid(alpha=0.3)
                st.pyplot(fig)
                plt.close()

# Tab 2: Monte Carlo Simulation
with tab2:
    st.header("Monte Carlo Simulation & Analysis")
    st.markdown("Run thousands of simulated plays to analyze the house edge and compare fair vs tweaked models.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Simulation Parameters")
        num_plays = st.slider("Number of plays:", 1000, 100000, 20000, 1000)
        sim_bet = st.number_input("Bet per play:", min_value=0.1, max_value=100.0, value=1.0, step=0.5)
        tweak_mode = st.selectbox("Tweak Type:", ["payout", "prob"], 
                                   help="Payout: Reduce payout. Prob: Weighted probabilities.")
        
        if st.button("▶️ Run Simulation", type="primary", use_container_width=True):
            with st.spinner("Running simulations..."):
                fair_results = simulate_game("fair", plays=num_plays, bet=sim_bet, tweak_type=tweak_mode)
                tweaked_results = simulate_game("tweaked", plays=num_plays, bet=sim_bet, tweak_type=tweak_mode)
                
                st.session_state.fair_sim = fair_results
                st.session_state.tweaked_sim = tweaked_results
            st.success("✅ Simulation complete!")
            st.rerun()
    
    with col2:
        if 'fair_sim' in st.session_state and 'tweaked_sim' in st.session_state:
            st.subheader("Simulation Results")
            
            # Summary metrics
            col_fair, col_tweaked = st.columns(2)
            
            with col_fair:
                st.markdown("#### 🟢 Fair Game")
                fair = st.session_state.fair_sim
                st.metric("Win Rate", f"{fair['win_rate']*100:.2f}%")
                st.metric("Mean Profit/Play", f"${fair['mean']:.4f}")
                st.metric("House Edge", f"{fair['house_edge']*100:.4f}%")
                st.metric("Total Profit", f"${fair['total']:.2f}")
                st.caption(f"Std Dev: ${fair['std']:.4f}")
            
            with col_tweaked:
                st.markdown("#### 🔴 Tweaked Game")
                tweaked = st.session_state.tweaked_sim
                st.metric("Win Rate", f"{tweaked['win_rate']*100:.2f}%")
                st.metric("Mean Profit/Play", f"${tweaked['mean']:.4f}")
                st.metric("House Edge", f"{tweaked['house_edge']*100:.4f}%", 
                         delta=f"{(tweaked['house_edge'] - fair['house_edge'])*100:.4f}%")
                st.metric("Total Profit", f"${tweaked['total']:.2f}")
                st.caption(f"Std Dev: ${tweaked['std']:.4f}")
            
            st.divider()
            
            # Visualizations
            st.subheader("📈 Comparative Analysis")
            
            tab_hist, tab_cum, tab_compare = st.tabs(["Profit Distribution", "Cumulative Profit", "Side-by-Side"])
            
            with tab_hist:
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
                
                ax1.hist(fair['profits'], bins=40, alpha=0.7, color='green', edgecolor='black')
                ax1.set_title(f"Fair Game - Profit Distribution")
                ax1.set_xlabel("Profit per Play ($)")
                ax1.set_ylabel("Frequency")
                ax1.axvline(fair['mean'], color='darkgreen', linestyle='--', linewidth=2, label=f"Mean: ${fair['mean']:.4f}")
                ax1.legend()
                ax1.grid(alpha=0.3)
                
                ax2.hist(tweaked['profits'], bins=40, alpha=0.7, color='red', edgecolor='black')
                ax2.set_title(f"Tweaked Game - Profit Distribution")
                ax2.set_xlabel("Profit per Play ($)")
                ax2.set_ylabel("Frequency")
                ax2.axvline(tweaked['mean'], color='darkred', linestyle='--', linewidth=2, label=f"Mean: ${tweaked['mean']:.4f}")
                ax2.legend()
                ax2.grid(alpha=0.3)
                
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            
            with tab_cum:
                fig, ax = plt.subplots(figsize=(12, 5))
                
                ax.plot(np.cumsum(fair['profits']), label='Fair Game', linewidth=2, color='green', alpha=0.8)
                ax.plot(np.cumsum(tweaked['profits']), label='Tweaked Game', linewidth=2, color='red', alpha=0.8)
                ax.set_title("Cumulative Profit Over Time")
                ax.set_xlabel("Play Number")
                ax.set_ylabel("Total Profit ($)")
                ax.legend()
                ax.grid(alpha=0.3)
                
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            
            with tab_compare:
                # Summary comparison table
                comparison_df = pd.DataFrame({
                    'Metric': ['Plays', 'Win Rate (%)', 'Mean Profit/Play ($)', 
                              'Std Dev ($)', 'House Edge (%)', 'Total Profit ($)'],
                    'Fair Game': [
                        f"{fair['plays']:,}",
                        f"{fair['win_rate']*100:.2f}",
                        f"{fair['mean']:.4f}",
                        f"{fair['std']:.4f}",
                        f"{fair['house_edge']*100:.4f}",
                        f"{fair['total']:.2f}"
                    ],
                    'Tweaked Game': [
                        f"{tweaked['plays']:,}",
                        f"{tweaked['win_rate']*100:.2f}",
                        f"{tweaked['mean']:.4f}",
                        f"{tweaked['std']:.4f}",
                        f"{tweaked['house_edge']*100:.4f}",
                        f"{tweaked['total']:.2f}"
                    ]
                })
                
                st.dataframe(comparison_df, use_container_width=True, hide_index=True)
                
                st.markdown("### 🎯 Key Findings")
                house_edge_diff = (tweaked['house_edge'] - fair['house_edge']) * 100
                st.write(f"""
                - **House Edge Difference**: {house_edge_diff:.4f}% 
                - The tweaked game creates a **{abs(house_edge_diff):.2f}% advantage** for the house
                - Over {num_plays:,} plays with ${sim_bet} bets, this translates to 
                  **${tweaked['total'] - fair['total']:.2f}** more profit for the house
                - The tweaked model maintains similar variance but shifts the mean payout negatively
                """)
        else:
            st.info("👆 Configure simulation parameters and click 'Run Simulation' to see results")

# Tab 3: About
with tab3:
    st.header("About This Simulation")
    
    st.markdown("""
    ### 🎲 Stochastic Game Simulation - Color Dice Game
    
    This project models a Filipino "perya" or casino-style **Color Game** where players bet on dice outcomes.
    
    #### Game Rules:
    1. **Six colored dice faces**: Red, Blue, Yellow, Green, White, Purple
    2. **Player bets** on one color (default: Red)
    3. **Dice rolls** - if it matches the bet, player wins; otherwise, loses the bet
    4. **Payout**: Fair game pays 5:1 (net +5× bet), Tweaked game pays 4.8:1 (net +4.8× bet)
    
    #### 🔬 Project Components:
    
    **1. Fair Game Model**
    - Equal probability for each color (16.67%)
    - Fair payout structure (5:1) ensuring zero house edge
    - Expected value ≈ 0 for player
    
    **2. Tweaked Game Model**
    Two tweak options:
    - **Payout Tweak**: Keep fair probabilities but reduce payout to 4.8:1
    - **Probability Tweak**: Increase Red probability to 20% while adjusting payout accordingly
    
    **3. Monte Carlo Simulation**
    - Run 10,000+ plays to generate statistical data
    - Analyze win rates, mean returns, variance, and house edge
    - Visualize profit distributions and cumulative outcomes
    
    **4. Exploratory Data Analysis (EDA)**
    - Compare fair vs tweaked game outcomes
    - Quantify house edge impact
    - Show how small tweaks create long-term profit for the house
    
    #### 📊 Key Insights:
    
    - Even small changes (5:1 → 4.8:1 payout) create significant house edge
    - The Law of Large Numbers ensures house profitability over many plays
    - Variance allows occasional player wins but mean converges to house advantage
    - Visualization shows how cumulative profit diverges between fair and tweaked models
    
    #### 🛠️ Technologies:
    - **Streamlit**: Interactive web interface
    - **NumPy**: Probability simulation and random sampling
    - **Matplotlib**: Data visualization
    - **Pandas**: Data analysis and tabulation
    
    ---
    
    **Created for**: Stochastic Systems & Monte Carlo Simulation Project  
    **Focus**: Probabilistic modeling, house edge analysis, and EDA
    """)

# Footer
st.divider()
st.caption("🎲 Color Dice Game | Stochastic Simulation Project | Built with Streamlit")
