import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def rotX(angle):
    return np.matrix([
        [1, 0, 0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ])

def rotY(angle):
    return np.matrix([
        [math.cos(angle), 0, math.sin(angle)],
        [0, 1, 0],
        [-math.sin(angle), 0, math.cos(angle)]
    ])

def rotZ(angle):
    return np.matrix([
        [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ])

l1 = 1
l2 = 1
l3 = 1
alfa = math.pi / 8 # 22.5'

pointAprim = np.matrix([0, 0, 0]).transpose()
pointBprim = np.matrix([l1, 0, 0]).transpose()
pointCprim = np.matrix([l2, 0, 0]).transpose()
pointDprim = np.matrix([l3, 0, 0]).transpose()

gamma2 = np.linspace(0, np.pi, 180)

def calcBeta(gamma):
    if gamma == 0: return 0
    #if gamma == 0: return -math.pi/2
    tempD = rotZ(alfa) * rotX(gamma) * rotZ(-alfa) * ((rotZ(-alfa) * rotX(-gamma) * rotZ(alfa) * pointDprim) + pointCprim) + pointBprim
    return -math.pi / 2 - math.atan2(tempD[2][0].item(), tempD[1][0].item())
    #return -math.atan2(tempD[2][0].item(), tempD[1][0].item()) - math.pi

betas = []

for i in gamma2:
    betas.append(calcBeta(i))

betas = np.asarray(betas)

print(betas * 180 / np.pi + 90)
#for i in range(0, 180, 9): print(betas[i] * 180 / np.pi + 90)

def func(x, a, b, c):
    #return a * np.exp(-b * x) + c
    return a * np.power(x, 2) + b * x + c

popt, pcov = curve_fit(func, gamma2, betas)

print(popt)
print("optimized function in radians: %1.5f * x^2 + %1.5f * x + %1.5f"% (popt[0], popt[1], popt[2]))


plt.plot(gamma2 * 180 / np.pi, betas * 180 / np.pi + 90, label='calculated values')
plt.plot(gamma2 * 180 / np.pi, func(gamma2, *popt) * 180 / np.pi + 90, 'r--', label='approximated values')
plt.xlabel("gamma2 angle")
plt.ylabel("beta angle")
plt.legend()
plt.show()