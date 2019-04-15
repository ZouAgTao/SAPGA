import matplotlib.pyplot as plt
import json

# x = range(1,601)
x = [3,6,9,12,15]
y1 = [13257,6932,4698,3631,2950]
y2 = [217,219,253.55,298.13,382.56]

# with open('./data-3none.json', 'r') as f:
#     result = json.load(f)
#     # sub = result[0][0]-result[len(result)-1][0]
#     for i in range(600):
#         # y1.append((result[i][0]-result[len(result)-1][0])/sub*100)
#         y1.append((result[i][0]))

# with open('./data-3have.json', 'r') as f:
#     result = json.load(f)
#     y.append((result[0][0] - result[len(result) - 1][0]) / len(result))
#
# with open('./data-6have.json', 'r') as f:
#     result = json.load(f)
#     y.append((result[0][0] - result[len(result) - 1][0]) / len(result))
#
# with open('./data-9have.json', 'r') as f:
#     result = json.load(f)
#     y.append((result[0][0]-result[len(result)-1][0])/len(result))


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

plt.title("小车平均等待时间变化情况")
plt.xlabel("小车数量（个）")
plt.ylabel("小车平均等待时间（秒）")

# plt.plot(x,y1,color='red', label='不计穿梭车实际长度')
# plt.plot(x,y2,color='green', label='6辆穿梭车')
# plt.plot(x,y2,color='skyblue', label='考虑穿梭车实际长度')

plt.plot()
plt.plot(x,y1,color='green')
plt.plot(x,y2,color='skyblue')

# plt.legend()
plt.show()