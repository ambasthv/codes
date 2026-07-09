//@version=5
strategy("Basic DMA Strategy", overlay=true, initial_capital=100000)

// =====================
// Inputs
// =====================
showDMA10  = input.bool(true,  "10 DMA")
showDMA20  = input.bool(false, "20 DMA")
showDMA50  = input.bool(true,  "50 DMA")
showDMA200 = input.bool(true,  "200 DMA")

signalMA = input.string(
     "50 DMA",
     title="Signal Moving Average",
     options=["10 DMA", "20 DMA", "50 DMA", "200 DMA"]
)

// =====================
// Daily Moving Averages
// =====================
dma10  = request.security(syminfo.tickerid, "D", ta.sma(close, 10))
dma20  = request.security(syminfo.tickerid, "D", ta.sma(close, 20))
dma50  = request.security(syminfo.tickerid, "D", ta.sma(close, 50))
dma200 = request.security(syminfo.tickerid, "D", ta.sma(close, 200))

// =====================
// Plot MAs
// =====================
plot(showDMA10  ? dma10  : na, title="10 DMA",  color=color.teal, linewidth=2)
plot(showDMA20  ? dma20  : na, title="20 DMA",  color=color.orange, linewidth=2)
plot(showDMA50  ? dma50  : na, title="50 DMA",  color=color.purple, linewidth=2)
plot(showDMA200 ? dma200 : na, title="200 DMA", color=color.black, linewidth=2)

// =====================
// Select Signal MA
// =====================
signalLine =
     signalMA == "10 DMA"  ? dma10 :
     signalMA == "20 DMA"  ? dma20 :
     signalMA == "50 DMA"  ? dma50 :
     dma200

// =====================
// Buy/Sell Conditions
// =====================
buySignal  = ta.crossover(close, signalLine)
sellSignal = ta.crossunder(close, signalLine)

// =====================
// Strategy Orders
// =====================
if buySignal
    strategy.close("Short")
    strategy.entry("Long", strategy.long)

if sellSignal
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

// =====================
// Buy/Sell Labels
// =====================
plotshape(
     buySignal,
     title="BUY",
     text="BUY",
     style=shape.labelup,
     location=location.belowbar,
     color=color.green,
     textcolor=color.white,
     size=size.small)

plotshape(
     sellSignal,
     title="SELL",
     text="SELL",
     style=shape.labeldown,
     location=location.abovebar,
     color=color.red,
     textcolor=color.white,
     size=size.small)

// =====================
// Alerts
// =====================
alertcondition(buySignal, title="Buy Alert", message="BUY Signal")
alertcondition(sellSignal, title="Sell Alert", message="SELL Signal")