import pandas as pd
import random

class QuestionPaser:
    def __init__(self) -> None:
        file_name = 'D:\\42th PRP\\name7.xlsx'
        f = open(file_name, 'rb')
        self.df = pd.read_excel(f, sheet_name='Sheet1')
        # f.close()
        
    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析与回答主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        results = []
        for question_type in question_types:
            if question_type == 'poem_writer':
                poem = entity_dict.get('poem_name')[0]
                df1 = self.df[self.df['标题'] == poem]
                ans = df1.iloc[0].iat[3]
                final_ans = '《{}》的作者是{}'.format(poem, ans)
                results.append(final_ans)
            
            elif question_type == 'poem_info':
                poems = entity_dict.get('poem_name')
                for poem in poems:
                    df1 = self.df[self.df['标题'] == poem]
                    dyn = df1.iloc[0].iat[2]
                    poet = df1.iloc[0].iat[3]
                    #需要去除汉字以外的字符
                    ans = df1.iloc[0].iat[4][14:-14].replace('\n','')
                    final_ans = '《{}》的作者是{}诗人{}，全诗内容如下：{}'.format(poem, dyn, poet, ans)
                    results.append(final_ans)
            
            elif question_type == 'poem_background':
                poem = entity_dict.get('poem_name')[0]
                df1 = self.df[self.df['标题'] == poem]
                ans = df1.iloc[0].iat[8]
                final_ans = '《{}》的创作背景是这样的:{}'.format(poem, ans)
                results.append(final_ans)

            elif question_type == 'poem_shangxi':
                poem = entity_dict.get('poem_name')[0]
                df1 = self.df[self.df['标题'] == poem]
                final_ans = df1.iloc[0].iat[7]
                results.append(final_ans)

            elif question_type == 'poem_translate':
                poem = entity_dict.get('poem_name')[0]
                df1 = self.df[self.df['标题'] == poem]
                trans = df1.iloc[0].iat[5]
                zhushi = df1.iloc[0].iat[6]
                final_ans1 = '《{}》的译文如下：{}'.format(poem, trans)
                final_ans2 = '如果你想知道更加详细的解释，以下注释也许可以帮助到你:{}'.format(zhushi)
                results.append(final_ans1)
                results.append(final_ans2)
            
            elif question_type == 'writer_dynasty':
                writers = entity_dict.get('writer')
                for writer in writers:
                    df1 = self.df[self.df['作者'] == writer]
                    ans = df1.iloc[0].iat[2]
                    final_ans = '{}是{}的诗人'.format(writer, ans)
                    results.append(final_ans)

            
            elif question_type == 'dynasty_find_writer':
                dynasty = entity_dict.get('dynasty')[0]
                df1 = self.df[self.df['朝代'] == dynasty]
                count = df1.shape[0]
                writer_list = []
                for i in range(5):
                    id=random.randint(0,count)
                    writer_list.append(df1.iloc[id].iat[3])
                writer_list = list(set(writer_list))
                final_ans = '{}的诗人有{}等等。'.format(dynasty, ','.join(writer_list))
                results.append(final_ans)
            
            elif question_type == 'writer_work':
                writers = entity_dict.get('writer')
                for writer in writers:
                    df1 = self.df[self.df['作者'] == writer]
                    count = df1.shape[0] 
                    num = count if count<=5 else 5
                    poem_list = []
                    for i in range(num):
                        name = '《{}》'.format(df1.iloc[i].iat[1])
                        poem_list.append(name)
                    final_ans = '{}的作品有{}等等。'.format(writer,'，'.join(poem_list))
                    results.append(final_ans)
            
            elif question_type == 'writer_info':
                writers = entity_dict.get('writer')
                for writer in writers:
                    df1 = self.df[self.df['作者'] == writer]
                    ans = df1.iloc[0].iat[9]
                    final_ans = '{}的个人简介如下：{}'.format(writer,ans)
                    results.append(final_ans)

        return results

if __name__ == '__main__':
    file_name = 'D:\\42th PRP\\name7.xlsx'
    handler = QuestionPaser()
    a=handler.parser_main({'args': {'唐代': ['dynasty'],'李白': ['writer']}, 'question_types': ['dynasty_find_writer']})
    for i in a:
        print(i)