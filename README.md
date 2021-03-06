# 机器学习
## 一、 kNN算法
**通过模仿sklearn算法，试验，得出kNN分类的类，后续随着学习的深入，还继续更新手写机器学习的基本算法**
### kNN的一般过程
1. 获取数据
- 对数据进行训练集和测试集的切分
- 对训练集和测试集都进行一次数据归一化
- 创建kNN的类，获取最优超参数(网格化搜索以cv的方式获取到最优超参数)
- 学习后得到的超参数，投入模型用于生产
### kNN的缺点
1. 效率极低
- 如果有m个样本，n个特征，预测一个新的数据，则需要O(m*n)的复杂度
- 高度数据相关，kNN相较而言受边界值的影响很大
- 预测结果不具有可解释性
- kNN很可能遭受维数灾难

## 二、线性回归
1. 主要用于解决回归问题
2. 解决问题简单，实现容易
3. 许多强大的非线性模型基础
4. 结果具有很好的可解释性
5. 蕴含机器学习中很多重要思想
### (一)简单线性回归
#### I过程：
1. 假设我们找到了一个最佳拟合方程：y = ax + b
2. 对于每个样本点x(i)，我们可以得出预测值为：$y^~_i = ax_i + b$
3. 我们希望y`(i) 和 y(i)的差尽可能小，考虑到所有样本，我们可以得出：$\sum_{i=1}^m(y_i - y^~_i) ^ 2$
4. 综上，我们可以得出损失函数：$\sum_{i=1}^m(y^i - ax^i - b) ^ 2$需要尽可能小才能拟合我们的直线方程
#### II目标
1. 需要找到a,b使得损失函数尽可能小
2. 这就是一个典型的最小二乘法的求解
3. 公式详见：公式推导
### III向量法求解
$$ a = \frac{\sum^m_{i=1}(X^{i} - x_{mean})(y^{i} - y_{mean})} {\sum^{m}_{i=1}(x^{i} - x_{mean})^2} $$

$$ b = y_{mean} - a*x_{mean} $$

通过观察我们可以发现，a,b的求解都满足$\sum_{i=1}^mw^{i} \cdot v^{i}$，所以我们可以归纳出最终的公式：
$a = /frac{(x - \hat x)·(y - \hat y)}{(x - \hat x)·(x - \hat x)}$
### (二)多元线性回归

#### 目标：
- 找到一个向量$\theta$，使得损失函数$\hat y^i = \theta_0 + \theta_1X^i_1 + \theta_2X^i_2+...+\theta_nX^i_n$尽可能小
#### 寻找：
1. 假设第i行数据的特征向量为：$X^i = (X_0^i,X^i,...,X_n^i)$，且$X_0^i ≡ 1$
2. 根据损失函数，我们可以归纳出$\hat y^i = X^i · \theta$
3. $\hat y = X_b · \theta$
4. $X_b = \left[
\begin{matrix}
1 & X_1^1 & ... & X_1^n \\
1 & X_1^2 & ... & X_2^n \\
. & ..... & ... & ..... \\
1 & X_1^m & ... & X_m^n \\
\end{matrix} \right]$
5. 最后可以得出结论公式：损失函数$(y - X_b·\theta)^T(y - X_b·\theta)$
6. 根据上式可以推导出多元线性回归的**正规方程解**：$\theta = (X^T_bX_b)^{-1}X^T_by$
7. 缺点：时间复杂度非常高
8. 优点：不需要数据归一化处理，因为数据是否统一都无所谓

## 衡量线性回归算法的指标
需要预测的值与实际值进行比较，可以通过MSE，RMSE，MAE，R²进行衡量
### 一、 MSE
MSE(Mean Squared Error)均方误差
1. 衡量标准：$\sum_{i=1}^m{(y^i_{test} - y^i)^2}$
2. 但是这个衡量标准是和m相关的，所以我们需要将上式整体除以m进行平均，我们就可以得到$MSE = \frac{\sum_{i=1}^m{(y^i_{test} - y^i)^2}}{m}$

### 二、 RMSEG
RMSE(Root Mean Squared Error)均方根误差
- 根据MSE的求解，我们可以看到这个量纲是带平方项的，所以我们需要去平方，根据基本数学原理，开方即可：
$$RMSE = \sqrt{MSE} = \sqrt{\frac{\sum_{i=1}^m{(y^i_{test} - y^i)^2}}{m}}$$

### 三、 MAE
MAE(Mean Absolute Error)平均绝对误差
- 根据推导的公式我们可以看出，两个点的距离也可以通过绝对值表现：$MAE = \frac{\sum_{i=1}^m|y^i_{test} - y^i|}{m}$

### 最好的衡量线性回归法的指标R²
上面小结看得出MSE、RMSE、MAE都无法很直观的看出一个合理范围的值，所以我们引入了R²，将分类准确度统一在0到1之间：0最差，1最好

1. 直接给出计算指标公式：$R^2 = 1 - \frac{SS_{residual}}{SS_{total}}$
2. 一般$SS_{residual}$解释为：Residual Sum of Squares，暨$SS_{residual} = \sum_{i=1}^{m}(y^i - y^i_h) ^ 2$
3. $SS_{total}$解释为：Total Sum of Squares，暨$SS_{total} = \sum_{i=1}^m(y_{mean} - y^i) ^ 2$
$$ R^2 = 1 - \frac {\sum_{i=1}^{m}(y^i - y^i_h) ^ 2}{\sum_{i=1}^m(y_{mean} - y^i) ^ 2}$$
4. R²的意义是：对于$SS_{residual}$来说，我们可以理解成我们预测模型计算出来产生的错误
5. 分母$SS_{total}$可以理解成基本错误，暨$y = y_{mean}$，记作Baseline Model，这个错误是比较多的预测
6. $R^2 <= 1$
7. $R ^ 2$越大越好，当且仅当预测模型没有任何错误的时候，$R^2==1$
8. $R^2 == 0$说明我们的模型等于baselin，训练无效
9. $R^2 < 0$说明我们学习到的模型还不如基本模型，此时可以判断得出我们的数据不是线性数据
10. 公式中分子分母同时除以m，可以得到变形公式：$$ R^2 = 1 - \frac {{\sum_{i=1}^{m}(y^i - y^i_h) ^ 2}\div{m}}{{\sum_{i=1}^m(y_{mean} - y^i) ^ 2} \div {m}}$$
11. 我么可以看出：${\sum_{i=1}^{m}(y^i - y^i_h) ^ 2}\div{m}$就是MSE
12. ${\sum_{i=1}^m(y_{mean} - y^i) ^ 2} \div {m}$就是方差
13. 暨$R ^ 2 = 1 - \frac{MSE(y^{h},y)}{var(y)}$
14. $R^2$具有统计意义的
