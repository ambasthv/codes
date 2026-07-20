//@version=5
strategy("Nifty Intraday AI Pro v1.2 - Vivek's Strategy", shorttitle="AI Intraday Pro", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10, commission_type=strategy.commission.percent, commission_value=0.04, pyramiding=1, max_labels_count=500)

// ==================== INPUTS ====================
groupCore     = "Core Settings"
groupRisk     = "Risk Management"
groupST       = "Supertrend"
groupDashboard= "Dashboard"

mode = input.string("Safe", "Trading Mode", options=["Safe", "Aggressive"], group=groupCore)
useTrailing = input.bool(false, "Use Trailing Stop", group=groupRisk)

riskATR = input.float(1.5, "Stop Loss (ATR)", step=0.1, group=groupRisk)
rewardATR = input.float(3.0, "Take Profit (ATR)", step=0.1, group=groupRisk)

// Supertrend
stATRPeriod = input.int(10, "Supertrend ATR Length", minval=1, group=groupST)
stFactor    = input.float(3.0, "Supertrend Factor", step=0.1, group=groupST)

showDashboard = input.bool(true, "Show Dashboard", group=groupDashboard)

// ==================== CORE INDICATORS ====================
ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
dma200 = request.security(syminfo.tickerid, "D", ta.ema(close, 200))

vwapValue = ta.vwap(hlc3)
atrValue = ta.atr(14)
rsiValue = ta.rsi(close, 14)

[macdLine, signalLine, hist] = ta.macd(close, 12, 26, 9)
relVol = volume / ta.sma(volume, 20)

// Supertrend
[supertrend, direction] = ta.supertrend(stFactor, stATRPeriod)
stBull = direction < 0
stBear = direction > 0

// Market Structure (simplified)
swingHigh = ta.pivothigh(high, 5, 5)
swingLow  = ta.pivotlow(low, 5, 5)

// Confidence Engine
trendScore   = stBull ? 85 : stBear ? 15 : 50
momentumScore = rsiValue > 60 ? 80 : rsiValue < 40 ? 20 : 50
volumeScore   = relVol > 1.5 ? 80 : relVol > 1.0 ? 60 : 30
vwapScore     = close > vwapValue ? 70 : 30

sma20 = ta.sma(close, 20)
slopeValue = (sma20 - sma20[5]) / 5
atrScore = atrValue > ta.sma(atrValue, 20) ? 65 : 45

buyConfidence  = math.round((trendScore + momentumScore + volumeScore + vwapScore + atrScore) / 5 * (mode == "Aggressive" ? 1.15 : 1.0))
sellConfidence = math.round(100 - buyConfidence * 0.95)

buyerPressure = (close > open ? volume : 0) / (volume + 1)
sellerPressure = 1 - buyerPressure

isTrending = math.abs(slopeValue) > atrValue * 0.5
regime = isTrending ? (stBull ? "Strong Bull" : "Bear Trend") : "Sideways"

// Signals
buyReady     = stBull and close > ema20 and rsiValue > 50
buyConfirmed = buyReady and ta.crossover(close, supertrend)

sellReady     = stBear and close < ema20 and rsiValue < 50
sellConfirmed = sellReady and ta.crossunder(close, supertrend)

// ==================== STRATEGY ENTRIES & EXITS ====================
if buyConfirmed and strategy.position_size == 0 and buyConfidence >= (mode == "Safe" ? 65 : 55)
    strategy.entry("Long", strategy.long)

if sellConfirmed and strategy.position_size == 0 and sellConfidence >= (mode == "Safe" ? 65 : 55)
    strategy.entry("Short", strategy.short)

// Exits
slLong  = strategy.position_avg_price - riskATR * atrValue
tpLong  = strategy.position_avg_price + rewardATR * atrValue

slShort = strategy.position_avg_price + riskATR * atrValue
tpShort = strategy.position_avg_price - rewardATR * atrValue

if strategy.position_size > 0
    strategy.exit("Long Exit", "Long", stop=slLong, limit=tpLong, trail_points=useTrailing ? atrValue * 1.0 : na)

if strategy.position_size < 0
    strategy.exit("Short Exit", "Short", stop=slShort, limit=tpShort, trail_points=useTrailing ? atrValue * 1.0 : na)

// ==================== PLOTS & DASHBOARD (same as before) ====================
plot(ema20, "EMA 20", color=color.blue)
plot(ema50, "EMA 50", color=color.orange)
plot(dma200, "200 DMA", color=color.purple, linewidth=2)
plot(vwapValue, "VWAP", color=color.yellow, linewidth=2)
plot(supertrend, "Supertrend", color=stBull ? color.lime : color.red, linewidth=3, style=plot.style_linebr)

bgcolor(stBull ? color.new(color.green, 92) : stBear ? color.new(color.red, 92) : na)

// Dashboard
var table dash = table.new(position.top_right, 2, 11, bgcolor=color.new(color.black, 80), border_width=1)

if barstate.islast and showDashboard
    table.cell(dash, 0, 0, "BUY Conf", text_color=color.white)
    table.cell(dash, 1, 0, str.tostring(buyConfidence) + "%", text_color=buyConfidence > 70 ? color.lime : color.yellow)

    table.cell(dash, 0, 1, "SELL Conf", text_color=color.white)
    table.cell(dash, 1, 1, str.tostring(sellConfidence) + "%", text_color=sellConfidence > 70 ? color.red : color.orange)

    table.cell(dash, 0, 2, "Regime", text_color=color.white)
    table.cell(dash, 1, 2, regime, text_color=stBull ? color.lime : stBear ? color.red : color.gray)

    table.cell(dash, 0, 3, "Buyers %", text_color=color.white)
    table.cell(dash, 1, 3, str.tostring(math.round(buyerPressure*100)) + "%", text_color=color.lime)

    table.cell(dash, 0, 4, "Exp. Move", text_color=color.white)
    table.cell(dash, 1, 4, str.tostring(math.round(rewardATR * atrValue, 1)) + " pts", text_color=color.aqua)

    table.cell(dash, 0, 5, "Mode", text_color=color.white)
    table.cell(dash, 1, 5, mode, text_color=mode=="Safe" ? color.blue : color.fuchsia)

// Alerts
if buyConfirmed
    alert("🚀 Nifty LONG Entry | Conf: " + str.tostring(buyConfidence) + "%", alert.freq_once_per_bar)
if sellConfirmed
    alert("🔻 Nifty SHORT Entry | Conf: " + str.tostring(sellConfidence) + "%", alert.freq_once_per_bar)