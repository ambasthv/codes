from pathlib import Path
import matplotlib.pyplot as plt

style_file = Path(
    r"C:\Vivek Ambastha\Dev\dev-id-bsd-model\01. Code\model_development\utils\resources\ow_style.mplstyle"
)

print("Style file:")
print(style_file)

print("Does it exist?")
print(style_file.exists())

plt.style.use(str(style_file))

print("STYLE LOADED SUCCESSFULLY")