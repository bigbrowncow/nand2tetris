# Project 6
# Nand2Tetris assembler
# With a little bit of help from ChatGPT


import sys
import os

# Use global disctionary for symbols
asm_symbol_index = 16
asm_symbols = {
'@R0':'0000000000000000',
'@R1':'0000000000000001',
'@R2':'0000000000000010',
'@R3':'0000000000000011',
'@R4':'0000000000000100',
'@R5':'0000000000000101',
'@R6':'0000000000000110',
'@R7':'0000000000000111',
'@R8':'0000000000001000',
'@R9':'0000000000001001',
'@R10':'0000000000001010',
'@R11':'0000000000001011',
'@R12':'0000000000001100',
'@R13':'0000000000001101',
'@R14':'0000000000001110',
'@R15':'0000000000001111',
'@SCREEN':'0100000000000000',
'@KBD':   '0110000000000000',
'@SP':    '0000000000000000',
'@LCL':   '0000000000000001',
'@ARG':   '0000000000000010',
'@THIS':  '0000000000000011',
'@THAT': '0000000000000100'
}

def print_progress_bar(message, current, total, bar_length=40):
    percent = current / total
    filled = int(bar_length * percent)
    bar =  message + '█' * filled + '-' * (bar_length - filled)
    print(f'\r|{bar}| {percent:.0%}', end='')
    sys.stdout.flush()



def add_symbol(symbol,address):
    # Add a symbol to the global dictionary
    asm_symbols['@'+symbol] = format(address, '016b')
    
def predefined(symbols):
    global asm_symbol_index
    
    if symbols in asm_symbols:
        # In the symbol list so just substitute
        bits=asm_symbols[symbols]
    elif symbols[1:].isdigit():
        # Hard coded constant
        number = int(symbols[1:])  # Extract number
        bits = format(number, '016b')  # Convert to 16-bit binary
    else:
        # New symbol - add to the list
        add_symbol(symbols[1:],asm_symbol_index)
        bits = format(asm_symbol_index, '016b')  # Convert to 16-bit binary
        asm_symbol_index += 1
        
    return bits






def ddd(symbols):
    bits = ['0', '0', '0']  # A, M, D
    for char in symbols:
        if char == 'M':
            bits[2] = '1'
        elif char == 'D':
            bits[1] = '1'
        elif char == 'A':
            bits[0] = '1'
        else:
            raise ValueError(f"Invalid ddd symbol '{char}' in line")
    return ''.join(bits)


def acccccc(symbols):
    bits = '000000'  # ALU
    a = '0'
    if 'M' in symbols:
        a = '1'
        symbols = symbols.replace('M','A') # Replace M with A
    if symbols == '0':
         bits='101010'
    elif symbols == '1':
         bits='111111'
    elif symbols == '-1':
         bits='111010'
    elif symbols == 'D':
         bits='001100'
    elif symbols == 'A':
         bits='110000'
    elif symbols == '!D':
         bits='001101'
    elif symbols == '!A':
         bits='110001'
    elif symbols == '-D':
         bits='001111'
    elif symbols == '-A':
         bits='110011'
    elif symbols == 'D+1':
         bits='011111'
    elif symbols == 'A+1':
         bits='110111'
    elif symbols == 'D-1':
         bits='001110'
    elif symbols == 'A-1':
         bits='110010'
    elif symbols == 'D+A':
         bits='000010'
    elif symbols == 'D-A':
         bits='010011'
    elif symbols == 'A-D':
         bits='000111'
    elif symbols == 'D&A':
         bits='000000'
    elif symbols == 'D|A':
         bits='010101'
    else:
        raise ValueError(f"Invalid acccccc symbol '{symbols}' in line")
    return  a+bits



def jjj(symbols):
    bits = '000' 
    if symbols == '':
         bits='000'
    elif symbols == 'JGT':
         bits='001'
    elif symbols == 'JEQ':
         bits='010'
    elif symbols == 'JGE':
         bits='011'
    elif symbols == 'JLT':
         bits='100'
    elif symbols == 'JNE':
         bits='101'
    elif symbols == 'JLE':
         bits='110'
    elif symbols == 'JMP':
         bits='111'
    else:
        raise ValueError(f"Invalid jjj symbol '{symbols}' in line")
    return  bits


if len(sys.argv) < 2:
    print("Usage: python hackassm.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

base, _ = os.path.splitext(filename)
output_filename = base + '.hack'
open(output_filename,'w').close() # delete output file contents

clean_lines = []


try:
    with open(filename, 'r') as file:
        lines = file.readlines()

    line_number=0
    for line in lines:
        print_progress_bar('Phase 1:',line_number,len(lines))
        line = ''.join(line.split())        # Remove all whitespace characters
        line = line.split('//')[0]          # Remove anything after '//' (including the slashes)

        if line.startswith('('):
            # New symbole to add to symbol table
            try:
                symbol = line.replace('(','')
                symbol = symbol.replace(')','')
                add_symbol(symbol,line_number)
            except ValueError:
                continue  # Skip further processing
        elif line:
            line_number += 1
            clean_lines.append(line);


    lines = clean_lines
        
    i = 0;   
    for line in lines:
        print_progress_bar('Phase 2:',i,len(lines)-1)
        i +=1 
        
        if line.startswith('@'):
            # Handle @number: extract number and convert to 16-bit binary or look up symbol
            try:
                
                binary = predefined(line)
                with open(output_filename, 'a', newline='\n') as f: #newline fixes bug in nand2tetris comparison tool
                    f.write(binary + '\n')

            except ValueError:
                print(f"Invalid number in line: {line}")
            continue  # Skip further processing for @ lines

        # Start with destination and calculate ddd code
        if '=' in line:
            prefix = line.split('=')[0].strip()
        else:
            prefix = ''  # No destination specified
        try:
            ddd_code = ddd(prefix)
#               print(ddd_code)
        except ValueError as ve:
            print(ve)

        # Next is the ALU opcode which will be between the = and ;
        between = line.split('=')[1] if '=' in line else line
        between = between.split(';')[0] if ';' in between else between
        try:
            acccccc_code = acccccc(between)
        except ValueError as ve:
            print(ve)

        # Then the compare code for JJJ instructions
        suffix = line.split(';',1)[1] if ';' in line else ''
        try:
            jjj_code = jjj(suffix)
#               print('111' + acccccc_code + ddd_code + jjj_code)
            with open(output_filename, 'a', newline='\n') as f: #send the whole opcode to the output file
                f.write('111' + acccccc_code + ddd_code + jjj_code + '\n')
        except ValueError as ve:
            print(ve)
            
        
            
except FileNotFoundError:
    print(f"File '{filename}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")