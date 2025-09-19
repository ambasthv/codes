Complete Metrics Comparison Table
Detailed Direction & Performance Guide
Metric
Higher = Better?
Good Range (1-100%)
Performance Breakdown
Best Use Case
PSI
(Population Stability Index)
✅ Higher
70-100%
Poor: 1-30% (No predictive power)
Fair: 31-50% (Weak predictor)
Good: 51-70% (Moderate predictor)
Excellent: 71-100% (Strong predictor)
Measuring model stability over time
KS
(Kolmogorov-Smirnov)
✅ Higher
60-100%
Poor: 1-40% (Weak separation)
Fair: 41-60% (Moderate separation)
Good: 61-80% (Strong separation)
Excellent: 81-100% (Outstanding separation)
Measuring model discrimination power
GINI
(Gini Coefficient)
✅ Higher
60-100%
Poor: 1-40% (Poor discrimination)
Fair: 41-60% (Moderate discrimination)
Good: 61-80% (Strong discrimination)
Excellent: 81-100% (Outstanding discrimination)
Overall model ranking ability
ACCURACY
✅ Higher
80-100%
Poor: 1-70% (Unacceptable)
Fair: 71-80% (Marginal)
Good: 81-90% (Acceptable)
Excellent: 91-100% (Outstanding)
Overall classification performance
Quick Reference Performance Levels
Performance Level
PSI Range
KS Range
GINI Range
ACCURACY Range
Description
Excellent Model
80-100%
80-100%
80-100%
90-100%
Production-ready, high confidence
Good Model
60-80%
60-80%
60-80%
80-90%
Deployable with monitoring
Fair Model
40-60%
40-60%
40-60%
70-80%
Needs improvement
Poor Model
1-40%
1-40%
1-40%
1-70%
Requires major rework

FINAL SUMMARY TABLE
Metric
Direction
Target Range
Thresholds
Industry Notes
PSI
Higher = Better
70-100%
>70% = Strong
<30% = Poor
Model stability tracking
KS
Higher = Better
60-100%
>60% = Good
>80% = Excellent
Discrimination power
GINI
Higher = Better
60-100%
>60% = Good
>80% = Excellent
Ranking ability
ACCURACY
Higher = Better
80-100%
>80% = Good
>90% = Excellent
Classification performance
Key Insights:
	•	All metrics are “higher = better” - unlike AUC which is 0.5-1.0
	•	Production Target: Aim for all metrics in the 70-100% range
	•	Consistency: Good models show balanced performance across all metrics
	•	Context: Industry benchmarks vary (finance: 85%+, marketing: 70%+)
	•	Pro Tip: For imbalanced datasets, KS & GINI are more reliable than accuracy
Copy either table above - the first has all details, the second is the concise summary!
