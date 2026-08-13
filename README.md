Absolutely. Let’s put the three variables side by side and focus only on the logic behind the cap/floor decisions — not the PPT wording.

The main thing to remember is that we are not looking for an exact mathematical breakpoint. We are looking for a sensible boundary that:

1. preserves the meaningful relationship between the variable and default;
2. avoids allowing extreme values to create excessive differentiation; and
3. is consistent with the broad decile/bucket evidence.

⸻

1. EBITDA / (Interest Expense + CPLTD + Short Term Debt)

Selected:

Floor = 0
Cap = 1.25

Candidate / region	What we see	Interpretation
Below 0	Highest-risk region	Negative/very low values represent the riskiest obligors
0 → ~0.85	Default rate consistently decreases	Strong and useful risk differentiation
~0.85 → 1.25	Default rate continues to be low, but relationship becomes less pronounced/noisier	Still some movement, but less reliable
1.25	Upper end of useful relationship	Good point to stop further differentiation
>1.25	Little additional reliable risk differentiation	Extreme/less useful tail

Why floor = 0?

The important economic interpretation is straightforward:

EBITDA relative to debt-service/short-term obligations is negative → very poor ability to cover those obligations → higher credit risk.

Once the ratio is below zero, we don’t have a strong reason to distinguish:

-0.1
-0.5
-1.0
-3.0

as increasingly different risk levels.

They are all in the very high-risk region.

So:

Floor = 0

means we group the negative/extreme lower tail at the high-risk boundary.

Why cap = 1.25?

The default rate falls consistently as the ratio improves.

But by approximately 0.85–1.25, the default rate is already relatively low and additional increases don’t provide strong, consistent evidence of additional risk differentiation.

So we allow the model to capture the relationship up to 1.25, but don’t let extreme positive values continue driving the relationship.

Mental picture

HIGH RISK                                      LOW RISK
   │                                               │
   ▼                                               ▼
---|-------------------------------|-------------------
   0                              1.25
   ↑                               ↑
 FLOOR                            CAP

Bottom line:
The floor protects against excessive differentiation among extremely poor EBITDA coverage values, while the cap prevents increasingly high coverage values from receiving potentially unsupported additional benefit.

⸻

2. (Operating Profits + Selling Expense) / Total Assets

Selected:

Floor = -0.60
Cap = 0.35

Candidate / region	What we see	Interpretation
Below -0.60	Very high default rates	Extreme negative tail / highest-risk region
-0.60 → -0.47	Default rate falls materially	Meaningful risk differentiation remains
-0.47 → ~0.16	Default rate continues falling	Useful relationship
~0.16 → 0.35	Default rate is already low	Relationship becomes less pronounced/noisier
0.35	Low-risk region	Reasonable point to stop differentiation
>0.35	Relatively noisy/limited additional differentiation	Cap appropriate

Why floor = -0.60 instead of -0.47?

This is the important distinction we discussed.

Suppose we selected:

Floor = -0.47

Then:

-2.0
-1.0
-0.8
-0.6
     ↓
   -0.47

All of those would effectively be treated as -0.47.

But the chart shows that the actual default rate is still meaningfully higher around -0.60 than around -0.47.

Therefore, we’d be flattening a portion of the relationship that the data actually supports.

By selecting:

Floor = -0.60

we preserve:

-0.60 → -0.47

as meaningful differentiation.

But below -0.60, we stop trying to distinguish increasingly extreme negative values.

Why cap = 0.35?

At the upper end, default rates are already relatively low.

Beyond approximately 0.35, there isn’t a strong, consistent downward relationship.

So:

Cap = 0.35

allows the model to capture the meaningful improvement in operating performance, but prevents increasingly high values from producing additional differentiation that isn’t strongly supported by the data.

Mental picture

HIGH RISK                                      LOW RISK
   │                                               │
   ▼                                               ▼
---|-----------------------------------------------|---
 -0.60                                            0.35
   ↑                                                 ↑
 FLOOR                                              CAP
        meaningful relationship retained
                 ────────────────→

Bottom line:
The floor is deliberately not -0.47, because doing so would flatten a meaningful part of the observed relationship. The cap is placed at 0.35 because the relationship has largely flattened/noisified by that point.

⸻

3. Profit Before Taxes / (Total Assets − Total Liabilities)

Selected:

Floor = -1.34
Cap = -0.34

Candidate / region	What we see	Interpretation
Below -1.34	Highest default rates	Extreme negative/high-risk region
-1.34 → -0.96	Very large decline in default rate	Strong risk differentiation
-0.96 → -0.71	Default rate continues declining	Meaningful relationship remains
-0.71 → -0.34	Further decline	Still useful differentiation
-0.34	Default rate is already relatively low	Appropriate upper boundary
> -0.34	Default rate remains low but becomes more variable	Limited additional differentiation

Why floor = -1.34?

At the extreme negative end, default rates are substantially higher.

But we don’t want to distinguish indefinitely between:

-47.5
-4.02
-2.07
-1.34

The -47.5 observation is particularly extreme.

The chart doesn’t give us sufficient evidence that an obligor at -47.5 should receive dramatically different risk treatment from another extremely negative obligor.

So:

Floor = -1.34

creates a boundary for the extreme high-risk tail.

Importantly, this doesn’t mean the relationship stops at -1.34. It means we don’t want increasingly extreme negative values below -1.34 to create additional differentiation.

⸻

Why cap = -0.34 instead of -0.71?

This is the decision we discussed most recently.

Consider the actual default rates:

-1.34   → ~6.6%
-0.96   → ~3.5%
-0.71   → ~3.1%
-0.51   → ~2.8%
-0.34   → ~2.0%
-0.17   → ~1.7%
 0.06   → ~1.9%

There is still meaningful improvement between:

-0.71 → -0.51 → -0.34

If we capped at -0.71, we’d lose that observed differentiation.

By choosing -0.34, we capture most of the meaningful downward movement.

Then beyond -0.34:

-0.34 → ~2.0%
-0.17 → ~1.7%
 0.06 → ~1.9%

The relationship becomes much less clean.

The actual default rate is now low and begins to fluctuate rather than continuing to decline consistently.

Therefore:

Cap = -0.34

is a reasonable point to stop further differentiation.

Mental picture

HIGH RISK                                      LOW RISK
   │                                               │
   ▼                                               ▼
---|-----------------------------------------------|---
 -1.34                                           -0.34
   ↑                                                 ↑
 FLOOR                                              CAP
       strong/meaningful relationship retained
                 ────────────────→

⸻

The three decisions together

Variable	Floor	Cap	Main reason for floor	Main reason for cap
EBITDA / (Interest Expense + CPLTD + Short Term Debt)	0	1.25	Negative values represent extreme/high-risk coverage	Relationship becomes less useful/noisier at high positive values
(Operating Profits + Selling Expense) / Total Assets	-0.60	0.35	Preserve differentiation down to -0.60; below this is extreme negative tail	Default rates are already low and relationship becomes noisy
Profit Before Taxes / (Total Assets − Total Liabilities)	-1.34	-0.34	Extreme negative values below -1.34 don’t justify further differentiation	Captures meaningful decline through -0.34; beyond it the relationship becomes less consistent

⸻

The pattern you should now recognize

There is actually a common logic across all three, despite the numbers being very different.

Floor

Ask:

“How far into the bad/negative tail can I go while still retaining meaningful risk differentiation?”

Then stop.

Cap

Ask:

“How far into the good/positive direction can I go while the data still provides convincing additional risk differentiation?”

Then stop.

So you’re essentially trying to identify:

        EXTREME             USEFUL RELATIONSHIP             EXTREME
        HIGH RISK                                      LOW RISK
           │                                                 │
           ▼                                                 ▼
───────────|─────────────────────────────────────────────────|───────────
          FLOOR                                             CAP
           │                                                 │
           └──── don't differentiate further ────→ ←── don't differentiate

And the cap/floor is not necessarily where the default rate visibly “turns.”

That’s probably the single most important thing to remember when you explain this to stakeholders.

The question is not:

“Where does the line change direction?”

It is:

“Where does the data stop providing sufficiently reliable additional risk differentiation, considering the broad bucket-level relationship and noise at the tails?”

That is the logic behind all three selections.