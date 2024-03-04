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
def proceso(env, nombre, cpu, ram, memoria_necesaria, instrucciones, tiempos_procesos):
    tiempo_inicio = env.now  # Tiempo de inicio del proceso
    print(f'{tiempo_inicio}: El proceso {nombre} creado, necesita {memoria_necesaria} de memoria, instrucciones {instrucciones}')

    # Solicitar RAM (Paso de Nuevo a Listo)
    with ram.get(memoria_necesaria) as solicitud:
        yield solicitud
        print(f'{env.now}: El proceso {nombre} ha obtenido el espacio de memoria y está listo para ser EJECUTADO')

        while instrucciones > 0:
            # Solicitar CPU (Paso de Listo a Ejecutándose)
            with cpu.request() as solicitud_cpu:
                yield solicitud_cpu
                print(f'{env.now}: El proceso {nombre} está siendo EJECUTADO')

                # Ejecutar instrucciones del proceso en un ciclo de CPU
                yield env.timeout(1)  # Representa un ciclo de CPU
                instrucciones -= min(INSTRUCCIONES_POR_CICLO, instrucciones)
                print(f'{env.now}: El proceso {nombre} ha ejecutado instrucciones, faltan {instrucciones}')

                if instrucciones <= 0:
                    print(f'{env.now}: El proceso {nombre} ha TERMINADO')
                    break
                else:
                    # Simular posibles esperas por I/O o decisiones post-ejecución
                    siguiente_paso = random.randint(1, 21)
                    if siguiente_paso == 1:
                        # Simular espera por I/O
                        print(f'{env.now}: El proceso {nombre} va a ESPERA por I/O')
                        yield env.timeout(1)  # Simular tiempo de espera por I/O
                        print(f'{env.now}: El proceso {nombre} vuelve a LISTO después de I/O')
                    elif siguiente_paso == 2:
                        print(f'{env.now}: El proceso {nombre} vuelve a LISTO sin I/O')
                    # Si siguiente_paso no es ni 1 ni 2, el proceso intentará volver a listo en el próximo ciclo sin una acción explícita aquí

    # Liberar RAM y registrar tiempo de finalización
    yield ram.put(memoria_necesaria)
    tiempo_fin = env.now  # Registrar tiempo de finalización
    tiempos_procesos.append([nombre, tiempo_inicio, tiempo_fin])  # Añadir tiempos al registro
    print(f'{env.now}: El proceso {nombre} ha liberado su memoria')
    yield ram.put(memoria_necesaria)
    tiempo_fin = env.now  # Registrar tiempo de finalización
    tiempos_procesos.append([nombre, tiempo_inicio, tiempo_fin])
    ram_log.append([tiempo_fin, 'LIBRE'])
    print(f'{env.now}: El proceso {nombre} ha liberado su memoria')

def proceso(env, nombre, cpu, ram, memoria_necesaria, instrucciones, tiempos_procesos, cpu_log, ram_log):
    tiempo_inicio = env.now  # Tiempo de inicio del proceso
    cpu_log.append([tiempo_inicio, 'EJECUTANDO'])
    ram_log.append([tiempo_inicio, 'EN USO'])

# Función para generar procesos durante la simulación
def generar_procesos(env, cpu, ram, tiempos_procesos):
    for i in range(NUM_PROCESOS):
        memoria_necesaria = random.randint(1, 10)
        instrucciones = random.randint(1, 10)
        env.process(proceso(env, f'Proceso {i}', cpu, ram, memoria_necesaria, instrucciones, tiempos_procesos))
        yield env.timeout(random.randint(1, INTERVALO))
def generar_procesos(env, cpu, ram, tiempos_procesos, cpu_log, ram_log):
    for i in range(NUM_PROCESOS):
        memoria_necesaria = random.randint(1, 10)
        instrucciones = random.randint(1, 10)
        env.process(proceso(env, f'Proceso {i}', cpu, ram, memoria_necesaria, instrucciones, tiempos_procesos, cpu_log, ram_log))
        yield env.timeout(random.randint(1, INTERVALO))

# Función para guardar los tiempos en un archivo CSV
def guardar_tiempos_a_csv(tiempos, nombre_archivo):
    df = pd.DataFrame(tiempos, columns=['Proceso', 'Tiempo de inicio', 'Tiempo final'])
    df.to_csv(nombre_archivo, index=False)


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


# Registrar tiempos de procesos y logs de CPU y RAM
tiempos_procesos = []
cpu_log = []  # Registro de estados de la CPU
ram_log = []  # Registro de estados de la RAM

# Configuración del entorno de simulación y recursos
env = simpy.Environment()
cpu = simpy.Resource(env, capacity=VELOCIDAD_CPU)
ram = simpy.Container(env, init=CAPACIDAD_RAM, capacity=CAPACIDAD_RAM)
env.process(generar_procesos(env, cpu, ram, tiempos_procesos))
env.run()

# Crear el nombre de archivo CSV con una marca de tiempo para evitar sobrescrituras
nombre_archivo_tiempos = f'tiempos_{NUM_PROCESOS}_procesos_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'
nombre_archivo_cpu = f'datos_cpu_{NUM_PROCESOS}_procesos_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'
nombre_archivo_ram = f'datos_ram_{NUM_PROCESOS}_procesos_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'

# Guardar datos en archivos CSV
guardar_tiempos_a_csv(tiempos_procesos, nombre_archivo_tiempos)
guardar_datos_cpu(cpu_log, nombre_archivo_cpu)
guardar_datos_ram(ram_log, nombre_archivo_ram)

# Mostrar estadísticas
df = pd.DataFrame(tiempos_procesos, columns=['Proceso', 'Tiempo de inicio', 'Tiempo final'])
df['Duracion'] = df['Tiempo final'] - df['Tiempo de inicio']
tiempo_promedio = df['Duracion'].mean()
desviacion_estandar_tiempo = df['Duracion'].std()

print(f"Tiempo promedio: {tiempo_promedio}, Desviación Estándar: {desviacion_estandar_tiempo}")
