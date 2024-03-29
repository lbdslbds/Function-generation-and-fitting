import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd
from progress.bar import Bar
from scipy.optimize import curve_fit
def func(x, a0, a1, a2, a3,m,k,b):
    # 10asin (mx+k)+5asin (8mx+j)+asin (nx +c)+bsin (3nx +d)+k
    return 10*a0*np.sin(m*x+k)+5*a0*np.sin(8*m*x+a1)+a0*np.sin(a2*x+a3)+b*np.sin(3*a2*x)+k
storage=[]
print("拟合方法:输入1代表使用curve_fit函数来拟合,输入2代表使用多项式拟合,输入3代表使用样条插值")
a=input("请输入起始值,终止值,步长,拟合方法，用空格分开 例如:100 11000 100 3 ")
result = a.split(" ")
bar_calculation = Bar('calculation:', max=(int(result[1])-int(result[0]))/int(result[2])+1)
for i in range(int(result[0]),int(result[1])+1,int(result[2])):
    caiyang=int(i)
    # 生成采样数据
    x_data_sampled = np.linspace(0, 5, caiyang)
    y_data_sampled = func(x_data_sampled, 2.5, 1.3, -0.5, 2,3,4,3.2)+np.random.normal(-1,1)
    # 生成模拟数据,生成10000000个点作为对比
    x_data = np.linspace(0, 5, 10000000)
    y_data=[]
    k=0
    for i in range(0,10000000):
        for j in range(k,caiyang):
            if x_data[i]<x_data_sampled[k]:
                y_data.append(func(x_data[i], 2.5, 1.3, -0.5, 2,3,4,3.2) + np.random.normal(-1,1))
                break
            elif x_data[i]==x_data_sampled[j]:
                y_data.append(y_data_sampled[j])
                k=j
                break
            elif x_data[i]>x_data_sampled[j]:
                y_data.append(func(x_data[i], 2.5, 1.3, -0.5, 2,3,4,3.2) + np.random.normal(-1,1))
                k=j+1
                break
    if int(result[3])==1:
        # 使用curve_fit函数来拟合非线性数据
        popt, pcov = curve_fit(func, x_data_sampled, y_data_sampled,maxfev=1000000)
        print("拟合参数：", popt)
        print("拟合参数的协方差矩阵：", pcov)
        y_data_fit = func(x_data, *popt)
    elif int(result[3])==2:
        #多项式拟合
        z1 = np.polyfit(x_data_sampled, y_data_sampled, 200)
        p1 = np.poly1d(z1)
        y_data_fit=p1(x_data)
    elif int(result[3])==3:
        # 样条插值
        interp_func = interp1d(x_data_sampled, y_data_sampled, kind='cubic')
        y_data_fit = interp_func(x_data)
    #残差计算
    cancha=0
    huanyuandu=0
    for item1, item2 in zip(y_data, y_data_fit):
        cancha+=(item1-item2)
        huanyuandu+=abs(item1-item2)
    # 画出原始数据和拟合曲线
    # plt.scatter(x_data_sampled, y_data_sampled, label="Data") 
    plt.plot(x_data, y_data, color='blue', label="Data")
    plt.plot(x_data, y_data_fit, color='red', label="Fitted curve")
    plt.legend()
    plt.savefig(f'D:/建模数据/100-11000带底噪/{caiyang}.png',dpi=300,bbox_inches='tight')
    plt.clf()
    storage.append((caiyang,cancha,huanyuandu/10000000))
    bar_calculation.next()
bar_calculation.finish()
df = pd.DataFrame(storage)
df.to_excel('D:/建模数据/100-11000带底噪/data底噪.xlsx', index=False)