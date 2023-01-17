import os.path
import os
import glob
import pandas as pd


def sum_csv(path):
    df = pd.read_csv(path, encoding="utf-8", sep=';',header=1,usecols=[4,8,12,16,20,24,28,32],names=["Context Match","Repetitions","100%","95% - 99%","85% - 94%","75% - 84%","50% - 74%","No Match"])
    # row_num = len(df.index)
    # col_num = len(df.columns)
    # x = df.loc[0:1]
    # x = df.loc[0:1]
    # x = df.loc[0:0]
    # print(x)
    # head = df.head()
    # print(head)
    # shape = df.shape
    # print(shape)
    filename = os.path.basename(path)
    lan_code = filename[:3]
    df2 = df.iloc[:,:].sum()
    df3 = df2.transpose()

    df3.columns = ["", lan_code]
    return [df3,lan_code]





def sum_CSVs_in_folder(path):
    all_csv = glob.glob(os.path.join(path, '*.csv'))
    all_data_frames = []
    lan_list = []
    for csv in all_csv:
        res = sum_csv(csv)
        all_data_frames.append(res[0])
        lan_list.append(res[1])
    data_frame_concat = pd.concat(all_data_frames, axis=1)  # axis = 0 表示数据垂直合并,等于1表示并排合并.
    # data_frame_concat.to_csv('server_csvfile.csv', index=False, header=None)
    data_frame_concat.to_excel(os.path.join(path, 'sum.xlsx'), header=lan_list)


# df3.to_excel(r'C:\Users\AnZhou\Downloads\word_count_stats\Task 1\test.xlsx')

p = input("Type in the folder containing the csv files:\n")
sum_CSVs_in_folder(p)