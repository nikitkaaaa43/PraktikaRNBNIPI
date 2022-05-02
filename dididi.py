import numpy as np
import math
def df1_du1(u1,u2):
    return -1

def df1_du2(u1,u2):
    return -2

def df2_du1(u1,u2):
    return 2-3*math.pow(u1,2)

def df2_du2(u1,u2):
    return -1

if __name__ == "__main__":
    i = 0
    for u1 in [x / 100.0 for x in range(0, 100, 5)]:
        for u2 in [x / 100.0 for x in range(0, 100, 5)]:
            i += 1
            print(str(i) + "\r")
            try:
                A = np.mat([[df1_du1(u1, u2),
                             df1_du2(u1, u2)],
                            [df2_du1(u1, u2),
                             df2_du2(u1, u2)]])
                w, v = np.linalg.eig(A)
                print(w)
                if w[0].real < 0 and w[1].real < 0:
                    with open("result.txt", "w") as f:
                        f.write("----------------------\n")
                        f.write("u1 = " + str(u1) + "\n")
                        f.write("u2 = " + str(u2) + "\n")
            except:
                continue

