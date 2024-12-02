import matplotlib.pyplot as plt
import pandas as pd
from collections import deque
import threading
import time
from LinhaDeProducao import LinhaDeProducao
from produtor import produtor
from consumidor import consumidor
import csv

def salvar_metricas(linha):
    with open('metricas_simulacao.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Métrica", "Valor"])
        writer.writerow(["Total produzido", linha.total_produzido])
        writer.writerow(["Total consumido", linha.total_consumido])


def analyze_results(estados_buffer):
    df = pd.DataFrame(estados_buffer, columns=["Timestep", "Buffer Occupancy"])
    print("\nTabela de resultados:")
    print(df)
    df.to_csv('estados_buffer.csv', index=False)
    plt.figure(figsize=(10, 10))
    plt.plot(df["Timestep"], df["Buffer Occupancy"], marker="o", label="Buffer Occupancy")
    plt.title("Buffer Occupancy Over Time")
    plt.xlabel("Timestep")
    plt.ylabel("Buffer Occupancy")
    plt.grid()
    plt.legend()
    plt.show()

def main():
    print("Configuração do Sistema de Produção e Consumo")
    buffer_capacity = int(input("Digite a capacidade do buffer: "))
    timesteps = int(input("Digite o número de timesteps: "))
    producers = int(input("Digite o número de produtores: "))
    consumers = int(input("Digite o número de consumidores: "))
    production_rate = int(input("Digite a taxa de produção por produtor: "))
    consumption_rate = int(input("Digite a taxa de consumo por consumidor: "))

    linha = LinhaDeProducao(buffer_capacity, producers, consumers, timesteps)

    threads = []
    for i in range(producers):
        threads.append(threading.Thread(target=produtor, args=(linha, i + 1, production_rate)))
    for i in range(consumers):
        threads.append(threading.Thread(target=consumidor, args=(linha, i + 1, consumption_rate)))

    for thread in threads:
        thread.start()

    for t in range(timesteps):
        linha.sincronizar_timestep()
        linha.registrar_estado_buffer(t)

    for thread in threads:
        thread.join()

    salvar_metricas(linha)
    linha.fechar_arquivos()
    analyze_results(linha.estados_buffer)


if __name__ == "__main__":
    main()


