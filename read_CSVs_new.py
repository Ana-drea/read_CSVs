import os.path
import os
import glob
import pandas as pd

sort_order = ["DEU", "FRA", "ITA", "ESP", "JPN", "KOR", "CHT", "CHS", "CSY", "PLK", "HUN", "RUS", "PTB"]


def sum_csv(path):
    df = pd.read_csv(path, encoding="utf-8", sep=';', header=1, usecols=[4, 8, 12, 16, 20, 24, 28, 32],
                     names=["Context Match", "Repetitions", "100%", "95% - 99%", "85% - 94%", "75% - 84%", "50% - 74%",
                            "No Match"])

    filename = os.path.basename(path)
    lan_code = filename[:3].upper()
    df2 = df.iloc[:, :].sum()
    df3 = df2.transpose()

    df3.columns = ["", lan_code]
    return [df3, lan_code]


def sum_CSVs_in_folder(path):
    #collecting all the files matching '*.csv' under the given path
    all_csv = glob.glob(os.path.join(path, '*.csv'))
    res_dic = {}
    all_data_frames = []
    lan_list = []
    for csv in all_csv:
        res = sum_csv(csv)
        res_dic[res[1]] = res[0]
    #looking for language code in the dict with the given order, pop out the corresponding dataframe
    for lan in sort_order:
        data = res_dic.pop(lan,None)
        if data is not None:
            lan_list.append(lan)
            all_data_frames.append(data)

    #then if there's still some language not in the order list, get their dataframe too
    if res_dic:
        for lan in res_dic.keys():
            lan_list.append(lan)
            all_data_frames.append(res_dic[lan])


    data_frame_concat = pd.concat(all_data_frames, axis=1)  # axis = 0, data will concat vertically; axis = 1,data will concat horizontally.
    # data_frame_concat.to_csv('server_csvfile.csv', index=False, header=None)
    #write the result to excel file
    data_frame_concat.to_excel(os.path.join(path, 'sum_new.xlsx'), header=lan_list)




p = input("Type in the folder containing the csv files:\n")
sum_CSVs_in_folder(p)
