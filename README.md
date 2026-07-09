//@version=6
strategy("Supertrend AI Intraday Strategy", overlay=true,
     initial_capital=100000,
     default_qty_type=strategy.percent_of_equity,
     default_qty_value=100,
     pyramiding=0)

// ===================== INPUTS =====================
stAtr      = input.int(7, "Supertrend ATR")
stFactor   = input.float(2.2, "Supertrend Factor")
rsiBuy     = input.int(58, "RSI Buy Level")
rsiSell    = input.int(48, "RSI Sell Level")
adxMin     = input.int(22, "Minimum ADX")
volFactor  = input.float(1.3, "Relative Volume")
buyerMin   = input.int(58, "Buyer Dominance %")
breakoutLB = input.int(5, "Breakout Lookback")

// ===================== INDICATORS =====================
[st, dir] = ta.supertrend(stFactor, stAtr)

rsi = ta.rsi(close,14)
dma200 = ta.sma(close,200)
vwapVal = ta.vwap(close)
volMA = ta.sma(volume,20)
atr = ta.atr(14)

[macdLine,signalLine,_] = ta.macd(close,12,26,9)

// ---------- Manual ADX ----------
upMove = high-high[1]
downMove = low[1]-low

plusDM = upMove > downMove and upMove > 0 ? upMove : 0
minusDM = downMove > upMove and downMove > 0 ? downMove : 0

tr = ta.tr(true)

plusDI = 100 * ta.rma(plusDM,14) / ta.rma(tr,14)
minusDI = 100 * ta.rma(minusDM,14) / ta.rma(tr,14)

dx = 100 * math.abs(plusDI-minusDI) / (plusDI+minusDI)
adx = ta.rma(dx,14)

// ===================== VOLUME DOMINANCE =====================
buyVol = close > open ? volume : 0
sellVol = close < open ? volume : 0

buyers = ta.sma(buyVol,20)
sellers = ta.sma(sellVol,20)

buyerPct = (buyers/(buyers+sellers))*100
sellerPct = 100-buyerPct

// ===================== CONFIDENCE ENGINE =====================
confidence = 0.0

confidence += dir < 0 ? 20 : 0
confidence += close > dma200 ? 15 : 0
confidence += adx > adxMin ? 15 : 0
confidence += volume > volMA*volFactor ? 15 : 0
confidence += rsi > rsiBuy ? 10 : 0
confidence += macdLine > signalLine ? 10 : 0
confidence += close > vwapVal ? 10 : 0
confidence += atr > ta.sma(atr,20) ? 5 : 0

// ===================== ENTRY FILTERS =====================
breakout = close > ta.highest(high, breakoutLB)[1]

longEntry =
     dir < 0 and dir[1] > 0 and
     rsi > rsiBuy and
     adx > adxMin and
     volume > volMA * volFactor and
     buyerPct > buyerMin and
     close > dma200 and
     close > vwapVal and
     breakout

// ===================== EXIT CONDITIONS =====================
exitScore = 0

exitScore += dir > 0 ? 1 : 0
exitScore += rsi < rsiSell ? 1 : 0
exitScore += macdLine < signalLine ? 1 : 0
exitScore += sellerPct > 60 ? 1 : 0
exitScore += close < vwapVal ? 1 : 0

exitLong = exitScore >= 2

// ===================== TARGETS =====================
targetATR =
     confidence >= 90 ? 4 :
     confidence >= 80 ? 3 :
     confidence >= 70 ? 2 :
     1.5

longTP = strategy.position_avg_price + atr * targetATR
longSL = strategy.position_avg_price - atr * 1.5

// ===================== STRATEGY =====================
if longEntry
    strategy.entry("Long", strategy.long)

strategy.exit(
     "Exit Long",
     "Long",
     stop=longSL,
     limit=longTP)

if exitLong
    strategy.close("Long")

// ===================== PLOTS =====================
plot(dir < 0 ? st : na,
     color=color.green,
     linewidth=2,
     style=plot.style_linebr)

plot(dir > 0 ? st : na,
     color=color.red,
     linewidth=2,
     style=plot.style_linebr)

plot(dma200,color=color.orange,linewidth=2,title="200 DMA")

// ===================== LABELS =====================
if longEntry
    label.new(
         bar_index,
         low,
         "BUY\n" +
         "Conf: "+str.tostring(math.round(confidence))+"%\n"+
         "Buyers: "+str.tostring(math.round(buyerPct))+"%\n"+
         "ADX: "+str.tostring(math.round(adx))+"\n"+
         "Exp Move: "+str.tostring(math.round(targetATR*atr/close*100,1))+"%",
         style=label.style_label_up,
         color=color.green,
         textcolor=color.white)

// ===================== ALERTS =====================
alertcondition(longEntry,"BUY","AI BUY Signal")
alertcondition(exitLong,"SELL","AI SELL Signal")