//=============================================================================
// INDICATORS
//=============================================================================

//--------------------------------------------------
// Moving Averages
//--------------------------------------------------

ema20 := ta.ema(close,20)
ema50 := ta.ema(close,50)

dma200 := request.security(
     syminfo.tickerid,
     "D",
     ta.sma(close,200))

plot(
     ema20,
     title="EMA 20",
     color=color.aqua,
     linewidth=2)

plot(
     ema50,
     title="EMA 50",
     color=color.orange,
     linewidth=2)

plot(
     dma200,
     title="200 DMA",
     color=color.white,
     linewidth=3)

//--------------------------------------------------
// VWAP
//--------------------------------------------------

vwapValue := ta.vwap(close)

plot(
     vwapValue,
     title="VWAP",
     color=color.yellow,
     linewidth=2)

//--------------------------------------------------
// ATR
//--------------------------------------------------

atr := ta.atr(14)

//--------------------------------------------------
// RSI
//--------------------------------------------------

rsi := ta.rsi(close,14)

//--------------------------------------------------
// MACD
//--------------------------------------------------

[macdLine,signalLine,histogram] :=
     ta.macd(
     close,
     12,
     26,
     9)






=======
table.cell(
     dashboard,
     1,
     5,
     close > ema20 ?
     "Bullish" :
     "Bearish",
     text_color=
     close > ema20 ?
     color.lime :
     color.red)

=====
 
table.cell(
     dashboard,
     1,
     6,
     str.tostring(
          math.round(rsi)),
     text_color=
          rsi>60?
          color.lime:
          rsi<40?
          color.red:
          color.orange)