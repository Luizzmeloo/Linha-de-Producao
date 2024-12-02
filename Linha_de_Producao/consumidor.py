import time

def consumidor(linha, id_consumidor, taxa_consumo):
    for t in range(linha.timesteps):
        linha.sem_itens_disponiveis.acquire()
        with linha.lock:
            quantidade_consumida = min(taxa_consumo, linha.buffer)
            quantidade_nao_consumida = taxa_consumo - quantidade_consumida

            if quantidade_consumida > 0:
                linha.buffer -= quantidade_consumida
                linha.total_consumido += quantidade_consumida
                print(f"Consumidor {id_consumidor} consumiu {quantidade_consumida} item(s). Buffer: {linha.buffer}")

        linha.sem_espaco_disponivel.release()

        with linha.lock_csv:
            linha.writer_consumidores.writerow([t, id_consumidor, quantidade_consumida, linha.buffer])

        linha.notificar_consumidor()
        time.sleep(0.1)
