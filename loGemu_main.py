import numpy as np
import re
import threading
import pygame
import time
import sys
from pathlib import Path
from pixel_window import PixelWindow
from ascii_keyboard import ASCIIKeyboard

kb = ASCIIKeyboard()
kb.start()
main_file = "main.txt"

runfile = Path(__file__).parent
exec_file = runfile / "rmdc" /"main.txt"
with open (exec_file, "r", encoding= 'utf-8') as file:
    code = file.readlines()
    pass

programmer_mod = False

labels = {}

call_stack = {}
counter_stack = {}
registers = {
    "0":0,
    "1":0,
    "2":0,
    "3":0,
    "4":0,
    "5":0,
    "6":0,
    "7":0,
    "8":0,
    "9":0,
    "10":0,
    "11":0,
    "12":0,
    "13":0,
    "14":0,
    "15":0,
    "16":0,
    "17":0,
    "18":0,
    "19":0,
    "20":0
    
    
}
ram = []
ram = np.zeros(131072, dtype=int)


W, H = 64, 64
SCALE = 12

x = 0
y = 0
charbuff = ""
win = PixelWindow(64, 64, scale=8)

matrix = np.zeros((64, 64), dtype=int)

main_branch = True
push_addr = 0




def program_encoding(code, registers, ram, x, y, charbuff, matrix, runfile, main_file, old_count, sys_jump):
    executing = False
    global main_branch
    global push_addr
    str_col2 = old_count
    if programmer_mod == True:
        print(f"\nfile:{sys_jump}\n")
    while executing == False and str_col2 < len(code):
        line = code[str_col2]
        if programmer_mod == True:
                    print (f"currocde: {line}")
        stropcodes = re.findall(r"\(([0-9-._]+)\)", line)
        prt3, prt5, prt6, prt7 = stropcodes

        opcode = re.search(r"([a-z_]+)", line)
        opcode = opcode.group(1)
        if opcode == "add":
            registers[prt5] = registers[prt7] + registers[prt6]
            pass
        if opcode == "mul":
            registers[prt5] = registers[prt7] * registers[prt6]
        if opcode == "div":
            registers[prt5] = registers[prt7] / registers[prt6]

        if opcode == "sub":
            registers[prt5] = registers[prt7] - registers[prt6]
            pass
        if opcode == "orp":
            if prt7 == "4":
                if registers[prt6] == 8:
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                else:
                    print(chr(registers[prt6]), end="", flush=True)
            if prt7 == "5":
                print(f"reg:{prt6}", registers[prt6])
            if prt7 == "1":
                x = registers[prt6]
                pass
            if prt7 == "2":
                y = registers[prt6]
                pass
            if prt7 == "3":
                charbuff = charbuff + chr(registers[prt6])
            pass
        if opcode == "onp":
            if prt7 == "2":
                if prt6 == "1":
                    print(f"\nterminal: {charbuff}")
                    charbuff = ""
                    pass
                if prt6 == "2":
                    charbuff = ""
            if prt7 == "3":
                if prt6 == "2":
                    win.fill(0)
                    pass
                if prt6 == "1":
                    win.set_pixel(x, y, 1)
                    pass
                if prt6 == "3":
                    win.close()
                if prt6 == "4":
                    matrix[x,y] = 1
                if prt6 == "5":
                    win.render(matrix)
                if prt6 == "6":
                    matrix = np.zeros((64, 64), dtype=np.uint8)
                pass
        
        if opcode == "adi":
            registers[prt5] = registers[prt7] + int(prt6)
        if opcode == "mli":
            registers[prt5] = registers[prt7] * int(prt6)
        if opcode == "dvi":
            registers[prt5] = registers[prt7] / int(prt6)
        if opcode == "ldi":
            registers[prt5] = int(prt6)

        if opcode == "sbi":
            registers[prt5] = registers[prt7] - int(prt6)
            pass

        if opcode == "jmp":
            label_jump = re.search(r"\{([A-Za-z0-9_]+)\}", line)
            label_jump = label_jump.group(1)
            label_jump = str(label_jump)
            str_col2 = labels[label_jump]
            pass
        if opcode == "gmp":
            sh_jump = re.search(r"\{([A-Za-z0-9._]+)\}", line)
            sh_jump = str(sh_jump.group(1))
            if sh_jump == "return":
                if push_addr >= 0:
                    stack_frame = call_stack[push_addr]
                    sys_jump = stack_frame['file_name']
                    str_col2 = stack_frame['return_line']
                    exec_file = runfile / "rmdc" / sys_jump
                    with open(exec_file, "r", encoding='utf-8') as file:
                        code = file.readlines()
                    lables_encoding(code)
                    program_encoding(code, registers, ram, x, y, charbuff, matrix, runfile, main_file, str_col2, sys_jump)
                    push_addr -= 1
                else:
                    # Ошибка: попытка возврата из пустого стека
                    raise IndexError("Stack Underflow: return without call")
            else:
                # Сохраняем текущее состояние перед переходом
                push_addr += 1
                call_stack[push_addr] = {
                    'file_name': sys_jump,
                    'return_line': str_col2 + 1, # Сохраняем номер строки для возврата
                }
                if programmer_mod == True:
                    print(call_stack[push_addr])
                # Определяем цель перехода
                match = re.search(r"\{([A-Za-z0-9._]+)\}", line)
                if match:
                    sys_jump = str(match.group(1))
                    if sys_jump == "dump":
                        sys_jump = str(registers[prt7]) + ".txt"
                    exec_file = runfile / "rmdc" / sys_jump
                    
                    with open(exec_file, "r", encoding='utf-8') as file:
                        code = file.readlines()
                    
                    # Сбрасываем счетчик строк для нового файла
                    str_col2 = 0
                    lables_encoding(code)
                    program_encoding(code, registers, ram, x, y, charbuff, matrix, runfile, main_file, str_col2, sys_jump)
                else:
                    raise ValueError("Invalid jump target format")

        if opcode == "mov":
            registers[prt5] = registers[prt7]
        if opcode == "brh":
            label_jump = re.search(r"\{([A-Za-z0-9_]+)\}", line)
            label_jump = label_jump.group(1)
            label_jump = str(label_jump)
            if registers[prt7] == registers[prt6]:
                str_col2 = labels[label_jump] - 1

            pass
        if opcode == "brn":
            label_jump = re.search(r"\{([A-Za-z0-9_]+)\}", line)
            label_jump = label_jump.group(1)
            label_jump = str(label_jump)
            if registers[prt7] == int(prt6):
                str_col2 = labels[label_jump] - 1

            pass
        if opcode == "brp":
            label_jump = re.search(r"\{([A-Za-z0-9_]+)\}", line)
            label_jump = label_jump.group(1)
            label_jump = str(label_jump)
            if registers[prt7] > registers[prt6]:
                str_col2 = labels[label_jump] - 1

            pass
        if opcode == "brm":
            label_jump = re.search(r"\{([A-Za-z0-9_]+)\}", line)
            label_jump = label_jump.group(1)
            label_jump = str(label_jump)
            if registers[prt7] < registers[prt6]:
                str_col2 = labels[label_jump] - 1
            pass
        if opcode == "irp":
            if prt7 == "3":
                    registers[prt5] = kb.get_ascii_code()
            if prt7 == "4":
                    registers[prt5] = kb.get_ascii_rel()
                    
        
        if opcode == "lrm":
            registers[prt5] = ram[int(prt6)]
        if opcode == "rlm":
            registers[prt6] = ram[registers[prt5]]
        if opcode == "wrm":
            ram[int(prt6)] = registers[prt7]
        if opcode == "wnm":
            ram[int(prt6)] = int(prt7)
        if opcode == "wam":
            str_code = str(line)
            array_ram = re.findall(r'\[(.*?)\]',str_code)
            array_ram = str(array_ram)
            array_ram = array_ram.replace("'", "")
            array_ram = array_ram.replace("[", "")
            array_ram = array_ram.replace("]", "")
            array_ram = array_ram.split(",")
            symb_c = len(array_ram)
            symb_ct = 0
            for symb_c in array_ram:
                ram[symb_ct +int(prt6)] = int(array_ram[symb_ct])
                symb_ct += 1
                symb_c =- 1

        if opcode == "rwm":
            ram[registers[prt6]] = registers[prt7]
        if opcode == "crg":
            registers = {
                    "0":0,
                    "1":0,
                    "2":0,
                    "3":0,
                    "4":0,
                    "5":0,
                    "6":0,
                    "7":0,
                    "8":0,
                    "9":0,
                    "10":0,
                    "11":0,
                    "12":0,
                    "13":0,
                    "14":0,
                    "15":0,
                    "16":0,
                    "17":0,
                    "18":0,
                    "19":0,
                    "20":0
            }
        if opcode == "non":
            pass
        if opcode == "hlt":
            print("\nsuccess execute!")
            executing = True
            exit()
        if opcode == "jmp":
            str_col2 = str_col2
        else:
            str_col2 += 1
        time.sleep(0.0000001)

        if programmer_mod == True:
                time.sleep(0.01)

        
def lables_encoding(code):
    executing2 = False
    str_col = 0
    while executing2 == False and str_col < len(code):
        line = code[str_col]
        
        label_assig = re.search(r"\[([A-Za-z0-9_]+)\]", line)
        
        if label_assig is not None:  # Проверяем, что поиск дал результат
            label2 = label_assig.group(1)
            if programmer_mod == True:  # Теперь можно безопасно вызывать group()
                print(f"Имя лейбла: {label2}")
            
            if label2 == "STP":
                executing2 = True
                str_col = 0
                continue
            
            labels[label2] = str_col
            if programmer_mod == True:
                print(f"Добавлен лейбл: {label2} -> {str_col}")
        else:
            None
        str_col = str_col + 1

    pass

if __name__=='__main__':
         win = PixelWindow(64, 64, scale=8)

         # 2. Подготавливаем данные для эмулятора
         old_count = 0
         sys_jump = "main.txt"
         lables_encoding(code)
     
         # 3. Запускаем эмулятор в побочном потоке
         emu_thread = threading.Thread(
             target=program_encoding,
             args=(code, registers, ram, x, y, charbuff, matrix, runfile,
                   main_file, old_count, sys_jump),
             daemon=True  # Поток умрет при закрытии программы
         )
     
         emu_thread.start()
     
         # 4. ГЛАВНЫЙ ЦИКЛ программы: здесь живет PyGame
         clock = pygame.time.Clock()
     
         while win.running:
             win.render()
             clock.tick(1000)  # Ограничиваем FPS интерфейса, чтобы не грузить CPU
     
         pygame.quit()