Great! Let me break down these three exception handling rules in plain English, then we'll build the ratios.

***

## EXPLANATION — What Each Rule Means

### **Rule 1: Negative Handling**

Think of a ratio as: **Ratio = Numerator / Denominator**

**Case A — Only denominator can be negative:**
- Example: `Net Sales / Total Assets`
- `Total Assets` normally shouldn't be negative (you can't have negative assets)
- But if it IS negative → the ratio becomes meaningless/wrong
- **→ Set ratio to MAX** (cap it at the highest valid value)

**Case B — Both numerator AND denominator can be negative:**
- Example: `EBITDA / Interest Expense`
- Both EBITDA and Interest can be negative
- If denominator is negative → the result is misleading
- **→ Set ratio to MIN** (floor it at the lowest valid value) when denominator < 0

***

### **Rule 2: Zero Handling**

- If the **numerator should NEVER be zero** (by definition) but IS zero:
- **→ Set ratio to NULL** (blank/missing)

- Example: `Net Sales / Total Assets`
- If `Net Sales = 0`, the company has no revenue → the ratio is not meaningful
- Treat it as missing data instead of a fake number

***

### **Rule 3: Infinite Handling (Waterfall = Check in Order)**

This is a **priority chain** — check conditions in this exact order:

**Step 1:** If BOTH numerator & denominator can be negative?  
→ **Do NOTHING** (infinity already handled by Rule 1's capping/flooring)

**Step 2:** If denominator should NEVER be zero?  
→ **Set to NULL**

**Step 3:** If neither above applies?  
→ **Set to MAX** (cap the infinity)

***

### **In Plain English for Management:**

> "When calculating financial ratios, raw division can produce nonsensical results — negative ratios where both numbers are negative, division by zero giving infinity, or zero numerators making the ratio meaningless. These three rules define exactly how to handle each situation depending on the nature of the variables, ensuring every ratio in the dataset is either a valid number or explicitly marked as missing — never a misleading value."

***

## NEXT STEP: Build the Ratios

Now I need you to tell me:

1. **Which ratios** you want to create
2. **What is the numerator and denominator** for each ratio
3. **For each variable (numerator & denominator), categorize it:**
   - Can it be negative? (Yes/No)
   - Can it be zero? (Yes/No)

### Example format:

| Ratio | Numerator | Num: Can be Negative? | Num: Can be Zero? | Denominator | Den: Can be Negative? | Den: Can be Zero? |
|-------|-----------|----------------------|-------------------|-------------|----------------------|-------------------|
| grossmargin | gross_profit | Yes | Yes | net_sales | No | No |
| netmargin | net_profit | Yes | Yes | net_sales | No | No |
| adjquick | current_assets | No | Yes | current_liabilities | Yes | Yes |
| debttotnw | total_debt | No | Yes | net_worth | No | No |
| sales_to_assets | net_sales | No | No | total_assets | No | No |

**Once you provide your ratios with these categorizations, I'll write the complete code** that:
- Applies Rule 1 for negative handling
- Applies Rule 2 for zero handling  
- Applies Rule 3 (waterfall) for infinite handling

What ratios do you want to build?

Sources

======================

Perfect! Let me walk through each of your three ratios **step-by-step** using the exception handling rules, with concrete examples so you fully understand the logic.

***

## Your Three Ratios

| Ratio | Formula | Numerator | Denominator |
|-------|---------|-----------|-------------|
| **Gross Margin** | (Gross Profit / Net Sales) × 100 | Gross Profit | Net Sales |
| **Net Margin** | (Net Profit / Net Sales) × 100 | Net Profit | Net Sales |
| **Sales to Assets** | Net Sales / Total Assets | Net Sales | Total Assets |

***

## FIRST: Categorize Each Variable

Before applying the rules, we need to categorize each variable:

### **Gross Profit**
- Can it be **negative**? → **YES** (company can have negative gross profit if costs > revenue)
- Can it be **zero**? → **YES** (company can have zero gross profit)

### **Net Profit**
- Can it be **negative**? → **YES** (company can have net loss)
- Can it be **zero**? → **YES** (company can have zero net profit)

### **Net Sales**
- Can it be **negative**? → **NO** (sales can't be negative — you can't sell less than zero)
- Can it be **zero**? → **YES** (company can have zero revenue)

### **Total Assets**
- Can it be **negative**? → **NO** (assets can't be negative normally)
- Can it be **zero**? → **NO** (company must have some assets)

***

## NOW: Apply the Rules to Each Ratio

***

## **RATIO 1: Gross Margin = (Gross Profit / Net Sales) × 100**

### Variable Categorization:
- **Numerator (Gross Profit)**: Can be negative? **YES** | Can be zero? **YES**
- **Denominator (Net Sales)**: Can be negative? **NO** | Can be zero? **YES**

***

### **Apply Rule 1: Negative Handling**

**Question:** Can both be negative?  
- Gross Profit: YES
- Net Sales: NO

**Answer:** Only **numerator** can be negative, denominator cannot be negative.

Wait — this is **different** from the two cases in Rule 1:
- Case A: Only **denominator** can be negative → set to MAX
- Case B: **Both** can be negative → set to MIN if denominator is negative

Since **denominator (Net Sales) cannot be negative**, Rule 1 **doesn't apply** here. Negatives are fine (negative gross profit ÷ positive sales = negative margin, which is valid).

***

### **Apply Rule 2: Zero Handling**

**Question:** Should numerator (Gross Profit) NEVER be zero?  
- Answer: **NO** — Gross Profit CAN be zero (it's expected sometimes)

**Result:** Rule 2 **doesn't apply**. If Gross Profit = 0, ratio = 0 (valid).

***

### **Apply Rule 3: Infinite Handling (Waterfall)**

**Step 1:** Can both numerator and denominator be negative?  
- Gross Profit: YES | Net Sales: NO  
- **Answer:** NO → Skip to Step 2

**Step 2:** Should denominator (Net Sales) NEVER be zero?  
- Answer: **NO** — Net Sales CAN be zero (though not ideal, it's possible)

**Step 3:** Neither condition met?  
- **Answer:** YES → **Set to MAX**

**What this means:** If Net Sales = 0, we get division by zero = infinity. Since Net Sales can be zero (not expected to NEVER be zero), we go to Step 3 and **cap at MAX**.

***

### **Gross Margin Examples:**

| Scenario | Gross Profit | Net Sales | Raw Calculation | After Rules | Why? |
|----------|--------------|-----------|-----------------|-------------|------|
| Normal | ₹500 | ₹1,000 | (500/1000)×100 = **50%** | **50%** | Valid |
| Negative profit | -₹200 | ₹1,000 | (-200/1000)×100 = **-20%** | **-20%** | Valid (negative margin is real) |
| Zero profit | ₹0 | ₹1,000 | (0/1000)×100 = **0%** | **0%** | Valid (zero is okay) |
| Zero sales | ₹500 | ₹0 | (500/0)×100 = **∞** | **MAX** | Rule 3 Step 3 → cap at MAX |
| Zero profit & zero sales | ₹0 | ₹0 | (0/0)×100 = **∞** | **MAX** | Rule 3 Step 3 → cap at MAX |

***

## **RATIO 2: Net Margin = (Net Profit / Net Sales) × 100**

### Variable Categorization:
- **Numerator (Net Profit)**: Can be negative? **YES** | Can be zero? **YES**
- **Denominator (Net Sales)**: Can be negative? **NO** | Can be zero? **YES**

***

### **Apply Rule 1: Negative Handling**

**Question:** Can both be negative?  
- Net Profit: YES
- Net Sales: NO

**Answer:** Only numerator can be negative → **Rule 1 doesn't apply**. Negative net margin is valid.

***

### **Apply Rule 2: Zero Handling**

**Question:** Should numerator (Net Profit) NEVER be zero?  
- Answer: **NO** — Net Profit CAN be zero

**Result:** Rule 2 **doesn't apply**. If Net Profit = 0, ratio = 0 (valid).

***

### **Apply Rule 3: Infinite Handling (Waterfall)**

**Step 1:** Can both be negative? → NO → Skip to Step 2  
**Step 2:** Should denominator (Net Sales) NEVER be zero? → NO → Skip to Step 3  
**Step 3:** Neither met? → **YES → Set to MAX**

**What this means:** If Net Sales = 0, division by zero = infinity → **cap at MAX**.

***

### **Net Margin Examples:**

| Scenario | Net Profit | Net Sales | Raw Calculation | After Rules | Why? |
|----------|------------|-----------|-----------------|-------------|------|
| Normal profit | ₹300 | ₹1,000 | (300/1000)×100 = **30%** | **30%** | Valid |
| Net loss | -₹150 | ₹1,000 | (-150/1000)×100 = **-15%** | **-15%** | Valid (negative margin) |
| Zero profit | ₹0 | ₹1,000 | (0/1000)×100 = **0%** | **0%** | Valid |
| Zero sales | ₹300 | ₹0 | (300/0)×100 = **∞** | **MAX** | Rule 3 Step 3 → cap at MAX |

***

## **RATIO 3: Sales to Assets = Net Sales / Total Assets**

### Variable Categorization:
- **Numerator (Net Sales)**: Can be negative? **NO** | Can be zero? **YES**
- **Denominator (Total Assets)**: Can be negative? **NO** | Can be zero? **NO**

***

### **Apply Rule 1: Negative Handling**

**Question:** Can both be negative?  
- Net Sales: NO
- Total Assets: NO

**Answer:** Neither can be negative → **Rule 1 doesn't apply**.

**Question:** Can only denominator be negative?  
- Total Assets: NO

**Answer:** Denominator cannot be negative → **Rule 1 doesn't apply at all**.

***

### **Apply Rule 2: Zero Handling**

**Question:** Should numerator (Net Sales) NEVER be zero?  
- Answer: **NO** — Net Sales CAN be zero

**Result:** Rule 2 **doesn't apply**. If Net Sales = 0, ratio = 0 (valid).

***

### **Apply Rule 3: Infinite Handling (Waterfall)**

**Step 1:** Can both be negative? → NO → Skip to Step 2  
**Step 2:** Should denominator (Total Assets) NEVER be zero?  
- Answer: **YES!** — Total Assets should NEVER be zero (company must have assets)

**Result:** **Set to NULL**

**What this means:** If Total Assets = 0, division by zero = infinity → Since Total Assets should NEVER be zero, we treat this as **missing data (NULL)** instead of capping.

***

### **Sales to Assets Examples:**

| Scenario | Net Sales | Total Assets | Raw Calculation | After Rules | Why? |
|----------|-----------|--------------|-----------------|-------------|------|
| Normal | ₹1,000 | ₹5,000 | 1000/5000 = **0.20** | **0.20** | Valid |
| Zero sales | ₹0 | ₹5,000 | 0/5000 = **0.00** | **0.00** | Valid (zero numerator is okay) |
| Zero assets | ₹1,000 | ₹0 | 1000/0 = **∞** | **NULL** | Rule 3 Step 2 → denominator should NEVER be zero |
| Zero sales & zero assets | ₹0 | ₹0 | 0/0 = **∞** | **NULL** | Rule 3 Step 2 → denominator should NEVER be zero |

***

## SUMMARY TABLE: What Happens to Each Ratio

| Ratio | When Numerator = 0 | When Denominator = 0 | When Denominator < 0 | When Both < 0 |
|-------|-------------------|---------------------|---------------------|---------------|
| **Gross Margin** | 0% (valid) | **MAX** (Rule 3 Step 3) | Can't happen (Net Sales ≥ 0) | Can't happen (Net Sales ≥ 0) |
| **Net Margin** | 0% (valid) | **MAX** (Rule 3 Step 3) | Can't happen (Net Sales ≥ 0) | Can't happen (Net Sales ≥ 0) |
| **Sales to Assets** | 0.00 (valid) | **NULL** (Rule 3 Step 2) | Can't happen (Assets ≥ 0) | Can't happen (both ≥ 0) |

***

## KEY INSIGHTS

### **Why Gross Margin and Net Margin behave the same:**
- Both have **Net Sales** as denominator
- Net Sales can be zero (not expected to NEVER be zero)
- So Rule 3 Step 3 applies → **MAX**

### **Why Sales to Assets is different:**
- Denominator is **Total Assets**
- Total Assets should NEVER be zero (by definition, a company must have assets)
- So Rule 3 Step 2 applies → **NULL**

### **Why no negative handling for any of these:**
- None of these ratios have a denominator that can be negative
- None have both numerator and denominator that can be negative
- So Rule 1 doesn't apply to any of them

***

## FINAL LOGIC FLOW FOR EACH RATIO

```
For Gross Margin and Net Margin:
┌─────────────────────────────┐
│ Step 1: Check negatives     │
│   → Denominator can't be    │
│     negative → Skip Rule 1  │
└─────────────┬───────────────┘
              │
┌─────────────▼───────────────┐
│ Step 2: Check zero numerator│
│   → Numerator CAN be zero   │
│   → Skip Rule 2             │
└─────────────┬───────────────┘
              │
┌─────────────▼───────────────┐
│ Step 3: Infinite handling   │
│   → Neither condition met   │
│   → Set to MAX if denom=0   │
└─────────────────────────────┘

For Sales to Assets:
┌─────────────────────────────┐
│ Step 1: Check negatives     │
│   → Neither can be negative │
│   → Skip Rule 1             │
└─────────────┬───────────────┘
              │
┌─────────────▼───────────────┐
│ Step 2: Check zero numerator│
│   → Numerator CAN be zero   │
│   → Skip Rule 2             │
└─────────────┬───────────────┘
              │
┌─────────────▼───────────────┐
│ Step 3: Infinite handling   │
│   → Denominator should      │
│     NEVER be zero           │
│   → Set to NULL if denom=0  │
└─────────────────────────────┘
```

***

Now you understand **exactly** how each rule applies to your three ratios! When we write the code later, it will follow this exact logic flow.

Do you have any questions about this explanation, or do you want me to clarify any part before we move to coding?

Sources

