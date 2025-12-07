from .task import TaskControlBlock, create_events
from .scheduler import schedulers
""" Implementacao de metodos para leitura e escrita do arquivo de parametrizacao/configuracao das:
    
    A funcao create_config sobreescreve o arquivo de configuracao padrao do sistema com configuracoes passadas pelo
    usuario na classe SystemIterface
    
    A funcao read_config le um arquivo com as configuracoes do sistema e retorna o escalonador, quantum e instancia
    as tarefas no TCB com base nessas configuracoes 

"""
def create_config(filepath, scheduler, quantum, alpha, temp_tasks_list):  # criacao/reescrita de arquivos
    try: 
        with open(filepath, 'w', encoding='utf-8') as file:
            f_line = f"{scheduler};{quantum};{alpha}\n"                   
            file.write(f_line)                                     # escreve a primeira linha do arquivo com scheduler e quantum

            for task in temp_tasks_list:                           # itera por cada linha no arquivo
                t_line = [
                    str(task.id),       
                    str(task.color),    
                    str(task.start),    
                    str(task.duration), 
                    str(task.prio),
                    str(task.events)      
                ]
                t_line = ";".join(t_line) + "\n"        # junta cada info da tarefa, separadas apenas por ; 
                file.write(t_line)                      # escreve a linha no arquivo
            return True
   
    except IOError:                                            # captura de erro de escrita
        print(f"\nErro de escrita no arquivo: {IOError}\n")
        return False

def read_config(file): # leitura de arquivos
    try:
        with open(file, 'r', encoding='utf-8') as config_file:
            
            content = config_file.read()                            # le todo o conteudo do arquivo, se tiver vazio, retorna erro
            if not content:
                raise ValueError(f"Arquivo {file} vazio.")
            
            config_file.seek(0)                                     # reposiciona o cursor para o topo do arquivo
                
            f_line = config_file.readline().strip('\n').split(';')  # verifica se o arquivo contem o escalonador e quantum
            if len(f_line) != 3:
                raise ValueError("Arquivo mal estruturado. Deve ser: 'escalonador;quantum;alpha'")
            
            scheduler = f_line[0]
            quantum = int(f_line[1])
            alpha = int(f_line[2])

            if scheduler not in schedulers: 
                raise ValueError(f"Escalonador {scheduler} invalido.")
            
            if quantum <= 0:
                raise ValueError(f"Quantum {quantum} invalido.")
            
            if alpha < 0:
                raise ValueError(f"Fator envelhecimento {alpha} invalido.")
            
            tasks_list = []
            for line in config_file:                        # le cada linha do arquivo
                line = line.strip().split(';')              # divide a linha por ; e armazena cada info em uma posicao de um vetor
                
                if len(line) < 5:
                    raise ValueError("Parametros insuficientes.")

                t_id = line[0]
                color = int(line[1])
                start = int(line[2])                        # pega cada configuracao da tarefa
                duration = int(line[3])
                prio = int(line[4])
                events = line[5:]

                events_list = create_events(events)
 
                if duration <= 0:
                    raise ValueError("Valor de duracao invalido.")
                if start < 0:
                    raise ValueError("Valor de ingresso invalido.")     
                if prio < 0:
                    raise ValueError("Valor de prioridade invalido.")
                
                new_task = TaskControlBlock(       # instancia uma tarefa no TCB
                t_id = t_id,
                color = color,
                start = start, 
                duration = duration, 
                prio = prio,
                events = events_list
                )   
                tasks_list.append(new_task)        # a adiciona na lista de tarefas
    
        print("Arquivo lido com sucesso!")
 
    except FileNotFoundError:
        print(f"Arquivo {file} nao encontrado.")
        return None, 0, 0, []
    
    except Exception as e:
        print(f"Erro: {e}")
        return None, 0, 0, []

    return scheduler, quantum, alpha, tasks_list