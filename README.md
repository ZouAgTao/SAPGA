# 单亲遗传算法流程概述

# !!**本项目仅供学习和研究，不可用于参加比赛或者其他类似的活动**!!

## 编码

考虑到编码与实际数据相结合存在冲突的问题，将编码设计成**基因型**和**表现型**两类染色体编码方案，并设计`gene_to_type`转换函数将基因型编码与表现型编码进行转换

基因型编码的染色体用于进行*单亲遗传算法*的单点交换变异，*单点倒位变异*，*单点移位变异*等操作，而表现型编码的染色体用于进行**个体适应度评估函数**的适应度计算

## 初始化种群

由于所有货物任务的各个任务总量固定，所以可以生成固定长度的染色体（L=522），再以随机的方式将522个任务放置到染色体中(以每N（N=3，6，9）个基因为一组（小车运行的一个任务周期）)

## 生成染色体的表现型编码

## 储存当代最优染色体记录到历史中

## 计算适应度

采用分支与模拟的方式进行总时长的计算，根据**小车数量**，**小车长度**，**小车运行速度**会有*自适应*的计算算法，能求解出总运行时间的*相对精确解*，用于作为该染色体的**适应度**（该方案的评估值）

## 选择函数

采用**轮盘赌**的方式+**竞标法**（优胜劣汰），轮盘赌方法将根据适应度对种群进行筛选，竞标法将适应度高的染色体**直接保留**到下一代，不参与交叉和变异

## 单亲遗传算法

### 换位算子：

在染色体中随机选择两个基因位，以一定概率**pe**交换这两个基因，生成新的染色体

### 倒位算子：

在染色体中随机选择一段基因，以一定概率**pr**把基因串中基因依次首位倒置，从而生成新的染色体

### 移位算子：

在染色体中随机选择一段基因，以一定概率**pm**把基因串中基因依次后移（或前移），从而生成新的染色体

## 进化

将本次进化后的染色体进行下一次循环，迭代到指定代数（G=600）

## 结果统计

![单亲遗传算法迭代图(不计长度)](https://github.com/ZouAgTao/SAPGA/blob/master/img_data/1/1.png?raw=true)



![单亲遗传算法迭代图(考虑长度)](https://github.com/ZouAgTao/SAPGA/blob/master/img_data/1/2.png?raw=true)

![单亲遗传算法收敛速率变化(不计长度)](https://github.com/ZouAgTao/SAPGA/blob/master/img_data/2/1.png?raw=true)

![单亲遗传算法收敛速率变化(考虑长度)](https://github.com/ZouAgTao/SAPGA/blob/master/img_data/2/2.png?raw=true)

![单亲遗传算法迭代图(3辆穿梭车)](https://github.com/ZouAgTao/SAPGA/blob/master/img_data/3/1.png?raw=true)

![单亲遗传算法迭代图(6辆穿梭车)](https://github.com/ZouAgTao/SAPGA/blob/master/img_data/3/2.png?raw=true)

![单亲遗传算法迭代图(9辆穿梭车)](https://github.com/ZouAgTao/SAPGA/blob/master/img_data/3/3.png?raw=true)

![系统运行时间变化情况](https://github.com/ZouAgTao/SAPGA/blob/master/img_data/4/1.png?raw=true)

![系统等待时间变化情况](https://github.com/ZouAgTao/SAPGA/blob/master/img_data/4/2.png?raw=true)

