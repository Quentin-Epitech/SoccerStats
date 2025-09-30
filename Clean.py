import pandas as pd 

read = pd.read_csv("top5-players.csv")

print(read.shape)
print(read.isna().sum())


nettoyage = read.fillna("None")

output_path = "Clean.csv"
nettoyage.to_csv(output_path, index=False)

print(f"Fichier: {output_path}")

