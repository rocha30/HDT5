import csv
import numpy as np
import simpy
import random
import pandas as pd
from datetime import datetime

# Parámetros de configuración
CAPACIDAD_RAM = 100  # Capacidad de la RAM
VELOCIDAD_CPU = 1  # Velocidad del CPU
NUM_PROCESOS = 25  # Número total de procesos a simular
INTERVALO = 10  # Intervalo de tiempo entre la creación de cada proceso
INSTRUCCIONES_POR_CICLO = 3  # Número de instrucciones que se pueden ejecutar en un ciclo de CPU

# Función que simula un proceso en el sistema
def proceso(env, nombre, cpu, ram, memoria_necesaria, instruciones, timepo_proceso):
    tiempo_inicio = env.now # Tiempo de inicio del proceso
    # Mensaje de creación del proceso
    print(f'{tiempo_inicio}: {nombre} creado, necesita {memoria_necesaria} de memoria, instrucciones {instruciones}')
    
     # Solicitar RAM (Paso de New a Ready)
    with ram.get(memoria_necesaria) as request:
        yield request
        # Mensaje indicando que el proceso está listo para ejecutarse
        print(f'{env.now}: {nombre} ha obtenido la memoria necesaria y está en READY')

        # Ciclo para ejecutar todas las instrucciones del proceso
        while instructions > 0:
             # Solicitar uso del CPU (Paso de Ready a Running)
            with cpu.request() as req:
                yield req
                 # Mensaje indicando que el proceso está en ejecución
                print(f'{env.now}: {nombre} está RUNNING')
                
                # Simular ejecución de instrucciones durante un ciclo de CPU
                yield env.timeout(1)  # Representa un ciclo de CPU
                instructions -= min(INSTRUCCIONES_POR_CICLO, instructions)
                 # Mensaje indicando instrucciones restantes
                print(f'{env.now}: {nombre} ha ejecutado instrucciones, restantes {instructions}')

                # Verificar si el proceso ha terminado
                if instructions <= 0:
                    print(f'{env.now}: {nombre} ha TERMINATED')
                    break
                else:
                    # Simular posibles interrupciones o decisiones post-ejecución
                    next_step = random.randint(1, 21)
                    if next_step == 1:
                        # Simulación de espera por I/O
                        print(f'{env.now}: {nombre} entra a WAITING por I/O')
                        yield env.timeout(1)  # Simulación de tiempo de espera por I/O
                        print(f'{env.now}: {nombre} vuelve a READY después de I/O')
                    elif next_step == 2:
                        print(f'{env.now}: {nombre} se dirige nuevamente a READY sin I/O')

    # Liberar RAM y registrar tiempo de finalización
    yield ram.put(memoria_necesaria)
    tiempo_fin = env.now  # Registrar tiempo de finalización
    tiempos_procesos.append([nombre, tiempo_inicio, tiempo_fin])  # Añadir tiempos al registro
    print(f'{env.now}: El proceso {nombre} ha liberado su memoria')
    


# Función para generar procesos durante la simulación
def generar_procesos(env, cpu, ram, tiempos_procesos):
    for i in range(NUM_PROCESOS):
        memoria_necesaria = random.randint(1, 10)
        instrucciones = random.randint(1, 10)
        yield env.process(proceso(env, f'Proceso {i}', cpu, ram, memoria_necesaria, instrucciones, tiempos_procesos, ))
        yield env.timeout(random.randint(1, INTERVALO))


# Función para guardar datos de CPU en un archivo CSV
def guardar_datos_cpu(cpu_log, nombre_archivo):
    df_cpu = pd.DataFrame(cpu_log, columns=['Tiempo', 'Estado'])
    df_cpu.to_csv(nombre_archivo, index=False)

# Función para guardar datos de RAM en un archivo CSV
def guardar_datos_ram(ram_log, nombre_archivo):
    df_ram = pd.DataFrame(ram_log, columns=['Tiempo', 'Estado'])
    df_ram.to_csv(nombre_archivo, index=False)

# Función para guardar tiempos de inicio y finalización en un archivo CSV
def guardar_tiempos_a_csv(tiempos, nombre_archivo):
    df = pd.DataFrame(tiempos, columns=['Proceso', 'Tiempo de inicio', 'Tiempo final'])
    df.to_csv(nombre_archivo, index=False)


# Guardar datos en archivos CSV
def guardar_tiempos_a_csv(tiempos_procesos, nombre_archivo_tiempos):
    with open(nombre_archivo_tiempos, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Proceso','Tiempo de Inicio', 'Tiempo de finalizacion'])
        total_veces = []
        for tiempo in tiempo: 
            writer.writerow(tiempo)
            tiempo_total = tiempo[2]- tiempo[1]
            total_veces.append(tiempo_total)
    avg_tiempo = np.mean(total_veces)
    std_dev_tiempo = np.std(total_veces)
    return avg_tiempo,std_dev_tiempo,total_veces
            
    
# Registrar tiempos de procesos y logs de CPU y RAM
tiempos_procesos = []

# Configuración del entorno de simulación y recursos
env = simpy.Environment()
cpu = simpy.Resource(env, capacity=VELOCIDAD_CPU)
ram = simpy.Container(env, init=CAPACIDAD_RAM, capacity=CAPACIDAD_RAM)
env.process(generar_procesos(env, cpu, ram, tiempos_procesos))
env.run()

# Crear el nombre de archivo CSV con una marca de tiempo para evitar sobrescrituras
nombre_archivo_tiempos = f'tiempos_{NUM_PROCESOS}_procesos_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'
avg_tiempo, std_dev_tiempo, total_veces = guardar_tiempos_a_csv(tiempos_procesos, nombre_archivo_tiempos)

# Mostrar estadísticas
print(f"Tiempo promedio: {avg_tiempo}, Desviación Estándar: {std_dev_tiempo}")
