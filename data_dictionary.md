# Data Dictionary - Mutual Fund Capstone Project

## dim_fund
The master dimension catalog tracking descriptive attributes for every listed fund asset scheme.

* **scheme_code** (INTEGER, PK): The distinct structural AMFI identification key for a scheme.
* **scheme_name** (TEXT): Complete legal title of the mutual fund scheme option.
* **fund_house** (TEXT): Corporate entity supervising asset distribution management.
* **category** (TEXT): Core structural asset grouping division (e.g., Equity, Debt).
* **sub_category** (TEXT): Specific allocation objective designation (e.g., Large Cap, Mid Cap).
* **type** (TEXT): Operational format boundaries of the scheme (Open-End vs Closed-End).
* **plan** (TEXT): Distribution route access type used (Direct or Regular).
* **risk_grade** (TEXT): Formal vulnerability classification category assigned to holdings.

## dim_date
Generated date tracking entity providing descriptive time hierarchies.

* **date_key** (TEXT, PK): ISO standardized calendar date string tracking timestamp layers.
* **day** (INTEGER): Integer tracking the specific day of the month.
* **month** (INTEGER): Integer tracking the numeric month classification value.
* **year** (INTEGER): Integer isolating the current four digit calendar year context.
* **quarter** (INTEGER): Numeric financial tracking marker classifying calendar quarter periods.
* **weekday** (TEXT): Text label identifying the corresponding day of the week.

## fact_nav
Granular tracking catalog charting historical continuous daily Net Asset Value pricing.

* **date** (TEXT, PK, FK): Reference linking back to corresponding calendar date structures.
* **scheme_code** (INTEGER, PK, FK): Reference connecting rows to the main fund asset dimension.
* **nav** (REAL): Net Asset Value units evaluated at end of daily trade processing.
* **repurchase** (REAL): Effective cash liquidation unit pricing value available to users.

## fact_transactions
Log tracking real transactional choices completed by retail accounts.

* **transaction_id** (INTEGER, PK): Auto incrementing system logging sequence key.
* **transaction_date** (TEXT, FK): Connection to date key components.
* **scheme_code** (INTEGER, FK): Reference pointer linking target transactional items to fund details.
* **transaction_type** (TEXT): Standardized processing method tracks used (SIP, Lumpsum, Redemption).
* **amount** (REAL): Complete metric evaluating financial trade scale in local denomination.
* **kyc_status** (TEXT): Legal verification validation code labels (Y, N, PENDING).
* **state** (TEXT): Geographical territory origin of the originating investor address account.

## fact_performance
Metrics tracking structural costs and return historical windows across schemes.

* **scheme_code** (INTEGER, PK, FK): Standard connector key to fund characteristics.
* **1_year_return** (REAL): Trailing twelve-month total performance asset percentage scale.
* **3_year_return** (REAL): Continuous annualized compound calculation return scale across 3 years.
* **5_year_return** (REAL): Continuous annualized compound calculation return scale across 5 years.
* **expense_ratio** (REAL): Standard structural management operational cost percentage charged.

## fact_aum
Standalone reference log track highlighting market asset allocation scale totals across firms.

* **fund_house** (TEXT, PK): Corporate management umbrella group entity name handle.
* **aum_crores** (REAL): Total asset portfolio volume value managed counted in Crores.
* **quarter** (TEXT): Log reference identifying evaluated logging performance timeline periods.