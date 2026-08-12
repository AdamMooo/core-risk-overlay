# Core-Risk-Overlay (Portfolio Thermostat)
### Operational Master Plan & System Architecture

## 1. Core Philosophy & Mandate
This repository implements a **Systematic Tail-Risk Insurance Overlay** optimized for long-term retail portfolios. It rejects high-frequency trading (HFT), micro-market day-trading, and binary (on/off) market-timing prediction loops. 

*   **The Equities Mandate:** We hold core, highly liquid index assets (S&P 500 / Nasdaq) **forever**. We never liquidate or trim our core long-term equity positions based on short-term noise.
*   **The Insurance Mandate:** The model operates strictly as a risk thermostat. It sits silently in the background measuring real-time structural market friction on a slow, weekly cadence. Its sole purpose is to indicate when to scale our out-of-the-money (OTM) USD option insurance layer up or down.

---

## 2. Repository & Execution Constraints
To eliminate the structural flaws of previous iterations, this codebase enforces the following immutable constraints:
*   **Data Cadence:** Strictly **Weekly Closing Prices (Log Returns)**. Intraday or high-frequency point processes (e.g., Hawkes) are entirely banned to filter out daily noise.
*   **Mathematical Core:** Purely **Likelihood-Based Time-Series Modeling** via a 2-Regime Switching Jump-Diffusion Model (`statsmodels.tsa.regimeswitching.markov_regression`). Machine learning clustering engines (e.g., K-Means) or rigid binary classifiers are completely forbidden.
*   **State Persistence Penalty:** The Hidden Markov Transition Matrix is tightly constrained (p00 ≈ 0.98). The model is mathematically blocked from constantly flipping between states, allowing it to transition only when a structural regime jump is undeniable.
*   **Model Output:** Clean, continuous posterior probabilities between 0.0 (0%) and 1.0 (100%), smoothed via an Exponentially Weighted Moving Average (EWMA) shock absorber.

---

## 3. Structural Plumbing (The Canadian Framework)
To execute this institutional strategy efficiently as a Canadian investor without friction or currency-drag, the capital plumbing is isolated into two clean sub-buckets:

1.  **Core Bucket (CAD Sub-Account):** Holds long-term compounding index assets (e.g., VFV, XEQT) or direct blue chips. This bucket is never sold during a crash.
2.  **Risk Overlay Bucket (USD Sub-Account):** Holds a small, dedicated cash buffer. Capital is converted from CAD to USD **exactly once** via low-spread institutional tools (e.g., Norbert's Gambit / IBKR native conversion) to eliminate ongoing currency friction. This pure USD cash is used exclusively to buy highly liquid, cheap US-listed S&P 500 (**SPY**) Put Options.

---

## 4. Operational Architecture (The File Pipeline)

```text
my-portfolio-thermostat/
├── STRATEGY_PLAN.md       # This file (The permanent guardrail)
├── main.py                # Main workflow script executed every Friday afternoon
└── src/
    ├── data_loader.py     # Module 1: Downloads weekly data and outputs log returns
    ├── jump_model.py      # Module 2: Fits the Markov Regression likelihood pipeline
    └── risk_engine.py     # Module 3: Smooths probabilities and maps them to option scaling
```

### Weekly Execution Protocol (Friday at 3:30 PM EST)
1.  **Run `main.py`:** Fetches weekly close returns and runs the likelihood jump engine.
2.  **Extract the Thermostat Score:** Reads the smoothed continuous panic probability metric.
3.  **Check the Portfolio Management System (PMS):** Identify total core portfolio value and its S&P 500 Beta.
4.  **Execute the Risk Tier Matrix:**
    *   **0% to 20% (Calm Regime):** Do absolutely nothing. Save USD insurance cash.
    *   **21% to 60% (Building Stress):** Open broker app. Allocate a tiny sliver of the USD cash tank to buy **3 to 6-month expiry SPY Put Options**, struck **10% to 20% out-of-the-money**.
    *   **61% to 100% (Hysteria/Jump Regime):** Maintain existing long-term puts. Let the options explode quadratically via Gamma and Vega inflation. Do NOT touch core equities.

---

## 5. Crisis Monetization Protocol (The Alpha Generator)
When a severe structural market jump or crash actively maps into the 90%+ panic threshold:
1.  **Harvest Volatility:** Sell the hyper-inflated SPY Put Options contracts to lock in massive, realized USD profits at the peak of implied volatility.
2.  **Discount Reinvestment:** Immediately transfer that fresh USD cash from the risk bucket into the core bucket. 
3.  **The Power Move:** Purchase more shares of the core index assets (SPY/QQQ) at deep, temporary market discounts, maximizing compounding performance when the market inevitably snaps back.
