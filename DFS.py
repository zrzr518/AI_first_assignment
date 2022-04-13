'''
DFS 
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
    #f_loss = 0
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

def DFS(start_node,end_state,max_deep):

    open=[start_node]  # stack -1端出入栈
    close=[] # visited 已经访问过的节点
    opt=['up','down','left','right'] # 操作集合
    cnt=1 # 总共扩展的节点数量
    result_ls=[] # 返回结果

    flag=0 # flag==0说明没找到解 flag==1说明找到解了

    for _ in tqdm(generator()):
        
        #出口1.open==[] 说明没找到解  break
        if open==[]:
            flag=0
            break
        
        node=open.pop(-1) # 出栈 node为当前访问的节点

        #出口2.如果为end 则找到解了 break
        if (node.state==end_state).all()==True:
            result_ls=[node,cnt]
            flag=1
            break
        
        #3.如果不为end 达到了最大深度 此时open不为空 那么就跳过本轮来continue
        if node.deep==max_deep:
            continue
        
        # close.append(node.state) 这一句看起来似乎没有道理
        #4.如果不为end 并且没有达到最大深度
        for item in opt:
            new_state=swap(node.state,item) # 创建新状态

            #如果新建立的状态 原来的node状态不相等
            if (new_state==node.state).all()==False:
                new_node=Node(new_state,node.deep+1,node) # 存在该状态则创建新节点
                open.append(new_node) # 入栈
                cnt+=1
    
    if flag==0:
        print(f'扩展的节点数{cnt}')
        print(f'当前深度{max_deep}下没有发现路径')
        return None
    elif flag==1:
        return result_ls




if __name__=='__main__':

    start_state = np.array([[8,3,2],[0,7,4],[6,1,5]])
    end_state = np.array([[1,2,3],[8,0,4],[7,6,5]])   # end_state只有1种
    max_deep=15
    start_node=Node(start_state,0,None)     #定义起始节点

    t0=time.time()
    result_ls=DFS(start_node,end_state,max_deep)
    if result_ls is not None:
        result_node,cnt=result_ls[0],result_ls[1]
        t1=time.time()

        answer_path = output_result(result_node) # 求解路径


        #打印结果  
        tb = pt.PrettyTable()
        tb.field_names = ['step','state']
        for node in answer_path:
            tb.add_row([node.deep, node.state])
            if node != answer_path[-1]:
                tb.add_row(['---','--------'])
        print(tb)
        print(f'扩展的节点数：{cnt}')
        print('用时：%.5fs'%(t1-t0))
        print(f'到达目标状态的路径长度：{len(answer_path)-1}')




    



