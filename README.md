Simulación de Procesos en un Sistema Operativo
Este código en Python simula la ejec

ución de procesos en un sistema operativo mediante la biblioteca SimPy. La simulación representa la ejecución de procesos que requieren acceso a la CPU y la memoria RAM, con posibles interrupciones y decisiones post-ejecución.

Configuración y Parámetros
Capacidad de RAM: 200 (puede ser ajustado)
Velocidad del CPU: 2 (puede ser ajustado)
Número total de procesos a simular: 200 (puede ser ajustado)
Intervalo de tiempo entre la creación de cada proceso: 10 (puede ser ajustado)
Número de instrucciones que se pueden ejecutar en un ciclo de CPU: 3 (puede ser ajustado)
Funciones Principales
process: Simula la ejecución de un proceso, solicitando acceso a la RAM y CPU, ejecutando instrucciones y manejando posibles interrupciones.

generate_processes: Genera procesos durante la simulación, especificando la cantidad de memoria y el número de instrucciones necesarios para cada uno.

save_times_to_csv: Guarda los tiempos de inicio y finalización de los procesos en un archivo CSV, calcula el tiempo total de ejecución para cada proceso y devuelve estadísticas como el tiempo promedio y la desviación estándar.

Ejecución de la Simulación
Se configuran los recursos del sistema (CPU y RAM) y se ejecuta la simulación de la generación de procesos.

Se guarda la información de tiempo en un archivo CSV con marca de tiempo para evitar sobreescrituras.

Se muestran estadísticas como el tiempo promedio y la desviación estándar.

Se grafica la distribución de los tiempos de ejecución de los procesos.

Cómo Ejecutar
Ajusta los parámetros de configuración según sea necesario.
Ejecuta el script en un entorno de Python.
Requisitos
Python
Bibliotecas: SimPy, NumPy, Matplotlib
Notas
Este código es una simulación simplificada y puede requerir ajustes según los requisitos específicos de la simulación deseada.
La simulación incluye mensajes de salida para comprender la secuencia de eventos durante la ejecución de cada proceso.

Autor
[Creado por: Mario Rocha]

