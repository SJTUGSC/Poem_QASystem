from question_classifier import *
from answer_get import *
import tkinter as tk
import textwrap

'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()

    def chat_main(self, sent):
        answer = '不好意思，这个问题我并不了解，或许你可以在网上搜索到它的答案！'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        results = self.parser.parser_main(res_classify)
        if not results:
            return answer
        else:
            return '\n'.join(results)

if __name__ == '__main__':
    handler = ChatBotGraph()

    while 1:
        question = input('用户:')
        answer = handler.chat_main(question)
        print('助理:', answer)

    # # 创建GUI窗口
    # window = tk.Tk()
    # window.title("问答系统")

    # # 创建标签和文本框
    # label = tk.Label(window, text="请输入您的问题:")
    # label.pack()
    # text_box = tk.Entry(window, width=50)
    # text_box.pack()
    # # 创建会话历史记录列表
    # history_list = tk.Listbox(window, height=5, width=50)
    # history_list.pack()
    # def answer_question():
    #     question = text_box.get()
    #     answer = handler.chat_main(question)
    #     # 显示答案
    #     wrapped_text = textwrap.wrap(answer, width=50)  # 使用textwrap模块自动换行
    #     answer = "\n".join(wrapped_text)
    #     answer_text.delete("1.0", tk.END) # 清空答案文本框
    #     answer_text.insert(tk.END,"回答:{}".format(answer)) # 将自动换行后的文本转换为字符串


    #     # 将问题和答案添加到会话历史记录中
    #     history_list.insert(tk.END, "问: " + question)
    #     history_list.insert(tk.END, "答: " + answer)

    # # 创建按钮
    # button = tk.Button(window, text="提问", command=answer_question)
    # button.pack()

    # # 创建答案文本框
    # answer_text = tk.Text(window, height=5, wrap=tk.WORD)
    # answer_text.pack()

    # # 运行GUI窗口
    # window.mainloop()