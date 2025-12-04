# Implementação dos Escalonadores 
# Escalonadores implementados: FIFO, PRIOP e SRTF
from abc import ABC, abstractmethod

# Classe abstrata para incluir novos algoritmos de escalonamento de forma simples
class Scheduler(ABC):
    @abstractmethod
    def select_next_task(self, ready_tasks, current_task):
        pass

class FCFS(Scheduler):
    def select_next_task(self, ready_tasks, current_task):
        if not ready_tasks:
            return current_task
        
        if current_task is not None:
            return current_task

        return ready_tasks[0]       # retorna a primeira tarefa da lista de prontos

class SRTF(Scheduler):
    def select_next_task(self, ready_tasks, current_task): 
        if not ready_tasks:
            return current_task
        
        chosen = min(ready_tasks, key=lambda task: task._remaining_time) 

        if current_task is None:    # nao tem tarefa executando no sistema 
            return chosen
        
        if chosen._remaining_time < current_task._remaining_time:  # compara se a tarefa escolha tem menor tempo restante que a atual
            return chosen

        return current_task         # retorna a com menor tempo restante 

class PRIOP(Scheduler):
    def select_next_task(self, ready_tasks, current_task):
        if not ready_tasks:
            return current_task
        
        max(ready_tasks)
        chosen = max(ready_tasks, key=lambda task: task.prio)
        
        if current_task is None:    # nao tem tarefa executando no sistema 
            return chosen

        if chosen.prio > current_task.prio:     # compara se a tarefa escolhida tem maior priodade que a executando
            return chosen
        
        return current_task

class PRIOD(Scheduler): # prioridade dinâmica (por envelhecimento)
    # aumenta prioridade enquanto ela está esperando o processador
    def select_next_task(self, ready_tasks, current_task, aging):
        aging # fator envelhecimento
        chosen = max(ready_tasks, key=lambda task: task.priod)
    
        for task in ready_tasks:
            if task != chosen:
                task.priod = task.priod + aging
        
        chosen.priod = chosen.prio # recebe o valor da sua prioridade estática

# Mapeia as strings dos algoritmos de escalonamento para sua funcao
schedulers = {
        "FCFS": FCFS,
        "SRTF": SRTF,
        "PRIOP": PRIOP,
        "RR": FCFS, 
        "PRIOD": PRIOD
}