'''
BFS 代码通过测试
'''

import time
import math
import numpy as np
import prettytable as pt
from tqdm import tqdm


def find_zero(state):
    '''
    找到空格的索引位置 索引从0开始
    '''
    temp_x, temp_y = np.where(state==0)
    return temp_x[0], temp_y[0]

def swap(ostate, direction):
    '''
    执行移动操作 指将0向哪里移动
    ostate: 当前状态
    direction: 移动方向
    如果无法向某个方向移动则返回原state
    '''
    x, y = find_zero(ostate) # 0所处的位置
    state = np.copy(ostate)
    if direction=='left':
        if y==0:
            return state  
        state[x][y] = state[x][y-1]
        state[x][y-1] = 0
        return state  
    if direction=='right':
        if y==2:
            return state  
        state[x][y] = state[x][y+1]
        state[x][y+1] = 0
        return state
    if direction=='up':
        if x==0:
            return state  
        state[x][y] = state[x-1][y]
        state[x-1][y] = 0
        return state
    if direction=='down':
        if x==2:
            return state  
        state[x][y] = state[x+1][y]
        state[x+1][y] = 0
        return state

def output_result(node):
    '''
    #5.结果输出
    #依次获取目标节点的父节点，形成求解路径
    '''
    path = [node]
    for i in range(node.deep):
        father_node = node.parent
        path.append(father_node)
        node = father_node
    return list(reversed(path))

class Node:
    '''
    Node表示节点
    state 当前八数码的样子
    deep DFS时进行到的深度
    parent 父状态
    '''
    deep = 0
    parent = None
    
    def __init__(self, state, deep, parent):
        self.state = state
        self.deep = deep
        self.parent = parent
        
def judge_in_nd(ls,ndary):
    '''
    判断某个ndarry变量是否在ls中
    '''
    for item in ls:
        if (ndary==item).all()==True:
            return True
    return False

def generator():
  while True:
    yield


def BFS(start_node,end_state):
    '''
    我总觉得BFS和层次遍历一模一样
    '''
    open=[start_node]
    close=[]
    opt=['up','down','left','right']
    cnt=1
    result_ls=[]

    for _ in tqdm(generator()):
        node=open.pop(0)
        #close.append(node.state)

        # 等于结果时 返回
        if (node.state==end_state).all()==True:
            result_ls=[node,cnt]
            return result_ls
        
        for item in opt:
            new_state=swap(node.state,item) # 创建新状态

            if (new_state==node.state).all()==False: # 新建立的节点不在其中
                new_node=Node(new_state,node.deep+1,node) # 存在该状态则创建新节点
                open.append(new_node) # 入栈
                cnt+=1

if __name__=='__main__':

    #start_state = np.array([[8,3,2],[0,7,4],[6,1,5]])
    start_state = np.array([[2,8,3],
                        [1,6,4],
                        [7,0,5]])
    end_state = np.array([[1,2,3],[8,0,4],[7,6,5]])   # end_state只有1种
    start_node=Node(start_state,0,None)     #定义起始节点

    t0=time.time()
    result_ls=BFS(start_node,end_state)
    result_node,cnt=result_ls[0],result_ls[1]
    t1=time.time()

    answer_path = output_result(result_node) # 求解路径

        #打印结果
    tb = pt.PrettyTable()
    tb.field_names = ['step','state','f_loss']
    for node in answer_path:
        tb.add_row([node.deep, node.state,node.f_loss])
        if node != answer_path[-1]:
            tb.add_row(['---','--------','---'])
    print(tb)
    print(f'扩展的节点数：{cnt}')
    print('用时：%.5fs'%(t1-t0))
    print(f'到达目标状态的路径长度：{len(answer_path)-1}')