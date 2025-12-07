from .enums import TaskState
from .clock import SystemClock
from .scheduler import schedulers

class Simulator():
    def __init__(self, scheduler, quantum, alpha, tasks_list):
        self.clock = SystemClock()
        
        valid_scheduler = schedulers.get(scheduler)                      # verifica que o scheduler esta no dicionario
        if not valid_scheduler:
            raise ValueError(f"Escalonador '{scheduler}' inválido")
        self.scheduler = valid_scheduler()

        self.alpha = alpha
        self._quantum = quantum
        self._quantum_tick = 0

        self.tasks_list = tasks_list
        self.current_task = None            # apenas uma tarefa pode estar no estado RUNNING
        self.ready_tasks = []    
        self.tick_data = []                 # lista para armazenar as informacoes de cada tick
    
    # checha se uma nova tarefa chegou no tick atual do sistema, se sim muda seu estado e coloca na lista de prontos
    def check_new_tasks(self):
        for task in self.tasks_list:
            if task.start == self.clock.current_time and task._state == TaskState.NEW:
                task.set_ready()
                self.ready_tasks.append(task)
   
    def increment_waiting_time(self): # aumenta o tempo de espera das tarefas na lista de prontos
        for task in self.ready_tasks:
            task._waiting_time += 1

    def select_task(self):            # chama o algoritmo de selecao de tarefa dos escalonamento
        return self.scheduler.select_next_task(self.ready_tasks, self.current_task, self.alpha)
    
    def existing_tasks(self):         # verifica se existe tarefa que falta executar
        for task in self.tasks_list:
            if task._state != TaskState.TERMINATED:
                return True
        return False 
    
    def is_running(self):              # verifica se tem tarefa executando
        if self.current_task == None:
            return False
        return True
    
    def is_terminated(self):           # verifica se uma tarefa terminou sua execucao
        if self.current_task._remaining_time == 0:
            return True
        return False
    
    # metodos auxiliares para armazenar as informacoes que aconteceram em cada tick do sistema 
    def register_running_tasks(self, current_tick, running_task): # registra tarefas que estao executando
        if running_task is not None:
            self.tick_data.append ({
                'tick': current_tick,
                'id': running_task, 
                'state': 'running'     
            })
    
    def register_waiting_tasks(self, current_tick): # registra tarefas que estao esperando o processador
        for task in self.ready_tasks:
            self.tick_data.append ({
            'tick': current_tick,
            'id': task.id,  
            'state': 'ready'  
            })

    # arrumar chamada do scheduler
    # Metodo de execucao de um tick da simulacao 
    def tick(self):
        self.increment_waiting_time()
        self.check_new_tasks()
        rescheduler = False

        current_tick = self.clock.current_time

        # se nao tem uma tarefa executando no sistema, seleciona uma
        if not self.is_running():
            if self.ready_tasks:
                chosen_task = self.select_task()
                self.ready_tasks.remove(chosen_task)    # PRONTA -> EXECUTANDO
                self.current_task = chosen_task

                self.current_task.set_running()
                self._quantum_tick = 0                  # reseta o tick

        else: # verifica se uma tarefa precisa ser interrompida por preempcao 
            chosen_task = self.select_task()
            if chosen_task != self.current_task:                # compara a tarefa selecionada com a atual 
                self.current_task.set_ready()                   # troca de contexto
                self.ready_tasks.append(self.current_task)

                self.current_task = chosen_task                 # a outra tarefa recebe o processamento
                self.ready_tasks.remove(self.current_task)

                self.current_task.set_running()
                self._quantum_tick = 0                 

            elif self._quantum_tick == self._quantum:
                self.current_task.set_ready()                   # muda seu estado para pronto e adiciona de volta para lista de prontos
                self.ready_tasks.append(self.current_task)
                
                self.current_task = None
                chosen_task = self.select_task()                # seleciona a proxima tarefa
                self.current_task = chosen_task
                self.ready_tasks.remove(self.current_task)
                self.current_task.set_running()
                
                self._quantum_tick = 0    

        running_task = None                                     # apenas para armazenar no historico

        if self.is_running():                                   # verifica se tem uma tarefa executando
            
            running_task = self.current_task.id

            self.current_task._remaining_time -= 1              # aumenta o tick e decrementa seu tempo restante
            self._quantum_tick += 1

            if self.is_terminated():                            # verifica se terminou a execucao da tarefa
                self.current_task.set_terminated()
                self.current_task._life_time = (self.clock.current_time + 1) - self.current_task.start
                self.current_task = None                        
                self._quantum_tick = 0
                
        self.register_running_tasks(current_tick, running_task)
        self.register_waiting_tasks(current_tick)

        self.clock.tick()                                       # avança o tick


