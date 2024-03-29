# Form implementation generated from reading ui file 'n.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import math
import numpy as np

from scipy.integrate import quad
import matplotlib.pyplot as plt





class Ui_MainWindow(object):
    def chto_to(self, k1=1, k2=0, M=0.05, N=20, sigma=30.18 * 10 ** -3, ro=1021.67, R=0.035, t=0.01, algoritm_type=0, m1=0.1):
        try:
            counter = 0
            v_l = []
            d_l = []
            d1_l = []
            t_l = []
            vr_l = []

            g = 9.8
            L0 = (M * g) / (2 * k1)
            znach1 = L0 * (N - 1) ** 2 / N ** 2
            znach2 = L0 * (N - 2) ** 2 / N ** 2
            L1 = L0 - znach1
            znach3 = znach1 - znach2

            start = -1

            def d(alpha):
                a = L1
                b = znach3
                return (b - a) * alpha / (2 * math.pi) + a


            if algoritm_type == 1:
                d_t = 2 * math.pi * (N - 1)
                d_k = d(2 * math.pi * (N - 1))
            else:
                d_t = 4 * math.pi
                d_k = d(4 * math.pi)

            def a_search():
                md1 = 100000
                a1 = 0
                for a in range(100, 350):
                    A_1 = a / 10000
                    r = A_1 * math.cosh(L1/ (2 * A_1))
                    if abs(r - R) < md1:
                        md1 = abs(r - R)
                        a1 = A_1
                return a1

            A = a_search()

            def b_search():
                md1 = 100000
                b1 = 0
                for b in range(0, 10000):
                    B_1 = b / 100
                    r = A * math.cosh(B_1 * L1 / 2)
                    if abs(r - R) < md1:
                        md1 = abs(r - R)
                        b1 = B_1
                return b1

            B = b_search()

            def for_integral_Y(x):
                return A * math.cosh(B * x) * (1 + (A * B * math.sinh(B * x)) ** 2) ** 0.5

            Y = 2 * math.pi * quad(for_integral_Y, -d_k / 2, d_k / 2)[0]



            while True:
                def a_search():
                    md1 = 100000
                    a1 = 0
                    for a in range(100, 350):
                        A_1 = a / 10000
                        r = A_1 * math.cosh(d_k / (2 * A_1))
                        if abs(r - R) < md1:
                            md1 = abs(r - R)
                            a1 = A_1
                    return a1
                A = a_search()

                def b_search():
                    md1 = 100000
                    b1 = 0
                    for b in range(0, 10000):
                        B_1 = b / 100
                        r = A * math.cosh(B_1 * d_k / 2)
                        if abs(r - R) < md1:
                            md1 = abs(r - R)
                            b1 = B_1
                    return b1

                B = b_search()



                m = N * 1.4 * 10 ** -3

                h = m / (ro * Y)

                def for_integral_Z(x):
                    return (A * math.cosh(B * x)) ** 2

                Z = quad(for_integral_Z, -d_k / 2, L1 / 2)[0]

                def for_integral_L(x):
                    return (1 + (A * B * math.sinh(B * x)) ** 2) ** 0.5

                L = quad(for_integral_L, -d_k / 2, d_k / 2)[0]

                if algoritm_type == 0:
                    a = ro * L * h * R * (math.pi / d_k) * (4 * math.pi ** 2 * Z / (d_k ** 2) + 1)
                    b = 4 * math.pi ** 2 * R ** 2 * k2 / d_k ** 2
                    c = -(m1 * 9.8 + (4 * sigma * L * math.pi * R) / d_k)
                    V0 = (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)

                    a = ro * L * h * (Z / (2 * R ** 2) + (d_k ** 2) / (8 * math.pi * R**2))
                    b = k2
                    c = -(m1 * 9.8 * d_k / (2 * math.pi * R) + 2 * sigma * L)
                    vR = ((-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a))
                else:
                    a = ro * L * h * R * (math.pi / d_k) * (4 * math.pi ** 2 * Z / (d_k ** 2) + 1)
                    b = 4 * math.pi ** 2 * R ** 2 * k2 / d_k ** 2
                    c = -(-m1 * 9.8 + (4 * sigma * L * math.pi * R) / d_k)
                    V0 = (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)

                    a = ro * L * h * (Z / (2 * R ** 2) + (d_k ** 2) / (8 * math.pi * R ** 2))
                    b = k2
                    c = -(-m1 * 9.8 * d_k / (2 * math.pi * R) + 2 * sigma * L)
                    vR = ((-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a))
                vr_l.append(vR)


                #
                # V0 = ((4 * sigma) / (ro * h * (1 + (Z * 4 * math.pi ** 2) / (d_k ** 2)))) ** 0.5


                if algoritm_type == 0:
                    d_t = V0 * t / R + d_t
                else:
                    d_t = d_t - V0 * t / R
                d_k = d(d_t)

                #print(d_k, V0, d_t)
                # counter += 1
                # if counter == 10:
                #     return
                # if start == -1:
                #     start = d_k
                new_proc = 100 - 100 * d_k / start
                self.textEdit.setText(str(round(new_proc, 5)) + ' %')
                if algoritm_type == 0:
                    d_l.append(d_t)
                else:
                    if d_l == []:
                        d_l.append(0)
                    else:
                        d_l.append(d_l[-1] + V0 * t / R)
                v_l.append(V0)

                d1_l.append(d_k)


                if t_l == []:
                    t_l.append(0)
                else:
                    t_l.append(t_l[-1] + t)
                # print('A, B, Y, Z, L, Vparal, Vrad, d')
                # print(A, B, Y, Z, L, V0, vR, d_k)


                if algoritm_type == 0:
                    if t_l[-1] > 2 * math.pi * R * N / vr_l[0]:
                        break
                else:
                    if d_t <= 4 * math.pi:
                        break
                # d_l = []
                # while V0 > 0:
                #     v_l.append(V0)
                #     d_l.append(d(V0 * 1/ R + 4 * math.pi))
                #     V0 = V0 - d(V0 * 1/ R + 4 * math.pi)

                QtCore.QCoreApplication.processEvents()
            self.textEdit.setText(f'found {len(d_l)} values, saving')
            figure, axis = plt.subplots(2, 2)
        r_t = ''
        r_d = ''
        r_dv = ''
        r_tv = ''
        for i in range(len(d_l)):
            r_t += f'{t_l[i]};{v_l[i]}\n'
            r_d += f'{d_l[i]};{v_l[i]}\n'
            r_dv += f'{d_l[i]};{vr_l[i]}\n'
            r_tv += f'{t_l[i]};{vr_l[i]}\n'

        with open('v_d_lResult.csv', 'w') as f:
            f.write(r_d)
        with open('v_d_tResult.csv', 'w') as f:
            f.write(r_t)
        with open('vr_d_lResult.csv', 'w') as f:
            f.write(r_dv)
        with open('vr_d_tResult.csv', 'w') as f:
            f.write(r_tv)

        axis[0, 0].plot(d_l, v_l)
        axis[0, 0].set_title("v от alpha")

        axis[0, 1].plot(t_l, v_l)
        axis[0, 1].set_title("v от t")

        axis[1, 1].plot(t_l, vr_l)
        axis[1, 1].set_title("vr от t")

        axis[1, 0].plot(d_l, vr_l)
        axis[1, 0].set_title("vr от alpha")

        plt.show()

    except Exception as e:
    print(e.args)


def setupUi(self, MainWindow):
    MainWindow.setObjectName("MainWindow")
    MainWindow.resize(1333, 895)
    self.centralwidget = QtWidgets.QWidget(MainWindow)
    self.centralwidget.setObjectName("centralwidget")
    self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
    self.gridLayout.setObjectName("gridLayout")
    self.label_8 = QtWidgets.QLabel(self.centralwidget)
    font = QtGui.QFont()
    font.setPointSize(60)
    self.label_8.setFont(font)
    self.label_8.setAlignment(QtCore.Qt.AlignCenter)
    self.label_8.setObjectName("label_8")
    self.gridLayout.addWidget(self.label_8, 0, 0, 1, 1)
    self.verticalLayout_2 = QtWidgets.QVBoxLayout()
    self.verticalLayout_2.setObjectName("verticalLayout_2")
    self.comboBox = QtWidgets.QComboBox(self.centralwidget)
    font = QtGui.QFont()
    font.setPointSize(17)
    self.comboBox.setFont(font)
    self.comboBox.setObjectName("comboBox")
    self.comboBox.addItem("")
    self.comboBox.addItem("")
    self.verticalLayout_2.addWidget(self.comboBox)
    self.verticalLayout = QtWidgets.QVBoxLayout()
    self.verticalLayout.setObjectName("verticalLayout")
    self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
    self.horizontalLayout_2.setObjectName("horizontalLayout_2")
    self.label = QtWidgets.QLabel(self.centralwidget)
    font = QtGui.QFont()
    font.setPointSize(15)
    self.label.setFont(font)
    self.label.setAlignment(QtCore.Qt.AlignCenter)
    self.label.setObjectName("label")
    self.horizontalLayout_2.addWidget(self.label)
    self.k1 = QtWidgets.QDoubleSpinBox(self.centralwidget)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.k1.sizePolicy().hasHeightForWidth())
    self.k1.setSizePolicy(sizePolicy)
    font = QtGui.QFont()
    font.setPointSize(15)
    self.k1.setFont(font)
    self.k1.setDecimals(10)
    self.k1.setObjectName("k1")
    self.horizontalLayout_2.addWidget(self.k1)
    self.verticalLayout.addLayout(self.horizontalLayout_2)
    self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
    self.horizontalLayout_4.setObjectName("horizontalLayout_4")
    self.label_9 = QtWidgets.QLabel(self.centralwidget)
    font = QtGui.QFont()
    font.setPointSize(15)
    self.label_9.setFont(font)
    self.label_9.setAlignment(QtCore.Qt.AlignCenter)
    self.label_9.setObjectName("label_9")
    self.horizontalLayout_4.addWidget(self.label_9)
    self.k2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
    sizePolicy.setHeightForWidth(self.M.sizePolicy().hasHeightForWidth())
    self.M.setSizePolicy(sizePolicy)
    font = QtGui.QFont()
    font.setPointSize(15)
    self.M.setFont(font)
    self.M.setDecimals(10)
    self.M.setObjectName("M")
    self.M.setMaximum(1000000)
    self.horizontalLayout_8.addWidget(self.M)
    self.verticalLayout.addLayout(self.horizontalLayout_8)
    self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
    self.horizontalLayout_11.setObjectName("horizontalLayout_11")
    self.label_3 = QtWidgets.QLabel(self.centralwidget)
    font = QtGui.QFont()
    font.setPointSize(15)
    self.label_3.setFont(font)
    self.label_3.setAlignment(QtCore.Qt.AlignCenter)
    self.label_3.setObjectName("label_3")
    self.horizontalLayout_11.addWidget(self.label_3)
    self.N = QtWidgets.QDoubleSpinBox(self.centralwidget)
    self.N.setMaximum(100000)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.N.sizePolicy().hasHeightForWidth())
    self.N.setSizePolicy(sizePolicy)
    font = QtGui.QFont()
    font.setPointSize(15)
    self.N.setFont(font)
    self.N.setDecimals(10)
    self.N.setObjectName("N")
    self.horizontalLayout_11.addWidget(self.N)
    self.verticalLayout.addLayout(self.horizontalLayout_11)
    self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
    self.horizontalLayout_10.setObjectName("horizontalLayout_10")
    self.label_4 = QtWidgets.QLabel(self.centralwidget)
    font = QtGui.QFont()
    font.setPointSize(15)
    self.label_4.setFont(font)
    self.label_4.setAlignment(QtCore.Qt.AlignCenter)
    self.label_4.setObjectName("label_4")
    self.horizontalLayout_10.addWidget(self.label_4)
    self.sigma = QtWidgets.QDoubleSpinBox(self.centralwidget)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.sigma.sizePolicy().hasHeightForWidth())
    self.sigma.setSizePolicy(sizePolicy)
    font = QtGui.QFont()
    font.setPointSize(15)
    self.sigma.setFont(font)
    self.sigma.setDecimals(10)
    self.sigma.setObjectName("sigma")
    self.horizontalLayout_10.addWidget(self.sigma)
    self.verticalLayout.addLayout(self.horizontalLayout_10)
    self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
    self.horizontalLayout_9.setObjectName("horizontalLayout_9")
    self.label_5 = QtWidgets.QLabel(self.centralwidget)
    font = QtGui.QFont()
    font.setPointSize(15)
    self.label_5.setFont(font)
    self.label_5.setAlignment(QtCore.Qt.AlignCenter)
    self.label_5.setObjectName("label_5")
    self.horizontalLayout_9.addWidget(self.label_5)
    self.ro = QtWidgets.QDoubleSpinBox(self.centralwidget)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.ro.sizePolicy().hasHeightForWidth())
    self.ro.setSizePolicy(sizePolicy)
    font = QtGui.QFont()
    font.setPointSize(15)
    self.ro.setFont(font)
    self.ro.setDecimals(10)
    self.ro.setObjectName("ro")
    self.horizontalLayout_9.addWidget(self.ro)
    self.verticalLayout.addLayout(self.horizontalLayout_9)
    self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
    self.horizontalLayout_7.setObjectName("horizontalLayout_7")
    self.label_6 = QtWidgets.QLabel(self.centralwidget)
    font = QtGui.QFont()
    font.setPointSize(15)
    self.label_6.setFont(font)

