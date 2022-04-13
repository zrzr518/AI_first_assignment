from re import M
import time
import math
import numpy as np
import prettytable as pt

start_state = np.array([[2,8,3],
                        [1,6,4],
                        [7,0,5]])
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
    
#3.定义启发式函数 --f(n)=d(n)+w(n)
#定义w(n)为当前状态逆序数
def cal_w(state):
    m_dist = 0
    alist = []
    alist.append(state[1][1])
    alist.append(state[0][0])
    alist.append(state[0][1])
    alist.append(state[0][2])
    alist.append(state[1][2])
    alist.append(state[2][2])
    alist.append(state[2][1])
    alist.append(state[2][0])
    alist.append(state[1][0])
    for i in range(9):
        for j in range(i,9):
            if alist[i]==0 or alist[j]==0:
                continue
            else:
                if alist[i]>alist[j]:
                    m_dist+=1
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
    print('用时：%.5fs'%(t1-t0))
    print(f'到达目标状态的路径长度：{len(answer_path)-1}')