# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 09:10:46 2022

@author: dell
"""

import time
import math
import numpy as np
import prettytable as pt

# # test
# start_state = np.array([[2,8,3],
#                         [0,1,4],
#                         [7,6,5]])

# # 0
# start_state = np.array([[2,8,3],
#                         [1,6,4],
#                         [7,0,5]])
#1
# start_state = np.array([[1,0,2],
#                         [8,4,3],
#                         [7,6,5]])
#2
# start_state = np.array([[2,8,3],
#                         [1,6,4],
#                         [7,5,0]])
# # # 3
# start_state = np.array([[2,0,8],
#                         [1,6,3],
#                         [7,5,4]])
# #4
# start_state = np.array([[2,6,8],
#                         [7,1,3],
#                         [0,5,4]])

# # 5
# start_state = np.array([[8,3,2],
#                       [0,7,4],
#                       [6,1,5]])

# #6
# start_state = np.array([[7,1,0],
#                       [8,6,2],
#                       [4,5,3]])
# #7
# start_state = np.array([[5,8,1],
#                       [2,6,0],
#                       [7,4,3]])
# #8
start_state = np.array([[0,5,8],
                      [4,3,2],
                      [7,6,1]])

end_state = np.array([[1,2,3],
                      [8,0,4],
                      [7,6,5]])
#随机生成八数码
def random_create():
    start_state = np.array(range(9))
    np.random.shuffle(start_state)
    start_state = start_state.reshape(3,3)
    #print(f'初始状态：{start_state}')

    return start_state

#判断是否有解
def judge_solu(state):
    tot = 0
    state_l = state.flatten()
    for i in range(9):
        for j in range(i):
            if state_l[j]>state_l[i]: tot+=1
    if tot%2 == 0:
        print('have a solution')
        return 1
    else:
        print('no solution')
        return 0

#2.定义操作（空格上移，下移，左移，右移）
def find_zero(state): #找到空格位置
    temp_x, temp_y = np.where(state==0)
    return temp_x[0], temp_y[0]

def swap(ostate, direction): #执行移动操作
    x, y = find_zero(ostate)
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
#
# #3.定义启发式函数 --f(n)=d(n)+w(n)
# #定义w(n)为曼哈顿距离(以及欧几里得距离、切比雪夫距离)展开，便于计算逆序数
def get_array(state):
    alist=[]
    alist.append(state[1][1])
    alist.append(state[0][0])
    alist.append(state[0][1])
    alist.append(state[0][2])
    alist.append(state[1][2])
    alist.append(state[2][2])
    alist.append(state[2][1])
    alist.append(state[2][0])
    alist.append(state[1][0])
    return alist
#不在位数码数
def cal_site(state):
    start=get_array(state)
    count=0
    for i in range(len(start)):
        if start[i]!=i:
            count+=1
    return count

#逆序数
def cal_inverse(state):
    start = get_array(state)
    count = 0
    for i in range(len(start)):
        for j in range(i):
            if start[j]==0 or start[i]==0:
                continue
            elif start[j]>start[i]:
                count+=1
    return count


def cal_w(state,n=1):
    I=cal_inverse(state) #逆序数
    S=cal_site(state)  #不在位
    m_dist=S+I*n
    return m_dist



#在open表种添加子节点    
def refresh_open(cnode):
    flag = 0 #标记open表中是否有该子节点
    for o in open_l:
        old_f_loss = o[0] 
        thisnode = o[1]
        if (cnode.state==thisnode.state).all(): #如果子节点在open表中则比较f，更新
            flag = 1
            old_f_loss = thisnode.f_loss
            new_f_loss = cnode.f_loss
            if old_f_loss<=cnode.f_loss:
                break
            else:
                thispos = open_l.index(o)
                open_l[thispos][0] = new_f_loss 
                open_l[thispos][1] = cnode
                open_l.sort(key=lambda x:x[0]) #重新排序
                break
    #如果不在open表
    if flag==0:
        open_l.append([cnode.f_loss,cnode])
        open_l.sort(key=lambda x:x[0])

#创建Node类
#具有4个属性：state, d(n), parent, f(n)
class Node:
    f_loss = 0
    deep = 0
    parent = None
    
    def __init__(self, state, deep, parent):
        self.state = state
        self.deep = deep
        self.parent = parent
        self.f_loss = deep+cal_w(state)
        
#4.A*算法
def a_distance():
    open_l.append([0, start_node])#把初始节点放进open表
    
    cnt = 0 #计算总共扩展的节点数
    while len(open_l)!=0:
        node = open_l.pop(0)[1] #①取出队头
        if (node.state == end_state).all(): #当前节点为目标状态
            return node, cnt
        closed_l.append(node)#②放入closed表
        for action in ['left','right','up','down']:
            child_node = Node(swap(node.state, action), node.deep+1, node)#③创建子节点
            if child_node not in closed_l: #如果在close表，就跳过
                refresh_open(child_node) #如果不在，（检查后）加入open表
        cnt += 1

#5.结果输出
def output_result(node): #依次获取目标节点的父节点，形成求解路径
    path = [node]
    for i in range(node.deep):
        father_node = node.parent
        path.append(father_node)
        node = father_node
    return list(reversed(path))

if __name__=='__main__':
    #1.定义初始状态、open表、closed表
    open_l = []
    closed_l = []
    start_node = Node(start_state, 0, None)
    
    #最终状态
    t0 = time.time()
    result_node, cnt = a_distance() 
    t1 = time.time()
    
    #求解路径
    answer_path = output_result(result_node) 
    
    #打印结果
    tb = pt.PrettyTable()
    tb.field_names = ['step','state','f_loss']
    for node in answer_path:
        tb.add_row([node.deep, node.state, node.f_loss])
        if node != answer_path[-1]:
            tb.add_row(['---','--------','---'])
    print(tb)
    print(f'扩展的节点数：{cnt}')
    print('用时：%.10fs'%(t1-t0))
    print(f'到达目标状态的路径长度：{len(answer_path)-1}')
    
