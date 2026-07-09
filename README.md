//@version=6
strategy(
     "Supertrend Reversal Strategy",
     overlay=true,
     initial_capital=100000,
     default_qty_type=strategy.percent_of_equity,
     default_qty_value=100,
     pyramiding=0,
     commission_type=strategy.commission.percent,
     commission_value=0.05)

// =========================
// Inputs
// =========================
atrPeriod = input.int(10, "ATR Length", minval=1)
factor = input.float(3.0, "Supertrend Factor", minval=0.1, step=0.1)

showLabels = input.bool(true, "Show Buy/Sell Labels")
showBackground = input.bool(true, "Trend Background")

// =========================
// Supertrend Calculation
// =========================
[supertrend, direction] = ta.supertrend(factor, atrPeriod)

// TradingView Supertrend uses:
// direction < 0 = Green Trend
// direction > 0 = Red Trend

longSignal  = direction < 0 and direction[1] > 0
shortSignal = direction > 0 and direction[1] < 0

// =========================
// Strategy Orders
// =========================
if longSignal
    strategy.close("Short")
    strategy.entry("Long", strategy.long)

if shortSignal
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

// =========================
// Plot Supertrend
// =========================
upTrend = plot(
     direction < 0 ? supertrend : na,
     title="Bullish Supertrend",
     color=color.green,
     linewidth=2,
     style=plot.style_linebr)

downTrend = plot(
     direction > 0 ? supertrend : na,
     title="Bearish Supertrend",
     color=color.red,
     linewidth=2,
     style=plot.style_linebr)

midBody = plot(
     (open + close) / 2,
     display=display.none)

if showBackground
    fill(midBody, upTrend,
         color=color.new(color.green, 90),
         fillgaps=false)

    fill(midBody, downTrend,
         color=color.new(color.red, 90),
         fillgaps=false)

// =========================
// Buy/Sell Labels
// =========================
plotshape(
     showLabels and longSignal,
     title="BUY",
     text="BUY",
     style=shape.labelup,
     location=location.belowbar,
     color=color.green,
     textcolor=color.white,
     size=size.small)

plotshape(
     showLabels and shortSignal,
     title="SELL",
     text="SELL",
     style=shape.labeldown,
     location=location.abovebar,
     color=color.red,
     textcolor=color.white,
     size=size.small)

// =========================
// Alerts
// =========================
alertcondition(
     longSignal,
     title="BUY Alert",
     message="Supertrend turned GREEN - Enter LONG")

alertcondition(
     shortSignal,
     title="SELL Alert",
     message="Supertrend turned RED - Enter SHORT")

alertcondition(
     longSignal or shortSignal,
     title="Trend Change",
     message="Supertrend changed direction")