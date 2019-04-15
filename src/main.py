#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# 2019.04.12
# author Agtao
#


# 导入包
import matplotlib.pyplot as plt
import math
import random
import sys
import copy
import json

import excel_manger

# 常量定义

# 种群数量
pop_size = 60
# 染色体长度
chromosome_length = 522
# 迭代次数
iter = 600 #500
# 倒位概率
pr = 0.6
# 移位概率
pm = 0.6
# 交换概率
pe = 0.01
# 每一代最优解
result = []
# a1,a2,b1,b2,b3,b4的任务数量
task_num = {}
# 小车数量
car_num = 3 #3，6，9
# 小车长度
car_length = 1.3 #1.3
# 小车速度
car_v = 1.5
# 轨道直线长度
track_line = 94
# 轨道弯道长度
track_curve = 6
# data.json文件名
filename = ""

tip = ""


# 初始化种群
def init_population(pop_size, chromosome_length):
    pop = []

    # 循环生成种群
    for i_chromosome in range(pop_size):

        num_t = []
        num_t.append(task_num["a1"])
        num_t.append(task_num["a2"])
        num_t.append(task_num["b1"])
        num_t.append(task_num["b2"])
        num_t.append(task_num["b3"])
        num_t.append(task_num["b4"])

        chromosome = []

        # 开始进行染色体生成
        for i_gene in range(chromosome_length):
            chance = 1

            while chance==1:
                chance = random.random()

            if 0<=chance and chance<(num_t[0])/sum(num_t):
                # 生成0用来+1~4边成“1，2，3，4”
                chromosome.append(0)
                num_t[0]-=1
            elif (num_t[0])/sum(num_t)<=chance and chance<(num_t[0]+num_t[1])/sum(num_t):
                # 生成4用来+1~4边成“5，6，7，8”
                chromosome.append(4)
                num_t[1] -= 1
            elif (num_t[0]+num_t[1])/sum(num_t) <= chance and chance < (num_t[0] + num_t[1] + num_t[2])/sum(num_t):
                # 生成9,10,11
                chromosome.append(9+random.randint(0,2))
                num_t[2]-=1
            elif (num_t[0] + num_t[1] + num_t[2])/sum(num_t) <= chance and chance < (num_t[0] + num_t[1] + num_t[2] + num_t[3])/sum(num_t) :
                # 生成12,13,14
                chromosome.append(12+random.randint(0,2))
                num_t[3]-=1
            elif (num_t[0] + num_t[1] + num_t[2] + num_t[3])/sum(num_t) <= chance and chance < (num_t[0] + num_t[1] + num_t[2] + num_t[3] + num_t[4])/sum(num_t):
                # 生成15,16,17
                chromosome.append(15+random.randint(0,2))
                num_t[4]-=1
            elif (num_t[0] + num_t[1] + num_t[2] + num_t[3] + num_t[4])/sum(num_t) <= chance and chance < (num_t[0] + num_t[1] + num_t[2] + num_t[3] + num_t[4] +num_t[5])/sum(num_t):
                # 生成18,19,20
                chromosome.append(18+random.randint(0,2))
                num_t[5]-=1

        # 将染色体加入种群
        pop.append(chromosome)

    # 返回生成的种群
    return pop

# 基因型转表现型
def gene_to_type(pop_gene):
    pop_type = copy.deepcopy(pop_gene)

    a2 = excel_manger.get_list_a1()
    a1 = excel_manger.get_list_a2()

    # 开始转化为表现型
    for i_chromosome in range(pop_size):

        cur_a1 = 0
        cur_a2 = 0

        for i_gene in range(chromosome_length):

            gene = pop_type[i_chromosome][i_gene]

            if gene==0:
                pop_type[i_chromosome][i_gene]=[1,a1[cur_a1]]
                cur_a1+=1
            elif gene==4:
                pop_type[i_chromosome][i_gene] = [2,a2[cur_a2]]
                cur_a2+=1
            elif gene in [9,10,11]:
                pop_type[i_chromosome][i_gene] = [3,gene-4]
            elif gene in [12,13,14]:
                pop_type[i_chromosome][i_gene] = [4,gene-7]
            elif gene in [15,16,17]:
                pop_type[i_chromosome][i_gene] = [5,gene-10]
            elif gene in [18,19,20]:
                pop_type[i_chromosome][i_gene] = [6,gene-13]

    # 返回表现型
    return pop_type

# 适应度评估函数
def satisfy(pop_type):

    pop_satisfy = []

    # 由源点序号确定源点位置
    satisfy_pos_src = [0.0,0.0,11.75,21.464,34.893,48.321,61.75]
    # 由终点序号确定终点位置
    satisfy_pos_dst = [0.0,14.75,28.179,41.607,55.036,64.75,76.5,88.25]

    # 开始计算
    for chromosome in pop_type:
        # 定义变量

        # 任务总时间
        satisfy_time = 0
        # 任务总数
        satisfy_task_num = len(chromosome)
        # 每个小车当前任务
        satisfy_tasks = chromosome[:car_num]
        # 每个小车当前位置
        satisfy_p_car = []
        # 每个小车当前任务序号
        satisfy_tasks_id = []
        # 每个小车当前是否正在工作
        satisfy_is_working = []
        # 每个小车的剩余工作时间
        satisfy_last_time = []
        # 每个小车当前是要(在)装货{0}还是卸货{1}
        satisfy_src_or_dst = []
        # 进货仓锁
        satisfy_lock_src = [False,False,False,False,False,False,False]
        # 出货仓锁
        satisfy_lock_dst = [False,False,False,False,False,False,False,False]
        for i in range(car_num):
            satisfy_is_working.append(False)
            satisfy_last_time.append(0)
            satisfy_src_or_dst.append(0)
            satisfy_tasks_id.append(0)
            satisfy_p_car.append((0-i*car_length+100)%100)

        # 开始计算
        # 剩余任务数量大于零，继续工作
        while satisfy_task_num>0:
            # 每car_num个任务为一周期
            for i in range(car_num):
                # 如果这个小车没有分配到任务，则跳过
                if satisfy_tasks[i]==[]:
                    continue
                # 如果这个小车不在工作
                if not satisfy_is_working[i]:
                    # 如果小车准备装货
                    if satisfy_src_or_dst[i]==0:
                        temp_src = satisfy_pos_src[satisfy_tasks[i][0]]
                        if temp_src<satisfy_p_car[i]:
                            temp_src = 100+temp_src

                        # 如果小车目的地和自己之间有一辆车
                        if satisfy_p_car[i]<satisfy_p_car[(i+car_num-1)%car_num] and satisfy_p_car[(i+car_num-1)%car_num] <= min(satisfy_p_car[i]+car_v,temp_src):
                            satisfy_p_car[i] = satisfy_p_car[(i+car_num-1)%car_num]-car_length
                        # 解决重合
                        elif satisfy_p_car[(i+car_num-1)%car_num]==satisfy_p_car[(i+car_num+1)%car_num]:
                            satisfy_p_car[i] = min(satisfy_p_car[i] + car_v, temp_src)
                            satisfy_p_car[i] = satisfy_p_car[i] % 100

                            if satisfy_lock_src[satisfy_tasks[i][0]] == False and satisfy_p_car[i] == satisfy_pos_src[
                                satisfy_tasks[i][0]]:
                                satisfy_is_working[i] = True
                                satisfy_last_time[i] = 10
                                satisfy_lock_src[satisfy_tasks[i][0]] = True
                        # 如果小车目的地和自己之间没有车
                        else:
                            satisfy_p_car[i] = min(satisfy_p_car[i]+car_v,temp_src)
                            satisfy_p_car[i] = satisfy_p_car[i]%100

                            if satisfy_lock_src[satisfy_tasks[i][0]] == False and satisfy_p_car[i] == satisfy_pos_src[satisfy_tasks[i][0]]:
                                satisfy_is_working[i] = True
                                satisfy_last_time[i] = 10
                                satisfy_lock_src[satisfy_tasks[i][0]]=True
                    # 如果小车准备卸货
                    else:
                        temp_dst = satisfy_pos_dst[satisfy_tasks[i][1]]
                        if temp_dst < satisfy_p_car[i]:
                            temp_dst = 100 + temp_dst
                        # 如果小车目的地和自己之间由一辆车
                        if satisfy_p_car[i] < satisfy_p_car[(i + car_num - 1) % car_num] and satisfy_p_car[(i + car_num - 1) % car_num] <= min(satisfy_p_car[i] + car_v,temp_dst):
                            satisfy_p_car[i] = satisfy_p_car[(i + car_num - 1) % car_num] - car_length
                        # 解决重合
                        elif satisfy_p_car[(i + car_num - 1) % car_num] == satisfy_p_car[(i + car_num + 1) % car_num]:
                            satisfy_p_car[i] = min(satisfy_p_car[i] + car_v, temp_dst)
                            satisfy_p_car[i] = satisfy_p_car[i] % 100

                            if satisfy_lock_dst[satisfy_tasks[i][1]] == False and satisfy_p_car[i] == satisfy_pos_dst[
                                satisfy_tasks[i][1]]:
                                satisfy_is_working[i] = True
                                satisfy_last_time[i] = 10
                                satisfy_lock_dst[satisfy_tasks[i][1]] = True
                        # 如果小车目的地和自己之间没有车
                        else:
                            satisfy_p_car[i] = min(satisfy_p_car[i] + car_v,temp_dst)
                            satisfy_p_car[i] = satisfy_p_car[i]%100

                            if satisfy_lock_dst[satisfy_tasks[i][1]]==False and satisfy_p_car[i] == satisfy_pos_dst[satisfy_tasks[i][1]]:
                                satisfy_is_working[i] = True
                                satisfy_last_time[i] = 10
                                satisfy_lock_dst[satisfy_tasks[i][1]] = True

                # 如果这个小车正在工作
                else:
                    # 剩余时间减1s
                    satisfy_last_time[i]-=1
                    # 如果工作结束
                    if satisfy_last_time[i]<=0:
                        # 剩余时间清零
                        satisfy_last_time[i]=0
                        # 结束工作状态
                        satisfy_is_working[i]=False

                        # 如果刚刚结束的是装货
                        if satisfy_src_or_dst[i]==0:
                            #解锁装货
                            satisfy_lock_src[satisfy_tasks[i][0]]=False
                            # 准备取卸货
                            satisfy_src_or_dst[i]=1
                        # 如果刚刚结束的是卸货
                        else:
                            # 解锁装货
                            satisfy_lock_dst[satisfy_tasks[i][1]] = False
                            # 重置为装货
                            satisfy_src_or_dst[i]=0
                            # 任务变更
                            satisfy_tasks_id[i]+=1
                            satisfy_id = satisfy_tasks_id[i]*car_num+i
                            if satisfy_id >= chromosome_length:
                                satisfy_tasks[i]=[]
                                satisfy_p_car[i]=-1
                            else:
                                satisfy_tasks[i]=chromosome[satisfy_id]

                            satisfy_task_num-=1

            # 时间加1s
            satisfy_time+=1

        # 将本次染色体适应度数值储存
        pop_satisfy.append(satisfy_time)

    # 返回适应度数组
    return pop_satisfy

# 选择函数
def choose(pop_gene, pop_satisfy):
    pop_next_gene = []

    # 计算其适应度比率
    sum_satisfy = sum(pop_satisfy)
    for i_compute in range(len(pop_satisfy)):
        pop_satisfy[i_compute]=pop_satisfy[i_compute]/sum_satisfy

    # 恶魔的轮盘赌
    for i_chromosome in range(int(pop_size/2)):
        gamble = random.random()
        addiction = 0
        for i_satisfy in range(len(pop_satisfy)):
            if addiction<=gamble and gamble<addiction+pop_satisfy[i_satisfy]:
                # 选中了
                pop_next_gene.append(pop_gene[i_satisfy])
                pop_next_gene.append(pop_gene[i_satisfy])
                break
            else:
                # 未选中，继续
                addiction+=pop_satisfy[i_satisfy]

    # 返回下一代种群基因型
    return pop_next_gene

# 换位算子
def opt_change(pop_gene,rate):
    for i_chromosome in range(len(pop_gene)):
        if random.random()<=rate:
            pos_a = random.randint(0,chromosome_length-1)
            pos_b = pos_a

            while pos_a==pos_b:
                pos_b = random.randint(0,chromosome_length-1)

            gene_temp = pop_gene[i_chromosome][pos_a]
            pop_gene[i_chromosome][pos_a] = pop_gene[i_chromosome][pos_b]
            pop_gene[i_chromosome][pos_b] = gene_temp

# 倒位算子
def opt_reserve(pop_gene,rate):
    for i_chromosome in range(len(pop_gene)):
        if random.random()<=rate:
            pos_a = random.randint(0,chromosome_length-1)
            pos_b = pos_a

            while pos_a==pos_b:
                pos_b = random.randint(0,chromosome_length-1)

            pos_min = min(pos_a,pos_b)
            pos_max = max(pos_a,pos_b)

            while pos_min<pos_max:
                temp_gene = pop_gene[i_chromosome][pos_min]
                pop_gene[i_chromosome][pos_min] = pop_gene[i_chromosome][pos_max]
                pop_gene[i_chromosome][pos_max] = temp_gene
                pos_min+=1
                pos_max-=1

# 移位算子
def opt_move(pop_gene,rate):
    for i_chromosome in range(len(pop_gene)):
        if random.random()<=rate:
            pos_a = random.randint(0,chromosome_length-1)
            pos_b = pos_a

            while pos_a==pos_b:
                pos_b = random.randint(0,chromosome_length-1)

            pos_min = min(pos_a, pos_b)
            pos_max = max(pos_a, pos_b)

            can_move_left = pos_min - 0
            can_move_right = chromosome_length-1-pos_max
            step = 0
            forward = True # True往左边移动，Flase往右边移动

            if can_move_left>can_move_right and can_move_left>=1:
                step = 1
                forward = True
            elif can_move_left<=can_move_right and can_move_right>=1:
                step = 1
                forward = False

            if step!=0:
                if forward:
                    for i_move in range(pos_max-pos_min+1):
                        temp_gene = pop_gene[i_chromosome][pos_min+i_move]
                        pop_gene[i_chromosome][pos_min + i_move] = pop_gene[i_chromosome][pos_min + i_move-step]
                        pop_gene[i_chromosome][pos_min + i_move - step] = temp_gene
                else:
                    for i_move in range(pos_max-pos_min+1):
                        temp_gene = pop_gene[i_chromosome][pos_max-i_move]
                        pop_gene[i_chromosome][pos_max - i_move] = pop_gene[i_chromosome][pos_max - i_move+step]
                        pop_gene[i_chromosome][pos_max - i_move + step] = temp_gene

# 记录
def store_best(pop_type,pop_satisfy):
    max_value = pop_satisfy[0]
    max_i = 0

    for i_best in range(len(pop_type)):
        if pop_satisfy[i_best]<max_value:
            max_value = pop_satisfy[i_best]
            max_i = i_best

    result.append([max_value,pop_type[max_i]])

# 整体流程
def main():
    # 生成种群基因型
    pop_gene = init_population(pop_size,chromosome_length)

    # 开始进行自然进化迭代
    for i_generation in range(iter):
        # 生成种群的表现型
        pop_type = gene_to_type(pop_gene)

        # 计算种群的适应度函数
        pop_satisfy = satisfy(pop_type)

        # 储存当代最优染色体
        store_best(pop_type,pop_satisfy)

        # 选择
        pop_next_gene = choose(pop_gene,pop_satisfy)

        # 单亲遗传-换位算子
        opt_change(pop_next_gene,pe)

        # 单亲遗传-倒位算子
        opt_reserve(pop_next_gene,pr)

        # 单亲遗传-移位算子
        opt_move(pop_next_gene,pm)

        # 保留本代最优个体
        pop_next_gene[0]=result[i_generation][1]

        # 进化
        pop_gene = pop_next_gene

        print ("【%s】完成第%d次进化"%(tip,i_generation+1))
        print ("本次最低耗时为:%d"%(result[i_generation][0]))

    # 储存result文件到json中
    with open('./'+filename, 'w') as f:
        json.dump(result, f)

def load_data():
    task_num["a1"] = 100
    task_num["a2"] = 100
    task_num["b1"] = 100
    task_num["b2"] = 51
    task_num["b3"] = 71
    task_num["b4"] = 100

load_data()

# # 生成12have的数据
# result = []
# car_num = 12
# car_length = 1.3
# filename = "data-12have.json"
# tip = "12have"
# main()
# with open("data-12have.json", 'r') as f:
#     resultss = json.load(f)
#     datass = resultss[len(resultss)-1][1]
#     excel_manger.write_array(datass,"data-12have.xls","有长度-12辆车",resultss[len(resultss)-1][0])
#
# # 生成15have的数据
# result = []
# car_num = 15
# car_length = 1.3
# filename = "data-15have.json"
# tip = "15have"
# main()
# with open("data-15have.json", 'r') as f:
#     resultss = json.load(f)
#     datass = resultss[len(resultss)-1][1]
#     excel_manger.write_array(datass,"data-15have.xls","有长度-15辆车",resultss[len(resultss)-1][0])

# 适应度评估函数
def compute_waiting(pop_type):

    pop_satisfy = []
    pop_waiting = []
    pop_dissss = []

    # 由源点序号确定源点位置
    satisfy_pos_src = [0.0,0.0,11.75,21.464,34.893,48.321,61.75]
    # 由终点序号确定终点位置
    satisfy_pos_dst = [0.0,14.75,28.179,41.607,55.036,64.75,76.5,88.25]

    # 开始计算
    for chromosome in pop_type:
        # 定义变量

        # 距离
        distence = 0
        # 每辆车的等待时间
        waiting = []
        # 任务总时间
        satisfy_time = 0
        # 任务总数
        satisfy_task_num = len(chromosome)
        # 每个小车当前任务
        satisfy_tasks = chromosome[:car_num]
        # 每个小车当前位置
        satisfy_p_car = []
        # 每个小车当前任务序号
        satisfy_tasks_id = []
        # 每个小车当前是否正在工作
        satisfy_is_working = []
        # 每个小车的剩余工作时间
        satisfy_last_time = []
        # 每个小车当前是要(在)装货{0}还是卸货{1}
        satisfy_src_or_dst = []
        # 进货仓锁
        satisfy_lock_src = [False,False,False,False,False,False,False]
        # 出货仓锁
        satisfy_lock_dst = [False,False,False,False,False,False,False,False]
        for i in range(car_num):
            satisfy_is_working.append(False)
            satisfy_last_time.append(0)
            satisfy_src_or_dst.append(0)
            satisfy_tasks_id.append(0)
            satisfy_p_car.append((0-i*car_length+100)%100)
            waiting.append(0)

        # 开始计算
        # 剩余任务数量大于零，继续工作
        while satisfy_task_num>0:
            # 每car_num个任务为一周期
            for i in range(car_num):
                # 如果这个小车没有分配到任务，则跳过
                if satisfy_tasks[i]==[]:
                    continue
                # 如果这个小车不在工作
                if not satisfy_is_working[i]:
                    # 如果小车准备装货
                    if satisfy_src_or_dst[i]==0:
                        temp_src = satisfy_pos_src[satisfy_tasks[i][0]]
                        if temp_src<satisfy_p_car[i]:
                            temp_src = 100+temp_src

                        # 如果小车目的地和自己之间有一辆车
                        if satisfy_p_car[i]<satisfy_p_car[(i+car_num-1)%car_num] and satisfy_p_car[(i+car_num-1)%car_num] <= min(satisfy_p_car[i]+car_v,temp_src):
                            distence+=(satisfy_p_car[(i+car_num-1)%car_num]-car_length-satisfy_p_car[i])
                            satisfy_p_car[i] = satisfy_p_car[(i+car_num-1)%car_num]-car_length
                            waiting[i]+=(1-((satisfy_p_car[(i+car_num-1)%car_num]-car_length-satisfy_p_car[i])/car_v))
                        # 解决重合
                        elif satisfy_p_car[(i+car_num-1)%car_num]==satisfy_p_car[(i+car_num+1)%car_num]:
                            distence += (min(satisfy_p_car[i] + car_v, temp_src)-satisfy_p_car[i])
                            satisfy_p_car[i] = min(satisfy_p_car[i] + car_v, temp_src)
                            satisfy_p_car[i] = satisfy_p_car[i] % 100

                            if satisfy_lock_src[satisfy_tasks[i][0]] == False and satisfy_p_car[i] == satisfy_pos_src[
                                satisfy_tasks[i][0]]:
                                satisfy_is_working[i] = True
                                satisfy_last_time[i] = 10
                                satisfy_lock_src[satisfy_tasks[i][0]] = True
                        elif satisfy_p_car[i]==satisfy_p_car[(i+car_num-1)%car_num]:
                            waiting[i]+=1
                        # 如果小车目的地和自己之间没有车
                        else:
                            distence+=(min(satisfy_p_car[i] + car_v, temp_src)-satisfy_p_car[i])
                            satisfy_p_car[i] = min(satisfy_p_car[i]+car_v,temp_src)
                            satisfy_p_car[i] = satisfy_p_car[i]%100

                            if satisfy_lock_src[satisfy_tasks[i][0]] == False and satisfy_p_car[i] == satisfy_pos_src[satisfy_tasks[i][0]]:
                                satisfy_is_working[i] = True
                                satisfy_last_time[i] = 10
                                satisfy_lock_src[satisfy_tasks[i][0]]=True
                    # 如果小车准备卸货
                    else:
                        temp_dst = satisfy_pos_dst[satisfy_tasks[i][1]]
                        if temp_dst < satisfy_p_car[i]:
                            temp_dst = 100 + temp_dst
                        # 如果小车目的地和自己之间由一辆车
                        if satisfy_p_car[i] < satisfy_p_car[(i + car_num - 1) % car_num] and satisfy_p_car[(i + car_num - 1) % car_num] <= min(satisfy_p_car[i] + car_v,temp_dst):
                            distence += (satisfy_p_car[(i + car_num - 1) % car_num] - car_length - satisfy_p_car[i])
                            satisfy_p_car[i] = satisfy_p_car[(i + car_num - 1) % car_num] - car_length
                            waiting[i]+=(1-((satisfy_p_car[(i+car_num-1)%car_num]-car_length-satisfy_p_car[i])/car_v))
                        # 解决重合
                        elif satisfy_p_car[(i + car_num - 1) % car_num] == satisfy_p_car[(i + car_num + 1) % car_num]:
                            distence += (min(satisfy_p_car[i] + car_v, temp_src) - satisfy_p_car[i])
                            satisfy_p_car[i] = min(satisfy_p_car[i] + car_v, temp_dst)
                            satisfy_p_car[i] = satisfy_p_car[i] % 100

                            if satisfy_lock_dst[satisfy_tasks[i][1]] == False and satisfy_p_car[i] == satisfy_pos_dst[
                                satisfy_tasks[i][1]]:
                                satisfy_is_working[i] = True
                                satisfy_last_time[i] = 10
                                satisfy_lock_dst[satisfy_tasks[i][1]] = True
                        elif satisfy_p_car[i]==satisfy_p_car[(i+car_num-1)%car_num]:
                            waiting[i]+=1
                        # 如果小车目的地和自己之间没有车
                        else:
                            distence += (min(satisfy_p_car[i] + car_v, temp_src) - satisfy_p_car[i])
                            satisfy_p_car[i] = min(satisfy_p_car[i] + car_v,temp_dst)
                            satisfy_p_car[i] = satisfy_p_car[i]%100

                            if satisfy_lock_dst[satisfy_tasks[i][1]]==False and satisfy_p_car[i] == satisfy_pos_dst[satisfy_tasks[i][1]]:
                                satisfy_is_working[i] = True
                                satisfy_last_time[i] = 10
                                satisfy_lock_dst[satisfy_tasks[i][1]] = True

                # 如果这个小车正在工作
                else:
                    # 剩余时间减1s
                    satisfy_last_time[i]-=1
                    # 如果工作结束
                    if satisfy_last_time[i]<=0:
                        # 剩余时间清零
                        satisfy_last_time[i]=0
                        # 结束工作状态
                        satisfy_is_working[i]=False

                        # 如果刚刚结束的是装货
                        if satisfy_src_or_dst[i]==0:
                            #解锁装货
                            satisfy_lock_src[satisfy_tasks[i][0]]=False
                            # 准备取卸货
                            satisfy_src_or_dst[i]=1
                        # 如果刚刚结束的是卸货
                        else:
                            # 解锁装货
                            satisfy_lock_dst[satisfy_tasks[i][1]] = False
                            # 重置为装货
                            satisfy_src_or_dst[i]=0
                            # 任务变更
                            satisfy_tasks_id[i]+=1
                            satisfy_id = satisfy_tasks_id[i]*car_num+i
                            if satisfy_id >= chromosome_length:
                                satisfy_tasks[i]=[]
                                satisfy_p_car[i]=-1
                            else:
                                satisfy_tasks[i]=chromosome[satisfy_id]

                            satisfy_task_num-=1

            # 时间加1s
            satisfy_time+=1

        # 将本次染色体适应度数值储存
        pop_satisfy.append(satisfy_time)
        pop_waiting.append(waiting)
        pop_dissss.append(distence)

    # 返回适应度数组
    return pop_dissss

pop_end = []

with open("data-3have.json", 'r') as f:
    resultss = json.load(f)
    pop_end.append(resultss[len(resultss)-1][1])

with open("data-6have.json", 'r') as f:
    resultss = json.load(f)
    pop_end.append(resultss[len(resultss)-1][1])

with open("data-9have.json", 'r') as f:
    resultss = json.load(f)
    pop_end.append(resultss[len(resultss)-1][1])

with open("data-12have.json", 'r') as f:
    resultss = json.load(f)
    pop_end.append(resultss[len(resultss)-1][1])

with open("data-15have.json", 'r') as f:
    resultss = json.load(f)
    pop_end.append(resultss[len(resultss)-1][1])

resss = compute_waiting(pop_end)

print(resss)
