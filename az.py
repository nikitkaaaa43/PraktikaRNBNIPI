import numpy as np
import math

# для 1 уравнения
def df1_du1(u1, v1, p1, ksi1, s1, v):
    return -v * (0.33 - 3 * math.exp(-math.pow(s1, 5)))


def df1_dv1(u1, v1, p1, ksi1, s1, v):
    return -v * (0.15 + 1.35 * math.exp(-math.pow(s1, 5)))


def df1_dp1(u1, v1, p1, ksi1, s1, v):
    return -0.3 * v


def df1_dksi1(u1, v1, p1, ksi1, s1, v):
    return 1


def df1_ds1(u1, v1, p1, ksi1, s1, v):
    return 22.5 * v * math.pow(s1, 4) * math.exp(-math.pow(s1, 5)) * (0.3 * v1 + 2 * u1 / 3)

# для 2 уравнения
############################
def df2_du1(u1, v1, p1, ksi1, s1, v):
    return -(0.5 + 4.5 * math.exp(-math.pow(s1, 5))) / phi


def df2_dv1(u1, v1, p1, ksi1, s1, v):
    return -2 * (0.5 + 4.5 * math.exp(-math.exp(s1, 5))) * lam / phi


def df2_dp1(u1, v1, p1, ksi1, s1, v):
    return 1


def df2_dksi1(u1, v1, p1, ksi1, s1, v):
    return 0


def df2_ds1(u1, v1, p1, ksi1, s1, lam, phi):
    return (22.5 * math.pow(s1, 4) * math.exp(-math.pow(s1, 4)) * (2 * lam * v1 + u1)) / phi

# для 3 уравнения
#############################
def df3_du1(beta):
    return 1 / beta


def df3_dv1(beta):
    return -1 / beta


def df3_dp1():
    return 0


def df3_dksi1():
    return 0


def df3_ds1():
    return 0

# для 4 уравнения
#############################
def df4_du1():
    return -1


def df4_dv1():
    return 0


def df4_dp1():
    return 0


def df4_dksi1():
    return 0


def df4_ds1():
    return 0

# для 5 уравнения
#############################
def df5_du1(u1, v1, p1, ksi1, s1, B, lam, gamma1):
    res = (2 * gamma1 * (0.5 + 4.5 * math.exp(-math.pow(s1, 5)))) * s1
    res = res * (u1 + 6 * (2 * lam * v1 + u1) * (3 * lam * v1 / (2 * u1)) - 9 * lam * lam * v1 * v1 / (
                4 * u1 * u1) - 2 * u1 * (1 - 3 * lam * v1 / (2 * u1)))
    res1 = -1 + 9 * lam * v1 / u1 - 27 * lam * lam * v1 * v1 / (2 * u1 * u1)
    res1 = res1 + 6 * (2 * lam * v1 + u1) * (
                -3 * lam * v1 / (2 * u1 * u1) + 9 * lam * lam * v1 * v1 / (2 * u1 * u1 * u1))
    return res * res1 / (B * s1 + 1)


def df5_dv1(u1, v1, p1, ksi1, s1, v):
    res = 1.5 * (27 * lam * lam * v1 * v1 - 3 * lam * v1 * u1 - 4 * u1 * u1) * lam * s1 * gamma1
    res = res * (
                54 * lam * lam * lam * v1 * v1 * v1 - 9 * lam * lam * u1 * v1 * v1 - 24 * lam * u1 * u1 * v1 + 2 * u1 * u1 * u1)
    res = res * (1 + 9 * math.exp(-math.pow(s1, 5)))
    return res / (math.pow(u1, 4) * (B * s1 + 1))


def df5_dp1(u1, v1, p1, ksi1, s1, v):
    return 0


def df5_dksi1(u1, v1, p1, ksi1, s1, v):
    return 0


def df5_ds1(u1, v1, p1, ksi1, s1, lam, phi):
    res = (22.5 * math.pow(s1, 5) + 22.5 * B * math.pow(s1, 6) - 4.5) * math.pow(u1, 6)
    res = res + (-540 * B * math.pow(s1, 6) + 108 - 540 * math.pow(s1, 5)) * v1 * lam * math.pow(u1, 5)
    res = res + (3037.5 * B * math.pow(s1, 6) - 607.5 + 3037.5 * math.pow(s1, 5)) * v1 * v1 * lam * lam * math.pow(u1,
                                                                                                                   4)
    res = res + (3645 * B * math.pow(s1, 6) - 729 + 3645 * math.pow(s1,
                                                                    5)) * v1 * v1 * v1 * lam * lam * lam * u1 * u1 * u1
    res = res + (-14124.375 * B * math.pow(s1, 6) + 2824.875 - 14124.375 * math.pow(s1, 5)) * math.pow(v1,
                                                                                                       4) * math.pow(
        lam, 4) * u1 * u1
    res = res + (-5467.5 * B * math.pow(s1, 6) + 1093.5 - 5467.5 * math.pow(s1, 5)) * math.pow(v1, 5) * math.pow(lam,
                                                                                                                 5) * u1
    res = res + (-3280.5 + 16402.5 * math.pow(s1, 5) + 16402.5 * B * math.pow(s1, 6)) * math.pow(v1, 6) * math.pow(lam,
                                                                                                                   6)
    res = res * math.exp(-math.pow(s1, 5))
    res = res - 0.5 * math.pow(u1, 6) + 12 * lam * math.pow(u1, 5) * v1
    res = res + (B * B * s1 * s1 + 2 * B * s1 - 67.5 * lam * lam * v1 * v1 + 1) * math.pow(u1, 4)
    res = res - 81 * lam * lam * lam * u1 * u1 * u1 * v1 * v1 * v1 + 313.875 * math.pow(lam, 4) * u1 * u1 * math.pow(v1,
                                                                                                                     4)
    res = res + 121.5 * math.pow(lam, 5) * u1 * math.pow(v1, 5) - 364.5 * math.pow(lam, 6) * math.pow(v1, 6)
    return -res * gamma1 / (u1 * u1 * u1 * u * B * s1 - 1 * (B * s1 + 1) * (B * s1 + 1))


if __name__ == "__main__":
    i = 0
    for lam in [x / 100.0 for x in range(0, 10, 2)]:
        for B in [x / 100.0 for x in range(0, 10, 2)]:
            for gamma in [x / 100.0 for x in range(0, 10, 2)]:
                for v in [x / 100.0 for x in range(0, 10, 2)]:
                    for beta in [x / 100.0 for x in range(0, 10, 2)]:
                        for u1 in [x / 100.0 for x in range(0, 10, 2)]:
                            for v1 in [x / 100.0 for x in range(0, 10, 2)]:
                                for p1 in [x / 100.0 for x in range(0, 10, 2)]:
                                    for ksi1 in [x / 100.0 for x in range(0, 10, 2)]:
                                        for s1 in [x / 100.0 for x in range(0, 10, 2)]:
                                            i += 1
                                            print(str(i) + "\r")
                                            try:
                                                A = np.mat([[df1_du1(u1, v1, p1, ksi1, s1, v),
                                                             df1_dv1(u1, v1, p1, ksi1, s1, v),
                                                             df1_dp1(u1, v1, p1, ksi1, s1, v),
                                                             df1_dksi1(u1, v1, p1, ksi1, s1, v),
                                                             df1_ds1(u1, v1, p1, ksi1, s1, v)],
                                                            [df2_du1(u1, v1, p1, ksi1, s1, v),
                                                             df2_dv1(u1, v1, p1, ksi1, s1, v),
                                                             df2_dp1(u1, v1, p1, ksi1, s1, v),
                                                             df2_dksi1(u1, v1, p1, ksi1, s1, v),
                                                             df2_ds1(u1, v1, p1, ksi1, s1, lam, phi)],
                                                            [df3_du1(beta), df3_dv1(beta), df3_dp1(), df3_dksi1(),
                                                             df3_ds1()],
                                                            [df4_du1(), df4_dv1(), df4_dp1(), df4_dksi1(), df4_ds1()],
                                                            [df5_du1(u1, v1, p1, ksi1, s1, B, lam, gamma1),
                                                             df5_dv1(u1, v1, p1, ksi1, s1, v),
                                                             df5_dp1(u1, v1, p1, ksi1, s1, v),
                                                             df5_dksi1(u1, v1, p1, ksi1, s1, v),
                                                             df5_ds1(u1, v1, p1, ksi1, s1, lam, lam / v)]
                                                            ])
                                                w, v = np.linalg.eig(A)
                                                print(w)
                                                if w[0].real < 0 and w[1].real < 0 and w[2].real < 0 and w[
                                                    3].real < 0 and w[4].real < 0:
                                                    with open("result.txt", "w") as f:
                                                        f.write("----------------------\n")
                                                        f.write("lambda = " + str(lam) + "\n")
                                                        f.write("B = " + str(B) + "\n")
                                                        f.write("gamma = " + str(gamma) + "\n")
                                                        f.write("v = " + str(v) + "\n")
                                                        f.write("beta = " + str(beta) + "\n")
                                                        f.write("u1 = " + str(u1) + "\n")
                                                        f.write("v1 = " + str(v1) + "\n")
                                                        f.write("p1 = " + str(p1) + "\n")
                                                        f.write("ksi1 = " + str(ksi1) + "\n")
                                                        f.write("s1 = " + str(s1) + "\n")
                                            except:
                                                continue

