# Dicionarios de cores para usar na interface do programa e na cricao de grafico

colors = {
    0: "\033[45m",       
    1: "\033[105m",      
    2: "\033[41m",      
    3: "\033[48;5;208m", 
    4: "\033[103m",      
    5: "\033[42m",       
    6: "\033[46m",       
    7: "\033[44m",      
}

colors_chart = {
    0: "#c6a0f6",
    1: "#df8fc1",
    2: "#f77d8c",
    3: "#ffa875", 
    4: "#f6d897",
    5: "#9fe58a",
    6: "#90c6c4",
    7: "#80a7fe"
}

color_state = {
    'RUNNING': None,
    'READY': "\033[100m",
    'SUSPENDED': "\033[100m", 
    'NEW': "\033[48;5;236m",  
    'TERMINATED': "\033[48;5;236m"
}

RESET = "\033[0m"