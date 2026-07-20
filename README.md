//@version=5
indicator("Nifty Intraday AI Pro v1.0 - Vivek's Dashboard", shorttitle="AI Intraday Pro", overlay=true, max_labels_count=500, max_lines_count=500, max_boxes_count=500)

// ==================== INPUTS ====================
groupCore     = "Core Settings"
groupST       = "Supertrend"
groupDashboard= "Dashboard"

mode = input.string("Safe", "Trading Mode", options=["Safe", "Aggressive"], group=groupCore)
showDashboard = input.bool(true, "Show Dashboard", group=groupDashboard)

// Supertrend
stATRPeriod = input.int(10, "Supertrend ATR Length", minval=1, group=groupST)
stFactor    = input.float(3.0, "Supertrend Factor", step=0.1, group=groupST)

// ==================== CORE INDICATORS ====================
ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
dma200 = request.security(syminfo.tickerid, "D", ta.ema(close, 200))

vwapValue = ta.vwap(hlc3)
atrValue = ta.atr(14)
rsiValue = ta.rsi(close, 14)

[macdLine, signalLine, hist] = ta.macd(close, 12, 26, 9)

// Relative Volume (simple approximation)
relVol = volume / ta.sma(volume, 20)

// Supertrend
[supertrend, direction] = ta.supertrend(stFactor, stATRPeriod)
stBull = direction < 0
stBear = direction > 0

// ==================== MARKET STRUCTURE ====================
swingHigh = ta.pivothigh(high, 5, 5)
swingLow  = ta.pivotlow(low, 5, 5)

var float lastSwingHigh = na
var float lastSwingLow  = na

if not na(swingHigh)
    lastSwingHigh := swingHigh
if not na(swingLow)
    lastSwingLow := swingLow

higherHigh = high > nz(lastSwingHigh[1])
lowerLow   = low < nz(lastSwingLow[1])

// ==================== CONFIDENCE ENGINE ====================
trendScore   = stBull ? 85 : stBear ? 15 : 50
momentumScore = rsiValue > 60 ? 80 : rsiValue < 40 ? 20 : 50
volumeScore   = relVol > 1.5 ? 80 : relVol > 1.0 ? 60 : 30
vwapScore     = close > vwapValue ? 70 : 30
atrScore      = atrValue > ta.sma(atrValue, 20) ? 65 : 45

buyConfidence  = math.round((trendScore + momentumScore + volumeScore + vwapScore + atrScore) / 5 * (mode == "Aggressive" ? 1.15 : 1.0))
sellConfidence = math.round(100 - buyConfidence * 0.95)  // Slight asymmetry

buyerPressure = (close > open ? volume : 0) / (volume + 1)
sellerPressure = 1 - buyerPressure

// Market Regime
isTrending = math.abs(ta.slope(ta.sma(close, 20), 5)) > atrValue * 0.5
regime = isTrending ? (stBull ? "Strong Bull" : "Bear Trend") : "Sideways"

// ==================== SIGNALS ====================
buyReady     = stBull and close > ema20 and rsiValue > 50
buyConfirmed = buyReady and ta.crossover(close, supertrend)

sellReady     = stBear and close < ema20 and rsiValue < 50
sellConfirmed = sellReady and ta.crossunder(close, supertrend)

// Early Entry (Aggressive mode)
earlyBuy  = mode == "Aggressive" and buyReady and not buyConfirmed
earlySell = mode == "Aggressive" and sellReady and not sellConfirmed

// ==================== PLOTS ====================
plot(ema20, "EMA 20", color=color.blue)
plot(ema50, "EMA 50", color=color.orange)
plot(dma200, "200 DMA", color=color.purple, linewidth=2)

plot(vwapValue, "VWAP", color=color.yellow, linewidth=2)

plot(showSupertrend ? supertrend : na, "Supertrend", color=stBull ? color.lime : color.red, linewidth=3, style=plot.style_linebr)

bgcolor(stBull ? color.new(color.green, 92) : stBear ? color.new(color.red, 92) : na)

// Labels
if buyConfirmed
    label.new(bar_index, low, "BUY\nCONFIRMED", color=color.green, style=label.style_label_up, textcolor=color.white)

if sellConfirmed
    label.new(bar_index, high, "SELL\nCONFIRMED", color=color.red, style=label.style_label_down, textcolor=color.white)

// ==================== PROFESSIONAL DASHBOARD ====================
var table dash = table.new(position.top_right, 2, 10, bgcolor=color.new(color.black, 80), border_width=1)

if barstate.islast
    table.cell(dash, 0, 0, "BUY Conf",  text_color=color.white)
    table.cell(dash, 1, 0, str.tostring(buyConfidence) + "%",  text_color=buyConfidence > 70 ? color.lime : color.yellow)

    table.cell(dash, 0, 1, "SELL Conf", text_color=color.white)
    table.cell(dash, 1, 1, str.tostring(sellConfidence) + "%", text_color=sellConfidence > 70 ? color.red : color.orange)

    table.cell(dash, 0, 2, "Regime", text_color=color.white)
    table.cell(dash, 1, 2, regime, text_color=stBull ? color.lime : stBear ? color.red : color.gray)

    table.cell(dash, 0, 3, "Buyers", text_color=color.white)
    table.cell(dash, 1, 3, str.tostring(math.round(buyerPressure*100)) + "%", text_color=color.lime)

    table.cell(dash, 0, 4, "Sellers", text_color=color.white)
    table.cell(dash, 1, 4, str.tostring(math.round(sellerPressure*100)) + "%", text_color=color.red)

    table.cell(dash, 0, 5, "Expected Move", text_color=color.white)
    table.cell(dash, 1, 5, str.tostring(math.round(2.5 * atrValue, 1)) + " pts", text_color=color.aqua)

    table.cell(dash, 0, 6, "Mode", text_color=color.white)
    table.cell(dash, 1, 6, mode, text_color=mode=="Safe" ? color.blue : color.fuchsia)

// ==================== ALERTS ====================
if buyConfirmed
    alert("Nifty BUY CONFIRMED - Confidence: " + str.tostring(buyConfidence) + "%", alert.freq_once_per_bar)

if sellConfirmed
    alert("Nifty SELL CONFIRMED - Confidence: " + str.tostring(sellConfidence) + "%", alert.freq_once_per_bar)