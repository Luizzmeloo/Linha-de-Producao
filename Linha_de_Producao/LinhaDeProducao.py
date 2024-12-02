import threading
import csv

class LinhaDeProducao:
    def __init__(self, capacidade_buffer, num_produtores, num_consumidores, timesteps):
        self.buffer = 0
        self.capacidade_buffer = capacidade_buffer
        self.lock = threading.Lock()
        self.lock_csv = threading.Lock()
        self.sem_espaco_disponivel = threading.Semaphore(capacidade_buffer)
        self.sem_itens_disponiveis = threading.Semaphore(0)
        self.num_produtores = num_produtores
        self.num_consumidores = num_consumidores
        self.timesteps = timesteps
        self.estados_buffer = []
        self.total_produzido = 0
        self.total_consumido = 0


        self.produtores_completaram = 0
        self.consumidores_completaram = 0
        self.timestep_cond = threading.Condition()

        self.file_produtores = open('produtores.csv', 'w', newline='')
        self.file_consumidores = open('consumidores.csv', 'w', newline='')
        self.writer_produtores = csv.writer(self.file_produtores)
        self.writer_consumidores = csv.writer(self.file_consumidores)

        self.writer_produtores.writerow(["Timestep", "Produtor ID", "Quantidade Produzida", "Buffer Após Produção"])
        self.writer_consumidores.writerow(["Timestep", "Consumidor ID", "Quantidade Consumida", "Buffer Após Consumo"])

    def registrar_estado_buffer(self, timestep):
        with self.lock:
            self.estados_buffer.append((timestep, self.buffer))

    def sincronizar_timestep(self):
        with self.timestep_cond:
            self.timestep_cond.wait_for(
                lambda: self.produtores_completaram == self.num_produtores and
                        self.consumidores_completaram == self.num_consumidores
            )
            self.produtores_completaram = 0
            self.consumidores_completaram = 0
            self.timestep_cond.notify_all()

    def notificar_produtor(self):
        with self.timestep_cond:
            self.produtores_completaram += 1
            self.timestep_cond.notify_all()

    def notificar_consumidor(self):
        with self.timestep_cond:
            self.consumidores_completaram += 1
            self.timestep_cond.notify_all()

    def fechar_arquivos(self):
        self.file_produtores.close()
        self.file_consumidores.close()
