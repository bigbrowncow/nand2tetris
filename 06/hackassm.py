# Project 6
# Nand2Tetris assembler
# With some help from ChatGPT


import sys
import os


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
            raise ValueError(f"Invalid symbol '{char}' in line")
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
        raise ValueError(f"Invalid symbol '{symbols}' in line")
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
        raise ValueError(f"Invalid symbol '{symbols}' in line")
    return  bits


if len(sys.argv) < 2:
    print("Usage: python script.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

base, _ = os.path.splitext(filename)
output_filename = base + '.hack'
open(output_filename,'w').close() # delete output file contents

try:
    with open(filename, 'r') as file:
        for line in file:
            line = line.split('//')[0]          # Remove anything after '//' (including the slashes)
            line = ''.join(line.split())        # Remove all whitespace characters
            
            if not line:
                continue
            
            if line.startswith('@'):
                # Handle @number: extract number and convert to 16-bit binary
                try:
                    number = int(line[1:])  # Extract number
                    binary = format(number, '016b')  # Convert to 16-bit binary
#                    print(binary)
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