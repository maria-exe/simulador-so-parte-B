# implementacao do relogio global do sistema
class SystemClock: 
    def __init__(self):            
        self._current_tick = 0

    def tick(self):                 # incrementa o tick 
        self._current_tick += 1 

    @property
    def current_time(self):         # retorna o tick atual
        return self._current_tick