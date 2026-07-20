
//--------------------------------------------------
// RELATIVE VOLUME
//--------------------------------------------------

volLength = input.int(20, "Relative Volume Length", group=groupVolume)

volMA = ta.sma(volume, volLength)
relativeVolume := volMA > 0 ? volume / volMA : 1.0

//--------------------------------------------------
// TREND STATE
//--------------------------------------------------

bool bullishTrend =
     close > ema20 and
     ema20 > ema50 and
     ema50 > dma200

bool bearishTrend =
     close < ema20 and
     ema20 < ema50 and
     ema50 < dma200

marketState :=
     bullishTrend ? "Bullish" :
     bearishTrend ? "Bearish" :
     "Sideways"

//--------------------------------------------------
// ATR INFORMATION
//--------------------------------------------------

atrPercent = atr / close * 100

//--------------------------------------------------
// MACD INFORMATION
//--------------------------------------------------

macdBull = macdLine > signalLine
macdBear = macdLine < signalLine

//--------------------------------------------------
// MOMENTUM SCORE
//--------------------------------------------------

int momentumScore = 0

if rsi > 60
    momentumScore += 1

if macdBull
    momentumScore += 1

if relativeVolume > 1.20
    momentumScore += 1

trendStrength =
     momentumScore == 3 ? "Strong" :
     momentumScore == 2 ? "Medium" :
     momentumScore == 1 ? "Weak" :
     "Poor"

===

table.cell(
     dashboard,
     1,
     2,
     marketState,
     text_color =
          bullishTrend ? color.lime :
          bearishTrend ? color.red :
          color.orange)

===

table.cell(
     dashboard,
     1,
     5,
     trendStrength,
     text_color =
          momentumScore == 3 ? color.lime :
          momentumScore == 2 ? color.green :
          momentumScore == 1 ? color.orange :
          color.red)

===


table.cell(
     dashboard,
     1,
     6,
     "RSI " +
     str.tostring(math.round(rsi)) +
     " | RV " +
     str.tostring(relativeVolume, "#.##"))
