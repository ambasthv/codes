Are you sure if all the rules applied, correctly, check step 2 once again, all looks good, but “sales_to_assets” ratio that comes from “netsales/ totalassets”. You have over seen this rule “If the numerator is not expected to have a zero value: set to null”.
But in data output, I see even if numerator is 0 and denominator has some values, it final answer is 0, and flag says its Normal.
But apply the condition, and say if numerator is 0, put Null, and in flag , write “ Zero Numerator”. 
Check the same scnarios for other ratios., \\
REWRITE THE CODE # 2. APPLY STRICT RULES + FLAGS (Overwrite where needed)
