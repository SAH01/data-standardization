import pandas as pd

def get_subject():
    df = pd.read_excel("std_subject_2009.xlsx")
    print(df.values[0])
    return None

if __name__ == '__main__':
    get_subject()