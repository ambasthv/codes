
print("Current working directory:")
print(os.getcwd())

print("\nPROJECT_ROOT:")
print(PROJECT_ROOT)

print("\nCODE_ROOT:")
print(CODE_ROOT)

print("\nStyle file:")
print(CODE_ROOT / "model_development" / "utils" / "resources" / "ow_style.mplstyle")

print("\nStyle file exists:")
print((CODE_ROOT / "model_development" / "utils" / "resources" / "ow_style.mplstyle").exists())