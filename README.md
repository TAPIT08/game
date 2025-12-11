# 🎲 Color Dice Game - Stochastic Simulation

A web-based simulation of a Filipino "perya" (carnival) Color Game that demonstrates probabilistic systems, Monte Carlo simulation, and house edge analysis.

## 🎯 Project Overview

This project models and compares two versions of a simple dice-based casino game:
1. **Fair Game**: Equal odds for player and house (zero expected house edge)
2. **Tweaked Game**: Subtle modifications that create a house advantage

## 🚀 Features

### Interactive Play Mode
- 🎮 Real-time dice rolling with animated results
- 💰 Track your profit/loss over multiple plays
- 📊 Live charts showing cumulative profit and distribution
- ⚙️ Switch between Fair and Tweaked game modes

### Monte Carlo Simulation
- 🔢 Run 1,000 to 100,000+ simulated plays
- 📈 Statistical analysis: win rates, mean returns, house edge
- 📉 Comparative visualizations (histograms, cumulative profit)
- 🎯 Quantify the impact of game "tweaks"

### Educational Analysis
- 📚 Detailed explanation of game mechanics
- 🔬 EDA (Exploratory Data Analysis) of simulation results
- 💡 Insights into how small changes create house advantage
- 📊 Side-by-side comparison of fair vs tweaked outcomes

## 🛠️ Installation

### Local Setup

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Open your browser** to `http://localhost:8501`

### Python Requirements
- Python 3.8 or higher
- NumPy, Pandas, Matplotlib, Streamlit (see requirements.txt)

## 🎲 How to Use

### Interactive Play
1. Navigate to the **"Interactive Play"** tab
2. Select game mode (Fair or Tweaked)
3. Set your bet amount
4. Click "Roll Dice" to play
5. View your results and statistics

### Monte Carlo Simulation
1. Navigate to the **"Monte Carlo Simulation"** tab
2. Configure:
   - Number of plays (1,000 - 100,000)
   - Bet amount per play
   - Tweak type (payout reduction or probability weighting)
3. Click "Run Simulation"
4. Analyze comparative results and visualizations

## 📊 Game Mechanics

### Rules
- Six possible outcomes (colors): Red, Blue, Yellow, Green, White, Purple
- Player always bets on **Red**
- If Red appears, player wins; otherwise, loses the bet

### Fair Game
- **Probability**: 1/6 (≈16.67%) for each color
- **Payout**: 5:1 (net profit = 5× bet)
- **Expected Value**: $0 (zero house edge)

### Tweaked Game (Payout Mode)
- **Probability**: 1/6 (same as fair)
- **Payout**: 4.8:1 (reduced from 5:1)
- **House Edge**: ~4% (player loses on average)

### Tweaked Game (Probability Mode)
- **Probability**: Red = 20%, Others = 16% each
- **Payout**: Adjusted to maintain house edge
- **House Edge**: Similar to payout mode

## 📈 Key Findings

Through Monte Carlo simulation (20,000+ plays), we observe:

1. **Fair Game**: Mean profit ≈ $0, house edge ≈ 0%
2. **Tweaked Game**: Mean profit ≈ -$0.04/play, house edge ≈ 4%
3. **Impact**: Small tweaks compound over time, guaranteeing house profit
4. **Variance**: Both games show similar standard deviation, allowing occasional big wins but ensuring long-term house advantage

## 🌐 Deployment

### Streamlit Cloud (Free)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository, branch, and `streamlit_app.py`
   - Click "Deploy"

3. **Your app will be live** at: `https://share.streamlit.io/<username>/<repo>/main/streamlit_app.py`

### Alternative Platforms
- **Heroku**: Use Procfile with `web: streamlit run streamlit_app.py --server.port=$PORT`
- **Railway**: Auto-detects Streamlit apps
- **Render**: Deploy as web service

## 📁 Project Structure

```
game/
├── streamlit_app.py       # Main Streamlit web application
├── Color Game.py          # Original tkinter GUI + CLI simulation
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── sim_outputs/          # Simulation results (CSV, PNG)
```

## 🎓 Educational Use

This project demonstrates:
- **Probability Theory**: Fair vs biased probability distributions
- **Monte Carlo Methods**: Large-scale random sampling for statistical analysis
- **House Edge**: How casinos/perya operators ensure profitability
- **Data Visualization**: Histograms, cumulative plots, comparative analysis
- **Python Programming**: NumPy, Pandas, Matplotlib, Streamlit

Perfect for:
- Statistics courses
- Data science projects
- Probability & stochastic systems education
- Understanding casino mathematics

## 🤝 Contributing

Feel free to fork, modify, and experiment! Suggestions:
- Add more colors or dice
- Implement different betting strategies
- Add bankroll management simulation
- Create multiplayer mode

## 📝 License

Free to use for educational purposes.

## 🙏 Acknowledgments

Inspired by traditional Filipino "perya" (carnival) games and casino probability analysis.

---

**Built with ❤️ using Python & Streamlit**
