# load in OW color scheme and plot style
print("CODE_ROOT:", CODE_ROOT)
print(
    "Style exists:",
    (CODE_ROOT / 'model_development/utils/resources/ow_style.mplstyle').exists()
)

plt.style.use(str(
    CODE_ROOT / 'model_development/utils/resources/ow_style.mplstyle'
))