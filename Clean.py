import pandas as pd 

read = pd.read_csv("top5-players.csv")

print(read.shape)
print(read.isna().sum())



