import os
from tqdm import tqdm 
from colorama import Fore, Back, Style 
import time

sec = 100

class progress_bar():
    for i in tqdm (range (sec),  
                   desc=Fore.WHITE + "Loading. . .",  
                   ascii=False, ncols=75): 
        time.sleep(0.01)       

    #the Fore.BLUE adds colour to the loading bar
    print(Fore.WHITE + "Complete. . .") 
    time.sleep(3) 
    #this will clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')