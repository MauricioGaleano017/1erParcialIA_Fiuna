import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Función para calcular los coeficientes de regresión manualmente
def regresion_manual(X, y):
    # Agregar una columna de unos para el término independiente
    X = np.c_[np.ones((len(X),1)),X]
    
    # Calcular los coeficientes utilizando la fórmula de la pseudo inversa
    coeficientes = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)

    return coeficientes  

# Función para predecir los valores de y
def predecir(X, coeficientes):
    Xm =  np.c_[np.ones((len(X),1)),X]# completar con lo mismo de la linea 7
    
    return  Xm@coeficientes
# Calcular métricas de evaluación manualmente
def rmse(y_true, y_pred):
    error=y_true-y_pred
    return np.sqrt(np.mean((error) ** 2))

def r2F(y_true, y_pred):
   # https://es.wikipedia.org/wiki/Coeficiente_de_determinaci%C3%B3n
   
    numerador = ((y_true - y_pred)**2).sum()
    denominador = ((y_true - y_true.mean()) ** 2).sum()
    return 1 - (numerador / denominador)
    
    # Función para ajustar el modelo y evaluarlo

def ajustar_evaluar_modelo(X, y):
    coeficientes = regresion_manual(X, y)
    y_pred = predecir(X, coeficientes)
    r2_ = r2F(y,y_pred)#completar
    rmse_val = rmse(y, y_pred)#completar
    return coeficientes, y_pred, r2_, rmse_val



opcion=int(input())
# Cargar los datos
path=r'C:\Users\magal\OneDrive\Documents\IA\Mediciones.csv'
data = pd.read_csv(path)
data.dropna(inplace=True)
# Definir las columnas de características (X) y la columna de objetivo (y)
if opcion==1:
    #imprimir numero de filas y numero de columnas
    print(np.shape(data))
    
    #seleccionar las caracteristicas(variables dependientes) y el objetivo
    caracteristicas =[PEEP , BPM , Volumen ,   VTI,    VTE,  VTI_F,  VTE_F,  PEEPV] #[completar]
    objetivo =[Pasos] #
    
    print(caracteristicas)
    print(objetivo)
elif opcion==2: 
    # modelo completo solo con VTI_F, completar la funcion regresion manual
    
    X = data['VTI_F']
    y = data['Pasos']
    coef =[regresion_manual(X, y)]# regresion_manual(X, y)
    print(coef)
elif opcion==3: 
    # modelo completo solo con VTI_F, completar las funciones que definen las métricas
    X = data['VTI_F']
    y = data['Pasos']
    coef = regresion_manual(X, y)
    print( coef)
    y_pred = predecir(X,coef)
    r2_ = r2F(y, y_pred)
    rmse_val = rmse(y, y_pred)
    # imprimir los primeros 2 elementos de y e y_pred
    #  print(y[:3],  y_pred [COMPLETAR])
    print(y[:3],  y_pred [:3])
    # imprimir r2 y rmse
    print(r2_,  rmse_val )
elif opcion==4: 
    # modelo completo solo con VTI_F, completar la función ajustar_evaluar_modelo
    X_todo =[]  #data[completar]
    y =[] # data[completar]
    coeficientes_todo, y_pred_todo, r2_todo, rmse_todo = ajustar_evaluar_modelo(X_todo, y)
    print(r2_todo, rmse_todo)
elif opcion==5:
   # Completar la combinaciones de características de los modelos solicitados 
    models = {
        'Modelo_1': ['VTI_F'],
        'Modelo_2': ['VTI_F', 'BPM'],
        'Modelo_3': ['VTI_F', 'PEEP'],
        'Modelo_4': ['VTI_F', 'PEEP','BPM'],
        'Modelo_5': ['VTI_F', 'PEEP','BPM','VTE_F']
    }
    for nombre_modelo, lista_caracteristicas in models.items():
        X = data[lista_caracteristicas]
        y = data['Pasos']
        coeficientes, y_pred, r2, rmse_val = ajustar_evaluar_modelo(X, y)
        print(nombre_modelo,r2, rmse_val)
elif opcion==6:
    # Modelos para cada combinación de PEEP y BPM
    valores_peep_unicos = np.unique(data['PEEP'])
    valores_bpm_unicos = np.unique(data['BPM'])

    print(valores_peep_unicos)
    print(valores_bpm_unicos)

    predicciones_totales = []
    for peep in valores_peep_unicos:
        for bpm in valores_bpm_unicos:

            datos_subset = data[(data['BPM'] == bpm) & (data['PEEP'] == peep)] # Filtrado de datos para cada par de PEEP y BPM
            # Completar el resto del código para ajustar el modelo y obtener la predicción
           
            X_subset = datos_subset[['VTI_F']]
            y_subset = datos_subset['Pasos']
            coeficientes_subset, y_pred_subset, r2_subset, rmse_subset = ajustar_evaluar_modelo(X_subset, y_subset)
            print(peep, bpm, r2_subset, rmse_subset)
            predicciones_totales.append(y_pred_subset)
            string = "BPM: "
            number = bpm
            result = string + str(number)
            string = "PEEP: "
            number = peep
            result = string + str(number)+result
            plt.plot(X_subset,y_subset, "o",label=result)
            Xi=np.linspace(200, 600, 1000)
            plt.plot(Xi, coeficientes_subset[0]+coeficientes_subset[1]*Xi, "k-")
            plt.xlabel('VTI_F')
            plt.ylabel('Pasos')
            plt.legend()
            

           
#plt.plot(X, Y, "bo")

#plt.plot(Xi, mejor_ajuste[0]+mejor_ajuste[1]*Xi+mejor_ajuste[2]*Xi*Xi+mejor_ajuste[3]*Xi*Xi, "r")
#plt.xlabel("$x$", fontsize=18)
#plt.ylabel("$y$", rotation=0, fontsize=18)
#plt.axis([-3, 3, 0, 10])
#plt.show()
#plt.show()
predicciones_concatenadas = np.concatenate(predicciones_totales)
y=data['Pasos']
r2_global = r2F(y, predicciones_concatenadas)
rmse_global = rmse(y, predicciones_concatenadas)
print('Global', r2_global, rmse_global)
