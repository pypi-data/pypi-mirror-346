import sys
import os
# 将项目根目录添加到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest


from querypipz import Queryr

# @pytest.mark.skip('等待')
def test_run():
    qur = Queryr(persist_dir='/Users/zhaoxuefeng/GitHub/test1/obsidian_kb/my_obsidian_notes')

    qur.query('hello')
    qur.retrieve('vv')

from querypipz import KnowledgeBaseManager

@pytest.mark.skip('等待')
def test_build():

    ### 加载成功
    manager = KnowledgeBaseManager(base_persist_dir='/Users/zhaoxuefeng/GitHub/test1/obsidian_kb')

    ### 注册
    manager.build_or_update_kb("my_obsidian_notes", ["/Users/zhaoxuefeng/GitHub/obsidian/工作/日记"])

@pytest.mark.skip('等待')
def test_build_list():
    manager = KnowledgeBaseManager(base_persist_dir='/Users/zhaoxuefeng/GitHub/test1/obsidian_kb')
    manager.list_kbs()

@pytest.mark.skip('等待')
def test_build_index():

    ### 获取知识库index
    manager = KnowledgeBaseManager(base_persist_dir='/Users/zhaoxuefeng/GitHub/test1/obsidian_kb')
    obsidian_index = manager.get_kb_index("my_obsidian_notes")

    if obsidian_index:
        query_engine = obsidian_index.as_query_engine()
        response = query_engine.query("What is the main topic of my notes?")
        print(response)


    def show(xx):
        return xx.response +"\n\n"+ xx.get_formatted_sources()

    show(xx)

