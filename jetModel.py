import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib.widgets import Slider

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


fig = plt.figure()
ax = plt.axes(projection='3d')

axPos1 = plt.axes([0.2, 0.08, 0.65, 0.03])
axPos2 = plt.axes([0.2, 0.05, 0.65, 0.03])
axPos3 = plt.axes([0.2, 0.02, 0.65, 0.03])
gamma1 = Slider(axPos1, 'Gamma1', 0.0, math.pi, valinit=0)
gamma2 = Slider(axPos2, 'Gamma2', 0.0, math.pi, valinit=0)
gamma3 = Slider(axPos3, 'Gamma3', -math.pi, 0.0, valinit=0)

l1 = 1
l2 = 1
l3 = 1
alfa = math.pi / 8 # 22.5'

pointAprim = np.matrix([0, 0, 0]).transpose()
pointBprim = np.matrix([l1, 0, 0]).transpose()
pointCprim = np.matrix([l2, 0, 0]).transpose()
pointDprim = np.matrix([l3, 0, 0]).transpose()

pointA = np.matrix([0, 0, 0]).transpose()
pointB = np.matrix([l1, 0, 0]).transpose() + pointA
pointC = np.matrix([l2, 0, 0]).transpose() + pointB
pointD = np.matrix([l3, 0, 0]).transpose() + pointC

def draw(A, B, C, D):
    ax.clear()
    ax.auto_scale_xyz
    theta = np.linspace(0, 2 * np.pi, 201)
    y = 1*np.cos(theta)
    z = 1*np.sin(theta)
    ax.plot(np.zeros(201), y, z)
            
    ax.plot([A[0][0].item(), B[0][0].item()],
            [A[1][0].item(), B[1][0].item()],
            [A[2][0].item(), B[2][0].item()], color = 'r', marker = "o")
    ax.plot([B[0][0].item(), C[0][0].item()],
            [B[1][0].item(), C[1][0].item()],
            [B[2][0].item(), C[2][0].item()], color = 'g', marker = "o")
    ax.plot([C[0][0].item(), D[0][0].item()],
            [C[1][0].item(), D[1][0].item()],
            [C[2][0].item(), D[2][0].item()], color = 'b', marker = "o")

draw(pointA, pointB, pointC, pointD)

def update(val):
    tempA = pointAprim
    tempB = pointBprim + tempA
    #tempC = (rotX(gamma1.val) * rotZ(alfa) * rotX(gamma2.val) * rotZ(-alfa) * pointCprim) + pointBprim
    #tempD = rotX(gamma1.val) * rotZ(alfa) * rotX(gamma2.val) * rotZ(-alfa) * ((rotZ(-alfa) * rotX(gamma3.val) * rotZ(alfa) * pointDprim) + pointCprim) + pointBprim
    tempC = (rotZ(alfa) * rotX(gamma2.val) * rotZ(-alfa) * pointCprim) + pointBprim
    tempD = rotZ(alfa) * rotX(gamma2.val) * rotZ(-alfa) * ((rotZ(-alfa) * rotX(-gamma2.val) * rotZ(alfa) * pointDprim) + pointCprim) + pointBprim
    tempGamma1 = -math.pi / 2 - math.atan2(tempD[2][0].item(), tempD[1][0].item())

    tempC = rotX(tempGamma1) * tempC
    tempD = rotX(tempGamma1) * tempD
    draw(tempA, tempB, tempC, tempD)

gamma1.on_changed(update)
gamma2.on_changed(update)
gamma3.on_changed(update)

plt.show()