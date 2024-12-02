import time

def produtor(linha, id_produtor, taxa_producao):
    for t in range(linha.timesteps):
        linha.sem_espaco_disponivel.acquire()
        with linha.lock:
            quantidade_produzida = min(taxa_producao, linha.capacidade_buffer - linha.buffer)
            if quantidade_produzida > 0:
                linha.buffer += quantidade_produzida
                linha.total_produzido += quantidade_produzida
                print(f"Produtor {id_produtor} produziu {quantidade_produzida} item(s). Buffer: {linha.buffer}")
        linha.sem_itens_disponiveis.release()

        with linha.lock_csv:
            linha.writer_produtores.writerow([t, id_produtor, quantidade_produzida, linha.buffer])

        linha.notificar_produtor()
        time.sleep(0.1)
