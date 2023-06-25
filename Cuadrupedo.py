import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits import mplot3d
from matplotlib import cm
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig, ax = plt.subplots()
plt.subplots_adjust(left = 0, bottom = 0.33, right =1, top = 1)
ax = plt.axes(projection = "3d")
def matriz_rotacionz(grados):
	rad = grados/180*np.pi
	rotacion = np.array([[np.cos(rad),-np.sin(rad),0,0],
						[np.sin(rad), np.cos(rad),0,0],
						[		   0,           0,1,0],
						[0,			0,		0,		1]])
	return rotacion
def matriz_rotacion_x(grados):
	rad = grados/180*np.pi #Convertimos radianes a grados
	#Declaramos la matriz de rotacion x
	rotacion = np.array([[1    ,0                     , 0,0],
					     [0    ,np.cos(rad), -np.sin(rad),0],
			    		 [0    ,np.sin(rad), np.cos(rad), 0],
						 [0	   ,	      0,			0,1]])
	return rotacion
#Creamos la funcion de animacion para rotar la figura en y
def matriz_rotacion_y(grados):
	rad = grados/180*np.pi #Convertimos radianes a grados
	#Declaramos la matriz de rotacion y
	rotacion = np.array([[np.cos(rad), 0, -np.sin(rad),0],
						 [0,           1,            0,0],
						 [np.sin(rad), 0,  np.cos(rad),0],
						 [ 0,		0,		0,			1]])
	return rotacion

def matriz_traslacion_x(x):
	traslacion = np.array([[1,0,0,x],
						  [0,1,0,0],
						  [0,0,1,0],
						  [0,0,0,1]])
	return traslacion

def matriz_traslacion_y(y):
	traslacion = np.array([[1,0,0,0],
						   [0,1,0,y],
						   [0,0,1,0],
						   [0,0,0,1]])
	return traslacion

def matriz_traslacion_z(z):
	traslacion = np.array([[1,0,0,0],
						  [0,1,0,0],
						  [0,0,1,z],
						  [0,0,0,1]])
	return traslacion
def configuracion_grafica():
	plt.title("Lares Illescas Cesar Joaquin\n Cuadrupedo",x =0.4, y = 27)
	ax.set_xlim(-12,12)
	ax.set_xlabel("x")
	ax.set_ylim(-12,12)
	ax.set_ylabel("y")
	ax.set_zlim(-12,12)
	ax.set_zlabel("z")
	ax.view_init(elev=25,azim=30)
	x = [0,1]
	y = [0,1]
	z = [0,1]
	#Para crear la estructura del cuadrupedo
	x1 = [0, 4,4, 0]
	y1 = [0, 0, 8,8]
	z1 = [0, 0, 0, 0]
	vertices = [list(zip(x1,y1,z1))]
	poly = Poly3DCollection(vertices, alpha=0.8, color = 'k')
	ax.add_collection3d(poly)


def sistema_cordenadas_movil(matriz_rotacionz):
	r_11 = matriz_rotacionz[0,0]
	r_12 = matriz_rotacionz[1,0]
	r_13 = matriz_rotacionz[2,0]
	r_21 = matriz_rotacionz[0,1]
	r_22 = matriz_rotacionz[1,1]
	r_23 = matriz_rotacionz[2,1]
	r_31 = matriz_rotacionz[0,2]
	r_32 = matriz_rotacionz[1,2]	
	r_33 = matriz_rotacionz[2,2]

	dx = matriz_rotacionz[0,3]
	dy = matriz_rotacionz[1,3]
	dz = matriz_rotacionz[2,3]
	ax.plot3D([dx,dx+r_11],[dy,dy+r_12],[dz,dz+r_13], color = "m")
	ax.plot3D([dx,dx+r_21],[dy,dy+r_22],[dz,dz+r_23], color = "c")
	ax.plot3D([dx,dx+ r_31],[dy,dy+r_32],[dz,dz+r_33], color = "green")
def dh(theta_i,d_i,a_i,alpha_i):
	MT = A1 = matriz_rotacionz(theta_i)@matriz_traslacion_z(d_i)@matriz_traslacion_x(a_i)@matriz_rotacion_x(alpha_i)
	return MT
def Robot_Cuadrupedo(theta1,d1,a1,alpha1,theta2,d2,a2,alpha2,
			 theta3,d3,a3,alpha3,theta4,d4,a4,alpha4,
			 theta5,d5,a5,alpha5,theta6,d6,a6,alpha6,
			 theta7,d7,a7,alpha7,theta8,d8,a8,alpha8):
	A0 = np.eye(4)
	A_0_1 = dh(theta1,d1,a1,alpha1)
	A_1_2= dh(theta2,d2,a2,alpha2)
	A_0_2 = A_0_1@A_1_2

	#Pata 2
	A1 = np.array([[1, 0, 0, 4],
				  [0, 1, 0, 0],
				  [0, 0, 1, 0],
				  [0, 0, 0, 1]])
	A1_0_1 = dh(theta3,d3,a3,alpha3)
	A1_1_2= dh(theta4,d4,a4,alpha4)
	A1_0_1 = A1@A1_0_1
	A1_0_2 = A1_0_1@A1_1_2
	#Pata 3
	A2 = np.array([[1, 0, 0, 0],
				  [0, 1, 0, 8],
				  [0, 0, 1, 0],
				  [0, 0, 0, 1]])
	A2_0_1 = dh(theta5,d5,a5,alpha5)
	A2_1_2 = dh(theta6,d6,a6,alpha6)
	A2_0_1 = A2@A2_0_1
	A2_0_2 = A2_0_1@A2_1_2
	#Pata 4
	A3 = np.array([[1, 0, 0, 4],
				  [0, 1, 0, 8],
				  [0, 0, 1, 0],
				  [0, 0, 0, 1]])
	A3_0_1 = dh(theta7,d7,a7,alpha7)
	A3_1_2 = dh(theta8,d8,a8,alpha8)
	A3_0_1 = A3@A3_0_1
	A3_0_2 = A3_0_1@A3_1_2
	sistema_cordenadas_movil(A0)
	#sistema_cordenadas_movil(A_0_1)
	#sistema_cordenadas_movil(A_0_2)
	sistema_cordenadas_movil(A1)
	#sistema_cordenadas_movil(A1_0_1)
	#sistema_cordenadas_movil(A1_0_2)
	sistema_cordenadas_movil(A2)
	#sistema_cordenadas_movil(A2_0_1)
	#sistema_cordenadas_movil(A2_0_2)
	sistema_cordenadas_movil(A3)
	#sistema_cordenadas_movil(A3_0_1)
	#sistema_cordenadas_movil(A3_0_2)


	ax.plot3D([A0[0,3],A_0_1[0,3]],[A0[1,3],A_0_1[1,3]],[A0[2,3],A_0_1[2,3]], color="red")
	ax.plot3D([A_0_1[0,3],A_0_2[0,3]],[A_0_1[1,3],A_0_2[1,3]],[A_0_1[2,3],A_0_2[2,3]], color="blue")
	ax.plot3D([A1[0,3],A1_0_1[0,3]],[A1[1,3],A1_0_1[1,3]],[A1[2,3],A1_0_1[2,3]], color="red")
	ax.plot3D([A1_0_1[0,3],A1_0_2[0,3]],[A1_0_1[1,3],A1_0_2[1,3]],[A1_0_1[2,3],A1_0_2[2,3]], color="blue")
	ax.plot3D([A2[0,3],A2_0_1[0,3]],[A2[1,3],A2_0_1[1,3]],[A2[2,3],A2_0_1[2,3]], color="red")
	ax.plot3D([A2_0_1[0,3],A2_0_2[0,3]],[A2_0_1[1,3],A2_0_2[1,3]],[A2_0_1[2,3],A2_0_2[2,3]], color="blue")
	ax.plot3D([A3[0,3],A3_0_1[0,3]],[A3[1,3],A3_0_1[1,3]],[A3[2,3],A3_0_1[2,3]], color="red")
	ax.plot3D([A3_0_1[0,3],A3_0_2[0,3]],[A3_0_1[1,3],A3_0_2[1,3]],[A3_0_1[2,3],A3_0_2[2,3]], color="blue")
	return A_0_2
#Funcion para crear los Sliders que controlaran los grados del robot
def actualizacion_juntas(val):
		ax.cla()
		configuracion_grafica()
		theta_1 = sld_ang_1.val
		theta_2 = sld_ang_2.val
		theta_3 = sld_ang_3.val
		theta_5 = sld_ang_5.val
		theta_7 = sld_ang_7.val
		Robot_Cuadrupedo(theta_1+45,0,4.5,-90,theta_2,0,6,0,
				 theta_3+270,0,4.5,-90,theta_2,0,6,0,
				 theta_5+90,0,4.5,-90,theta_2,0,6,0,
				 theta_7-90,0,4.5,-90,theta_2,0,6,0)
		plt.draw()
		plt.pause(1e-2)
#Aqui ubican las coordenadas donde estaran localizados los sliders
ax1 = plt.axes([0.2,0.25,0.65,0.03])
ax2 = plt.axes([0.2,0.2,0.65,0.03])
ax3 = plt.axes([0.2,0.15,0.65,0.03])
ax5 = plt.axes([0.2,0.1,0.65,0.03])
ax7 = plt.axes([0.2,0.05,0.65,0.03])
#Damos nombre a Sliders y sus rangos
sld_ang_1 = Slider(ax1, "Theta_1 ",0,180,valinit = 131)
sld_ang_2 = Slider(ax2, "Theta_2",-90,90,valinit = 0)
sld_ang_3 = Slider(ax3, "Theta_3",0,180,valinit = 90)
sld_ang_5 = Slider(ax5, "Theta_5",0,180,valinit = 90)
sld_ang_7 = Slider(ax7, "Theta_7",0,180,valinit = 90)
configuracion_grafica()
sld_ang_1.on_changed(actualizacion_juntas)
sld_ang_2.on_changed(actualizacion_juntas)
sld_ang_3.on_changed(actualizacion_juntas)
sld_ang_5.on_changed(actualizacion_juntas)
sld_ang_7.on_changed(actualizacion_juntas)
Robot_Cuadrupedo(176,0,4.5,-90,0,0,6,0,
		 360,0,4.5,-90,0,0,6,0,
		 180,0,4.5,-90,0,0,6,0,
		 0,0,4.5,-90,0,0,6,0)
#plt.draw()
plt.show()