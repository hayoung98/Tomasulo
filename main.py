import pandas as pd
import numpy as np

ARF = [-23,16,45,5,3,4,1,2]
RAT = [0,0,0,0,0,0,0,0]
Cycle = 1
add_cycle = 1
sub_cycle = 1
mul_cucle = 10
div_cycle = 40
ALU_empty_check = [True, True]
alu_done_cycle = 0

def StateTable(l):
    ST = []
    for i in range(l):
        ST.append([])
    return ST

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

def GetRegNum(r):  #  回傳指定RS的編號
    if r[0] == 'R':
        index = int(r[1:])
        return index

def RSupdate(r,inst,i):
    r.append(i)  #  填入inst. id
    r.extend(list(inst.iloc[i,0:2]))  #  填入OP,DstTag
    for t in range(2,4):  #  填入Tag1 or Val1, Tag2 or Val2
        if RAT[GetRegNum(inst.iloc[i,t])-1] == 0:
            r.append(ARF[GetRegNum(inst.iloc[i,t])-1])
        else:
            r.append(RAT[GetRegNum(inst.iloc[i,t])-1])
    # print(r)
    RAT[GetRegNum(r[3])-1] = r[0]  # 把(RS+編號)放到RAT


def issue(inst, i, ST, Cycle):
    if i < 6 :
        if inst[0][i] == 'DIV' or inst[0][i] == 'MUL':
            for r in rs[3:]:  #  div和mul用rs4,rs5
                if RSisEmpty(r):
                    RSupdate(r,inst,i)

                    '''這邊要寫入status table => 填入cycle'''
                    ST[i].append(Cycle)

                    i+=1
                    break
        elif inst[0][i] == 'ADD' or inst[0][i] == 'SUB':
            for r in rs[0:3]:  #  add和sub用rs1,rs2,rs3
                if RSisEmpty(r):
                    RSupdate(r,inst,i)

                    '''這邊要寫入status table => 填入cycle'''
                    ST[i].append(Cycle)

                    i+=1
                    break
    return i

def ALU(r, ip, ST, Cycle):
    if is_int(r[4]) and is_int(r[5]):
        if inst_table[0][ip] == 'DIV' or inst_table[0][ip] == 'MUL':
            if ALU_empty_check[1] == True:
                print("instruction",ip+1,". is in ALU!")
                ST[ip].append(Cycle)
                ALU_empty_check[1] = False            
        elif inst_table[0][ip] == 'ADD' or inst_table[0][ip] == 'SUB':
            if ALU_empty_check[0] == True:
                print("instruction",ip+1,". is in ALU!")
                ST[ip].append(Cycle)  
                ALU_empty_check[0] = False 

def writeback_time(op, ip):    
    if op == 'DIV':        
        t = ST[ip][1] + div_cycle
    elif op == 'MUL':
        t = ST[ip][1] + mul_cucle
    elif op == 'ADD':
        t = ST[ip][1] + add_cycle
    elif op == 'SUB':
        t = ST[ip][1] + sub_cycle
    return t
    
def is_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

def compute(r):
    if r[2] == 'DIV' or r[2] == 'MUL':
        ALU_empty_check[1] = True
        if r[2] == 'DIV':
            return (r[4]/r[5])
        elif r[2] == 'MUL':
            return (r[4]*r[5])
    elif r[2] == 'ADD' or r[2] == 'SUB':
        ALU_empty_check[0] = True
        if r[2] == 'ADD':
            return (r[4]+r[5])
        elif r[2] == 'SUB':
            return (r[4]-r[5])


def Write_Back(r, ip, ST, Cycle):
    if is_int(r[4]) and is_int(r[5]):  #  如果都有確切的值，即可運算
        answer = compute(r)
        # print("answer: ",answer)
        ST[ip].append(Cycle)
        # print("now r: ",r)

        '''
        -----寫回RS裡的tag-----
        '''
        for write_r in rs:  
            try:
                if write_r[4] == r[0]:  #  r[0]為RS的tag編號 ex.RS3
                    write_r[4] = answer
                elif write_r[5] == r[0]:
                    write_r[5] = answer
            except IndexError:
                pass

        '''
        -----寫回RAT，之後馬上更新ARF-----
        '''
        for rat_i in range(len(RAT)):
            if RAT[rat_i] == r[0]:
                RAT[rat_i] = 0
                ARF[rat_i] = answer

        '''
        -----釋出RS空間、ALU空間-----
        '''
        for clean in rs:
            if clean == r:
                for i in range(5):
                    clean.pop()
        



if __name__ == '__main__':
    inst_table = pd.read_table('input.txt',header=None,sep=",")
    print(inst_table)
    ST = StateTable(len(inst_table))
    rs = RS(5)
    # alu1 = ['RS1', 'ADD', 'R3', 1, 2]  #  運算add,sub
    # alu2 = []  #  運算mul,div
    issue_pointer = 0
    while Cycle > 0:
        print('--------------------')
        print('Cycle: ', Cycle)
        print()
        # if len(alu1) != 0:
        #     ALU(alu1)
        issue_pointer = issue_pointer2 = issue(inst_table, issue_pointer, ST, Cycle)
        for ip in range(issue_pointer):
            if Cycle > ST[ip][0] and len(ST[ip])<2:   #  後者判斷此inst有沒有進E_state了  
                for r in rs:                    
                    try:  #  判斷RS裡有沒有東西
                        if r[1] == ip:
                            ALU(r, ip, ST, Cycle)
                    except IndexError:
                        pass         
                
                # print("ALU_empty_check: ", ALU_empty_check)
            if len(ST[ip])==2:
                alu_done_cycle = writeback_time(inst_table[0][ip], ip)
            if Cycle == alu_done_cycle:
                for r in rs:
                    try:  #  判斷RS裡有沒有東西
                        if r[1] == ip:
                            Write_Back(r, ip, ST, Cycle)                            
                            issue_pointer2 = issue(inst_table, issue_pointer, ST, Cycle)
                    except IndexError:
                        pass
        Cycle += 1
        issue_pointer = issue_pointer2
        done_check = False
        print("ARF: ",ARF)
        print("RAT: ",RAT)
        print("RS: ",rs)
        print("issue pointer: ",issue_pointer)

        print("State Table: ")
        print('{:>7}'.format('I'), end = '')
        print('{:>5}'.format('E'), end = '')
        print('{:>5}'.format('W'))
        c = 0
        for st_i in range(len(ST)):
            try:
                print('{:>2}'.format(st_i+1), end = '')
                print('{:>5}'.format(ST[st_i][0]), end = '')
                print('{:>5}'.format(ST[st_i][1]), end = '')                
            except IndexError:
                print('{:>5}'.format(''), end = '')
    
            try:
                print('{:>5}'.format(ST[st_i][2]))
            except IndexError:
                print('{:>5}'.format(''))     

            '''
            -----確認有沒有完成-----
            '''       
            if len(ST[st_i]) == 3:
                c += 1
            if c == len(ST):
                done_check = True

        print('')
        print('已完成: ',c)
        print('共: ',len(ST))
        if done_check == True:
            break
        
        
        

