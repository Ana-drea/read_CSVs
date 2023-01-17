import os.path
import os
import glob
import pandas as pd

sort_order = ["DEU", "FRA", "ITA", "ESP", "JPN", "KOR", "CHT", "CHS", "CSY", "PLK", "HUN", "RUS", "PTB"]


def sum_csv(path):
    df = pd.read_csv(path, encoding="utf-8", sep=';', header=1, usecols=[4, 9, 14, 19, 24, 29, 34, 39],
                     names=["Context Match", "Repetitions", "100%", "95% - 99%", "85% - 94%", "75% - 84%", "50% - 74%",
                            "No Match"])
    filename = os.path.basename(path)
    lan_code = filename[:5].upper()
    df2 = df.iloc[:, :].sum()
    df3 = df2.transpose()

    df3.columns = ["", lan_code]
    return [df3, lan_code]




p = input("Type in the folder containing the csv files:\n")
res = sum_csv(p)
print(res)
