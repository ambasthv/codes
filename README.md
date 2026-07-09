//@version=6
strategy("Supertrend Confidence Strategy", overlay=true, initial_capital=100000,
     default_qty_type=strategy.percent_of_equity,
     default_qty_value=100,
     pyramiding=0)

// ======================
// INPUTS
// ======================
atrPeriod = input.int(10, "Supertrend ATR Length")
factor = input.float(3.0, "Supertrend Factor", step=0.1)

rsiLength = input.int(14, "RSI Length")
adxLength = input.int(14, "ADX Length")
volLength = input.int(20, "Volume MA Length")
dmaLength = input.int(200, "Trend DMA")

// ======================
// INDICATORS
// ======================
[supertrend, direction] = ta.supertrend(factor, atrPeriod)

rsi = ta.rsi(close, rsiLength)
volMA = ta.sma(volume, volLength)
dma200 = ta.sma(close, dmaLength)
atr = ta.atr(14)

// ADX Calculation
upMove = high - high[1]
downMove = low[1] - low

plusDM = (upMove > downMove and upMove > 0) ? upMove : 0
minusDM = (downMove > upMove and downMove > 0) ? downMove : 0

trur = ta.rma(ta.tr, adxLength)

plusDI = 100 * ta.rma(plusDM, adxLength) / trur
minusDI = 100 * ta.rma(minusDM, adxLength) / trur

dx = math.abs(plusDI - minusDI) / (plusDI + minusDI) * 100
adx = ta.rma(dx, adxLength)

// MACD
[macdLine, signalLine, histLine] = ta.macd(close,12,26,9)

// ======================
// CONFIDENCE SCORE
// ======================
confidence = 0

confidence += direction < 0 ? 20 : 0
confidence += volume > volMA ? 15 : 0
confidence += close > dma200 ? 20 : 0
confidence += (rsi > 55 and rsi < 70) ? 10 : 0
confidence += adx > 25 ? 15 : 0
confidence += macdLine > signalLine ? 10 : 0
confidence += volume > volume[1] ? 10 : 0

// ======================
// VOLUME DOMINANCE
// ======================
buyVol = close > open ? volume : 0
sellVol = close < open ? volume : 0

buyPower = ta.sma(buyVol,20)
sellPower = ta.sma(sellVol,20)

bullPercent = (buyPower/(buyPower+sellPower))*100
bearPercent = (sellPower/(buyPower+sellPower))*100

volumeControl = bullPercent > bearPercent ? "BUYERS" : "SELLERS"

// ======================
// EXPECTED MOVE
// ======================
expectedMovePercent = (atr * 2 / close) * 100

// ======================
// TREND STRENGTH
// ======================
trendStrength =
     confidence >= 85 ? "VERY STRONG" :
     confidence >= 70 ? "STRONG" :
     confidence >= 55 ? "MODERATE" :
     "WEAK"

// ======================
// SIGNALS
// ======================
longSignal = direction < 0 and direction[1] > 0
shortSignal = direction > 0 and direction[1] < 0

// ======================
// STRATEGY ORDERS
// ======================
if longSignal
    strategy.close("Short")
    strategy.entry("Long", strategy.long)

if shortSignal
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

// ======================
// PLOTS
// ======================
plot(direction < 0 ? supertrend : na,
     color=color.green,
     linewidth=2,
     style=plot.style_linebr)

plot(direction > 0 ? supertrend : na,
     color=color.red,
     linewidth=2,
     style=plot.style_linebr)

// ======================
// LABELS
// ======================
if longSignal
    label.new(
         bar_index,
         low,
         "BUY\nConfidence: " + str.tostring(confidence) + "%\n" +
         trendStrength + "\n" +
         volumeControl + " Control\n" +
         "Expected Move: +" + str.tostring(math.round(expectedMovePercent,1)) + "%",
         style=label.style_label_up,
         color=color.green,
         textcolor=color.white)

if shortSignal
    label.new(
         bar_index,
         high,
         "SELL\nConfidence: " + str.tostring(confidence) + "%\n" +
         trendStrength + "\n" +
         volumeControl + " Control\n" +
         "Expected Move: -" + str.tostring(math.round(expectedMovePercent,1)) + "%",
         style=label.style_label_down,
         color=color.red,
         textcolor=color.white)

// ======================
// ALERTS
// ======================
alertcondition(longSignal,"BUY","Supertrend BUY Signal")
alertcondition(shortSignal,"SELL","Supertrend SELL Signal")