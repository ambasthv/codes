print("Columns related to receivables:")
print([c for c in df.columns if 'rec' in c.lower() or 'receiv' in c.lower()])