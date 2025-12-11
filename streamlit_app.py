import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import random

# DICE-EM! - Stochastic Game Simulation
# A Boston mafia-style color dice game with sinister tweaks
# Developed by: Maria Angela Matubis, Lj Jan Saldivar, Jester Carlo Tapit

st.set_page_config(page_title="DICE-EM!", page_icon="🎲", layout="wide")

# Game configuration
colors = ["Red", "Blue", "Yellow", "Green", "White", "Purple"]
fair_probabilities = [1/6] * 6

# Difficulty levels for tweaked game
DIFFICULTY_LEVELS = {
    "Slightly Rigged": {
        "probabilities": [0.14, 0.172, 0.172, 0.172, 0.172, 0.172],
        "payout_multiplier": 4.9,
        "description": "Barely noticeable... or is it?"
    },
    "Moderately Unfair": {
        "probabilities": [0.12, 0.176, 0.176, 0.176, 0.176, 0.176],
        "payout_multiplier": 4.5,
        "description": "The house is smilin' now"
    },
    "Heavily Stacked": {
        "probabilities": [0.10, 0.18, 0.18, 0.18, 0.18, 0.18],
        "payout_multiplier": 4.0,
        "description": "You're gonna lose, pal"
    },
    "Almost Impossible": {
        "probabilities": [0.05, 0.19, 0.19, 0.19, 0.19, 0.19],
        "payout_multiplier": 3.5,
        "description": "Don't even bother tryin'"
    }
}

# Boston mafia-style captions
MAFIA_CAPTIONS = [
    "Try your luck, you won't have one.",
    "You sure you wanna play?",
    "GO, play it.",
    "You're really testing your luck here.",
    "Good Luck, you're gonna need it.",
    "The house always wins, capisce?",
    "Think you're tough? Prove it.",
    "Your money, my pocket. Let's dance.",
    "Feelin' lucky, punk?",
    "One more roll... what's the worst that could happen?"
]

UNICODE_DICE = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
COLOR_HEX = {
    "Red": "#e74c3c",
    "Blue": "#3b82f6",
    "Yellow": "#facc15",
    "Green": "#10b981",
    "White": "#f8f9fa",
    "Purple": "#9b59b6",
}

# Custom CSS for themes with difficulty-based progression
def load_custom_css(mode, difficulty=None):
    if mode == "Fair":
        # Fun, playful theme
        st.markdown("""
        <style>
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .stButton>button {
            background: linear-gradient(90deg, #56ab2f 0%, #a8e063 100%);
            color: white;
            font-weight: bold;
            border-radius: 20px;
            border: none;
            padding: 12px 24px;
            font-size: 18px;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        h1, h2, h3 {
            color: #ffffff !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .dice-container {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border-radius: 25px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        # Sinister themes that get progressively worse
        if difficulty == "Slightly Rigged":
            # Dark but not too scary yet
            bg_gradient = "linear-gradient(135deg, #2c2c3e 0%, #1f1f2e 50%, #16161e 100%)"
            glow_color = "rgba(200,0,0,0.3)"
            glow_hover = "rgba(200,0,0,0.5)"
            pulse_shadow = "0 0 30px rgba(200,0,0,0.3), inset 0 0 15px rgba(0,0,0,0.7)"
            pulse_shadow_max = "0 0 45px rgba(200,0,0,0.6), inset 0 0 25px rgba(0,0,0,0.8)"
            animation_speed = "2s"
        elif difficulty == "Moderately Unfair":
            # Getting darker and more ominous
            bg_gradient = "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0e17 100%)"
            glow_color = "rgba(255,0,0,0.5)"
            glow_hover = "rgba(255,0,0,0.8)"
            pulse_shadow = "0 0 40px rgba(255,0,0,0.4), inset 0 0 20px rgba(0,0,0,0.8)"
            pulse_shadow_max = "0 0 60px rgba(255,0,0,0.8), inset 0 0 30px rgba(0,0,0,0.9)"
            animation_speed = "1.5s"
        elif difficulty == "Heavily Stacked":
            # Very dark and aggressive
            bg_gradient = "linear-gradient(135deg, #0a0a0a 0%, #1a0000 50%, #000000 100%)"
            glow_color = "rgba(255,20,20,0.7)"
            glow_hover = "rgba(255,0,0,1.0)"
            pulse_shadow = "0 0 50px rgba(255,0,0,0.6), inset 0 0 25px rgba(0,0,0,0.9)"
            pulse_shadow_max = "0 0 80px rgba(255,0,0,1.0), inset 0 0 40px rgba(0,0,0,1.0)"
            animation_speed = "1s"
        else:  # Almost Impossible
            # CHAOS! Maximum darkness and glitchy effects
            bg_gradient = "linear-gradient(135deg, #000000 0%, #0d0000 25%, #1a0000 50%, #0d0000 75%, #000000 100%)"
            glow_color = "rgba(255,0,0,0.9)"
            glow_hover = "rgba(255,50,0,1.0)"
            pulse_shadow = "0 0 70px rgba(255,0,0,0.8), inset 0 0 30px rgba(0,0,0,1.0)"
            pulse_shadow_max = "0 0 100px rgba(255,0,0,1.0), inset 0 0 50px rgba(255,0,0,0.3)"
            animation_speed = "0.7s"
        
        st.markdown(f"""
        <style>
        .main {{
            background: {bg_gradient};
            animation: bg-flicker {animation_speed} infinite;
        }}
        @keyframes bg-flicker {{
            0%, 100% {{ filter: brightness(1); }}
            50% {{ filter: brightness(0.95); }}
        }}
        .stButton>button {{
            background: linear-gradient(90deg, #8b0000 0%, #dc143c 50%, #8b0000 100%);
            color: #ffffff;
            font-weight: bold;
            border-radius: 10px;
            border: 2px solid #ff0000;
            padding: 12px 24px;
            font-size: 18px;
            transition: all 0.3s;
            box-shadow: 0 0 20px {glow_color};
            text-shadow: 0 0 10px {glow_color};
        }}
        .stButton>button:hover {{
            transform: scale(1.05) rotate(2deg);
            box-shadow: 0 0 30px {glow_hover};
            background: linear-gradient(90deg, #dc143c 0%, #8b0000 50%, #dc143c 100%);
        }}
        h1, h2, h3 {{
            color: #ff4444 !important;
            text-shadow: 0 0 10px {glow_color}, 2px 2px 4px rgba(0,0,0,0.8);
            font-family: 'Courier New', monospace;
            animation: text-flicker {animation_speed} infinite;
        }}
        @keyframes text-flicker {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.95; }}
        }}
        .dice-container {{
            background: linear-gradient(135deg, #2d1b1b 0%, #1a0505 100%);
            border: 3px solid #8b0000;
            border-radius: 15px;
            padding: 30px;
            box-shadow: {pulse_shadow};
            animation: sinister-pulse {animation_speed} infinite;
        }}
        @keyframes sinister-pulse {{
            0%, 100% {{ 
                box-shadow: {pulse_shadow};
            }}
            50% {{ 
                box-shadow: {pulse_shadow_max};
                transform: scale(1.01);
            }}
        }}
        .sidebar .sidebar-content {{
            background: linear-gradient(180deg, #1a0505 0%, #0a0000 100%);
        }}
        </style>
        """, unsafe_allow_html=True)


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
if 'mafia_caption' not in st.session_state:
    st.session_state.mafia_caption = random.choice(MAFIA_CAPTIONS)
if 'dice_animation' not in st.session_state:
    st.session_state.dice_animation = False
if 'animation_frames' not in st.session_state:
    st.session_state.animation_frames = []

# Simulation functions
def simulate_game(mode, plays=20000, bet=1.0, difficulty="Slightly Rigged"):
    """Run Monte Carlo simulation"""
    chosen_color = "Red"
    chosen_idx = colors.index(chosen_color)
    p_fair = np.array([1/6.0] * 6)
    
    if mode == "fair":
        probs = p_fair
        payout_net = (1 - p_fair[chosen_idx]) / p_fair[chosen_idx]  # Fair payout = 5.0
    elif mode == "tweaked":
        difficulty_config = DIFFICULTY_LEVELS[difficulty]
        probs = np.array(difficulty_config["probabilities"])
        payout_net = difficulty_config["payout_multiplier"]
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
        "difficulty": difficulty if mode == "tweaked" else "N/A",
        "plays": plays,
        "bet": bet,
        "profits": profits,
        "total": float(total),
        "mean": float(mean),
        "std": float(std),
        "win_rate": float(win_rate),
        "house_edge": float(house_edge),
    }

def play_round(mode, bet_amount, difficulty="Slightly Rigged"):
    """Play one round and return outcome and profit"""
    if mode == "Fair":
        probs = fair_probabilities
        payout_multiplier = 5.0
    else:
        difficulty_config = DIFFICULTY_LEVELS[difficulty]
        probs = difficulty_config["probabilities"]
        payout_multiplier = difficulty_config["payout_multiplier"]
    
    outcome = np.random.choice(colors, p=probs)
    
    if outcome == "Red":
        profit = bet_amount * payout_multiplier - bet_amount
    else:
        profit = -bet_amount
    
    return outcome, profit

def animate_dice(mode, placeholder, num_spins=15):
    """Animate dice rolling"""
    spin_delay = 0.05 if mode == "Fair" else 0.08
    
    for i in range(num_spins):
        # Random dice face and color
        random_idx = np.random.randint(0, 6)
        random_color = colors[random_idx]
        color_bg = COLOR_HEX[random_color]
        
        # More chaotic animation for tweaked mode
        rotation = 0 if mode == "Fair" else random.randint(-15, 15)
        scale = 1.0 if mode == "Fair" else random.uniform(0.95, 1.05)
        
        text_color = '#000' if random_color in ['White', 'Yellow'] else '#fff'
        
        placeholder.markdown(f"""
            <div class="dice-container" style="text-align: center; transform: rotate({rotation}deg) scale({scale}); transition: all 0.1s;">
                <div style="background-color: {color_bg}; border-radius: 20px; padding: 20px; display: inline-block;">
                    <h1 style="font-size: 100px; margin: 0; color: {text_color};">
                        {UNICODE_DICE[random_idx]}
                    </h1>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        time.sleep(spin_delay)
    
    return True

# Title and caption
st.markdown(f"""
    <h1 style='text-align: center; font-size: 72px; margin-bottom: 0;'>
        🎲 DICE-EM! 🎲
    </h1>
    <p style='text-align: center; font-size: 24px; font-style: italic; margin-top: 10px; opacity: 0.9;'>
        "{st.session_state.mafia_caption}"
    </p>
""", unsafe_allow_html=True)

st.markdown("---")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Game Settings")
    
    # Mode selection
    play_mode = st.radio(
        "Choose Your Fate:",
        ["Fair", "Tweaked"],
        help="Fair: Honest game. Tweaked: The house has... advantages."
    )
    
    # Difficulty for tweaked mode
    difficulty = None
    if play_mode == "Tweaked":
        st.markdown("### 😈 Difficulty Level")
        difficulty = st.select_slider(
            "How much pain?",
            options=list(DIFFICULTY_LEVELS.keys()),
            value="Moderately Unfair"
        )
        st.caption(DIFFICULTY_LEVELS[difficulty]["description"])
    
    # Load theme based on mode AND difficulty
    load_custom_css(play_mode, difficulty)
    
    st.markdown("---")
    
    # Bet amount with conditional minimum
    if play_mode == "Tweaked":
        st.warning("⚠️ Minimum bet: $100 (We don't play for pennies here, pal)")
        bet_amount = st.number_input(
            "💰 Bet Amount:",
            min_value=100,
            max_value=10000,
            value=100,
            step=50,
            help="High stakes only for the unfair game!"
        )
    else:
        bet_amount = st.number_input(
            "💰 Bet Amount:",
            min_value=1,
            max_value=1000,
            value=10,
            step=5
        )
    
    st.markdown("---")
    
    # Developer credits
    st.markdown("### 👥 Developed By:")
    st.markdown("""
    - **Maria Angela Matubis**
    - **Lj Jan Saldivar**
    - **Jester Carlo Tapit**
    """)
    
    st.markdown("---")
    st.caption("© 2025 DICE-EM! | Perya Simulation")

tab1, tab2, tab3 = st.tabs(["🎮 Play Now", "📊 Run Simulation", "ℹ️ About"])

# Tab 1: Interactive Play
with tab1:
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.subheader("🎲 Dice Roll Area")
        
        # Dice display area
        dice_placeholder = st.empty()
        result_placeholder = st.empty()
        
        if st.session_state.last_outcome:
            outcome = st.session_state.last_outcome
            idx = colors.index(outcome)
            color_bg = COLOR_HEX[outcome]
            text_color = '#000' if outcome in ['White', 'Yellow'] else '#fff'
            
            dice_placeholder.markdown(f"""
                <div class="dice-container" style="text-align: center;">
                    <div style="background-color: {color_bg}; border-radius: 20px; padding: 30px; display: inline-block; min-width: 200px;">
                        <h1 style="font-size: 120px; margin: 0; color: {text_color};">
                            {UNICODE_DICE[idx]}
                        </h1>
                        <h2 style="margin: 10px 0; color: {text_color}; font-size: 32px;">
                            {outcome}
                        </h2>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.last_profit > 0:
                result_placeholder.success(f" WINNER! You won ${st.session_state.last_profit:.2f}!", icon="💰")
            else:
                result_placeholder.error(f" YOU LOSE! Lost ${abs(st.session_state.last_profit):.2f}", icon="😈")
        else:
            dice_placeholder.markdown("""
                <div class="dice-container" style="text-align: center;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; padding: 30px; display: inline-block; min-width: 200px;">
                        <h1 style="font-size: 120px; margin: 0; color: white;">
                            ⚀
                        </h1>
                        <h2 style="margin: 10px 0; color: white; font-size: 24px;">
                            Ready to roll?
                        </h2>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # Action buttons
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🎲 ROLL THE DICE", type="primary", use_container_width=True):
                # Animate dice
                animate_dice(play_mode, dice_placeholder, num_spins=15 if play_mode == "Fair" else 20)
                
                # Play round
                outcome, profit = play_round(play_mode, bet_amount, difficulty if difficulty else "Slightly Rigged")
                st.session_state.last_outcome = outcome
                st.session_state.last_profit = profit
                st.session_state.total_profit += profit
                st.session_state.plays += 1
                st.session_state.history.append(profit)
                st.session_state.outcome_history.append(outcome)
                st.rerun()
        
        with col_btn2:
            if st.button("🔄 Reset Game", use_container_width=True):
                st.session_state.total_profit = 0.0
                st.session_state.plays = 0
                st.session_state.history = []
                st.session_state.outcome_history = []
                st.session_state.last_outcome = None
                st.session_state.last_profit = None
                st.session_state.mafia_caption = random.choice(MAFIA_CAPTIONS)
                st.rerun()
    
    with col_right:
        st.subheader("📊 Your Stats")
        
        # Metrics
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Total Plays", st.session_state.plays)
        with col_m2:
            profit_delta = f"${st.session_state.last_profit:.2f}" if st.session_state.last_profit else None
            st.metric("Total Profit", f"${st.session_state.total_profit:.2f}", delta=profit_delta)
        
        # Show history charts
        if len(st.session_state.history) > 1:
            st.markdown("#### 📈 Performance")
            
            # Cumulative profit
            fig, ax = plt.subplots(figsize=(6, 3))
            cumulative = np.cumsum(st.session_state.history)
            ax.plot(cumulative, linewidth=2, color='#e74c3c' if cumulative[-1] < 0 else '#10b981')
            ax.axhline(y=0, color='white', linestyle='--', alpha=0.5)
            ax.set_title("Cumulative Profit", fontsize=12, color='white')
            ax.set_xlabel("Play Number", fontsize=10, color='white')
            ax.set_ylabel("Total Profit ($)", fontsize=10, color='white')
            ax.set_facecolor('#1a1a2e' if play_mode == "Tweaked" else '#667eea')
            fig.patch.set_facecolor('none')
            ax.tick_params(colors='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(alpha=0.2, color='white')
            st.pyplot(fig)
            plt.close()
            
            # Win/Loss distribution
            wins = sum(1 for p in st.session_state.history if p > 0)
            losses = sum(1 for p in st.session_state.history if p <= 0)
            
            st.markdown("#### 🎯 Win/Loss Ratio")
            col_w, col_l = st.columns(2)
            with col_w:
                st.metric("Wins", wins, f"{wins/len(st.session_state.history)*100:.1f}%")
            with col_l:
                st.metric("Losses", losses, f"{losses/len(st.session_state.history)*100:.1f}%")
        else:
            st.info("Roll the dice to start tracking your stats!")


# Tab 2: Monte Carlo Simulation
with tab2:
    st.header("📊 Monte Carlo Simulation & Analysis")
    st.markdown("Run thousands of simulated plays to analyze the house edge and compare outcomes.")
    
    # Simulation settings in columns
    col_sim1, col_sim2, col_sim3 = st.columns(3)
    
    with col_sim1:
        num_plays = st.slider("Number of plays:", 1000, 100000, 20000, 1000)
    
    with col_sim2:
        sim_bet = st.number_input("Bet per play:", min_value=0.1, max_value=100.0, value=1.0, step=0.5)
    
    with col_sim3:
        sim_difficulty = st.selectbox("Tweaked Difficulty:", list(DIFFICULTY_LEVELS.keys()), index=1)
    
    if st.button("▶️ Run Full Simulation", type="primary", use_container_width=True):
        with st.spinner("Running Monte Carlo simulations... The house is counting your money."):
            fair_results = simulate_game("fair", plays=num_plays, bet=sim_bet)
            tweaked_results = simulate_game("tweaked", plays=num_plays, bet=sim_bet, difficulty=sim_difficulty)
            
            st.session_state.fair_sim = fair_results
            st.session_state.tweaked_sim = tweaked_results
        st.success("✅ Simulation complete! Check the results below.")
        st.rerun()
    
    if 'fair_sim' in st.session_state and 'tweaked_sim' in st.session_state:
        st.markdown("---")
        st.subheader("🎯 Simulation Results")
        
        # Summary metrics
        col_fair, col_tweaked = st.columns(2)
        
        with col_fair:
            st.markdown("### 🟢 Fair Game")
            fair = st.session_state.fair_sim
            
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.metric("Win Rate", f"{fair['win_rate']*100:.2f}%")
                st.metric("Mean Profit/Play", f"${fair['mean']:.4f}")
            with metric_col2:
                st.metric("House Edge", f"{fair['house_edge']*100:.4f}%")
                st.metric("Total Profit", f"${fair['total']:.2f}")
            
            st.caption(f"Standard Deviation: ${fair['std']:.4f}")
            st.caption(f"Plays: {fair['plays']:,}")
        
        with col_tweaked:
            st.markdown("### 🔴 Tweaked Game")
            tweaked = st.session_state.tweaked_sim
            
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.metric("Win Rate", f"{tweaked['win_rate']*100:.2f}%")
                st.metric("Mean Profit/Play", f"${tweaked['mean']:.4f}")
            with metric_col2:
                st.metric("House Edge", f"{tweaked['house_edge']*100:.4f}%", 
                         delta=f"{(tweaked['house_edge'] - fair['house_edge'])*100:.4f}%")
                st.metric("Total Profit", f"${tweaked['total']:.2f}")
            
            st.caption(f"Standard Deviation: ${tweaked['std']:.4f}")
            st.caption(f"Difficulty: {tweaked['difficulty']}")
        
        st.markdown("---")
        
        # Visualizations
        tab_hist, tab_cum, tab_compare = st.tabs(["📊 Distribution", "📈 Cumulative", "⚖️ Comparison"])
        
        with tab_hist:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
            fig.patch.set_facecolor('#1a1a2e' if play_mode == "Tweaked" else '#f0f2f6')
            
            # Fair game histogram
            ax1.hist(fair['profits'], bins=40, alpha=0.8, color='#10b981', edgecolor='black')
            ax1.set_title("Fair Game - Profit Distribution", fontsize=14, color='white' if play_mode == "Tweaked" else 'black')
            ax1.set_xlabel("Profit per Play ($)", fontsize=11, color='white' if play_mode == "Tweaked" else 'black')
            ax1.set_ylabel("Frequency", fontsize=11, color='white' if play_mode == "Tweaked" else 'black')
            ax1.axvline(fair['mean'], color='darkgreen', linestyle='--', linewidth=2, label=f"Mean: ${fair['mean']:.4f}")
            ax1.legend()
            ax1.set_facecolor('#16213e' if play_mode == "Tweaked" else 'white')
            ax1.tick_params(colors='white' if play_mode == "Tweaked" else 'black')
            ax1.grid(alpha=0.3, color='white' if play_mode == "Tweaked" else 'gray')
            
            # Tweaked game histogram
            ax2.hist(tweaked['profits'], bins=40, alpha=0.8, color='#e74c3c', edgecolor='black')
            ax2.set_title("Tweaked Game - Profit Distribution", fontsize=14, color='white' if play_mode == "Tweaked" else 'black')
            ax2.set_xlabel("Profit per Play ($)", fontsize=11, color='white' if play_mode == "Tweaked" else 'black')
            ax2.set_ylabel("Frequency", fontsize=11, color='white' if play_mode == "Tweaked" else 'black')
            ax2.axvline(tweaked['mean'], color='darkred', linestyle='--', linewidth=2, label=f"Mean: ${tweaked['mean']:.4f}")
            ax2.legend()
            ax2.set_facecolor('#16213e' if play_mode == "Tweaked" else 'white')
            ax2.tick_params(colors='white' if play_mode == "Tweaked" else 'black')
            ax2.grid(alpha=0.3, color='white' if play_mode == "Tweaked" else 'gray')
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        
        with tab_cum:
            fig, ax = plt.subplots(figsize=(14, 6))
            fig.patch.set_facecolor('#1a1a2e' if play_mode == "Tweaked" else '#f0f2f6')
            
            ax.plot(np.cumsum(fair['profits']), label='Fair Game', linewidth=2.5, color='#10b981', alpha=0.9)
            ax.plot(np.cumsum(tweaked['profits']), label='Tweaked Game', linewidth=2.5, color='#e74c3c', alpha=0.9)
            ax.axhline(y=0, color='white' if play_mode == "Tweaked" else 'gray', linestyle='--', alpha=0.7)
            ax.set_title("Cumulative Profit Over Time", fontsize=16, color='white' if play_mode == "Tweaked" else 'black')
            ax.set_xlabel("Play Number", fontsize=12, color='white' if play_mode == "Tweaked" else 'black')
            ax.set_ylabel("Total Profit ($)", fontsize=12, color='white' if play_mode == "Tweaked" else 'black')
            ax.legend(fontsize=12)
            ax.set_facecolor('#16213e' if play_mode == "Tweaked" else 'white')
            ax.tick_params(colors='white' if play_mode == "Tweaked" else 'black')
            ax.grid(alpha=0.3, color='white' if play_mode == "Tweaked" else 'gray')
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        
        with tab_compare:
            # Summary table
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
            
            st.markdown("### 🎯 Analysis")
            house_edge_diff = (tweaked['house_edge'] - fair['house_edge']) * 100
            total_diff = tweaked['total'] - fair['total']
            
            st.write(f"""
            **Key Findings:**
            
            - 💰 **House Edge Difference**: {house_edge_diff:.4f}%
            - 🎰 The tweaked game (**{tweaked['difficulty']}**) creates a **{abs(house_edge_diff):.2f}% advantage** for the house
            - 💸 Over **{num_plays:,}** plays with **${sim_bet}** bets, the house gains approximately **${abs(total_diff):.2f}** more
            - 📉 Win rate drops from **{fair['win_rate']*100:.2f}%** to **{tweaked['win_rate']*100:.2f}%**
            - ⚠️ The tweaked model maintains variance (occasional wins) but shifts mean payout negatively
            - 🏦 **Bottom line**: The house always wins in the long run
            """)
    else:
        st.info("👆 Configure simulation parameters and click 'Run Full Simulation' to see results")


# Tab 3: About
with tab3:
    st.header("About DICE-EM!")
    
    col_about1, col_about2 = st.columns([2, 1])
    
    with col_about1:
        st.markdown("""
        ### 🎲 The Game That Always Wins (For Us)
        
        Welcome to **DICE-EM!** - a Boston mafia-style simulation of a Filipino "perya" color game. 
        We're here to show you exactly how the house *always* wins. Capisce?
        
        #### 🎯 Game Mechanics:
        
        - **Six colors**: Red, Blue, Yellow, Green, White, Purple
        - **You bet on Red** (because we said so)
        - **Match the color?** You win. **Don't match?** We take your money.
        - Simple. Brutal. Profitable (for us).
        
        #### 🟢 Fair Game (The Honest One):
        - Equal probability: 16.67% for each color
        - Fair payout: 5:1 (bet $10, win $50, net +$40)
        - Expected value: $0 (neither you nor the house makes money... in theory)
        - **Reality check**: It's fair, but you'll still probably lose
        
        #### 🔴 Tweaked Game (The Real Deal):
        Multiple difficulty levels, each worse than the last:
        
        - **Slightly Rigged**: You might not even notice... at first
        - **Moderately Unfair**: Now the house is smilin'
        - **Heavily Stacked**: You're gonna lose, pal
        - **Almost Impossible**: Don't even bother tryin'
        
        Each level reduces your winning probability and/or payout. We're in the money-making business, 
        and business is *good*.
        
        #### 🔬 The Science of Losing:
        
        This project demonstrates:
        - **Probability Theory**: How we stack the deck
        - **Monte Carlo Simulation**: Proof that you'll lose in the long run
        - **House Edge**: The mathematical guarantee that we win
        - **Stochastic Systems**: Fancy words for "random, but we still win"
        
        #### 💡 Educational Value:
        
        Learn about:
        - Why casinos and perya operators never go broke
        - How small tweaks create massive advantages
        - The Law of Large Numbers (spoiler: it favors us)
        - Variance vs Expected Value (you might win once, but keep playing...)
        
        ---
        
        ### 🎓 Project Details:
        
        **Course**: Stochastic Systems & Monte Carlo Simulation  
        **Focus**: Probabilistic modeling, house edge analysis, exploratory data analysis  
        **Technologies**: Python, Streamlit, NumPy, Pandas, Matplotlib
        
        """)
    
    with col_about2:
        st.markdown("### 👥 The Developers")
        st.markdown("""
        This masterpiece was created by:
        
        - **Maria Angela Matubis**
        - **Lj Jan Saldivar**
        - **Jester Carlo Tapit**
        
        ---
        
        ### 📚 Features:
        
        ✅ Interactive gameplay  
        ✅ Animated dice rolling  
        ✅ Multiple difficulty levels  
        ✅ Monte Carlo simulation  
        ✅ Statistical analysis  
        ✅ Fair vs Tweaked comparison  
        ✅ Boston mafia attitude  
        ✅ Responsive design  
        
        ---
        
        ### 🎨 Design Philosophy:
        
        **Fair Mode**: Fun, colorful, playful - like a real carnival game should be
        
        **Tweaked Mode**: Dark, sinister, foreboding - because that's what rigged games feel like
        
        ---
        
        ### ⚠️ Disclaimer:
        
        This is an educational simulation. No real money is involved. 
        
        But if it were... we'd be rich by now. 😈
        
        ---
        
        ### 🏆 Learning Outcomes:
        
        - Understanding probability distributions
        - Monte Carlo methods
        - Statistical significance
        - Risk assessment
        - Why you shouldn't gamble
        
        """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h3>🎲 DICE-EM! 🎲</h3>
        <p><i>"The house always wins, capisce?"</i></p>
        <p>© 2025 | Developed by Maria Angela Matubis, Lj Jan Saldivar & Jester Carlo Tapit</p>
        <p>Stochastic Systems Project | For Educational Purposes</p>
    </div>
""", unsafe_allow_html=True)

