# VM Translaotr
# Nand2Tetris Project 7

# Read .vm file and generate .asm
# No Copilot this time :D

# Unit tests
# SimpleAdd.vm - pass
# BasicTest.vm - pass
# PointerTest.vm - pass
# StackTest.vm - pass
# StaticTest.vm - pass

#todo: error checking/handling



import os
import sys

arithmetic_sym = {
'sub':'D=A-D',
'add':'D=D+A',
'neg':'D=-D',
'eq':'D=A-D',
'gt':'D=A-D',
'lt':'D=A-D',
'and':'D=D&A',
'or':'D=D|A',
'not':'D=!D'
}

truefalse_index = '0'

def c_arithmetic(symbol):
# Implement true as -1 and false as 0
    global truefalse_index
    asm=[]


    if symbol == 'not':
        asm.extend([
            '@SP',
            'A=M-1',
            'M=!M'])
    elif symbol == 'neg':
        asm.extend([
            '@SP',
            'A=M-1',
            'M=-M'])
    else:
        

        asm.extend([
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            'A=A-1',
            'A=M'])
        asm.extend([arithmetic_sym[symbol]]) # e.g. 'D=D-A'
        
        if symbol == 'eq':
            asm.extend([
                '@true'+truefalse_index,
                'D;JEQ',
                'D = 0',
                '@next'+truefalse_index,
                'D;JMP',
                '(true'+truefalse_index+')',
                'D = -1',
                '(next'+truefalse_index+')'])
            truefalse_index += '1'

        if symbol == 'lt':
            asm.extend([
                '@true'+truefalse_index,
                'D;JLT',
                'D = 0',
                '@next'+truefalse_index,
                'D;JMP',
                '(true'+truefalse_index+')',
                'D = -1',
                '(next'+truefalse_index+')'])
            truefalse_index += '1'

        if symbol == 'gt':
            asm.extend([
                '@true'+truefalse_index,
                'D;JGT',
                'D = 0',
                '@next'+truefalse_index,
                'D;JMP',
                '(true'+truefalse_index+')',
                'D = -1',
                '(next'+truefalse_index+')'])
            truefalse_index += '0'

            
            
        #pop D on the stack
        asm.extend([
            '@SP',
            'A=M-1',
            'M=D'])
 
    return asm
    
    

def c_push(line):
    args = line.split()
    #args0 push
    #args1 segment
    #args2 value

    asm=[]
    segments = {
    'local':'@LCL',
    'argument':'@ARG',
    'this':'@THIS',
    'that':'@THAT'}
    
    if args[1] == 'constant':
        # @xxx to stack
        asm.extend([
            '@'+args[2],
            'D=A //move constant to D'])
    
    elif args[1] in segments:
        # segment pointer + i to stack
        asm.extend([
            segments[args[1]], # e.g. @LCL
            'D=M',
            '@'+args[2],
            'A=D+A',
            'D=M // move segment+i to D'])            

    elif args[1] == 'static':
        # 16 + i pointer to stack
        asm.extend([
            '@static_'+args[2], # e.g. static_8
            'D=M // move segment+i to D'])
            
    elif args[1] == 'temp':
        # 5 + i pointer to stack
        asm.extend([
            '@'+str(5+int(args[2])), # e.g. 0,1,2
            'D=M // move segment+i to D'])
            
    elif args[1] == 'pointer' and args[2]== '0':
         asm.extend([
            '@THIS',
            'D=M //move THIS to D'])

    elif args[1] == 'pointer' and args[2]== '1':
         asm.extend([
            '@THAT',
            'D=M //move THIS to D'])
   
    else:
         raise ValueError(f"Invalid segment '{args[1]}' in line")


    asm.extend([
        '@SP',
        'A=M',
        'M=D',
        'D=A+1',
        '@SP',
        'M=D'])
        
    return(asm)


def c_pop(line):
    args = line.split()
    #args0 pop
    #args1 segment
    #args2 value



    segments = {
    'local':'@LCL',
    'argument':'@ARG',
    'this':'@THIS',
    'that':'@THAT'}
    
    asm=[]

    asm.extend([
        '@SP //stackpointer',
        'M=M-1 // SP--',
        'A=M',
        'D=M // move top of stack to D'])
    
#    if args[1] == 'constant':
        # doesn't mean anything
        
    if args[1] in segments:
        # segment pointer + i from stack
        asm.extend([segments[args[1]]]) # e.g. @LCL
        asm.extend(['A=M'])
        for i in range(int(args[2])):
            asm.extend(['A=A+1']) # calculate index
        asm.extend(['M=D'])


    elif args[1] == 'static':
        # 16 + i pointer to stack
        asm.extend([
            '@static_'+args[2], # e.g. static_8
            'M=D'])
            
    elif args[1] == 'temp':
        # 5 + i pointer to stack
        asm.extend([
            '@'+str(5+int(args[2])), # e.g. 0,1,2
            'M=D'])
            
    elif args[1] == 'pointer' and args[2]== '0':
         asm.extend([
            '@THIS',
            'M=D'])

    elif args[1] == 'pointer' and args[2]== '1':
         asm.extend([
            '@THAT',
            'M=D'])
   
    else:
        raise ValueError(f"Invalid segment {args[1]} in line")



        
    return(asm)






if len(sys.argv) < 2:
    print("Usage: python hackassm.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

base, _ = os.path.splitext(filename)
output_filename = base + '.asm'
open(output_filename,'w').close() # delete output file contents



with open(filename, 'r') as file:
    lines = file.readlines()



output = []

for line in lines:
#        print_progress_bar('Phase 1:',line_number,len(lines))
#    line = ''.join(line.split())        # Remove all whitespace characters
    line = line.split('//')[0]          # Remove anything after '//' (including the slashes)

    if not ''.join(line.split()):
        continue
        
    output.extend(['\n// '+line])

    if line.startswith('push'):
        output.extend(c_push(line))
    elif line.startswith('pop'):
        output.extend(c_pop(line))

    elif line.split()[0] in arithmetic_sym:
        output.extend(c_arithmetic(line.split()[0]))
            

with open(output_filename, 'a', newline='\n') as f: #send the whole opcode to the output file
    for item in output:
        f.write(str(item)+'\n')
 #       print(str(item) + '\n')





# hasMoreLines()
# advance()

# commandType()
# C_ARITHMETIC
# C_PUSH C_POP

# arg1(): Returns the first argument of the current command;
# In the case of C_ARITHMETIC, the command itself is returned (string)
# arg2(): Returns the second argument of the current command (int);
# Called only if the current command is C_PUSH, C-POP, C_FUNCTION, or C_CALL



# Arithmetic Logical commands
# add
# sub
# neg
# eq
# gt
# lt
# and
# or
# not


    
    

        # for local, argument, this that
        #// pop segment i
        #addr ← segmentpointer + i
        #SP--
        #RAM[addr] ← RAM[SP]    


# static is fixed block starting at 16 and finishing at 255
#--- use assembler to allocate

# temp is a fixed 8 entry segment temp0...temp7
#---
# maps to ram[5]...ram[12]

#push/pop pointer 0 is THIS
#push/pop point 1 is THAT

#constant is just integers onto main stack
