Here is the exact Jupyter notebook structure, cell by cell. Paste each cell into Jupyter in order, then save the notebook as `financial_ratio_calculator.ipynb`.

## Cell 1 — Markdown
```markdown
# Financial Ratio Calculator with Exception Handling

This notebook calculates:
- Gross Margin
- Net Margin
- Sales to Assets

It applies the three rules for:
- Negative handling
- Zero handling
- Infinite handling
```

## Cell 2 — Code
```python
def calculate_ratio_safe(numerator, denominator, 
                         num_can_be_negative, num_can_be_zero,
                         den_can_be_negative, den_can_be_zero):
    """
    Main function to calculate a ratio with exception handling.
    """

    MAX = 999999
    MIN = -999999
    NULL = None

    # Rule 1: Negative handling
    if den_can_be_negative and not num_can_be_negative:
        if denominator < 0:
            return MAX

    if num_can_be_negative and den_can_be_negative:
        if denominator < 0:
            return MIN

    # Rule 2: Zero handling
    if not num_can_be_zero and numerator == 0:
        return NULL

    # Rule 3: Infinite handling
    if not den_can_be_zero:
        if denominator == 0:
            return NULL

    if denominator == 0:
        return MAX

    return numerator / denominator
```

## Cell 3 — Code
```python
def calculate_gross_margin(gross_profit, net_sales):
    """
    Gross Margin = (Gross Profit / Net Sales) × 100
    """
    ratio = calculate_ratio_safe(
        numerator=gross_profit,
        denominator=net_sales,
        num_can_be_negative=True,
        num_can_be_zero=True,
        den_can_be_negative=False,
        den_can_be_zero=True
    )

    if ratio is not None:
        ratio = ratio * 100

    return ratio
```

## Cell 4 — Code
```python
def calculate_net_margin(net_profit, net_sales):
    """
    Net Margin = (Net Profit / Net Sales) × 100
    """
    ratio = calculate_ratio_safe(
        numerator=net_profit,
        denominator=net_sales,
        num_can_be_negative=True,
        num_can_be_zero=True,
        den_can_be_negative=False,
        den_can_be_zero=True
    )

    if ratio is not None:
        ratio = ratio * 100

    return ratio
```

## Cell 5 — Code
```python
def calculate_sales_to_assets(net_sales, total_assets):
    """
    Sales to Assets = Net Sales / Total Assets
    """
    ratio = calculate_ratio_safe(
        numerator=net_sales,
        denominator=total_assets,
        num_can_be_negative=False,
        num_can_be_zero=True,
        den_can_be_negative=False,
        den_can_be_zero=False
    )

    return ratio
```

## Cell 6 — Code
```python
def test_all_ratios():
    print("=" * 70)
    print("TESTING ALL RATIOS WITH EXCEPTION HANDLING")
    print("=" * 70)

    print("\n" + "=" * 70)
    print("GROSS MARGIN = (Gross Profit / Net Sales) × 100")
    print("=" * 70)

    test_cases_gross = [
        ("Normal profit", 500, 1000, 50.0),
        ("Negative gross profit", -200, 1000, -20.0),
        ("Zero gross profit", 0, 1000, 0.0),
        ("Zero net sales (division by zero)", 500, 0, 99999900),
        ("Zero profit & zero sales", 0, 0, 99999900),
    ]

    for desc, gp, ns, expected in test_cases_gross:
        result = calculate_gross_margin(gp, ns)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"{status} | {desc}: GP={gp}, NS={ns} → {result} (expected {expected})")

    print("\n" + "=" * 70)
    print("NET MARGIN = (Net Profit / Net Sales) × 100")
    print("=" * 70)

    test_cases_net = [
        ("Normal profit", 300, 1000, 30.0),
        ("Net loss", -150, 1000, -15.0),
        ("Zero net profit", 0, 1000, 0.0),
        ("Zero net sales (division by zero)", 300, 0, 99999900),
    ]

    for desc, np, ns, expected in test_cases_net:
        result = calculate_net_margin(np, ns)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"{status} | {desc}: NP={np}, NS={ns} → {result} (expected {expected})")

    print("\n" + "=" * 70)
    print("SALES TO ASSETS = Net Sales / Total Assets")
    print("=" * 70)

    test_cases_assets = [
        ("Normal", 1000, 5000, 0.2),
        ("Zero sales (valid)", 0, 5000, 0.0),
        ("Zero assets (should NEVER be zero)", 1000, 0, None),
        ("Zero sales & zero assets", 0, 0, None),
    ]

    for desc, ns, ta, expected in test_cases_assets:
        result = calculate_sales_to_assets(ns, ta)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"{status} | {desc}: NS={ns}, TA={ta} → {result} (expected {expected})")

    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETED")
    print("=" * 70)
```

## Cell 7 — Code
```python
test_all_ratios()
```

## How to save it
1. Open Jupyter Notebook.
2. Create a new notebook.
3. Add the cells in the same order.
4. Run them.
5. Save as `financial_ratio_calculator.ipynb`.

## Tiny note
In your earlier code, `99999900` comes from `999999 × 100` because the margin functions multiply by 100. That is why the test expects `99999900` for zero sales in margin ratios.

Would you like me to also format this as a ready-to-copy `.ipynb` JSON notebook content?

Sources
