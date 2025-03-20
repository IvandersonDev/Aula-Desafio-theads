import threading
import time

def calcular_pares(inicio, fim):
    return sum(i for i in range(inicio, fim) if i % 2 == 0)

def calcular_impares(inicio, fim):
    return sum(i for i in range(inicio, fim) if i % 2 == 1)

def testar_desempenho():
    inicio = 1
    fim = 10_000_000

    print("Executando serial...")
    start_time = time.time()
    soma_pares = calcular_pares(inicio, fim)
    soma_impares = calcular_impares(inicio, fim)
    tempo_serial = time.time() - start_time
    print(f"Tempo serial: {tempo_serial:.2f} segundos\n")

    print("Executando com 2 threads...")
    start_time = time.time()

    thread1 = threading.Thread(target=calcular_pares, args=(inicio, fim))
    thread2 = threading.Thread(target=calcular_impares, args=(inicio, fim))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    tempo_2_threads = time.time() - start_time
    print(f"Tempo com 2 threads: {tempo_2_threads:.2f} segundos\n")

    print("Executando com 10 threads...")
    start_time = time.time()

    threads = []
    step = (fim - inicio) // 10

    for i in range(10):
        t_inicio = inicio + i * step
        t_fim = t_inicio + step if i < 9 else fim
        thread = threading.Thread(target=calcular_pares if i % 2 == 0 else calcular_impares, args=(t_inicio, t_fim))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    tempo_10_threads = time.time() - start_time
    print(f"Tempo com 10 threads: {tempo_10_threads:.2f} segundos\n")

    resultados = [
        (1, tempo_serial, 1.0, 1.0),  
        (2, tempo_2_threads, tempo_serial / tempo_2_threads, (tempo_serial / tempo_2_threads) / 2),  
        (10, tempo_10_threads, tempo_serial / tempo_10_threads, (tempo_serial / tempo_10_threads) / 10),  
    ]

    print("Tabela de Speedups e Eficiências:")
    print(f"{'Threads (p)':<12}{'Tempo (s)':<12}{'Speedup (S)':<12}{'Eficiência (E)':<12}")
    for p, tempo, speedup, eficiencia in resultados:
        print(f"{p:<12}{tempo:<12.2f}{speedup:<12.2f}{eficiencia:<12.2f}")

if __name__ == "__main__":
    testar_desempenho()
