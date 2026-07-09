//@version=6
strategy("Supertrend AI Confidence Strategy", overlay=true,
     initial_capital=100000,
     default_qty_type=strategy.percent_of_equity,
     default_qty_value=100,
     pyramiding=0)

//----------------------------------------------------
// Inputs
//----------------------------------------------------
atrPeriod  = input.int(10, "Supertrend ATR Length")
factor     = input.float(3.0, "Supertrend Factor")
rsiLength  = input.int(14, "RSI Length")
adxLength  = input.int(14, "ADX Length")
volLength  = input.int(20, "Volume Average Length")
dmaLength  = input.int(200, "200 DMA Length")

//----------------------------------------------------
// Indicators
//----------------------------------------------------
[supertrend, direction] = ta.supertrend(factor, atrPeriod)

rsiValue = ta.rsi(close, rsiLength)
dma200 = ta.sma(close, dmaLength)
volMA = ta.sma(volume, volLength)
atrValue = ta.atr(14)

[macdLine, signalLine, histLine] = ta.macd(close, 12, 26, 9)

vwapValue = ta.vwap(close)

//----------------------------------------------------
// Manual ADX Calculation
//----------------------------------------------------
upMove = high - high[1]
downMove = low[1] - low

plusDM = (upMove > downMove and upMove > 0) ? upMove : 0
minusDM = (downMove > upMove and downMove > 0) ? downMove : 0

trueRange = ta.tr(true)

smoothedTR = ta.rma(trueRange, adxLength)
smoothedPlusDM = ta.rma(plusDM, adxLength)
smoothedMinusDM = ta.rma(minusDM, adxLength)

plusDI = 100 * smoothedPlusDM / smoothedTR
minusDI = 100 * smoothedMinusDM / smoothedTR

dx = 100 * math.abs(plusDI - minusDI) / (plusDI + minusDI)

adx = ta.rma(dx, adxLength)

//----------------------------------------------------
// Buyer Seller Dominance
//----------------------------------------------------
buyVol = close > open ? volume : 0
sellVol = close < open ? volume : 0

bullVol = ta.sma(buyVol, 20)
bearVol = ta.sma(sellVol, 20)

totalVol = bullVol + bearVol

buyerDominance = totalVol > 0 ? bullVol / totalVol * 100 : 50
sellerDominance = 100 - buyerDominance

//----------------------------------------------------
// Confidence Score
//----------------------------------------------------
confidence = 0

confidence += direction < 0 ? 20 : 0
confidence += close > dma200 ? 15 : 0
confidence += adx > 30 ? 15 : adx > 20 ? 10 : 0
confidence += volume > volMA ? 15 : 0
confidence += (rsiValue > 55 and rsiValue < 75) ? 10 : 0
confidence += macdLine > signalLine ? 10 : 0
confidence += close > vwapValue ? 10 : 0
confidence += atrValue > ta.sma(atrValue,20) ? 5 : 0

//----------------------------------------------------
// Market State
//----------------------------------------------------
sidewaysRisk =
     adx < 20 ? 70 :
     adx < 25 ? 50 :
     adx < 30 ? 30 :
     15

expectedMovePercent = (atrValue / close) * confidence / 10

trendStrength =
     confidence >= 90 ? "EXTREME" :
     confidence >= 80 ? "VERY STRONG" :
     confidence >= 70 ? "STRONG" :
     confidence >= 60 ? "MODERATE" :
     "WEAK"

//----------------------------------------------------
// Entry Conditions
//----------------------------------------------------
longSignal = direction < 0 and direction[1] > 0
shortSignal = direction > 0 and direction[1] < 0

//----------------------------------------------------
// Strategy Orders
//----------------------------------------------------
if longSignal
    strategy.close("Short")
    strategy.entry("Long", strategy.long)

if shortSignal
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

//----------------------------------------------------
// Stop Loss and Targets
//----------------------------------------------------
longSL = strategy.position_avg_price - atrValue * 1.5
longTP = strategy.position_avg_price + atrValue * 3

shortSL = strategy.position_avg_price + atrValue * 1.5
shortTP = strategy.position_avg_price - atrValue * 3

strategy.exit("Long Exit", "Long", stop=longSL, limit=longTP)
strategy.exit("Short Exit", "Short", stop=shortSL, limit=shortTP)

//----------------------------------------------------
// Plot Supertrend
//----------------------------------------------------
plot(direction < 0 ? supertrend : na,
     color=color.green,
     linewidth=2,
     style=plot.style_linebr)

plot(direction > 0 ? supertrend : na,
     color=color.red,
     linewidth=2,
     style=plot.style_linebr)

plot(dma200,
     color=color.orange,
     linewidth=2,
     title="200 DMA")

//----------------------------------------------------
// Labels
//----------------------------------------------------
if longSignal
    label.new(
         bar_index,
         low,
         "BUY\nConf: " + str.tostring(confidence) + "%\nBuyer: " +
         str.tostring(math.round(buyerDominance)) + "%\nMove: +" +
         str.tostring(math.round(expectedMovePercent,1)) + "%\n" +
         trendStrength,
         style=label.style_label_up,
         color=color.green,
         textcolor=color.white)

if shortSignal
    label.new(
         bar_index,
         high,
         "SELL\nConf: " + str.tostring(confidence) + "%\nSeller: " +
         str.tostring(math.round(sellerDominance)) + "%\nMove: -" +
         str.tostring(math.round(expectedMovePercent,1)) + "%\n" +
         trendStrength,
         style=label.style_label_down,
         color=color.red,
         textcolor=color.white)

//----------------------------------------------------
// Alerts
//----------------------------------------------------
alertcondition(longSignal, title="BUY", message="BUY Signal Generated")
alertcondition(shortSignal, title="SELL", message="SELL Signal Generated")