import sys
import os
# 将项目根目录添加到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest


from llmada import BianXieAdapter

from promptlibz import Templates, TemplateType

def test_Functionality():
    prompt = Templates(TemplateType.JUDGETYPE)
    assert type(prompt.format(task = '任务')) == str


class Test_Performance():

    def test_judgetype(self):
        # TODO
        prompt = Templates(TemplateType.JUDGETYPE)


    def test_es(self):
        prompt = Templates(TemplateType.ESTIMATE_DURATION)  
        bx = BianXieAdapter()

        print(bx.product(prompt.format(task = "打扫房间")))

