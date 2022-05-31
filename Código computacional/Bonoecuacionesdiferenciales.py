"""
Nombre: Alejandro Ruiz Salazar
Código: 202013520
Correo: a.ruiz2@uniandes.edu.co
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

"""
Datos constantes
"""

b_a = 0.1
m = 1
b = 30
g = 9.8
k = 101006.5

"""
Funciones transformadas a un sistema de ecuaciones y' = -(b_a/m)*y - g & y'= -(k/m)*x.
"""

def CaídaLibre(v,t):
    x,y = v
    return [y, -((b_a/m)*y)-g]

def MasaResorte(v,t):
    x,y=v
    return [y, -((k/m)*x)-((b/m)*y)-g]

"""
Se crea una función la cual tenga el objetivo de buscar el punto en el que x se vuelva negativo para el caso
de caída libre y el punto en el que x se vuelva positivo en el caso de masa-resorte.
"""

def busquedatparax0(fun,ci,t0,tf,funcion,lista):
    lapsus = 100000
    tiempo = np.linspace(t0,tf,lapsus)
    solucion = integrate.odeint(fun,ci,tiempo)
    centinela = True
    i = 0
    while centinela == True:
        if i < lapsus:
            if funcion == 'CaidaLibre':
                if float(solucion[i][0]) <= 0 and float(solucion[i][1]) < 0:
                    nuevot0 = tiempo[i]
                    nuevoci = [float(solucion[i][0]),float(solucion[i][1])]
                    x = nuevoci[0]
                    v = nuevoci[1]
                    lista.append((nuevot0,x,v))
                    centinela = False
            else:
                if float(solucion[i][0]) > 0 and float(solucion[i][1]) > 0:
                    nuevot0 = tiempo[i]
                    nuevoci = [float(solucion[i][0]),float(solucion[i][1])]
                    x = nuevoci[0]
                    v = nuevoci[1]
                    lista.append((nuevot0,x,v))
                    centinela = False
        else:
            centinela = False
        i += 1
    return lista[-1]

"""
Funciones para agregar las posiciones, velocidades y tiempo para graficar.
"""

def x(sol,lista):
    for i in range(len(sol)):
        lista.append(sol[i][0])
    return lista

def v(sol,lista):
    for i in range(len(sol)):
        lista.append(sol[i][1])
    return lista

def t(t,lista):
    for i in range(len(t)):
        lista.append(t[i])
    return lista

"""
Función recursiva que busca los x que cumplan con los requisitos anteriormente mencionados, luego se van
guardando en una lista de posiciones, velocidades y tiempo para poder ser graficados. 
Este proceso funciona perfectamente hasta que se itera 7 veces ya que aparece un error, sin embargo, con 
6 iteraciones se logra ver el efecto buscado.
"""

def coordenadas(fun1,fun2,inicioiteraciones,finaliteraciones,ci,to,tf,posicion,velocidad,tiempo):
    if inicioiteraciones != finaliteraciones:
        inicioiteraciones += 1
        t1,x1,v1 = busquedatparax0(fun1, ci, to, tf,'CaidaLibre',lista=[])
        cicaidalibre = [x1,v1]
        tiempocaidalibre = np.linspace(to,t1,100000)
        solcaidalibre = integrate.odeint(fun1,ci,tiempocaidalibre)
        x(solcaidalibre,posicion)
        v(solcaidalibre,velocidad)
        t(tiempocaidalibre,tiempo)
        t2,x2,v2 = busquedatparax0(fun2, cicaidalibre, t1, tf, 'MasaResorte',lista=[])
        cimasaresorte = [x2,v2]
        tiempomasaresorte = np.linspace(t1,t2,100000)
        solmasaresorte = integrate.odeint(fun2,cicaidalibre,tiempomasaresorte)
        x(solmasaresorte,posicion)
        v(solmasaresorte,velocidad)
        t(tiempomasaresorte,tiempo)
        coordenadas(fun1,fun2,inicioiteraciones,finaliteraciones,cimasaresorte,t2,tf,posicion,velocidad,tiempo)
    return posicion,velocidad,tiempo

"""
Finalmente, se muestran las iteraciones, las condiciones iniciales del problema y se grafica.
"""

iteraciones = 6
condicionesiniciales = [10,0]
posiciontotal,velocidadtotal,tiempototal = coordenadas(CaídaLibre,MasaResorte,0,iteraciones,condicionesiniciales,0,10,posicion=[],velocidad=[],tiempo=[])

plt.plot(tiempototal,velocidadtotal,'-.',color='red')
plt.legend(['Velocidad'],fontsize=13)
plt.plot(tiempototal,posiciontotal,color='darkblue')
plt.title('Posición contra tiempo',fontsize=14)
plt.xlabel('Tiempo (s)',fontsize=14)
plt.ylabel('Posición (m)',fontsize=14)
plt.grid()

