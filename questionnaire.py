import pandas as pd
import xlwt
def get_excel():
    df=pd.read_excel("questionnaire.xlsx")
    #输出测试
    # print(df)
    #输出列名
    """
    ['name' 'college' 'major' 'tel' 'sex' 'grade' 'subject3' 'subject4'
    'subject5' 'subject6' 'subject7']
    """
    # print(df.columns.values)
    #输出具体行列测试
    # print(df.loc[0].values)
    #输出几行几列测试 0:0,0:0
    print(df.loc[[0,2],:])
    return None

if __name__ == '__main__':
    get_excel()
