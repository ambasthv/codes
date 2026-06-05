Run these 3 checks one by one:

Check 1 — See the actual raw values

print(df["netmargin"].describe())


This shows min, max, mean instantly — confirms if -50,000 is real.

Check 2 — Find those extreme rows

extreme = df[df["netmargin"] < -1000][["cif", "lifestage_mapped", "year", "netmargin"]].sort_values("netmargin")
print(extreme.head(20))


This shows exactly which CIFs have extreme values and which year/lifestage they belong to.

Check 3 — Is it a % or raw dollar?

print(df["netmargin"].quantile([0.01, 0.25, 0.50, 0.75, 0.99]))


If 99th percentile is around 0–100 → it’s a percentage (normal).
If values are in thousands → it’s a raw dollar amount stored in the wrong column — data issue.

Share the output of Check 1 here and I’ll tell you exactly what’s wrong and how to fix it — whether it needs capping, scaling, or those rows need filtering out before charting.