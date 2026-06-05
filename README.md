Great output! Everything saved successfully. Now let me explain every number.

First — what are IQR and Z-Score in plain English?

IQR (Interquartile Range) — thinks locally. It looks at the middle 50% of your data and says “anything too far outside this middle range is an outlier.” Like saying “most students score 40–70, so anyone below 10 or above 100 is unusual.”

Z-Score — thinks globally. It measures how many standard deviations a value is from the average. Anything beyond 3 standard deviations is flagged. Much stricter — only catches the truly extreme cases.

Why IQR always finds MORE outliers than Z-Score

IQR is sensitive to the shape of your data. Financial data is heavily skewed — so IQR casts a wider net. Z-Score only catches the most extreme 0.3% of a normal distribution. Both are correct — they just answer different questions.

Now reading YOUR table row by row:

Gross Margin

Total records:  255,202
IQR outliers:   10,246  (4.0%)  ← 4 in every 100 companies flagged
Z-Score:           440  (0.2%)  ← only the most extreme 440 flagged
Q1:             25.13   ← 25% of companies below 25% gross margin
Q3:             78.80   ← 75% of companies below 78% gross margin
Lower fence:   -55.37   ← below this = outlier (negative margin)
Upper fence:   159.31   ← above this = outlier (suspiciously high)
Min:        -92,300     ← worst gross margin in entire portfolio
Max:          3,906     ← highest gross margin (data quality flag)


Management message: Most companies have healthy gross margins between 25–79%. The 10,246 IQR outliers are companies significantly outside this range — either deeply loss-making or suspiciously high. The extreme min of -92,300 confirms the data quality issue we found earlier.

Net Margin

IQR outliers:  38,894  (15.2%)  ← 1 in 6 companies flagged!
Z-Score:        1,449   (0.6%)
Q1:            -245.6   ← 25% of companies have margin below -245
Q3:              -6.9   ← 75% still negative!
Lower fence:   -603.7
Upper fence:    351.1
Min:        -1,944,900  ← confirmed data quality issue
Max:           418,600


Management message: This is your most problematic ratio. 15% flagged by IQR is very high. More importantly — both Q1 AND Q3 are negative, meaning the majority of your portfolio companies have negative net margins. Combined with the extreme min/max values, this column needs data quality investigation before using in any model.

Adj Quick Ratio

IQR outliers:  30,042  (11.8%)
Z-Score:          910   (0.4%)
Q1:              1.06   ← 25% below 1.06 (just above the danger line)
Q3:              5.83   ← 75% below 5.83
Lower fence:    -6.09   ← negative quick ratio = data issue
Upper fence:    12.98
Min:           -4,362
Max:            8,583


Management message: A quick ratio below 1 means a company can’t cover its short-term obligations. Your Q1 is 1.06 — meaning 25% of companies are right at the edge of liquidity stress. The 11.8% IQR outliers include both very illiquid companies and suspiciously high values worth checking.

Debt to Net Worth (debttotnw)

IQR outliers:  36,528  (14.3%)  ← second highest flag rate
Z-Score:          698   (0.3%)
Q1:             -1.68   ← negative! means negative net worth
Q3:              1.24
Lower fence:    -6.06
Upper fence:     5.62
Min:           -5,868
Max:            9,096


Management message: A negative debt-to-net-worth means the company’s liabilities exceed its assets — technically insolvent. Your Q1 is -1.68, meaning at least 25% of your portfolio has negative net worth. The 14.3% IQR flag rate is high and warrants segment-level review.

One overall message for management:

“Our outlier analysis across 255,202 records reveals that net margin and debt-to-net-worth have the highest concentration of outliers — 15% and 14% respectively by IQR method. Gross margin is relatively cleaner at 4%. Key concern is that median net margin and Q1 debt-to-net-worth are both negative across the portfolio, suggesting a meaningful portion of our borrowers are either loss-making or technically insolvent. We recommend a data quality review on net margin extreme values and a targeted credit review on the flagged CIFs in the IQR outlier sheets.”