# import matplotlib.pyplot as plt
# import pandas as pd

# # 读取Excel文件
# df = pd.read_excel('F:/数学建模/建模数据/10-11000带底噪/data底噪.xlsx', usecols=[0,1,2])  # usecols=[0]表示读取第一列
# # 获取第一列数据
# x_data = df.iloc[:, 0].values
# y_data=df.iloc[:, 1].values
# y_data_fit=df.iloc[:, 2].values
# #认为39之前的点不能体现出函数的全部信息
# # x_data = x_data[30:]
# # y_data=y_data[30:]
# # y_data_fit=y_data_fit[30:]
# # plt.plot(x_data, y_data, color='blue', label="residual")
# # plt.plot(x_data, y_data_fit, color='red', label="Reducibility")
# plt.scatter(x_data, y_data_fit, color='red',marker='.',label="Reducibility")
# plt.legend()
# plt.savefig('F:/数学建模/建模数据/10-11000带底噪/10-11000底噪还原度.png',dpi=1000,bbox_inches='tight')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
def func (x, a0,a1, a2,a3):
    return a0*(a3**(x+a1))+a2
# 读取Excel文件
df = pd.read_excel('F:/数学建模/建模数据/10-11000/k.xlsx', usecols=[0,1,2])  # usecols=[0]表示读取第一列
# 获取数据
x_data = df.iloc[:, 0].values#采样点数
y_data=df.iloc[:, 1].values#残差
y_data_fit=df.iloc[:, 2].values#还原度
#认为39之前的点不能体现出函数的全部信息
x_data = x_data[30:]
y_data=y_data[30:]
y_data_fit=y_data_fit[30:]
#拟合数据
fit=[]
popt, pcov = curve_fit(func, x_data, y_data_fit, maxfev=1000000,p0=[5.51044732e+00,-4.06195159e+01,8.11339959e-03,8.84073319e-01])
print(popt)
fit=func(x_data, *popt)
#残差计算
cancha=0
huanyuandu=0
for item1, item2 in zip(y_data_fit, fit):
    cancha+=(item1-item2)
    huanyuandu+=(item1-item2)**2
print("残差：",cancha)
print("还原度：",huanyuandu/10000000)
#求导
x_data_xielv=[]
for i in range(min(x_data),max(x_data+1)):
    x_data_xielv.append(i)
y_data_xielv=func(x_data_xielv, *popt)
gradient=np.gradient(y_data_xielv,x_data_xielv)
# #斜率计算
# x_data_xielv=[]
# xielv=[]
storage=[]
for item1, item2 in zip(x_data_xielv, gradient):
        storage.append((item1,item2))
# for i in range(len(x_data)-1):
#     x_data_xielv.append((x_data[i+1]+x_data[i])/2)
#     xielv.append((y_data_fit[i+1]-y_data_fit[i])/(x_data[i+1]-x_data[i]))
#     storage.append(((x_data[i+1]+x_data[i])/2,(y_data_fit[i+1]-y_data_fit[i])/(x_data[i+1]-x_data[i])))
# plt.scatter(x_data, y_data, color='blue',marker='.',label="Reducibility")
# plt.plot(x_data, fit, color='blue', label="fitting")
# plt.plot(x_data, y_data_fit, color='red', label="Reducibility")
# plt.legend()
# plt.savefig('F:/数学建模/建模数据/10-11000带底噪/10-11000底噪残差.png',dpi=1000,bbox_inches='tight')
# plt.clf()
plt.plot(x_data_xielv, gradient, color='purple', label="k")
plt.semilogx(x_data_xielv, gradient, color='purple')
plt.legend()
# plt.show()
plt.savefig('F:/数学建模/建模数据/10-11000带底噪/10-11000k新.png',dpi=1000,bbox_inches='tight')
# df = pd.DataFrame(storage)
# df.to_excel('F:/数学建模/建模数据/10-11000带底噪/k.xlsx', index=False)
