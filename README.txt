#Adamo Calibrator

Explicación del problema

##Funcionamiento
El funcionaiento del calibrador puede ser dividido en tres etapas:
El handshake, es la primer etapa de calibración esta consiste en
El intercambio de datos de los clics
Y por úlitmo está el proceso de calibración.

>    DIAGRAMA DE CALIBRACION

###Primer etapa
En esta etapa el calibrador recibe la resolución de la pantalla. Ésta es dividida en n^2 bloques (definidos en el calibrador) por medio del siguiente cálculo:

>`` BloqueX = Ancho / nbloques``

>`` BloqueY = Alto / nbloques``


El cálculo anterior permite establecer una ubicación fija de los puntos, los cuales van a ser utilizados en la calibracion, independientemente de la resolución del sistema.
Por defecto el calibrador divide la pantalla en 64 bloques, 8 por cada eje, y localiza los puntos tal como se muestra la imagen.

>    IMAGEN DE LOS PUNTOS Y DELTA X/Y

----------------------------------

###Segunda etapa
En esta etapa el calibrador recibe los clicks de los usuarios. Además determina si éstos son válidos y debido a que los clicks realizados por el usuario pueden no estar en la misma posición que los registrados por el controlador del calibrador realiza una comprobación de los ejes para determinar si se deben invertir los ejes X y/o Y, y además cambiar el eje X por el Y y viceversa.

####Tipos de Clicks
Los tipos de clicks que el calibrador puede detectar son los siguientes:

* Los **clicks desplazados**: La comprobación de éste tipo de click se realiza una vez que se registró el primer click válido realizado por el usuario. La comprobación consiste en calcular la distancia entre cada una de las coordenadas del último click recibido con respecto a ambas coordenadas de cada uno de los clicks almacenados como válidos previos. Si esta distancia de ambas coordenadas del nuevo click es superior a un umbral definido, se determina que este click fue inválido y se solicita al usuario que realize el click nuevamente.

* Los **clicks dobles**: Al igual que con los **clicks desplazados** la comprobación de éste tipo de clicks se realiza una vez almacenado el primer click válido. Ésta comprobación consiste en verificar que el último click realizado por el usuario no esté localizado dentro de un radio definido de cualquiera de los otros clicks almacenados previamente.

* Los **clicks válidos**: Si no se detectó ninguno de los anteriores clicks o la lista de clicks registrado está vacia, el último click recibido se lo registra como válido.

>    IMAGEN DE TIPOS DE CLICK


####Comprobación y corrección de ejes
Esta comprobación se realiza una vez que se registra el primer click válido y consiste en verificar si el click dada la posición del puntero calculada en el primer paso coincide con la posicion esperada del click. Ésta posicion se reduce para simplificar al concepto de cuadrantes en matemática, realizando una transformación y trasladando la posicion (0, 0) del eje de coordenadas a la mitad de la pantalla dividiendo así la pantalla en cuatro grandes áreas y calculando en que cuadrante deberia estar el click y en que cuadrante se registró el click.

>    IMAGEN DE CUADRANTES

El cálculo de los cuadrantes se lo define como la siguiente función en python.
``` python
def quadrant(width, height, x, y):
    x_middle = width / 2
    y_middle = height / 2
    if (x - x_middle) > 0 and (y - y_middle) > 0:
        quadrant = 1
    elif (x - x_middle) < 0 and (y - y_middle) > 0:
        quadrant = 2
    elif (x - x_middle) < 0 and (y - y_middle) < 0:
        quadrant = 3
    elif (x - x_middle) > 0 and (y - y_middle) < 0:
        quadrant = 4

    return quadrant
```
Cabe destacar que en el código no se utiliza la igualdad ya que los puntos previamente fueron verificados como válidos y no se va a dar el caso nunca de que estén posicionados en el medio del eje de coordenadas.

Una vez realizado esto se pueden dar diversos casos. Debajo se muestran unos ejemplos para aclarar el problema.

* El click fué registrado en el cuadrante 1, pero lo esperaba en el cuadrante 2. En éste caso se debe invertir el eje X para que el punto coincida con el esperado.
* El click fué registrado en el cuadrante 1, pero se lo esperaba en el cuadrante 4. En éste otro caso se debe invertir el eje Y para obtener el resultado esperado.
* Por último el click fué registrado en el cuadrante 1, pero se lo esperaba en el cuadrante 3. En éste último caso se deben invertir ambos ejes para obtener el resultado esperado.

----------------------------------

###Tercer Etapa

Esta útlima etapa consiste en la calibración, para calcular los nuevos valores se utiliza un esquema de dos constantes. Este esquema permite corregir problemas de alineacion de los ejes X e Y, y además problemas de escalas entre la resolución de la pantalla y el controlador del touchscreen, pero no permite corregir desperfectos de rotación de la pantalla.

El procedimiento consiste en transformar las coordenadas recibidas por el controlador del touchscreen en las coordenadas de la pantalla por medio de la multiplicación de dos constantes tal como se muestra en las siguientes fórmulas:

> `` Y' = aY + b ``

> `` X' = cX + d ``

Donde:
* X': es la coordenada en x de la pantalla.
* Y': es la coordenada en y de la pantalla.
* X: es la coordenada en x del controlador del touchscreen.
* Y: es la coordenada en y del controlador del touchscreen.
* a, b, c, d: son constantes.
