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
# BasicLoop.vm - pass
# FibonacciSeries.vm - pass
# SimpleFunction.vm - pass
# NestedCall.asm - pass
# FibonacciElement - pass
# StaticsTest - pass

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

branch_sym = ['label','goto','if-goto']

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
                'D=0',
                '@next'+truefalse_index,
                'D;JMP',
                '(true'+truefalse_index+')',
                'D=-1',
                '(next'+truefalse_index+')'])
            truefalse_index += '1'

        if symbol == 'lt':
            asm.extend([
                '@true'+truefalse_index,
                'D;JLT',
                'D=0',
                '@next'+truefalse_index,
                'D;JMP',
                '(true'+truefalse_index+')',
                'D=-1',
                '(next'+truefalse_index+')'])
            truefalse_index += '1'

        if symbol == 'gt':
            asm.extend([
                '@true'+truefalse_index,
                'D;JGT',
                'D=0',
                '@next'+truefalse_index,
                'D;JMP',
                '(true'+truefalse_index+')',
                'D=-1',
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
    
    global statics_offset

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
            'D=A'])
    
    elif args[1] in segments:
        # segment pointer + i to stack
        asm.extend([
            segments[args[1]], # e.g. @LCL
            'D=M',
            '@'+args[2],
            'A=D+A',
            'D=M'])            

    elif args[1] == 'static':
        # 16 + i pointer to stack
        asm.extend([
            '@static_'+str(int(args[2])+statics_offset), # e.g. static_8
            'D=M'])
            
    elif args[1] == 'temp':
        # 5 + i pointer to stack
        asm.extend([
            '@'+str(5+int(args[2])), # e.g. 0,1,2
            'D=M'])
            
    elif args[1] == 'pointer' and args[2]== '0':
         asm.extend([
            '@THIS',
            'D=M'])

    elif args[1] == 'pointer' and args[2]== '1':
         asm.extend([
            '@THAT',
            'D=M'])
   
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

    global statics_offset

    segments = {
    'local':'@LCL',
    'argument':'@ARG',
    'this':'@THIS',
    'that':'@THAT'}
    
    asm=[]

    asm.extend([
        '@SP',
        'M=M-1',
        'A=M',
        'D=M'])
    
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
            '@static_'+str(int(args[2])+statics_offset), # e.g. static_8
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



def c_branching(line):
    args = line.split()
    #args0 branch
    #args1 label
    
    asm=[]


    if args[0] == 'label':
        asm.extend(['(lb_'+args[1]+')']) #(lb_xxxx)
        
            
    elif args[0] == 'goto':
        asm.extend([
            '@lb_'+args[1], # @lb_xxx
            'D;JMP'])
            
    elif args[0] == 'if-goto':
        # True is -1
         asm.extend([
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            '@lb_'+args[1], # @lb_xxx
            'D;JNE'])
 
   
    else:
        raise ValueError(f"Invalid segment {args[1]} in line")



        
    return(asm)

function_return_index = 0

def c_call(line):
    args = line.split()
    #args0 call
    #args1 functionName
    #args2 nArgs
    
    global function_return_index
    
    pushDtoSP = [
        '@SP',
        'A=M',
        'M=D',
        'D=A+1',
        '@SP',
        'M=D']
    
    

    retAddrLabel = args[1]+'$ret.'+str(function_return_index)

    asm=[]
    
    
 #   push retAddrLabel foo.bar$ret.1
    asm.extend([
        '@'+retAddrLabel,
        'D=A'])
    asm.extend(pushDtoSP)
        
 #   push LCL
    asm.extend([
        '@LCL',
        'D=M'])
    asm.extend(pushDtoSP)
 #   push ARG
    asm.extend([
        '@ARG',
        'D=M'])
    asm.extend(pushDtoSP)
 #   push THIS
    asm.extend([
        '@THIS',
        'D=M'])
    asm.extend(pushDtoSP)
 #   push THAT
    asm.extend([
        '@THAT',
        'D=M'])
    asm.extend(pushDtoSP)
 #   ARG = SP - 5 - nArgs
    asm.extend([
        '@SP',
        'D=M',
        '@5',
        'D=D-A'])
    for i in range(int(args[2])):
        asm.extend(['D=D-1']) # calculate index
    asm.extend([
        '@ARG',
        'M=D'])



 #   LCL = SP
    asm.extend([
        '@SP',
        'D=M',
        '@LCL',
        'M=D'])

 #   goto functionName
    asm.extend([
        '@fn_'+args[1],
        'D;JMP'])

 #   (retAddrLabel)
    asm.extend([
        '('+retAddrLabel+')'])

    function_return_index += 1
 
    return asm
    
def c_function(line):
    args = line.split()
    #args0 function
    #args1 functionName
    #args2 nVars
    
    pushDtoSP = [
    '@SP',
    'A=M',
    'M=D',
    'D=A+1',
    '@SP',
    'M=D']
 #  push 0 (x nVars)
 
    asm = []
    asm.extend([
        '(fn_'+args[1]+')'])
    for i in range(int(args[2])):
        asm.extend(['D=0']) # calculate index
        asm.extend(pushDtoSP)
 
    return asm 
 
 
def c_return(line):

    asm = [
    
    #   endFrame = LCL
    '@LCL',
    'D=M',
    '@endFrame',
    'M=D',
    #   retAddr = *(endFrame – 5) // gets the return address
    '@5',
    'A=D-A',
    'D=M',
    '@retAddr',
    'M=D',
    #   *ARG = pop() // puts the return value for the caller
    '@SP',
    'AM=M-1',
    'D=M',
    '@ARG',
    'A=M',
    'M=D',
#   SP = ARG + 1 // repositions SP
    '@ARG',
    'D=M+1',
    '@SP',
    'M=D',
#   THAT = *(endFrame – 1) // restores THAT
    '@endFrame',
    'A=M-1',
    'D=M',
    '@THAT',
    'M=D',
#   THIS = *(endFrame – 2) // restores THIS
    '@endFrame',
    'A=M-1',
    'A=A-1',
    'D=M',
    '@THIS',
    'M=D',
#   ARG = *(endFrame – 3) // restores ARG
    '@endFrame',
    'A=M-1',
    'A=A-1',
    'A=A-1',
    'D=M',
    '@ARG',
    'M=D',
#   LCL = *(endFrame – 4) // restores LCL
    '@endFrame',
    'A=M-1',
    'A=A-1',
    'A=A-1',
    'A=A-1',
    'D=M',
    '@LCL',
    'M=D',
#   goto retAddr
 
    
        '@retAddr',
        'A=M','D;JMP']
        
    return asm
        
def print_progress_bar(message, current, total, bar_length=40):
    percent = current / total
    filled = int(bar_length * percent)
    bar =  message + '█' * filled + '-' * (bar_length - filled)
    print(f'\r|{bar}| {percent:.0%}', end='')
    sys.stdout.flush()
 

statics_offset = 0 


if len(sys.argv) < 2:
    print("Usage: python hackassm.py <filename>")
    sys.exit(1)


# filename = sys.argv[1]

base, _ = os.path.splitext(sys.argv[1])
output_filename = base + '.asm'
open(output_filename,'w').close() # delete output file contents


output = []

output.extend([
    '//BOOTSTRAP',
    '@256',
    'D=A',
    '@SP',
    'M=D'])
output.extend(c_call('call Sys.init 0'))
output.extend(['//BOOTSTRAP END'])


# Need to pass all filenames as arguments
# Wildcards don't work
# Output file is first argument filename renamed as .asm

lines = []
for filename in sys.argv[1:]:
    with open(filename, 'r') as file:
        output.extend(['///////////'+filename])

        lines = file.readlines()

        i = 0
        for line in lines:
            print_progress_bar('filename:',i,len(lines)-1)
            i+=1
        #    line = ''.join(line.split())        # Remove all whitespace characters
            line = line.split('//')[0]          # Remove anything after '//' (including the slashes)
         

            if not ''.join(line.split()):
                continue
                
            output.extend(['\n// '+line])

            if line.split()[0] == 'push':
                output.extend(c_push(line))
            elif line.split()[0] == 'pop':
                output.extend(c_pop(line))

            elif line.split()[0] in arithmetic_sym:
                output.extend(c_arithmetic(line.split()[0]))
                
            elif line.split()[0] in branch_sym:
                output.extend(c_branching(line))

            elif line.split()[0] == 'call':
                output.extend(c_call(line))

            elif line.split()[0] == 'function':
                output.extend(c_function(line))
                    
            elif line.split()[0] == 'return':
                output.extend(c_return(line))

    statics_offset += 16

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
