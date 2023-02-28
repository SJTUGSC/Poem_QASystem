import requests
from lxml import etree
urls=['https://www.xungushici.com/shici/%d'%p for p in range(1,20001)]#用列表生成表达式批量产生链接

ls1=[]
k = 0
p = 0
for count in range(0,20000):
    try:
        get = requests.get(urls[count]).text # get(url) 得到我们的网页, text将源网页转化为字符串
        selector = etree.HTML(get) # 将源码转换为xpath可以识别的TML格式
        Xpath={'标题':'/html/body/div/div/div[1]/div[1]/div/h3',
              '朝代':'/html/body/div/div/div[1]/div[1]/div/p/a[1]',
              '作者':'/html/body/div/div/div[1]/div[1]/div/p/a[2]',
              '正文':'/html/body/div/div/div[1]/div[1]/div/div[1]',#需要合并
              '译文':'/html/body/div/div/div[1]/div[2]/div[2]/p[2]',#需要合并
              '注释':'/html/body/div/div/div[1]/div[2]/div[2]/p[4]',
              '赏析':'/html/body/div/div/div[1]/div[3]/div[2]/p[%d]',
              '创作背景':'/html/body/div/div/div[1]/div[4]/div[2]/p',
              '关于诗人':'/html/body/div/div/div[2]/div[2]/div[2]/p'}
        Xpath_keys=['标题', '朝代', '作者', '正文','译文', '注释', '赏析', '创作背景','关于诗人']
        content={}
        content['pome_id']=count+1#将页面链接最后的数字保存
        for i in range(9):
            if i in [3,4,5]:
                ls=[]
                ls=selector.xpath('/'+Xpath[Xpath_keys[i]]+'/text()')
                if i==3:
                    content[Xpath_keys[i]] = '\n'.join(ls)
                else:
                    content[Xpath_keys[i]] = ''.join(ls)
            elif i==6:
                ls=[]
                for j in range(1,17):
                    path='/html/body/div/div/div[1]/div[3]/div[2]/p[%d]'%j
                    ls+=selector.xpath('/'+path+'/text()')
                content[Xpath_keys[i]] = ''.join(ls)
            else:
                content[Xpath_keys[i]] = selector.xpath('/'+Xpath[Xpath_keys[i]]+'/text()')[0]
        flag = True
        for i in range(9):
            if len(content[Xpath_keys[i]].split()) == 0:
                flag = False
        if flag:
            k += 1
            ls1.append(content)
            print("下载的数量：%d  诗的编号%d"%(k,content['pome_id']))
    except:
        p+= 1
        print("pass:%d"%p)
        pass


import xlwt
import pandas as pd
def export_excel(export):
   #将字典列表转换为DataFrame
    pf = pd.DataFrame(list(export))
   #指定字段顺序
    order = ['pome_id','标题', '朝代', '作者', '正文','译文', '注释', '赏析', '创作背景','关于诗人']
    pf = pf[order]
    columns_map = {
        'pome_id':'pome_id',
      '标题':'标题',
      '朝代':'朝代',
      '作者':'作者',
      '正文':'正文',
      '译文':'译文',
        '注释':'注释',
        '赏析':'赏析',
        '创作背景':'创作背景',
        '关于诗人':'关于诗人'
    }
    pf.rename(columns =columns_map ,inplace = True)
   #指定生成的Excel表格名.称
    file_path = pd.ExcelWriter('name7.xlsx')
   #替换空单元格
    pf.fillna(' ',inplace = True)
   #输出
    pf.to_excel(file_path,encoding = 'utf-8',index = False)
   #保存表格
    file_path.save()
if __name__ == '__main__':
    #将分析完成的列表导出为excel表格
    export_excel(ls1)










