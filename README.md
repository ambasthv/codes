✅ Here is a clear summary table for the three ratios based on your cleaning rules from Excel + .py file:
Rule / Treatment
grossmargin
netmargin
sales_to_assets
Negative Handling
Set to Null
Set to Null
Set to Null
Zero Numerator Handling
Set to Null
Set to Null
Set to Null
Zero Denominator Handling
Set to Null
Set to Null
Set to Null
Positive Infinite
Set to Null
Set to Null
Set to Null
Negative Infinite
Set to Null
Set to Null
Set to Null
Cap (Upper Bound)
99.75th percentile
99.75th percentile
99.75th percentile
Floor (Lower Bound)
0.25th percentile
0.25th percentile
0
Null Treatment
Imputed with Median (if enabled)
Imputed with Median (if enabled)
Imputed with Median (if enabled)
Flag Columns Created
_negative_flag, _zero_flag, _inf_flag, _null_flag, _cap_floor_flag, _invalid_flag
Same as left
Same as left

Summary:
	•	All three ratios follow similar strict rules.
	•	Invalid values (negative, zero, infinite) are mostly set to Null.
	•	Extreme values are capped/floored.
	•	Missing values are imputed with median (if null_treatment=True).
Would you like me to add this summary as a DataFrame in code so you can export it to Excel?
