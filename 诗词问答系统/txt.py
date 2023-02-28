import pandas as pd


def excel_to_list(col):  #col指定所用为第几列数据
    df = pd.read_excel(r'D:\\42th PRP\\name7.xlsx',usecols=[col],names=None)
    df_li = df.values.tolist()
    result = []
    for s_li in df_li:
        result.append(s_li[0])
    result=list(set(result))  
    return result    
    

if __name__ == '__main__':

    #获取包含诗词题目的列表
    name_list = excel_to_list(1)   
    f = open("D:\\42th PRP\诗词问答系统\\name.txt","w",encoding='utf-8')
    for i in name_list:
        f.write(i+'\n')
    f.close()

    #获取包含朝代的列表
    dynasty_list = excel_to_list(2)  
    f = open("D:\\42th PRP\诗词问答系统\dynasty.txt","w",encoding='utf-8')
    for i in dynasty_list:
        f.write(i+'\n')
    f.close()

    #获取包含诗人的列表
    writer_list = excel_to_list(3)
    f = open("D:\\42th PRP\诗词问答系统\writer.txt","w",encoding='utf-8')
    for i in writer_list:
        f.write(i+'\n')
    f.close()

