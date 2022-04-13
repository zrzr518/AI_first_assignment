# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 09:52:03 2022

@author: dell
"""

import copy
import time
import heapq
import numpy as np
import prettytable as pt


end_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
node_num  = 0
start_state = [[1, 3, 10, 4],[5, 2, 6, 8], [14, 11, 12, 0],[7, 13, 9, 15]]

dx = [0, -1, 0, 1]
dy = [1, 0, -1, 0]

OPEN = []
CLOSED = set() 
path = []

def print_path(node):
    if node.parent != None:
        print_path(node.parent)
    path.append(node)
    return path

# 状态结点
class Node(object):
    def __init__(self, gn=0, hn=0, state=None, hash_value=None, parent=None):
       self.gn = gn
       self.hn = hn
       self.fn = self.gn + self.hn
       self.state = state
       self.hash_value = hash_value
       self.parent = parent

    def __lt__(self, node): # heapq的比较函数
        if self.fn == node.fn:
            return self.gn > node.gn
        return self.fn < node.fn

#A*_曼哈顿距离
def manhattan(state):
    M = 0
    for i in range(4):
        for j in range(4):
            if state[i][j] == end_state[i][j] or state[i][j] == 0:
                continue
            else:
                x = (state[i][j] - 1) // 4   
                y = state[i][j] - 4 * x -1 
                M += (abs(x - i) + abs(y - j))
    return M

#A*_“不在位”
def misplaced(state):
    sum = 0
    for i in range(4):
        for j in range(4):
            if state[i][j] == 0:
                continue
            if state[i][j] != end_state[i][j]:
                sum += 1
    return sum


def A_star(start, Fx):
    root = Node(0, 0, start, hash(str(start)), None) 
    OPEN.append(root)
    heapq.heapify(OPEN)
    CLOSED.add(root.hash_value)
    while len(OPEN) != 0:
        top = heapq.heappop(OPEN)
        global node_num 
        node_num += 1
        if top.state == end_state:
            return print_path(top)
        for i in range(4):
            for j in range(4):
                if top.state[i][j] != 0:
                    continue
                for d in range(4):
                    new_x = i + dx[d]
                    new_y = j + dy[d]
                    if 0 <= new_x <= 3 and 0 <= new_y <= 3:
                        state = copy.deepcopy(top.state)
                        state[i][j], state[new_x][new_y] = state[new_x][new_y], state[i][j]
                        h = hash(str(state))
                        if h in CLOSED:
                            continue
                        CLOSED.add(h)
                        child = Node(top.gn+1, Fx(state), state, h ,top)
                        heapq.heappush(OPEN, child)


if __name__ == '__main__':
    t0 = time.time()
    PATH = np.asarray(A_star(start_state, misplaced))
    t1 = time.time()

    start_state = np.asarray(start_state)
    '''
    for i, p in enumerate(PATH):  #路径打印
        if i == 0:
            print("15-Puzzle initial state:")
            print(p)
        else:
            print('Move: %d' %(i))
            print(p)

    print('Total Step %d' %(len(path)-1))
    print("Used Time %f" %(t2-t1), "sec")
    print("Expanded %d nodes" %(node_num))'''
    tb = pt.PrettyTable()
    tb.field_names = ['step','state','f_loss']
    for node in PATH:
        tb.add_row([node.gn, node.state, node.fn])
        if node != PATH[-1]:
            tb.add_row(['---','--------','---'])
    print(tb)
    print(f'扩展的节点数：{node_num}')
    print('用时：%.5f ms'%((t1 - t0)*1000))
    print(f'到达目标状态的路径长度：{len(path)-1}')
    