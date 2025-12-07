# Implementação dos Escalonadores 
# Escalonadores implementados: FIFO, PRIOP e SRTF
from abc import ABC, abstractmethod

# Classe abstrata para incluir novos algoritmos de escalonamento de forma simples
class Scheduler(ABC):
    @abstractmethod
    def select_next_task(self, ready_tasks, current_task, alpha):
        pass

class FCFS(Scheduler):
    def select_next_task(self, ready_tasks, current_task, alpha):
        if not ready_tasks:
            return current_task
        
        if current_task is not None:
            return current_task

        return ready_tasks[0]       # retorna a primeira tarefa da lista de prontos

class SRTF(Scheduler):
    def select_next_task(self, ready_tasks, current_task, alpha): 
        if not ready_tasks:
            return current_task
        
        chosen = min(ready_tasks, key=lambda task: task._remaining_time) 

        if current_task is None:                                   # nao tem tarefa executando no sistema 
            return chosen
        
        if chosen._remaining_time < current_task._remaining_time:  # compara se a tarefa escolha tem menor tempo restante que a atual
            return chosen

        return current_task                                        # retorna a com menor tempo restante 

class PRIOP(Scheduler):
    def select_next_task(self, ready_tasks, current_task, alpha):
        if not ready_tasks:
            return current_task

        chosen = max(ready_tasks, key=lambda task: task.prio)
        
        if current_task is None:                # nao tem tarefa executando no sistema 
            return chosen

        if chosen.prio > current_task.prio:     # compara se a tarefa escolhida tem maior priodade que a executando
            return chosen
        
        return current_task

class PRIOPEnv(Scheduler): # prioridade dinâmica (por envelhecimento)
    def select_next_task(self, ready_tasks, current_task, alpha):
        if not ready_tasks:
            return current_task
        
        chosen = max(ready_tasks, key=lambda task: task.priod)
    
        if current_task is None:
            return chosen

        if chosen.priod > current_task.priod:
            for task in ready_tasks:
                if task is not chosen: 
                    task.priod = task.priod + alpha
            
            chosen.priod = chosen.prio
            return chosen
        
        return current_task

# Mapeia as strings dos algoritmos de escalonamento para sua funcao
schedulers = {
        "FCFS": FCFS,
        "SRTF": SRTF,
        "PRIOP": PRIOP,
        "RR": FCFS, 
        "PRIOPEnv": PRIOPEnv
}