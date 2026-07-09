//@version=6
strategy("Supertrend AI Confidence Strategy", overlay=true,
     initial_capital=100000,
     default_qty_type=strategy.percent_of_equity,
     default_qty_value=100,
     pyramiding=0)

// =========================
// INPUTS
// =========================
atrPeriod  = input.int(10, "Supertrend ATR Length")
factor     = input.float(3.0, "Supertrend Factor", step=0.1)
rsiLength  = input.int(14, "RSI Length")
adxLength  = input.int(14, "ADX Length")
volLength  = input.int(20, "Volume MA Length")
dmaLength  = input.int(200, "Trend DMA Length")

// =========================
// CORE INDICATORS
// =========================
[supertrend, direction] = ta.supertrend(factor, atrPeriod)

rsi = ta.rsi(close, rsiLength)
dma200 = ta.sma(close, dmaLength)
volMA = ta.sma(volume, volLength)
atr = ta.atr(14)
vwapValue = ta.vwap(close)

[macdLine, signalLine, histLine] = ta.macd(close,12,26,9)
adx = ta.adx(adxLength)

// =========================
// BUYER / SELLER DOMINANCE
// =========================
buyVol = close > open ? volume : 0.0
sellVol = close < open ? volume : 0.0

bullVol = ta.sma(buyVol,20)
bearVol = ta.sma(sellVol,20)

totalVol = bullVol + bearVol

buyerDominance =
     totalVol > 0 ?
     bullVol / totalVol * 100 :
     50

sellerDominance = 100 - buyerDominance

buyersInControl = buyerDominance > sellerDominance

// =========================
// CONFIDENCE ENGINE
// =========================
confidence = 0

// Supertrend
confidence += direction < 0 ? 20 : 0

// Trend Filter
confidence += close > dma200 ? 15 : 0

// ADX
confidence += adx > 30 ? 15 :
              adx > 20 ? 10 : 0

// Volume
confidence += volume > volMA ? 15 : 0

// RSI
confidence += (rsi > 55 and rsi < 75) ? 10 : 0

// MACD
confidence += macdLine > signalLine ? 10 : 0

// VWAP
confidence += close > vwapValue ? 10 : 0

// ATR Expansion
confidence += atr > ta.sma(atr,20) ? 5 : 0

// =========================
// SIDEWAYS PROBABILITY
// =========================
sidewaysProbability =
     adx < 20 ? 70 :
     adx < 25 ? 50 :
     adx < 30 ? 30 :
     15

// =========================
// EXPECTED MOVE
// =========================
expectedMovePercent = (atr / close) * confidence / 10

// =========================
// TREND STRENGTH
// =========================
trendStrength =
     confidence >= 90 ? "EXTREME" :
     confidence >= 80 ? "VERY STRONG" :
     confidence >= 70 ? "STRONG" :
     confidence >= 60 ? "MODERATE" :
     "WEAK"

// =========================
// SIGNALS
// =========================
longSignal =
     direction < 0 and
     direction[1] > 0

shortSignal =
     direction > 0 and
     direction[1] < 0

// =========================
// STRATEGY EXECUTION
// =========================
if longSignal
    strategy.close("Short")
    strategy.entry("Long", strategy.long)

if shortSignal
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

// =========================
// ATR TARGETS
// =========================
longSL = strategy.position_avg_price - atr * 1.5
longTP = strategy.position_avg_price + atr * 3

shortSL = strategy.position_avg_price + atr * 1.5
shortTP = strategy.position_avg_price - atr * 3

strategy.exit("Long Exit","Long",
     stop=longSL,
     limit=longTP)

strategy.exit("Short Exit","Short",
     stop=shortSL,
     limit=shortTP)

// =========================
// PLOTS
// =========================
plot(direction < 0 ? supertrend : na,
     title="Bull Trend",
     color=color.green,
     linewidth=2,
     style=plot.style_linebr)

plot(direction > 0 ? supertrend : na,
     title="Bear Trend",
     color=color.red,
     linewidth=2,
     style=plot.style_linebr)

plot(dma200,
     title="200 DMA",
     color=color.orange,
     linewidth=2)

// =========================
// LABELS
// =========================
if longSignal
    label.new(
         bar_index,
         low,
         "BUY\n" +
         "Confidence: " + str.tostring(confidence) + "%\n" +
         "Strength: " + trendStrength + "\n" +
         "Buyer Control: " + str.tostring(math.round(buyerDominance)) + "%\n" +
         "Expected Move: +" + str.tostring(math.round(expectedMovePercent,1)) + "%\n" +
         "Sideways Risk: " + str.tostring(sidewaysProbability) + "%",
         style=label.style_label_up,
         color=color.green,
         textcolor=color.white)

if shortSignal
    label.new(
         bar_index,
         high,
         "SELL\n" +
         "Confidence: " + str.tostring(confidence) + "%\n" +
         "Strength: " + trendStrength + "\n" +
         "Seller Control: " + str.tostring(math.round(sellerDominance)) + "%\n" +
         "Expected Move: -" + str.tostring(math.round(expectedMovePercent,1)) + "%\n" +
         "Sideways Risk: " + str.tostring(sidewaysProbability) + "%",
         style=label.style_label_down,
         color=color.red,
         textcolor=color.white)

// =========================
// ALERTS
// =========================
alertcondition(longSignal,
     title="BUY Signal",
     message="Supertrend AI Strategy BUY")

alertcondition(shortSignal,
     title="SELL Signal",
     message="Supertrend AI Strategy SELL")