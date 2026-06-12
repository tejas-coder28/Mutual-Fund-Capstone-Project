

import pandas as pd
import numpy as np
from pathlib import Path

PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
REPORTS_DIR   = Path(__file__).parent.parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

RISK_FREE_RATE_ANNUAL = 0.065  # ~6.5% RBI repo rate proxy


def load_nav_history() -> pd.DataFrame:
    path = PROCESSED_DIR / "02_nav_history_clean.csv"
    df = pd.read_csv(path, parse_dates=["date"])
    df.sort_values(["scheme_code", "date"], inplace=True)
    return df


def compute_rolling_sharpe(df: pd.DataFrame, window: int = 252) -> pd.DataFrame:
    """Rolling annualised Sharpe ratio per scheme."""
    rfr_daily = RISK_FREE_RATE_ANNUAL / 252
    df = df.copy()
    df["daily_return"] = df.groupby("scheme_code")["nav"].pct_change()
    df["excess_return"] = df["daily_return"] - rfr_daily
    df["rolling_sharpe"] = (
        df.groupby("scheme_code")["excess_return"]
        .transform(lambda x: x.rolling(window).mean() / x.rolling(window).std() * np.sqrt(252))
    )
    return df


def compute_var_cvar(df: pd.DataFrame, confidence: float = 0.95) -> pd.DataFrame:
    """Historical VaR and CVaR per scheme."""
    results = []
    for scheme, grp in df.groupby("scheme_code"):
        returns = grp["daily_return"].dropna()
        if len(returns) < 30:
            continue
        var   = returns.quantile(1 - confidence)
        cvar  = returns[returns <= var].mean()
        results.append({"scheme_code": scheme, "VaR_95": var, "CVaR_95": cvar})
    return pd.DataFrame(results)


if __name__ == "__main__":
    print("Loading NAV history...")
    nav_df = load_nav_history()

    print("Computing rolling Sharpe...")
    nav_df = compute_rolling_sharpe(nav_df)
    nav_df[["scheme_code", "date", "rolling_sharpe"]].dropna().to_csv(
        REPORTS_DIR / "rolling_sharpe.csv", index=False
    )

    print("Computing VaR / CVaR...")
    risk_df = compute_var_cvar(nav_df)
    risk_df.to_csv(REPORTS_DIR / "var_cvar_report.csv", index=False)

    print(f"[DONE] Metrics saved to {REPORTS_DIR}")
