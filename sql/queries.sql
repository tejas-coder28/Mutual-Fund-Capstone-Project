SELECT fund_house, aum_crores FROM fact_aum ORDER BY aum_crores DESC LIMIT 5;

SELECT strftime('%Y-%m', date) AS calendar_month, AVG(nav) AS avg_nav FROM fact_nav GROUP BY calendar_month ORDER BY calendar_month;

SELECT strftime('%Y', transaction_date) AS tx_year, SUM(amount) AS total_sip_amount FROM fact_transactions WHERE transaction_type = 'SIP' GROUP BY tx_year ORDER BY tx_year;

SELECT state, SUM(amount) AS total_invested FROM fact_transactions GROUP BY state ORDER BY total_invested DESC;

SELECT f.scheme_name, p.expense_ratio FROM fact_performance p JOIN dim_fund f ON p.scheme_code = f.scheme_code WHERE p.expense_ratio < 1.0 ORDER BY p.expense_ratio;

SELECT kyc_status, COUNT(*) AS total_transactions FROM fact_transactions GROUP BY kyc_status;

SELECT f.risk_grade, AVG(p."5_year_return") AS avg_5yr_return FROM fact_performance p JOIN dim_fund f ON p.scheme_code = f.scheme_code GROUP BY f.risk_grade ORDER BY avg_5yr_return DESC;

SELECT category, COUNT(*) AS scheme_count FROM dim_fund GROUP BY category ORDER BY scheme_count DESC;

SELECT d.weekday, COUNT(t.transaction_id) AS total_tx FROM fact_transactions t JOIN dim_date d ON t.transaction_date = d.date_key GROUP BY d.weekday ORDER BY total_tx DESC;

SELECT f.scheme_name, f.risk_grade, p."3_year_return" FROM fact_performance p JOIN dim_fund f ON p.scheme_code = f.scheme_code WHERE f.risk_grade = 'High Risk' AND p."3_year_return" < 5.0;