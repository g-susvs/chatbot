import pandas as pd
import numpy as np

# Clasificar Pokemons por sus niveles de Ataque y Defensa
# 1 para Bueno, 0 para Malo
info = {
    "Ataque": [0.80, 0.70, 0.10, 0.20, 0.95, 0.6, 0.12, 0.30],
    "Defensa": [0.80, 0.90, 0.10, 0.30, 0.99, 0.7, 0.30, 0.30],
    'Target': [1, 1, 0, 0, 1, 1, 0, 0]
}

data = pd.DataFrame(info)
n_inputs = 2
weights = np.random.rand(n_inputs)
print(data)
print(weights)



bias = 0.5
l_rate = 0.1
epochs = 1000 # iteraciones
epoch_loss = []

def get_weighted_sum(feature, weights, bias):
    return np.dot(feature, weights) + bias

def sigmoid(w_sum):
    return 1/(1+np.exp(-w_sum))

def cross_entropy(target, prediction):
    return -(target * np.log10(prediction) + (1 - target) * np.log10(1 - prediction))


def update_weights(weights, l_rate, target, prediction, feature):
    new_weights = []
    for x, w in zip(feature, weights):
        new_w = w + l_rate * (target - prediction) * x
        new_weights.append(new_w)
    return new_weights

def update_bias(bias, l_rate, target, prediction):
    return bias + l_rate*(target-prediction)

def train_model(data, weights, bias, l_rate, epochs):
    print("Primeros pesos: ", weights)

    # Iterar en un rango de epocas
    for e in range(epochs):   
         # Crear lista para Perdida                                                      
        individual_loss = [] 

        # itera sobre un número determinado de épocas (iteraciones) especificado por el argumento epochs.                                                      
        for i in range(len(data)):        
            # Extrae las características (atributos) de un ejemplo de entrenamiento, excluyendo el último elemento, que generalmente se asume que es la etiqueta (target) del ejemplo.                                          
            feature = data.loc[i][:-1]     
            # Obtiene la etiqueta (target) del ejemplo de entrenamiento.                                         
            target = data.loc[i][-1]     
            # Calcula la suma ponderada de las características utilizando la función get_weighted_sum, que probablemente es una función que realiza la multiplicación de características y pesos y luego suma el sesgo (bias).                                           
            w_sum = get_weighted_sum(feature, weights, bias)        
            # Calcula una predicción utilizando una función sigmoide en la suma ponderada.                
            prediction = sigmoid(w_sum)  
            # Calcula la pérdida (loss) utilizando una función de pérdida de entropía cruzada entre la etiqueta real y la predicción.                                           
            loss = cross_entropy(target, prediction)       
             # Agrega la pérdida individual al conjunto de pérdidas para este ejemplo.                         
            individual_loss.append(loss)                                           

            # gradient descent
            # Calcula la pérdida media para todas las pérdidas individuales en esta época.
            weights = update_weights(weights, l_rate, target, prediction, feature)  
            # Actualiza el valor del sesgo en un modelo de aprendizaje automático utilizando una regla de actualización basada en el descenso de gradiente y los valores de predicción y objetivo
            bias = update_bias(bias, l_rate, target, prediction)                    

        # Calcula la pérdida media para todas las pérdidas individuales en esta época.
        mean_loss = sum(individual_loss)/len(individual_loss)                       
        # Agrega la pérdida media de esta época a una lista llamada epoch_loss, que probablemente se utiliza para rastrear la evolución de la pérdida durante el entrenamiento.
        epoch_loss.append(mean_loss)                                                

    print("Nuevos pesos: ", weights)
    print("Nuevo bias: ", bias)
    return weights, bias

uWeights, uBias = train_model(data, weights, bias, l_rate, epochs)     

# utiliza la biblioteca Matplotlib en Python para crear un gráfico de líneas que muestra la evolución de la pérdida (loss) durante el entrenamiento del modelo
import matplotlib.pyplot as plt                                                     
plt.plot(epoch_loss)


def load_weights(): return uWeights
def load_bias(): return uBias
## =========== Función para probar el modelo entrenado ============
def test(inputs, update_weights, update_bias):
    w_sum = get_weighted_sum(inputs, update_weights, update_bias)
    prediction = sigmoid(w_sum)
    return prediction


# Valores para probar
new_inputs = [0.70, 0.65]
predicted_output = test(new_inputs, uWeights, uBias)

if predicted_output < 0.5:
  print("Clasificación: Bajo nivel :(" )
else:
  print("Clasificación: Buen nivel ;)" )

print("Predicción:", predicted_output)


