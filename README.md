//@version=5
strategy("Vivek Basic DMA Strategy", overlay=true, initial_capital=100000)

// Inputs
showDMA10  = input.bool(true, title="Show 10 DMA")
showDMA20  = input.bool(false, title="Show 20 DMA")
showDMA50  = input.bool(true, title="Show 50 DMA")
showDMA200 = input.bool(true, title="Show 200 DMA")

signalMA = input.string("50 DMA", title="Signal Moving Average", options=["10 DMA", "20 DMA", "50 DMA", "200 DMA"])

// Daily Moving Averages
dma10  = request.security(syminfo.tickerid, "D", ta.sma(close, 10))
dma20  = request.security(syminfo.tickerid, "D", ta.sma(close, 20))
dma50  = request.security(syminfo.tickerid, "D", ta.sma(close, 50))
dma200 = request.security(syminfo.tickerid, "D", ta.sma(close, 200))

// Plot Moving Averages
plot(showDMA10 ? dma10 : na, title="10 DMA", color=color.teal, linewidth=2)
plot(showDMA20 ? dma20 : na, title="20 DMA", color=color.orange, linewidth=2)
plot(showDMA50 ? dma50 : na, title="50 DMA", color=color.purple, linewidth=2)
plot(showDMA200 ? dma200 : na, title="200 DMA", color=color.black, linewidth=2)

// Select Signal Line
signalLine = dma50

if signalMA == "10 DMA"
    signalLine := dma10
else if signalMA == "20 DMA"
    signalLine := dma20
else if signalMA == "50 DMA"
    signalLine := dma50
else
    signalLine := dma200

// Buy and Sell Conditions
buySignal = ta.crossover(close, signalLine)
sellSignal = ta.crossunder(close, signalLine)

// Strategy Orders
if buySignal
    strategy.close("Short")
    strategy.entry("Long", strategy.long)

if sellSignal
    strategy.close("Long")
    strategy.entry("Short", strategy.short)

// Buy Label
plotshape(
     buySignal,
     title="BUY",
     text="BUY",
     style=shape.labelup,
     location=location.belowbar,
     color=color.green,
     textcolor=color.white,
     size=size.small)

// Sell Label
plotshape(
     sellSignal,
     title="SELL",
     text="SELL",
     style=shape.labeldown,
     location=location.abovebar,
     color=color.red,
     textcolor=color.white,
     size=size.small)

// Alerts
alertcondition(buySignal, title="Buy Alert", message="BUY signal generated")
alertcondition(sellSignal, title="Sell Alert", message="SELL signal generated")