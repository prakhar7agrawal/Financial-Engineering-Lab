# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.stats import norm

# ======================================================
# 1. INTRO
# ======================================================

def load_excel(file):
    df = pd.read_excel(file)
    df.iloc[:,0] = pd.to_datetime(df.iloc[:,0])
    df.set_index(df.columns[0], inplace=True)
    df.sort_index(inplace=True)
    return df

bse = load_excel("bsedata1.xlsx")
nse = load_excel("nsedata1.xlsx")

data = pd.concat([bse, nse], axis=1)

# ======================================================
# 2. RESAMPLING
# ======================================================

def weekly_data(df):
    return df.resample('W-FRI').last()

def monthly_data(df):
    return df.resample('ME').last()   # FIXED (no warning)

# ======================================================
# 3. RETURNS
# ======================================================

def arithmetic_returns(df):
    return df.pct_change().dropna()

def log_returns(df):
    return np.log(df/df.shift(1)).dropna()

def normalize(r):
    return (r - r.mean())/r.std()

# ======================================================
# 4. GBM SIMULATION (CORRECT SCALING)
# ======================================================

def simulate_gbm(S0, mu, sigma, steps, dt):
    Z = np.random.normal(size=steps)
    W = np.cumsum(Z)*np.sqrt(dt)
    t = np.arange(1, steps+1)*dt
    S = S0*np.exp((mu - 0.5*sigma**2)*t + sigma*W)
    return S

# ======================================================
# 5. OUTPUT FILES
# ======================================================

all_pdf = PdfPages("All_Plots.pdf")
report_pdf = PdfPages("Report_Plots.pdf")

summary_list = []

# Choose representative assets automatically (highest volatility 2021-24)
vols = []
for col in data.columns:
    train = data[[col]].loc["2021-01-01":"2024-12-31"].dropna()
    if len(train) > 0:
        r = log_returns(train)
        vols.append((col, r.std().values[0]))

vols = sorted(vols, key=lambda x: x[1], reverse=True)
representative_assets = [vols[0][0], vols[len(vols)//2][0], vols[-1][0]]

print("Representative assets selected:", representative_assets)

# ======================================================
# 6. MAIN LOOP
# ======================================================

for col in data.columns:

    df_daily = data[[col]].dropna()
    df_weekly = weekly_data(df_daily)
    df_monthly = monthly_data(df_daily)

    freq_dict = {
        "Daily": (df_daily, 252),
        "Weekly": (df_weekly, 52),
        "Monthly": (df_monthly, 12)
    }

    # ============================
    # PRICE PLOTS
    # ============================
    for freq, (df, _) in freq_dict.items():

        plt.figure(figsize=(8,4))
        plt.plot(df.index, df[col])
        plt.title(f"{col} Price ({freq})")
        plt.grid()
        all_pdf.savefig()
        if col in representative_assets:
            report_pdf.savefig()
        plt.close()

    # ============================
    # ARITHMETIC RETURNS
    # ============================
    for freq, (df, _) in freq_dict.items():

        ret = arithmetic_returns(df)
        norm_ret = normalize(ret[col])
        x = np.linspace(-5,5,1000)

        plt.figure(figsize=(6,4))
        plt.hist(norm_ret, bins=50, density=True, alpha=0.6)
        plt.plot(x, norm.pdf(x), 'r', lw=2)
        plt.title(f"{col} Arithmetic Normalized ({freq})")
        plt.grid()
        all_pdf.savefig()
        if col in representative_assets:
            report_pdf.savefig()
        plt.close()

        # Tail Zoom
        plt.figure(figsize=(6,4))
        plt.hist(norm_ret[np.abs(norm_ret)>2], bins=30, density=True)
        plt.title(f"{col} Tail Zoom ({freq})")
        plt.grid()
        all_pdf.savefig()
        plt.close()

        summary_list.append([
            col, freq,
            norm_ret.mean(),
            norm_ret.std(),
            norm_ret.skew(),
            norm_ret.kurt()
        ])

    # ============================
    # LOG RETURNS
    # ============================
    for freq, (df, _) in freq_dict.items():

        ret = log_returns(df)
        norm_ret = normalize(ret[col])
        x = np.linspace(-5,5,1000)

        plt.figure(figsize=(6,4))
        plt.hist(norm_ret, bins=50, density=True, alpha=0.6)
        plt.plot(x, norm.pdf(x), 'r', lw=2)
        plt.title(f"{col} Log Normalized ({freq})")
        plt.grid()
        all_pdf.savefig()
        if col in representative_assets:
            report_pdf.savefig()
        plt.close()

    # ============================
    # SIMULATION (DAILY, WEEKLY, MONTHLY)
    # ============================

    for freq, (df, periods_per_year) in freq_dict.items():

        train = df.loc["2021-01-01":"2024-12-31"]
        test = df.loc["2025-01-01":"2025-12-31"]

        if len(train) > 0 and len(test) > 0:

            log_ret = log_returns(train)

            # Estimate annualized parameters
            mu_hat = log_ret[col].mean() * periods_per_year
            sigma_hat = log_ret[col].std() * np.sqrt(periods_per_year)

            dt = 1/periods_per_year
            S0 = test.iloc[0,0]
            steps = len(test)

            sim = simulate_gbm(S0, mu_hat, sigma_hat, steps, dt)

            plt.figure(figsize=(8,4))
            plt.plot(test.index, test[col], label="Actual")
            plt.plot(test.index, sim, label="Simulated")
            plt.legend()
            plt.title(f"{col} 2025 Simulation ({freq})")
            plt.grid()
            all_pdf.savefig()
            if col in representative_assets:
                report_pdf.savefig()
            plt.close()

# ======================================================
# SAVE SUMMARY
# ======================================================

summary_df = pd.DataFrame(summary_list,
    columns=["Asset","Frequency","Mean","Std","Skewness","Kurtosis"])

summary_df.to_csv("Summary_Statistics.csv", index=False)

all_pdf.close()
report_pdf.close()

print("All_Plots.pdf created")
print("Report_Plots.pdf created")
print("Summary_Statistics.csv created")
