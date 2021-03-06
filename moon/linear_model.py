# -*- coding: utf-8 -*-#
"""
@File    :   linear_model.py    
@Contact :   sheng_jun@yeah.net
@Author  :   Ace
@Description: 
@Modify Time      @Version    @Desciption
------------      --------    -----------
2021-07-30 22:56    1.0         None
"""

import numpy as np
from moon import metrics

"""
经测试，使用循环的方式会大大降低计算效率，故使用vectorization的方式进行复写
"""


# class LinearRegression1:
#     def __init__(self):
#         self.coef_ = None
#         self.intercept_ = None
#
#     def fit(self, x_train, y_train):
#         assert x_train.ndim == 1, "简单线性回归的特征向量只能是一个列向量"
#         assert len(x_train) == len(y_train), "特征向量的数量必须与结果向量的数量相等"
#         x_mean = np.mean(x_train)
#         y_mean = np.mean(y_train)
#         num = 0
#         d = 0
#         for x_i, y_i in zip(x_train, y_train):
#             num += (x_i - x_mean) * (y_i - y_mean)
#             d += (x_i - x_mean) ** 2
#         self.coef_ = num / d
#         self.intercept_ = y_mean - self.coef_ * x_mean
#         return self


class SimpleLinearRegression:
    def __init__(self):
        self.coef_ = None
        self.intercept_ = None

    def fit(self, x_train, y_train):
        assert x_train.ndim == 1, "简单线性回归的特征向量只能是一个列向量"
        assert len(x_train) == len(y_train), "特征向量的数量必须与结果向量的数量相等"
        x_mean = np.mean(x_train)
        y_mean = np.mean(y_train)

        self.coef_ = (x_train - x_mean).dot(y_train - y_mean) / (x_train - x_mean).dot(x_train - x_mean)
        self.intercept_ = y_mean - self.coef_ * x_mean
        return self

    def predict(self, x_predict):
        assert x_predict.ndim == 1, "简单线性回归的特征向量只能是一个列向量"
        assert self.coef_ is not None and self.intercept_ is not None, "运行预测方法之前必须先进行数据的拟合"
        return np.array([self._predict(x) for x in x_predict])

    def _predict(self, single_x):
        return self.coef_ * single_x + self.intercept_


class MultipleLinearRegression:
    def __init__(self):
        self.coef_ = None
        self.intercept_ = None
        self._theta = None

    def fit_normal(self, X_train, y_train):
        """
        进行数据拟合，训练出coef、intercept、theta
        :param X_train:
        :param y_train:
        :return:
        """
        assert X_train.shape[0] == y_train.shape[0], "特征矩阵的个数必须等于目标矩阵的个数"
        X_b = self.get_X_b(X_train)
        self._theta = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y_train)
        self.intercept_ = self._theta[0]
        self.coef_ = self._theta[1:]
        return self

    def fit_gradient_descent(self, X_train, y_train, eta=0.01, n_iters=1e4):
        """
        根据训练模型X_train，y_train，使用梯度下降法训练Linear Regression模型
        :param X_train: 训练模型矩阵
        :param y_train: 训练结果向量
        :param eta: 学习率
        :param n_iters: 最大学习次数
        :return:
        """
        assert X_train.shape[0] == y_train.shape[0], "训练结果向量的数量必须等于训练特征集的数量"

        def J(theta, X_b, y):
            try:
                return np.sum((y - X_b.dot(theta)) ** 2) / len(X_b)
            except:
                return float("inf")

        def dJ(theta, X_b, y):
            # result = np.empty(len(theta))
            # result[0] = np.sum(X_b.dot(theta) - y)
            # for i in range(1, len(theta)):
            #     result[i] = (X_b.dot(theta) - y).dot(X_b[:, i])
            # return result * 2 / len(X_b)
            return X_b.T.dot(X_b.dot(theta) - y) * 2 / len(X_b)

        def gradient_descent(X_b, y, initial_theta, eta, n_iter=1e4, epsilon=1e-8):
            theta = initial_theta
            cur_iter = 0
            while cur_iter < n_iter:
                gradient = dJ(theta, X_b, y)
                last_theta = theta
                theta = theta - eta * gradient
                if abs(J(last_theta, X_b, y) - J(theta, X_b, y)) < epsilon:
                    break
                cur_iter += 1
            return theta

        X_b = self.get_X_b(X_train)
        initial_theta = np.zeros(X_b.shape[1])
        self._theta = gradient_descent(X_b, y_train, initial_theta, eta, n_iters)
        self.intercept_ = self._theta[0]
        self.coef_ = self._theta[1:]
        return self

    def predict(self, X_test):
        """
        对X_test进行预测
        :param X_test:
        :return:
        """
        assert self.coef_ is not None and self.intercept_ is not None, "预测之前必须进行数据拟合训练"
        assert len(self.coef_) == X_test.shape[1], "测试的特征向量维度必须和训练的特征维度相等"
        X_b = self.get_X_b(X_test)
        return X_b.dot(self._theta)

    def score(self, X_test, y_test):
        """
        使用R²计算得分
        :param X_test:
        :param y_test:
        :return:
        """
        y_predict = self.predict(X_test)
        return metrics.r2_score(y_test, y_predict)

    @staticmethod
    def get_X_b(X):
        """
        计算X_b并且返回
        :param X:
        :return:
        """
        return np.hstack([np.ones((len(X), 1)), X])
