import pandas as pd
data_diem = pd.read_csv("data_diem.csv")

def sap_xep_tang_dan(data):
    data_tang_dan = data.sort_values(by=['TB'])
    return data_tang_dan
