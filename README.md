//@version=6
strategy(
    "Supertrend Strategy",
    overlay=true,
    initial_capital=100000,
    default_qty_type=strategy.percent_of_equity,
    default_qty_value=100,
    pyramiding=0
)

// Inputs
atrPeriod = input.int(10, title="ATR Length", minval=1)
factor = input.float(3.0, title="Factor", minval=0.1, step=0.1)
showLabels = input.bool(true, title="Show Buy/Sell Labels")
showBackground = input.bool(true, title="Show Background")

// Supertrend
[supertrend, direction] = ta.supertrend(factor, atrPeriod)

// Signals
longSignal = direction < 0 and direction[1] > 0
shortSignal = direction > 0 and direction[1] < 0

// Strategy Orders
if longSignal
    strategy.close("Short")
    strategy.entry("Long", strategy.long)

if shortSignal
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

// Plots
upTrend = plot(
     direction < 0 ? supertrend : na,
     title="Up Trend",
     color=color.green,
     linewidth=2,
     style=plot.style_linebr)

downTrend = plot(
     direction > 0 ? supertrend : na,
     title="Down Trend",
     color=color.red,
     linewidth=2,
     style=plot.style_linebr)

bodyMiddle = plot(
     (open + close) / 2,
     display=display.none)

// Background Fill (must remain outside any if block)
fill(
     bodyMiddle,
     upTrend,
     color=showBackground ? color.new(color.green, 90) : na,
     fillgaps=false)

fill(
     bodyMiddle,
     downTrend,
     color=showBackground ? color.new(color.red, 90) : na,
     fillgaps=false)

// Buy Labels
plotshape(
     showLabels and longSignal,
     title="BUY",
     text="BUY",
     style=shape.labelup,
     location=location.belowbar,
     color=color.green,
     textcolor=color.white,
     size=size.small)

// Sell Labels
plotshape(
     showLabels and shortSignal,
     title="SELL",
     text="SELL",
     style=shape.labeldown,
     location=location.abovebar,
     color=color.red,
     textcolor=color.white,
     size=size.small)

// Alerts
alertcondition(
     longSignal,
     title="Buy Alert",
     message="Supertrend turned GREEN")

alertcondition(
     shortSignal,
     title="Sell Alert",
     message="Supertrend turned RED")

alertcondition(
     longSignal or shortSignal,
     title="Trend Change",
     message="Supertrend changed direction")