import os.path
import os
import glob
import pandas as pd
from pandas import DataFrame, Series

sort_order = ["DEU", "FRA", "ITA", "ESP", "JPN", "KOR", "CHT", "CHS", "CSY", "PLK", "HUN", "RUS", "PTB"]
index_order = ["Context Match", "100%", "Repetitions", "95% - 99%", "75%-95% Fuzzy",
               "0%-75% - New",
               "Post Editing - Raw MT Output - New"]


def sum_csv(path):
    df_1 = pd.read_csv(path, encoding="utf-8", sep=';', header=1, usecols=[4, 12],
                       names=["Context Match", "100%"])
    df_2 = pd.read_csv(path, encoding="utf-8", sep=';', header=1, usecols=[8, 16],
                       names=["Repetitions", "95% - 99%"])
    df: DataFrame | Series = pd.concat([df_1, df_2], axis=1)
    # sum the 85% - 94% (Words) & 75% - 84% (Words) into 75%-95% Fuzzy
    df["75%-95% Fuzzy"] = pd.read_csv(path, encoding="utf-8", sep=';', header=1, usecols=[20, 24]).sum(axis=1)
    df["0%-75% - New"] = pd.DataFrame([0])
    # sum the 50% - 74% (Words) & No Match (Words) into Post Editing - Raw MT Output - New
    df["Post Editing - Raw MT Output - New"] = pd.read_csv(path, encoding="utf-8", sep=';', header=1,
                                                           usecols=[28, 32]).sum(axis=1)
    filename = os.path.basename(path)
    lan_code = filename[:3].upper()
    df2 = df.iloc[:, :].sum()
    df3 = pd.DataFrame(df2, columns=[lan_code])
    return [df3, lan_code]


def sum_CSVs_in_project(path):
    # collecting all the files matching '*.csv' under the given path
    all_csv = glob.glob(os.path.join(path, '*.csv'))
    res_dic = {}
    all_data_frames = []

    for csv in all_csv:
        res = sum_csv(csv)
        res_dic[res[1]] = res[0]
    # looking for language code in the dict with the given order, pop out the corresponding dataframe
    for lan in sort_order:
        empty_df = pd.DataFrame([0, 0, 0, 0, 0, 0, 0],
                                index=index_order, columns=[lan])
        # empty_df is the default value if target lan doesn't exist in res_dic
        data = res_dic.pop(lan, empty_df)
        all_data_frames.append(data)

    data_frame_4_project = pd.concat(all_data_frames,
                                     axis=1)  # axis = 0, data will concat vertically; axis = 1,data will concat horizontally.
    return data_frame_4_project


dfs = []
p = input("Type in the root folder containing the csv files:\n")
for project in os.listdir(p):
    project_path = os.path.join(p, project)
    if os.path.isdir(project_path):
        df = sum_CSVs_in_project(project_path)
        dfs.append(df)
df = dfs[0]
shape = df.shape
# concat all the dataframes into a single sheet
dataframes = pd.concat(dfs, axis=0)
df_sum = pd.DataFrame(columns=sort_order, index=index_order)

# add the wordcount of all sheets together
for i in range(shape[0]):
    for j in range(shape[1]):
        sum = 0
        for k in range(len(dfs)):
            sum += dfs[k].iloc[i, j]
        df_sum.iloc[i, j] = sum

# write the result to excel file
dataframes.to_excel(os.path.join(p, 'wordcounts.xlsx'))
df_sum.to_excel(os.path.join(p, 'sum.xlsx'))


