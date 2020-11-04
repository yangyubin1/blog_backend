# -*- coding: utf-8 -*-
__author__ = 'yubin.yang'
__date__ = '2020/9/27 11:05'
import json
if __name__ == '__main__':
    a =[{'label': '小萌新', 'username': '342785426', 'avatar': 'boy.png', 'ChildsSon': [], 'time':'', 'content': '123', 'comment_id': 10}]
    print(json.loads(a))
