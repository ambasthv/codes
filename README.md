//@version=5
indicator(title="Vivek Nifty Master [5min]", overlay=true, max_labels_count=500, max_lines_count=200)

C_BUY   = color.new(#00E5FF, 0)
C_SELL  = color.new(#FF1744, 0)
C_VWAP  = color.new(#FFD600, 0)
C_ST_UP = color.new(#00C853, 0)
C_ST_DN = color.new(#FF1744, 0)
C_SL    = color.new(#FF6D00, 80)
C_TGT   = color.new(#00E676, 80)

ut_key     = input.int(1,       "UT Bot | Key Value",      group="1 · UT Bot")
ut_atr     = input.int(10,      "UT Bot | ATR Period",     group="1 · UT Bot")
ut_ha      = input.bool(false,  "UT Bot | Heikin Ashi",    group="1 · UT Bot")
stc_len    = input.int(12,      "STC | Cycle Length",      group="2 · STC")
stc_fast   = input.int(26,      "STC | Fast EMA",          group="2 · STC")
stc_slow   = input.int(50,      "STC | Slow EMA",          group="2 · STC")
stc_smth   = input.float(0.5,   "STC | Smoothing",         group="2 · STC", step=0.1)
qqe_rsi    = input.int(14,      "QQE | RSI Length",        group="3 · QQE")
qqe_sf     = input.int(5,       "QQE | RSI Smoothing",     group="3 · QQE")
qqe_fac    = input.float(4.238, "QQE | Fast Factor",       group="3 · QQE")
st_atr     = input.int(10,      "Supertrend | ATR Period", group="4 · Supertrend")
st_mult    = input.float(3.0,   "Supertrend | Multiplier", group="4 · Supertrend")
adx_len    = input.int(14,      "ADX | Length",            group="5 · ADX")
adx_thresh = input.int(20,      "ADX | Min Strength",      group="5 · ADX")
show_vwap  = input.bool(true,   "Show VWAP",               group="6 · VWAP")
sig_mode   = input.string("MAJORITY (3 of 4)", "Confirmation Mode", options=["ALL AGREE (4 of 4)", "MAJORITY (3 of 4)"], group="7 · Signal Logic")
sl_mult    = input.float(1.5,   "SL  | ATR Multiplier",   group="8 · SL & Target")
tgt_mult   = input.float(3.0,   "TGT | ATR Multiplier",   group="8 · SL & Target")
show_sltgt = input.bool(true,   "Show SL/Target Lines",    group="8 · SL & Target")

ut_src   = ut_ha ? request.security(ticker.heikinashi(syminfo.tickerid), timeframe.period, close) : close
ut_xATR  = ta.atr(ut_atr)
ut_nLoss = ut_key * ut_xATR

var float ut_trail = 0.0
ut_trail := (ut_src > nz(ut_trail[1]) and ut_src[1] > nz(ut_trail[1])) ? math.max(nz(ut_trail[1]), ut_src - ut_nLoss) : (ut_src < nz(ut_trail[1]) and ut_src[1] < nz(ut_trail[1])) ? math.min(nz(ut_trail[1]), ut_src + ut_nLoss) : (ut_src > nz(ut_trail[1])) ? ut_src - ut_nLoss : ut_src + ut_nLoss

var int ut_pos = 0
ut_pos := (ut_src[1] < nz(ut_trail[1]) and ut_src > nz(ut_trail[1])) ? 1 : (ut_src[1] > nz(ut_trail[1]) and ut_src < nz(ut_trail[1])) ? -1 : nz(ut_pos[1])

ut_ema  = ta.ema(ut_src, 1)
ut_buy  = ut_src > ut_trail and ta.crossover(ut_ema, ut_trail)
ut_sell = ut_src < ut_trail and ta.crossover(ut_trail, ut_ema)

_macd(s, f, sl) => ta.ema(s, f) - ta.ema(s, sl)

_stc(len, fast, slow, smth) =>
    var float f1  = 0.0
    var float pf  = 0.0
    var float f2  = 0.0
    var float pff = 0.0
    float macd = _macd(close, fast, slow)
    float lo1  = ta.lowest(macd, len)
    float hi1  = ta.highest(macd, len) - lo1
    f1  := hi1 > 0 ? (macd - lo1) / hi1 * 100 : nz(f1[1])
    pf  := na(pf[1]) ? f1 : pf[1] + smth * (f1 - pf[1])
    float lo2 = ta.lowest(pf, len)
    float hi2 = ta.highest(pf, len) - lo2
    f2  := hi2 > 0 ? (pf - lo2) / hi2 * 100 : nz(f2[1])
    pff := na(pff[1]) ? f2 : pff[1] + smth * (f2 - pff[1])
    pff

stc_val  = _stc(stc_len, stc_fast, stc_slow, stc_smth)
stc_bull = stc_val > stc_val[1] and stc_val < 75
stc_bear = stc_val < stc_val[1] and stc_val > 25

qqe_wild  = qqe_rsi * 2 - 1
qqe_rsiV  = ta.rsi(close, qqe_rsi)
qqe_rsiMa = ta.ema(qqe_rsiV, qqe_sf)
qqe_atrR  = math.abs(qqe_rsiMa[1] - qqe_rsiMa)
qqe_maAtr = ta.ema(qqe_atrR, qqe_wild)
qqe_dar   = ta.ema(qqe_maAtr, qqe_wild) * qqe_fac

var float qqe_lb = 0.0
var float qqe_sb = 0.0
var int   qqe_tr = 0

qqe_lb := (qqe_rsiMa[1] > qqe_lb[1] and qqe_rsiMa > qqe_lb[1]) ? math.max(qqe_lb[1], qqe_rsiMa - qqe_dar) : qqe_rsiMa - qqe_dar
qqe_sb := (qqe_rsiMa[1] < qqe_sb[1] and qqe_rsiMa < qqe_sb[1]) ? math.min(qqe_sb[1], qqe_rsiMa + qqe_dar) : qqe_rsiMa + qqe_dar
qqe_tr := ta.cross(qqe_rsiMa, qqe_sb[1]) ? 1 : ta.cross(qqe_lb[1], qqe_rsiMa) ? -1 : nz(qqe_tr[1], 1)

var int qqe_xl = 0
var int qqe_xs = 0
qqe_xl   := qqe_tr ==  1 ? qqe_xl + 1 : 0
qqe_xs   := qqe_tr == -1 ? qqe_xs + 1 : 0
qqe_bull  = qqe_xl == 1
qqe_bear  = qqe_xs == 1

[st_val, st_dir] = ta.supertrend(st_mult, st_atr)
st_bull = st_dir < 0
st_bear = st_dir > 0
plot(st_bull ? st_val : na, "ST Bull", color=C_ST_UP, linewidth=2, style=plot.style_linebr)
plot(st_bear ? st_val : na, "ST Bear", color=C_ST_DN, linewidth=2, style=plot.style_linebr)

[_, __, adx_val] = ta.dmi(adx_len, adx_len)
adx_ok = adx_val >= adx_thresh

vwap_val = ta.vwap(hlc3)
plot(show_vwap ? vwap_val : na, "VWAP", color=C_VWAP, linewidth=2)

bool ut_bull_state = ut_pos ==  1
bool ut_bear_state = ut_pos == -1
int bull_score = (ut_bull_state ? 1 : 0) + (stc_bull ? 1 : 0) + (qqe_tr ==  1 ? 1 : 0) + (st_bull ? 1 : 0)
int bear_score = (ut_bear_state ? 1 : 0) + (stc_bear ? 1 : 0) + (qqe_tr == -1 ? 1 : 0) + (st_bear ? 1 : 0)
int req = sig_mode == "ALL AGREE (4 of 4)" ? 4 : 3

bool BUY_SIGNAL  = (ut_buy  or qqe_bull) and bull_score >= req and adx_ok and close > vwap_val
bool SELL_SIGNAL = (ut_sell or qqe_bear) and bear_score >= req and adx_ok and close < vwap_val

float atr14    = ta.atr(14)
var float sl_line  = na
var float tgt_line = na

if BUY_SIGNAL
    sl_line  := close - sl_mult  * atr14
    tgt_line := close + tgt_mult * atr14
    if show_sltgt
        line.new(bar_index, sl_line,  bar_index + 15, sl_line,  color=C_SL,  width=1, style=line.style_dashed)
        line.new(bar_index, tgt_line, bar_index + 15, tgt_line, color=C_TGT, width=1, style=line.style_dashed)

if SELL_SIGNAL
    sl_line  := close + sl_mult  * atr14
    tgt_line := close - tgt_mult * atr14
    if show_sltgt
        line.new(bar_index, sl_line,  bar_index + 15, sl_line,  color=C_SL,  width=1, style=line.style_dashed)
        line.new(bar_index, tgt_line, bar_index + 15, tgt_line, color=C_TGT, width=1, style=line.style_dashed)

plotshape(BUY_SIGNAL,  title="BUY",  text="BUY",  style=shape.labelup,   location=location.belowbar, color=C_BUY,  textcolor=color.black, size=size.normal)
plotshape(SELL_SIGNAL, title="SELL", text="SELL", style=shape.labeldown, location=location.abovebar, color=C_SELL, textcolor=color.white, size=size.normal)

barcolor(BUY_SIGNAL  ? C_BUY  : na)
barcolor(SELL_SIGNAL ? C_SELL : na)
bgcolor(BUY_SIGNAL   ? color.new(C_BUY,  88) : na)
bgcolor(SELL_SIGNAL  ? color.new(C_SELL, 88) : na)

var table info = table.new(position.top_right, 2, 7, bgcolor=color.new(#0D1117, 10), border_color=color.new(#30363D, 0), border_width=1)
_c(col, row, txt, bg, tc) => table.cell(info, col, row, txt, bgcolor=bg, text_color=tc, text_size=size.small)

_c(0, 0, "INDICATOR",  color.new(#21262D, 0), color.new(#8B949E, 0))
_c(1, 0, "STATUS",     color.new(#21262D, 0), color.new(#8B949E, 0))
_c(0, 1, "UT Bot",     color.new(#161B22, 0), color.white)
_c(1, 1, ut_bull_state ? "BULL" : "BEAR", ut_bull_state ? color.new(#00C853, 40) : color.new(#FF1744, 40), color.white)
_c(0, 2, "STC",        color.new(#161B22, 0), color.white)
_c(1, 2, stc_bull ? "BULL" : "BEAR",     stc_bull      ? color.new(#00C853, 40) : color.new(#FF1744, 40), color.white)
_c(0, 3, "QQE",        color.new(#161B22, 0), color.white)
_c(1, 3, qqe_tr == 1 ? "BULL" : "BEAR",  qqe_tr == 1   ? color.new(#00C853, 40) : color.new(#FF1744, 40), color.white)
_c(0, 4, "Supertrend", color.new(#161B22, 0), color.white)
_c(1, 4, st_bull ? "BULL" : "BEAR",      st_bull       ? color.new(#00C853, 40) : color.new(#FF1744, 40), color.white)
_c(0, 5, "ADX",        color.new(#161B22, 0), color.white)
_c(1, 5, adx_ok ? str.tostring(math.round(adx_val)) + " OK" : str.tostring(math.round(adx_val)) + " WEAK", adx_ok ? color.new(#00C853, 40) : color.new(#FF6D00, 40), color.white)
_c(0, 6, "VWAP",       color.new(#161B22, 0), color.white)
_c(1, 6, close > vwap_val ? "ABOVE" : "BELOW", close > vwap_val ? color.new(#00C853, 40) : color.new(#FF1744, 40), color.white)

alertcondition(BUY_SIGNAL,               title="VIVEK BUY",           message="BUY | {ticker} | {interval}min | Price: {close}")
alertcondition(SELL_SIGNAL,              title="VIVEK SELL",          message="SELL | {ticker} | {interval}min | Price: {close}")
alertcondition(BUY_SIGNAL or SELL_SIGNAL,title="VIVEK Master Signal", message="SIGNAL | {ticker} | {interval}min | Price: {close}")
