//@version=5
indicator("UT Bot + STC Combo", overlay=true, max_labels_count=500)

atrLen = input.int(10, "UT ATR Length", minval=1)
atrMult = input.float(1.0, "UT ATR Multiplier", step=0.1)
stcFast = input.int(23, "STC Fast Length", minval=1)
stcSlow = input.int(50, "STC Slow Length", minval=2)
stcCycle = input.int(10, "STC Cycle Length", minval=1)
stcSmooth = input.int(3, "STC Smoothing", minval=1)
useHA = input.bool(false, "Use Heikin Ashi Source")
showLabels = input.bool(true, "Show Labels")
showScore = input.bool(true, "Show Strength Score")

src = useHA ? request.security(ticker.heikinashi(syminfo.tickerid), timeframe.period, close) : close
atr = ta.atr(atrLen)

var float trail = na
trail := na(trail[1]) ? src - atrMult * atr : src > trail[1] and src[1] > trail[1] ? math.max(trail[1], src - atrMult * atr) : src < trail[1] and src[1] < trail[1] ? math.min(trail[1], src + atrMult * atr) : src > trail[1] ? src - atrMult * atr : src + atrMult * atr

utBuy = ta.crossover(src, trail)
utSell = ta.crossunder(src, trail)

macd = ta.ema(src, stcFast) - ta.ema(src, stcSlow)
macdMin = ta.lowest(macd, stcCycle)
macdMax = ta.highest(macd, stcCycle)
fk = macdMax != macdMin ? 100 * (macd - macdMin) / (macdMax - macdMin) : 50.0
stoch1 = ta.ema(fk, stcSmooth)
stc = ta.ema(stoch1, stcSmooth)

stcBull = stc > 50 and stc > stc[1]
stcBear = stc < 50 and stc < stc[1]

buySignal = utBuy and stcBull
sellSignal = utSell and stcBear
exitLong = utSell or stcBear
exitShort = utBuy or stcBull

ema20 = ta.ema(src, 20)
volMA = ta.sma(volume, 20)
volStrength = volume > volMA
trendBull = src > ema20
trendBear = src < ema20

scoreLong = (trendBull ? 30 : 0) + (volStrength ? 20 : 0) + (stcBull ? 25 : 0) + (src > src[1] ? 15 : 0) + (src > trail ? 10 : 0)
scoreShort = (trendBear ? 30 : 0) + (volStrength ? 20 : 0) + (stcBear ? 25 : 0) + (src < src[1] ? 15 : 0) + (src < trail ? 10 : 0)

plot(trail, "UT Trail", color=src >= trail ? color.lime : color.red, linewidth=2)
plot(ema20, "EMA 20", color=color.new(color.blue, 0))

plotshape(buySignal, title="Buy", style=shape.labelup, text="BUY", color=color.new(color.green, 0), textcolor=color.white, location=location.belowbar, size=size.tiny)
plotshape(sellSignal, title="Sell", style=shape.labeldown, text="SELL", color=color.new(color.red, 0), textcolor=color.white, location=location.abovebar, size=size.tiny)
plotshape(exitLong, title="Exit Long", style=shape.xcross, text="XL", color=color.new(color.orange, 0), textcolor=color.white, location=location.abovebar, size=size.tiny)
plotshape(exitShort, title="Exit Short", style=shape.xcross, text="XS", color=color.new(color.orange, 0), textcolor=color.white, location=location.belowbar, size=size.tiny)

if showLabels and (buySignal or sellSignal)
    label.new(bar_index, buySignal ? low : high, buySignal ? "BUY" : "SELL", style=buySignal ? label.style_label_up : label.style_label_down, color=buySignal ? color.green : color.red, textcolor=color.white)

if showScore and (buySignal or sellSignal)
    label.new(bar_index, buySignal ? low : high, (buySignal ? "Long" : "Short") + " Score: " + str.tostring(buySignal ? scoreLong : scoreShort), style=label.style_none, textcolor=color.white)

alertcondition(buySignal, "UT Bot + STC Buy", "BUY signal")
alertcondition(sellSignal, "UT Bot + STC Sell", "SELL signal")
alertcondition(exitLong, "Exit Long", "Exit long")
alertcondition(exitShort, "Exit Short", "Exit short")
