from .enums import TaskState

# Armazena as informações das tarefas antes, durante e depois da simulação
class TaskControlBlock:
    def __init__(self, t_id, color, start, duration, prio, priod, events):
        
        self.id = t_id
        self.color = color
        self.start = start
        self.duration = duration
        self.prio = prio
        self.priod = priod      # prioridade dinâmica
        self.events = events    # eventos
        
        self._remaining_time = duration  # Tempo restante de execução
        self._waiting_time = 0           # Tempo de espera
        self._life_time = 0              # Tempo de vida da tarefa
        
        self._state = TaskState.NEW      # Estado da tarefa 
    
    # Metodos para visualizacao de informacoes das tarefas
    def __repr__(self):
        return (f"Task(id={self.id}, start={self.start}, state={self._state.name} "
                f"remaining={self._remaining_time}, waiting time={self._waiting_time})")
    
    def __str__(self):
        return (f"{self.id} START: {self.start} " 
                f"DURATION:{self.duration} PRIORIDADE: {self.prio} REMAINING: {self._remaining_time} ESTADO: {self._state.name} ")
    
    # Metodos para mudancas de estados
    def set_ready(self):
        self._state = TaskState.READY

    def set_running(self):
        self._state = TaskState.RUNNING

    def set_terminated(self):
        self._state = TaskState.TERMINATED
    
    def set_suspended(self):
        self._state = TaskState.SUSPENDED