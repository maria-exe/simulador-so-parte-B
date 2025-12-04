from scr.config_reader import read_config, create_config
from scr.task import TaskControlBlock
from scr.simulator import Simulator
from scr.enums import Scheduler
from ui.ui_aux import colors, color_state
from ui.gantt_chart import GanttChart
import os, sys, tty, termios

class SystemInterface:
    def __init__(self):
        self.default_file = "config/DEFAULT.txt"           # Configuracao padrao do sistema, que pode ser sobreescrito pelo usuario
    
        if getattr(sys, 'frozen', False):
            self.dir = sys._MEIPASS

        else: 
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.dir = os.path.dirname(script_dir)

        self.file_path = os.path.join(self.dir, self.default_file)

        self.scheduler, self.quantum, self.tasks = read_config(self.file_path)
        self.simulator1 = Simulator(self.scheduler, self.quantum, self.tasks)
        self.tasks_map = {}

    # Metodo principal classe para controlar outras partes do programa de acordo com as entradas do usuario
    def main_menu(self):
        while True:
            try: 
                self.clear_terminal()
                print("--- SimuladorOS ---\n")
                print("Digite o numero da opcao desejada:\n" \
                "      1. INICIAR\n" \
                "      2. CARREGAR ARQUIVO\n" \
                "      3. CONFIGURACAO\n" \
                "      4. SAIR\n")

                command = int(input("Digite: "))
                
                match command:
                    case 1: 
                        print("Selecione o modo de simulacao: (1. Passo-a-passo, 2. Completa)")
                        mode = int(input("Digite: "))
                        if mode == 1:
                            self.by_step_simulation()       
                        elif mode == 2:
                            self.complete_simulation()

                        print("\nQuer salvar o resultado como .png? (1. Sim, 2. Não)")
                        mode = int(input("Digite: "))
                        if mode == 1:          
                            #gantt = GanttChart(self.simulator1, self.scheduler) 
                            #gantt.create_chart()   
                            pass                              # cria e salva o grafico
                        elif mode == 2:
                            print("Adeus!")
                            sys.exit(0)                                          # finaliza o program

                    case 2:
                        caminho = input("Digite o caminho do arquivo: ")
                        configs = read_config(caminho)  # le o arquivo do usuario e sobrescreve o arquivo padrao
                        
                        scheduler, quantum, tasks = configs
                    
                        if scheduler is None:
                            print(f"Erro ao carregar arquivo\n")
                        
                        else:
                            # instancia uma nova simulacao com base nas consiguracoes lidas no arquivo do usuario
                            self.scheduler, self.quantum, self.tasks = configs
                            self.simulator1 = Simulator(self.scheduler, self.quantum, self.tasks)
                            print(f"Arquivo '{caminho}' carregado.\n")
                    
                    case 3: # sobreescreve arquivo default com as config do usuario
                        scheduler, quantum, tasks_list = self.create_tasks()  # metodo para criacao das configuracoes do sistema e tarefas

                        if scheduler is None:
                            print("Nenhuma alteração foi salva")
                        
                        create_config(self.file_path, scheduler, quantum, tasks_list) 
            
                        # instancia uma nova simulacao com base nas consiguracoes passadas pelo usuario
                        self.scheduler = scheduler
                        self.quantum = quantum
                        self.tasks = tasks_list 
                        
                        self.simulator1 = Simulator(self.scheduler, self.quantum, self.tasks)
                        self.tasks_map = {} 
                    
                    case 4:
                        sys.exit(0) # encerramento do programa
                    case _:
                        raise ValueError(f"Entrada invalida")

            except Exception as e:
                print(f"ERRO: {e}")

    def create_tasks(self):                     # metodo principal para parametrizacao do sistema do usuario
        try:
            self.clear_terminal()   # limpa terminal
            print("Escolha o escalonador entre as opcoes: (1. FCFS, 2. SRTF e 3. PRIOP)\n")
            
            # le e verifica as entradas de escalonamento e quantum 

            valid_scheduler = [1, 2, 3]
            entry = int(input("Digite o valor correspondente: "))
            if entry not in valid_scheduler:
                raise ValueError(f"Entrada {entry} invalida.")
            
            sch_string = Scheduler(entry)   
            scheduler = sch_string.name
                
            quantum = int(input("Digite o valor do quantum: "))
            if quantum <= 0:
                raise ValueError(f"Entrada {quantum} invalida.")
            
            print("\n ----- Configuracao de tarefas ----- \n")
            created_tasks = [] # lista para armazenar as tarefas criadas pelo usuario
            
            is_adding = True
            while(is_adding): # loop que chama o metodo edit_task_aux para criacao de tasks
                print("\n--- Quer criar adicionar uma nova tarefa? (1. Sim, 2. Não) ---\n")
                command = int(input("Digite o valor correspondente: "))

                if command == 1:
                    task = self.edit_task_aux()
                    created_tasks.append(task)  
                elif command == 2:
                    is_adding = False
                    break
                else: 
                    raise ValueError(f"Entrada {command} invalida.")
        
        except Exception as e:
            print(f"ERRO: {e}")
            return None, 0, []
        return scheduler, quantum, created_tasks

    def edit_task_aux(self):                    # metodo para receber as configuracoes das tarefas do usuario
        try:
            self.clear_terminal()
            t_id = input("Digite o id: ")
            
            # le e valida as configuracoes das tarefas passadas pelo usuario
            print("Selecione uma cor: (0. Roxo, 1. Rosa, 2. Vermelho, 3. Laranja, 4. Amarelo, 5. Verde, 6. Ciano, 7. Azul)")
            valid_colors = [0, 1, 2, 3, 4, 5, 6, 7]
            color = int(input("Digite o valor correspondente: "))
            if color not in valid_colors:
                raise ValueError
            
            start = int(input("Digite o ingresso: "))
            if start < 0:
                raise ValueError
            
            duration = int(input("Digite a duracao: "))
            if duration <= 0: 
                raise ValueError
            
            prio  = int(input("Digite a prioridade: "))
            if prio < 0: 
                raise ValueError
            
            # Adiciona essas info em um dicionario temporario
            task = TaskControlBlock(
                t_id = t_id, 
                color = color,
                start = start,
                duration = duration,
                prio = prio
            )
            return task
        
        except ValueError:
            print(f"ERRO: Entrada {ValueError} invalida.")
            return None
    
    def by_step_simulation(self): # equnato existir tarefas a serem executadas, mostra a execucao de tick por tick
        is_running = True
        while is_running:
            if not self.simulator1.existing_tasks():
                is_running = False

            print("Clique espaço para avançar a simulação\n") # a simulacao avanca com o click do usuario
                                                    
            click = self.user_click()
            if click == " " or click == "c":
                self.by_step()

    def complete_simulation(self):
        while(self.simulator1.existing_tasks()):    # execucao completa da simulacao
                self.by_step()

    def by_step(self):
        current_tick = self.simulator1.clock.current_time  # tick atual
        self.simulator1.tick()

        if not self.tasks_map:                             # adicona na lista o id tarefas que entraram nesse tick
            self.tasks_map = {task.id: task for task in self.simulator1.tasks_list}

        tick_history = self.simulator1.tick_data            # pega os dados do tick do sistem
        tick_data = {} 

        max_time = self.simulator1.clock.current_time       # tempo maximo
        
        for task_id in self.tasks_map.keys():               # inicia o estado de cada tarefa com oscioso
            tick_data[task_id] = ['IDLE'] * max_time 
            
        for entry in tick_history:                          # preenche cada tarefa com seu estado
            tick_time = entry['tick']
            task_id = entry['id']
            
            if task_id not in tick_data:
                continue

            state = entry['state'].upper()
            
            if state == 'RUNNING' or tick_data[task_id][tick_time] == 'IDLE':
                tick_data[task_id][tick_time] = state

        clean = "\033[H\033[J"
        reset = "\033[0m"
        print(clean, end="")

        # ids das tarefas para exibir no terminal
        display_ids = sorted(tick_data.keys(), reverse=True) # ordena as tarefas, para ser T1 embaixo e ir subindp
        
        if not display_ids: 
            print(f"\ntick:\t{current_tick}")                # imprime os ticks
            return

        print(f"Escalonador: {self.scheduler} Quantum: {self.quantum}")
        for task_id in display_ids:                          # exibe cada tarefa
            history = tick_data[task_id]
            task = self.tasks_map[task_id]
            column = f"{task.id}  | "

            # atribui as cores de acordo com o estado
            for state in history: 
                color_code = "\033[40m"
                
                if state == 'RUNNING':
                    color_code = colors.get(task.color, "\033[47m") 
                
                elif state == 'READY' or state == 'SUSPENDED':
                    color_code = color_state.get(state, "\033[100m")

                column = column + f"{color_code}    {reset}" 
            
            print(column)
        
        padding = "      "                  # formata a saida do programa
        axis_x = padding

        for tick in range(max_time):        # tamanho do caractere/bloco por tarefa
            axis_x = axis_x + f"{tick:<4}"
        
        print(axis_x)
        print(f"\nTick:\t{current_tick}")

        for task in self.simulator1.tasks_list:
            print(task)

    def user_click(self):                       # captura click do teclado
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try: 
            tty.setcbreak(fd)
            click = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
        return click

    def clear_terminal(self):                   # limpa terminal
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

