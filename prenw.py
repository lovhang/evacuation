import csv
from pandas import *
import matplotlib.pyplot as plt
import pickle
import numpy as np

x_min = -96.82036511
x_max = -94.34020794
y_min = 28.93832832
y_max = 30.88910535

demand_data = read_csv(r'G:\My Drive\postdoc\ridersharing\demand_location.csv')
x_demand_data = demand_data['x_cord'].tolist()
y_demand_data = demand_data['y_cord'].tolist()
near_demand_node = demand_data['NEAR_FID'].tolist()

shelter_data = read_csv(r'G:\My Drive\postdoc\ridersharing\shelter_location.csv')
x_shelter_data = shelter_data['x_cord'].tolist()
y_shelter_data = shelter_data['y_cord'].tolist()
near_shelter_node = shelter_data['JOIN_FID'].tolist()

x_cord = [x_min]
y_cord = [y_min]
near_node = [0]

for _ in x_demand_data:
    x_cord.append(_)
for _ in x_shelter_data:
    x_cord.append(_)
for _ in y_demand_data:
    y_cord.append(_)
for _ in y_shelter_data:
    y_cord.append(_)
for _ in near_demand_node:
    near_node.append(_)
for _ in near_shelter_node:
    near_node.append(_)
x_cord.append(x_max)
y_cord.append(y_max)
near_node.append(len(near_node))

scenario = 2
sc_set = [i for i in range(scenario)]
ttm = np.array([None for i in range(scenario)])
spm = np.array([None for i in range(scenario)])

for i in sc_set:
    with open('realcaseNetwork/case{case_num}_SPM.pkl'.format(case_num = i+1), 'rb') as f:
        spm[i], ttm[i] = pickle.load(f)
    f.close()
num = len(spm[0][0])
print(ttm[1][428][418])
#print(num)
bigM = 10000
tt = np.array([[[bigM for k in sc_set] for j in range(num)] for i in range(num)])
sp = np.array([[[None for k in sc_set] for j in range(num)] for i in range(num)])
for i in range(0, num): # assign node other than dummy node
    for j in range(0, num):
        if j != i:
            for k in sc_set:
                #print(ttm[k][i][j])
                tt[i][j][k] = ttm[k][i][j][0]
                sp[i][j][k] = spm[k][i][j]
print(tt[428][418])
new_num = len(x_cord)
print(new_num)
ttn = np.array([[[bigM for k in sc_set] for j in range(new_num)] for i in range(new_num)])
spn = np.array([[[None for k in sc_set] for j in range(new_num)] for i in range(new_num)])
service_time=2.0
for i in range(1,new_num-1):
    o_node = near_node[i]
    for j in range(1,new_num-1):
        d_node = near_node[j]
        if o_node == d_node:
            for k in sc_set:
                ttn[i][j][k] = service_time
                spn[i][j][k] = [i,j]
        else:
            for k in sc_set:
                ttn[i][j][k] = tt[o_node][d_node][k] + 2*service_time
                spn[i][j][k] = sp[o_node][d_node][k]

sd = new_num-2
for i in range(0, new_num):
    for k in sc_set:
        ttn[0][i][k] = 1.0  # Zero node to all nodes for all scenarios
        ttn[i][0][k] = 1.0  # All nodes to 0 for all scenarios
        #ttn[sd][i][k] = 1.0  # superdriver to all nodes for all scenarios
        #ttn[i][sd][k] = 1.0  # all nodes to superdriver for all scenarios
        ttn[i][i][k] = 1.0  # node to itself for all scenarios
        ttn[i][-1][k] = 1.0  # node to last dummy node
        ttn[-1][i][k] = 1.0  # last dummy node to all node
print(ttn[165][1007])
print(near_node[164])
print(near_node[1007])
#print(ttn[838][725])
#print(tt[411][408][0])
with open('realcaseNetwork/1000demand_SPM.pkl', 'wb') as f:
        pickle.dump([x_cord, y_cord, ttn, spn], f)
f.close()