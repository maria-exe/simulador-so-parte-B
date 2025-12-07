from enum import Enum, auto
# Estados das tarefas
class TaskState(Enum):
    NEW = auto(),
    READY = auto(),
    RUNNING = auto(), 
    TERMINATED = auto(),
    SUSPENDED = auto()

# para relacionar a escolha do usuario no user_interface (feita por um inteiro) a string que representa o escalonador
class Scheduler(Enum):
    FCFS   = 1
    SRTF   = 2
    PRIOP  = 3
    PRIOPEnv = 4