import simpy
import random
import csv
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# Parámetros de configuración
RAM_CAPACITY = 100  # Capacidad de la RAM
CPU_SPEED = 1  # Velocidad del CPU
NUM_PROCESSES = 25  # Número total de procesos a simular
INTERVAL = 10  # Intervalo de tiempo entre la creación de cada proceso
INSTRUCTIONS_PER_CYCLE = 3  # Número de instrucciones que se pueden ejecutar en un ciclo de CPU

# Función que simula un proceso en el sistema
def process(env, name, cpu, ram, memory_needed, instructions, process_times):
    start_time = env.now  # Tiempo de inicio del proceso
    # Mensaje de creación del proceso
    print(f'{start_time}: {name} creado, necesita {memory_needed} de memoria, instrucciones {instructions}')

    # Solicitar RAM (Paso de New a Ready)
    with ram.get(memory_needed) as request:
        yield request
        # Mensaje indicando que el proceso está listo para ejecutarse
        print(f'{env.now}: {name} ha obtenido la memoria necesaria y está en READY')

        # Ciclo para ejecutar todas las instrucciones del proceso
        while instructions > 0:
            # Solicitar uso del CPU (Paso de Ready a Running)
            with cpu.request() as req:
                yield req
                # Mensaje indicando que el proceso está en ejecución
                print(f'{env.now}: {name} está RUNNING')

                # Simular ejecución de instrucciones durante un ciclo de CPU
                yield env.timeout(1)  # Representa un ciclo de CPU
                instructions -= min(INSTRUCTIONS_PER_CYCLE, instructions)
                # Mensaje indicando instrucciones restantes
                print(f'{env.now}: {name} ha ejecutado instrucciones, restantes {instructions}')

                # Verificar si el proceso ha terminado
                if instructions <= 0:
                    print(f'{env.now}: {name} ha TERMINATED')
                    break
                else:
                    # Simular posibles interrupciones o decisiones post-ejecución
                    next_step = random.randint(1, 3)
                    if next_step == 1:
                        # Simulación de espera por I/O
                        print(f'{env.now}: {name} entra a WAITING por I/O')
                        yield env.timeout(1)  # Simulación de tiempo de espera por I/O
                        print(f'{env.now}: {name} vuelve a READY después de I/O')

    # Liberar RAM y registrar tiempo de finalización
    yield ram.put(memory_needed)
    finish_time = env.now  # Registrar tiempo de finalización
    process_times.append([name, start_time, finish_time])  # Añadir tiempos al registro
    print(f'{env.now}: {name} ha liberado su memoria')

# Función para generar procesos durante la simulación
def generate_processes(env, cpu, ram, process_times):
    for i in range(NUM_PROCESSES):
        memory_needed = random.randint(1, 10)
        instructions = random.randint(1, 10)
        env.process(process(env, f'Proceso {i}', cpu, ram, memory_needed, instructions, process_times))
        yield env.timeout(random.randint(1, INTERVAL))

# Función para guardar los tiempos en un CSV
def save_times_to_csv(times, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Proceso', 'Tiempo de Inicio', 'Tiempo de Finalización'])
        # Lista para registrar los tiempos de cada proceso
        total_times = []
        for time in times:
            writer.writerow(time)
            # Calcular el tiempo total para cada proceso
            total_time = time[2] - time[1]
            total_times.append(total_time)

    # Calcular tiempo promedio y desviación estándar
    avg_time = np.mean(total_times)
    std_dev_time = np.std(total_times)
    return avg_time, std_dev_time, total_times

# Lista para registrar los tiempos de cada proceso
process_times = []

# Configuración del entorno de simulación y recursos
env = simpy.Environment()
cpu = simpy.Resource(env, capacity=CPU_SPEED)
ram = simpy.Container(env, init=RAM_CAPACITY, capacity=RAM_CAPACITY)
env.process(generate_processes(env, cpu, ram, process_times))
env.run()

# Nombre del archivo CSV con marca de tiempo para evitar sobreescrituras
filename = f'times_{NUM_PROCESSES}_processes_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'
avg_time, std_dev_time, total_times = save_times_to_csv(process_times, filename)

# Mostrar estadísticas
print(f"Tiempo promedio: {avg_time}, Desviación Estándar: {std_dev_time}")

# Graficar la distribución de tiempos de ejecución de los procesos
plt.figure(figsize=(10, 6))
plt.hist(total_times, bins=10, color='skyblue', edgecolor='black')
plt.title('Distribución de Tiempos de Ejecución')
plt.xlabel('Tiempo de Ejecución')
plt.ylabel('Frecuencia')
plt.grid(axis='y', alpha=0.75)
plt.show()
import simpy
import random
import csv
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# Parámetros de configuración
RAM_CAPACITY = 100  # Capacidad de la RAM
CPU_SPEED = 1  # Velocidad del CPU
NUM_PROCESSES = 25  # Número total de procesos a simular
INTERVAL = 10  # Intervalo de tiempo entre la creación de cada proceso
INSTRUCTIONS_PER_CYCLE = 3  # Número de instrucciones que se pueden ejecutar en un ciclo de CPU

# Función que simula un proceso en el sistema
def process(env, name, cpu, ram, memory_needed, instructions, process_times):
    start_time = env.now  # Tiempo de inicio del proceso
    # Mensaje de creación del proceso
    print(f'{start_time}: {name} creado, necesita {memory_needed} de memoria, instrucciones {instructions}')

    # Solicitar RAM (Paso de New a Ready)
    with ram.get(memory_needed) as request:
        yield request
        # Mensaje indicando que el proceso está listo para ejecutarse
        print(f'{env.now}: {name} ha obtenido la memoria necesaria y está en READY')

        # Ciclo para ejecutar todas las instrucciones del proceso
        while instructions > 0:
            # Solicitar uso del CPU (Paso de Ready a Running)
            with cpu.request() as req:
                yield req
                # Mensaje indicando que el proceso está en ejecución
                print(f'{env.now}: {name} está RUNNING')

                # Simular ejecución de instrucciones durante un ciclo de CPU
                yield env.timeout(1)  # Representa un ciclo de CPU
                instructions -= min(INSTRUCTIONS_PER_CYCLE, instructions)
                # Mensaje indicando instrucciones restantes
                print(f'{env.now}: {name} ha ejecutado instrucciones, restantes {instructions}')

                # Verificar si el proceso ha terminado
                if instructions <= 0:
                    print(f'{env.now}: {name} ha TERMINATED')
                    break
                else:
                    # Simular posibles interrupciones o decisiones post-ejecución
                    next_step = random.randint(1, 3)
                    if next_step == 1:
                        # Simulación de espera por I/O
                        print(f'{env.now}: {name} entra a WAITING por I/O')
                        yield env.timeout(1)  # Simulación de tiempo de espera por I/O
                        print(f'{env.now}: {name} vuelve a READY después de I/O')

    # Liberar RAM y registrar tiempo de finalización
    yield ram.put(memory_needed)
    finish_time = env.now  # Registrar tiempo de finalización
    process_times.append([name, start_time, finish_time])  # Añadir tiempos al registro
    print(f'{env.now}: {name} ha liberado su memoria')

# Función para generar procesos durante la simulación
def generate_processes(env, cpu, ram, process_times):
    for i in range(NUM_PROCESSES):
        memory_needed = random.randint(1, 10)
        instructions = random.randint(1, 10)
        env.process(process(env, f'Proceso {i}', cpu, ram, memory_needed, instructions, process_times))
        yield env.timeout(random.randint(1, INTERVAL))

# Función para guardar los tiempos en un CSV
def save_times_to_csv(times, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Proceso', 'Tiempo de Inicio', 'Tiempo de Finalización'])
        # Lista para registrar los tiempos de cada proceso
        total_times = []
        for time in times:
            writer.writerow(time)
            # Calcular el tiempo total para cada proceso
            total_time = time[2] - time[1]
            total_times.append(total_time)

    # Calcular tiempo promedio y desviación estándar
    avg_time = np.mean(total_times)
    std_dev_time = np.std(total_times)
    return avg_time, std_dev_time, total_times

# Lista para registrar los tiempos de cada proceso
process_times = []

# Configuración del entorno de simulación y recursos
env = simpy.Environment()
cpu = simpy.Resource(env, capacity=CPU_SPEED)
ram = simpy.Container(env, init=RAM_CAPACITY, capacity=RAM_CAPACITY)
env.process(generate_processes(env, cpu, ram, process_times))
env.run()

# Nombre del archivo CSV con marca de tiempo para evitar sobreescrituras
filename = f'times_{NUM_PROCESSES}_processes_{datetime.now().strftime("%H%M%S")}.csv'
avg_time, std_dev_time, total_times = save_times_to_csv(process_times, filename)

# Mostrar estadísticas
print(f"Tiempo promedio: {avg_time}, Desviación Estándar: {std_dev_time}")

# Graficar la distribución de tiempos de ejecución de los procesos
plt.figure(figsize=(10, 6))
plt.hist(total_times, bins=10, color='skyblue', edgecolor='black')
plt.title('Distribución de Tiempos de Ejecución')
plt.xlabel('Tiempo de Ejecución')
plt.ylabel('Frecuencia')
plt.grid(axis='y', alpha=0.75)
plt.show()
