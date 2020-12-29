import pandas as pd
import numpy as np

ARF = [-23,16,45,5,3,4,1,2]
RAT = [0,0,0,0,0,0,0,0]
Cycle = 1
add_cycle = 1
sub_cycle = 1
mul_cucle = 10
div_cycle = 40

def RS(cols):
    a = []
    for i in range(cols):
        b = []
        b.append('RS'+str(i+1))
        a.append(b)
    return a

def RSisEmpty(rs):
    if rs[1:] == []:
        return True
    else:
        return False

def RSupdate(r,inst,i):
    r.extend(list(inst.iloc[i,0:2]))  #  填入OP,DstTag
    for t in range(2,4):  #  填入Tag1 or Val1, Tag2 or Val2
        if RAT[GetRegNum(inst.iloc[i,t])-1] == 0:
            r.append(ARF[GetRegNum(inst.iloc[i,t])-1])
        else:
            r.append(RAT[GetRegNum(inst.iloc[i,t])-1])
    # print(r)
    RAT[GetRegNum(r[2])-1] = r[0]  # 把(RS+編號)放到RAT


def issue(inst, i):
    if inst[0][i] == 'DIV' or inst[0][i] == 'MUL':
        for r in rs[3:]:  #  div和mul用rs4,rs5
            if RSisEmpty(r):
                RSupdate(r,inst,i)
                '''這邊要寫入status table => 填入cycle'''
                i += 1
                break
    elif inst[0][i] == 'ADD' or inst[0][i] == 'SUB':
        for r in rs[0:3]:  #  add和sub用rs1,rs2,rs3
            if RSisEmpty(r):
                RSupdate(r,inst,i)
                i += 1
                break
    return i

# def ALU(a):
#     if a[1] == 'ADD':


def GetRegNum(r):
    if r[0] == 'R':
        index = int(r[1:])
        return index

if __name__ == '__main__':
    inst_table = pd.read_table('input.txt',header=None,sep=",")
    print(inst_table)
    rs = RS(5)
    # alu1 = ['RS1', 'ADD', 'R3', 1, 2]  #  運算add,sub
    # alu2 = []  #  運算mul,div
    issue_pointer = 0
    while Cycle < 10:
        print('------------')
        print('Cycle: ', Cycle)
        print('------------')
        # if len(alu1) != 0:
        #     ALU(alu1)
        issue_pointer = issue(inst_table, issue_pointer)

        Cycle += 1
        print(ARF)
        print(RAT)
        print(rs)
        print(issue_pointer)



