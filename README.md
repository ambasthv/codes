//@version=1
study("Basic DMA's", overlay=true)
// inputs
dma10 = input(true, title="10 DMA")
dma20 = input(false, title="20 DMA")
dma50 = input(true, title="50 DMA")
dma200= input(true, title="200 DMA")
// Color reference: https://www.rapidtables.com/web/color/html-color-codes.html
plot((dma10)?security(tickerid, "D", sma(close, 10)):na, title="10 DMA", color=#008B8B, linewidth=0, style=line, transp=0)
plot((dma20)?security(tickerid, "D", sma(close, 20)):na, title="20 DMA", color=orange, linewidth=0, style=line, transp=0)
plot((dma50)?security(tickerid, "D", sma(close, 50)):na, title="50 DMA", color=#FF1493, linewidth=0, style=line, transp=0)
plot((dma200)?security(tickerid, "D", sma(close, 200)):na, title="200 DMA", color=black, linewidth=0, style=line, transp=0)
