# Niche Mapping
niche_mapping = {
    "SOFTWARE": "SOFTWARE",
    "LIFE SCIENCE": "LIFE SCIENCE",
    "HARDWARE": "HARDWARE",
    "NNO": "OTHER",
    "ERI": "OTHER",
    "ENERGY AND RESOURCE INNOVATION": "OTHER",
    "HEALTHCARE": "OTHER",
    "None": "OTHER",
    "RELIGIOUS": "OTHER",
    "REAL ESTATE": "OTHER",
    "NON-NICHE": "OTHER",
    "VENTURE CAPITAL": "OTHER",
    "PRIVATE BANK": "OTHER",
    "RELIGIOUS LENDING": "OTHER",
    "PREMIUM WINE": "OTHER",
    "PRIVATE EQUITY FUND": "OTHER"
}

# Apply mapping (replace '1205' with your actual column name if different)
df['niche_mapped'] = df['1205'].map(niche_mapping).fillna("OTHER")

print("Niche Mapping Applied Successfully!")
print(df['niche_mapped'].value_counts())