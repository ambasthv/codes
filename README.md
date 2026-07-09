//@version=5
indicator("UT Bot + STC Combo Pro", overlay=true, max_labels_count=500)

// Inputs
atrLen      = input.int(10, "UT ATR Length", minval=1)
atrMult     = input.float(1.0, "UT ATR Multiplier", step=0.1)
stcFast     = input.int(23, "STC Fast Length", minval=1)
stcSlow     = input.int(50, "STC Slow Length", minval=2)
stcCycle    = input.int(10, "STC Cycle Length", minval=1)
stcSmooth   = input.int(3, "STC Smoothing", minval=1)
emaLen      = input.int(20, "EMA Length", minval=1)
volLen      = input.int(20, "Volume MA Length", minval=1)
useHA       = input.bool(false, "Use Heikin Ashi Source")
confirmed   = input.bool(true, "Signal Only On Bar Close")
showLabels  = input.bool(true, "Show Labels")
showScore   = input.bool(true, "Show Strength Score")
showBg      = input.bool(false, "Background Trend Color")

// Source
src = useHA ? request.security(ticker.heikinashi(syminfo.tickerid), timeframe.period, close) : close
atr = ta.atr(atrLen)
barOk = confirmed ? barstate.isconfirmed : true

// UT Bot trailing stop
var float trail = na
trail := na(trail[1]) ? src - atrMult * atr :
     src > trail[1] and src[1] > trail[1] ? math.max(trail[1], src - atrMult * atr) :
     src < trail[1] and src[1] < trail[1] ? math.min(trail[1], src + atrMult * atr) :
     src > trail[1] ? src - atrMult * atr : src + atrMult * atr

utBuyRaw  = ta.crossover(src, trail)
utSellRaw = ta.crossunder(src, trail)

// STC calculation
macd = ta.ema(src, stcFast) - ta.ema(src, stcSlow)
macdMin = ta.lowest(macd, stcCycle)
macdMax = ta.highest(macd, stcCycle)
fk = macdMax != macdMin ? 100 * (macd - macdMin) / (macdMax - macdMin) : 50.0
stc1 = ta.ema(fk, stcSmooth)
stc  = ta.ema(stc1, stcSmooth)

// Filters
ema20 = ta.ema(src, emaLen)
volMA = ta.sma(volume, volLen)
volOk = volume > volMA
trendBull = src > ema20
trendBear = src < ema20
stcBull = stc > 50 and stc > stc[1]
stcBear = stc < 50 and stc < stc[1]

// Final signals
buySignal  = barOk and utBuyRaw and stcBull and trendBull
sellSignal = barOk and utSellRaw and stcBear and trendBear

exitLong  = barOk and (utSellRaw or stcBear or src < ema20)
exitShort = barOk and (utBuyRaw or stcBull or src > ema20)

// Strength score
scoreLong = (trendBull ? 25 : 0) + (volOk ? 20 : 0) + (stcBull ? 25 : 0) + (src > trail ? 15 : 0) + (src > src[1] ? 15 : 0)
scoreShort = (trendBear ? 25 : 0) + (volOk ? 20 : 0) + (stcBear ? 25 : 0) + (src < trail ? 15 : 0) + (src < src[1] ? 15 : 0)

score = buySignal ? scoreLong : sellSignal ? scoreShort : na

// Plots
plot(trail, "UT Trail", color=src >= trail ? color.lime : color.red, linewidth=2)
plot(ema20, "EMA", color=color.new(color.blue, 0), linewidth=1)

bgcolor(showBg ? (trendBull ? color.new(color.green, 90) : trendBear ? color.new(color.red, 90) : na) : na)

plotshape(buySignal, title="Buy", style=shape.labelup, text="BUY", color=color.new(color.green, 0), textcolor=color.white, location=location.belowbar, size=size.tiny)
plotshape(sellSignal, title="Sell", style=shape.labeldown, text="SELL", color=color.new(color.red, 0), textcolor=color.white, location=location.abovebar, size=size.tiny)
plotshape(exitLong, title="Exit Long", style=shape.xcross, text="XL", color=color.new(color.orange, 0), textcolor=color.white, location=location.abovebar, size=size.tiny)
plotshape(exitShort, title="Exit Short", style=shape.xcross, text="XS", color=color.new(color.orange, 0), textcolor=color.white, location=location.belowbar, size=size.tiny)

if showLabels and buySignal
    label.new(bar_index, low, "BUY\nScore: " + str.tostring(scoreLong), style=label.style_label_up, color=color.green, textcolor=color.white)

if showLabels and sellSignal
    label.new(bar_index, high, "SELL\nScore: " + str.tostring(scoreShort), style=label.style_label_down, color=color.red, textcolor=color.white)

if showScore and (buySignal or sellSignal)
    label.new(bar_index, buySignal ? low : high, "Confidence: " + str.tostring(score), style=label.style_none, textcolor=color.white)

// Alerts
alertcondition(buySignal, title="UT Bot + STC Buy", message="BUY signal")
alertcondition(sellSignal, title="UT Bot + STC Sell", message="SELL signal")
alertcondition(exitLong, title="Exit Long", message="Exit long")
alertcondition(exitShort, title="Exit Short", message="Exit short")
