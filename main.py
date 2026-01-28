import numpy
import re
import cv2

code = [
    "adi (0)(1)(8)(1)",
    "sub (0)(1)(1)(0)",
    "orp (0)(0)(1)(5)",
    "hlt (0)(0)(0)(0)[LB2]",
    "[STP]"
]

labels = {}

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
    "12":0,
    "13":0,
    "14":0,
    "15":0
    
    
}



def program_encoding(code, registers):
    executing = False
    str_col2 = 0
    print("emulation.console:\n")
    while executing == False and str_col2 < len(code):
        line = code[str_col2]
        stropcodes = re.findall(r"\(([0-9_]+)\)", line)
        prt3, prt5, prt6, prt7 = stropcodes
        

        opcode = re.search(r"([a-z_]+)", line)
        opcode = opcode.group(1)
        if opcode == "add":
            registers[prt5] = registers[prt7] + registers[prt6]
            pass

        if opcode == "sub":
            registers[prt5] = registers[prt7] - registers[prt6]
            pass

        if opcode == "orp":
            if prt7 == "5":
                print(f"reg:{prt6}", registers[prt6])
            pass

        if opcode == "adi":
            registers[prt5] = registers[prt7] + int(prt6)

        if opcode == "sbi":
            registers[prt5] = registers[prt7] - int(prt6)
            pass

        if opcode == "jmp":
            label_jump = re.search(r"\{([A-Z0-9_]+)\}", line)
            label_jump = label_jump.group(1)
            label_jump = str(label_jump)
            str_col2 = labels[label_jump]
            pass
            
        
        if opcode == "brh":
            label_jump = re.search(r"\{([A-Z0-9_]+)\}", line)
            label_jump = label_jump.group(1)
            label_jump = str(label_jump)
            if registers[prt7] == registers[prt6]:
                str_col2 = labels[label_jump]

            pass
        if opcode == "brn":
            label_jump = re.search(r"\{([A-Z0-9_]+)\}", line)
            label_jump = label_jump.group(1)
            label_jump = str(label_jump)
            if registers[prt7] == int(prt6):
                str_col2 = labels[label_jump]

            pass
        if opcode == "brp":
            label_jump = re.search(r"\{([A-Z0-9_]+)\}", line)
            label_jump = label_jump.group(1)
            label_jump = str(label_jump)
            if registers[prt7] > registers[prt6]:
                str_col2 = labels[label_jump]

            pass
        if opcode == "brm":
            label_jump = re.search(r"\{([A-Z0-9_]+)\}", line)
            label_jump = label_jump.group(1)
            label_jump = str(label_jump)
            if registers[prt7] < registers[prt6]:
                str_col2 = labels[label_jump]

            pass

        if opcode == "non":
            pass
        if opcode == "hlt":
            executing = True
            continue
        if opcode == "jmp":
            str_col2 = str_col2
        else:
            str_col2 += 1

        
def lables_encoding():
    pass
if __name__=='__main__':
    executing2 = False
    str_col = 0
    
    while executing2 == False and str_col < len(code):
        line = code[str_col]
        
        label_assig = re.search(r"\[([A-Z0-9_]+)\]", line)
        
        if label_assig is not None:  # Проверяем, что поиск дал результат
            label2 = label_assig.group(1)  # Теперь можно безопасно вызывать group()
            print(f"Имя лейбла: {label2}")
            
            if label2 == "STP":
                executing2 = True
                str_col = 0
                continue
            
            labels[label2] = str_col
            print(f"Добавлен лейбл: {label2} -> {str_col}")
        else:
            None
            
        str_col = str_col + 1
program_encoding(code, registers)    
    