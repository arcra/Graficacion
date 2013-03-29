******************************
*  Adrián Revuelta Cuauhtli	 *
* -------------------------  *
*  Tarea 4					 *
******************************

Sobre la tarea
---------------
Se utilizan dos archivos:
- arcGL.py: incluye la API de graficación que estoy desarrollando.
- Tarea4.py: Utiliza el módulo arcGL para hacer lo requerido para la tarea.

El módulo arcGL incluye métodos para hacer transformaciones, cambios de marcos de referencia, multiplicación de matrices, operaciones entre vectores, etc.

En el programa de la Tarea4 define los puntos de las 6 caras que corresponden a un cubo de 2x2x2 (se define cada cara como un polígono con 4 puntos), posiciona la cámara en el punto (4, 3, 3) y rota los puntos y la cámara cada 0.1 seg (en realidad no lo hace tan rápido, porque el render toma mucho tiempo) para desplegarlo en la pantalla.

La iluminación se implementó con el modelo de constantes de luz ambiente, difusa y especular.



Sobre el "ejecutable"
---------------------
+ Lenguaje: Python
+ Intérprete de desarrollo: Python 2.7
+ Dependencias: PyQt 4 (python-qt4)
+ Plataforma de desarrollo: Ubuntu/Linux (Debería funcionar en cualquier ambiente con intérprete de python, Qt y PyQt 4 instalados, probablemente ya estén instalados en muchas distribuciones de linux y/o macOS)

Instrucciones para ejecutar
----------------------------
En un ambiente con python, Qt y PyQt instalados, ejecutar el siguiente comando en consola, desde la ubicación del archivo fuente (asumiendo que la ubicación del intérprete está incluido en la variable de ambiente que especifica dónde buscar programas):

python Tarea4.py

Para correrlos es necesario que estén los dos archivos en el mismo directorio, o bien, exportar la ubicación del módulo arcGL a la variable de ambiente PYTHONPATH.


Referencias
----------------
+ Refencia sobre Qt:
	http://pyqt.sourceforge.net/Docs/PyQt4/classes.html
