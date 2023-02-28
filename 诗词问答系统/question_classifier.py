import ahocorasick

class QuestionClassifier:
    def __init__(self):
        #　特征词路径
        self.dynasty_path = 'D:\\42th PRP\诗词问答系统\dynasty.txt'
        self.poemname_path = 'D:\\42th PRP\诗词问答系统\\name.txt'
        self.writer_path = 'D:\\42th PRP\诗词问答系统\writer.txt'
        
        # 加载特征词
        self.dynasty_wds= [i.strip() for i in open(self.dynasty_path,encoding='utf-8') if i.strip()]
        self.poem_name_wds= [i.strip() for i in open(self.poemname_path,encoding='utf-8') if i.strip()]
        self.writer_wds= [i.strip() for i in open(self.writer_path,encoding='utf-8') if i.strip()]
        self.region_words = set(self.dynasty_wds + self.poem_name_wds + self.writer_wds)

        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典(所有词对应的类型)
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.writer_qwds = ['作者', '诗人', '是谁写的', '作者是谁', '写']
        self.background_qwds = ['创作背景', '背景', '背后', '故事']
        self.shangxi_qwds = ['赏析', '鉴赏', '表达', '欣赏', '抒发', '描绘']
        self.translate_qwds = ['解释','意思', '白话', '现代汉语', '什么意思', '译文', '写了什么']
        self.dynasty_qwds = ['朝代', '时代', '时期', '时间', '代']
        self.zuopin_qwds = ['作品', '创作', '写', '代表作']
        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        poem_dict = self.check_poem(question)
        if not poem_dict:
            return {}
        data['args'] = poem_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in poem_dict.values():
            types += type_
        question_type = 'others'
       
        question_types = []

        #查询诗词作者
        if self.check_words(self.writer_qwds, question) and ('poem_name' in types):
            question_type = 'poem_writer'
            question_types.append(question_type)
        
        #查询诗词创作背景
        if self.check_words(self.background_qwds, question) and ('poem_name' in types):
            question_type = 'poem_background'
            question_types.append(question_type)
        
        #查询诗词赏析
        if self.check_words(self.shangxi_qwds, question) and ('poem_name' in types):
            question_type = 'poem_shangxi'
            question_types.append(question_type)

        #查询诗词的译文
        if self.check_words(self.translate_qwds, question) and ('poem_name' in types):
            question_type = 'poem_translate'
            question_types.append(question_type)

        #查询作者朝代
        if self.check_words(self.dynasty_qwds, question) and ('writer' in types):
            question_type = 'writer_dynasty'
            question_types.append(question_type)

        #查询作者的作品
        if self.check_words(self.zuopin_qwds, question) and ('writer' in types):
            question_type = 'writer_work'
            question_types.append(question_type)
        
        #查询朝代的诗人
        if self.check_words(self.writer_qwds, question) and ('dynasty' in types):
            question_type = 'dynasty_find_writer'
            question_types.append(question_type)
        
        #查询诗词信息
        if question_types == [] and 'poem_name' in types:
            question_types = ['poem_info']

        #查询诗人的信息
        if question_types == [] and 'writer' in types:
            question_types = ['writer_info']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.dynasty_wds:
                wd_dict[wd].append('dynasty')
            if wd in self.poem_name_wds:
                wd_dict[wd].append('poem_name')
            if wd in self.writer_wds:
                wd_dict[wd].append('writer')
        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_poem(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)