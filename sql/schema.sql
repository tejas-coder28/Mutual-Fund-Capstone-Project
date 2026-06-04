CREATE TABLE dim_fund (
    scheme_code INTEGER PRIMARY KEY,
    scheme_name TEXT,
    fund_house TEXT,
    category TEXT,
    sub_category TEXT,
    type TEXT,
    plan TEXT,
    risk_grade TEXT
);

CREATE TABLE dim_date (
    date_key TEXT PRIMARY KEY,
    day INTEGER,
    month INTEGER,
    year INTEGER,
    quarter INTEGER,
    weekday TEXT
);

CREATE TABLE fact_nav (
    date TEXT,
    scheme_code INTEGER,
    nav REAL,
    repurchase REAL,
    PRIMARY KEY (date, scheme_code),
    FOREIGN KEY (scheme_code) REFERENCES dim_fund(scheme_code),
    FOREIGN KEY (date) REFERENCES dim_date(date_key)
);

CREATE TABLE fact_transactions (
    transaction_id INTEGER PRIMARY KEY,
    transaction_date TEXT,
    scheme_code INTEGER,
    transaction_type TEXT,
    amount REAL,
    kyc_status TEXT,
    state TEXT,
    FOREIGN KEY (scheme_code) REFERENCES dim_fund(scheme_code),
    FOREIGN KEY (transaction_date) REFERENCES dim_date(date_key)
);

CREATE TABLE fact_performance (
    scheme_code INTEGER PRIMARY KEY,
    "1_year_return" REAL,
    "3_year_return" REAL,
    "5_year_return" REAL,
    expense_ratio REAL,
    FOREIGN KEY (scheme_code) REFERENCES dim_fund(scheme_code)
);

CREATE TABLE fact_aum (
    fund_house TEXT PRIMARY KEY,
    aum_crores REAL,
    quarter TEXT
);