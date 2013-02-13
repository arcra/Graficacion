******************************
*  Adrián Revuelta Cuauhtli	 *
* -------------------------  *
*  Tarea 2					 *
******************************

Sobre la tarea
---------------
Se generan dos ventanas:
- La primera dibuja un fondo negro y 3 puntos blancos (ensanchados, en realidad dibuja 9 puntos juntos en un cuadro de 3x3) formando un triángulo.
- La segunda dibuja el mismo triángulo (los vértices) pero rotado sobre su centro 30°.

El código incluye:
- Función: multiplyMatrices - multiplicación de matrices
- Función: getTransformationMatrix - obtiene una matriz de transformación que puede incluir un escalamiento, rotación y traslación al mismo tiempo.
- Clase: arcCanvasWindow - extiende la clase QWidget de la librería Qt, y es la que se utiliza para dibujar
- Clase: arcPoint - se utiliza para que cada CanvasWindow almacene los puntos que tiene que dibujar y de qué color.

Para rotar el triángulo sobre su centro, para cada vértice del triángulo, se traslada al origen con respecto al centro del triángulo y después se rota, se traslada nuevamente y se agrega a la ventana de imagen rotada.

Para hacer las transformaciones se puede especificar un ángulo, un desplazamiento en x, un desplazamiento en y, un factor de escalamiento en x y un factor de escalamiento en y, con los que se obtiene la matriz de transformación (en 2D) y se multiplica por el vector de posición para encontrar la nueva posición.



Sobre el "ejecutable"
---------------------
+ Lenguaje: Python
+ Intérprete de desarrollo: Python 2.7
+ Dependencias: PyQt 4 (python-qt4)
+ Plataforma de desarrollo: Ubuntu/Linux (Debería funcionar en cualquier ambiente con intérprete de python, Qt y PyQt instalados, probablemente ya estén instalados en muchas distribuciones de linux y/o macOS)

Instrucciones para ejecutar
----------------------------
En un ambiente con python, Qt y PyQt instalados, ejecutar el siguiente comando en consola, desde la ubicación del archivo fuente (asumiendo que la ubicación del intérprete está incluido en la variable de ambiente que especifica dónde buscar programas):

python Tarea2.py


Referencias
----------------
+ Refencia sobre Qt:
	http://pyqt.sourceforge.net/Docs/PyQt4/classes.html
