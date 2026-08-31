# Financial Engineering Lab (MA374)

Lab assignments for the **MA374 – Financial Engineering** course at IIT Guwahati. Each lab explores a core topic in quantitative/derivatives pricing through a mix of analytical models, numerical methods, and real market data (NSE/BSE equities, NIFTY options).

## Contents

| Lab | Topic | Key files |
|---|---|---|
| [Lab 1](financial%20lab/lab1) | CRR binomial tree pricing for European & American options; convergence to Black-Scholes as steps increase | `lab1.py`, `report.pdf`, `output.pdf` |
| [Lab 2](financial%20lab/lab2) | Binomial pricing under two different (u, d) parametrizations; sensitivity of option prices to model parameters | `lab2.py`, `output_file.pdf` |
| [Lab 4](financial%20lab/lab4) | Markowitz mean-variance portfolio optimization — analytical inputs (Q1) and real market data via CSV (Q2); efficient frontier construction | `lab4_fe.py`, `lab_report_4.pdf` |
| [Lab 5](financial%20lab/lab5) | Efficient frontier extended to minimum-variance/market portfolios; CAPM beta estimation and the Security Market Line | `lab05fe.ipynb`, `outputfile.pdf` |
| [Lab 6](financial%20lab/lab6) | Empirical analysis of BSE/NSE stock data — daily/weekly/monthly resampling, log & arithmetic returns, GBM parameter calibration and simulation vs. actual prices, normality diagnostics | `fe_lab06.py`, `BSE_DATA.xlsx`, `NSE_DATA.xlsx`, `ALLPLOTS.pdf`, `REPORT_PLOTS.pdf` |
| [Lab 7](financial%20lab/lab7) | Distributional analysis of BSE/NSE daily returns: descriptive stats, boxplots, Q-Q plots, Kolmogorov–Smirnov & Shapiro–Wilk normality tests, MLE of mean/variance with 95% CIs — repeated for log returns and at weekly/monthly frequency | `MA374_lab7.pdf` |
| [Lab 8](financial%20lab/lab8) | Black-Scholes call/put price surfaces C(t,s), P(t,s) over time-to-maturity and spot price; 2D and 3D plots; sensitivity of prices to model parameters (r, σ, K, T) | `MA374_lab8.pdf` |
| [Lab 9](financial%20lab/lab9) | Historical volatility estimation from BSE/NSE data (rolling 1-month windows extended backward), BSM pricing of 6-month calls/puts across a range of strikes (K = 0.5–1.5 × S₀), and compiling a NIFTY options price dataset (`NIFTYoptiondata.xlsx`) across strikes/maturities | `MA374_lab9.pdf` |
| [Lab 10](financial%20lab/lab10) | Implied volatility surfaces from real NIFTY options data via Black-Scholes inversion (numerical root-finding on price → σ) | `LAB10.ipynb`, `NIFTYoptiondata.csv`, `nsedata1.xlsx`, `MA374_Lab10_Report.pdf` |
| [Lab 11](financial%20lab/lab11) | GBM stock path simulation (real-world & risk-neutral drift), Monte Carlo pricing of Asian options, variance reduction, sensitivity to *r* and *σ* | `lab11.ipynb`, `report.pdf` |
| [Lab 12](financial%20lab/lab12) | Short-rate term structure modeling with the Vasicek and CIR models — yield curves for multiple parameter sets and initial rates r(0), plotted out to 10 and 500/600 time units | `MA374_lab12.pdf` |

> Note: there is no Lab 3 in this repository.

Each lab folder also contains the original problem statement PDF (`MA374_labN.pdf`) alongside the solution code/notebook and generated report/output PDFs.

## Tech stack

- **Python 3** (scripts and Jupyter notebooks)
- `numpy`, `pandas`, `matplotlib`, `scipy` (`scipy.stats`, `scipy.optimize`)
- Market data provided as `.xlsx` / `.csv` (BSE, NSE, NIFTY options)

## Running the labs

Scripts (`.py`):
```bash
pip install numpy pandas matplotlib scipy openpyxl
python "financial lab/lab1/lab1 3/lab1.py"
```

Notebooks (`.ipynb`):
```bash
pip install notebook numpy pandas matplotlib scipy openpyxl
jupyter notebook "financial lab/lab5/45p.agrawalMA374lab05/lab05fe.ipynb"
```

Some scripts (e.g. Lab 6) expect the accompanying `.xlsx`/`.csv` data files to be in the same working directory — run them from inside their own lab folder.

## Author

Prakhar Agrawal — B.Tech Mathematics and Computing, IIT Guwahati
