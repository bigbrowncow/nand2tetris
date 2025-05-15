// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

//// Replace this comment with your code.


@R2
M=0


@R0
//move R0 into counter
D=M
@END
D;JEQ
//use i as counter
@i
M=D

(LOOP)
//add R1 onto R2
@R1
D=M
@R2
M=D+M

//reduce i by 1
@i
M=M-1
D=M
//go back to Loop if i>1
@LOOP
D;JGT


(END)
@END
0;JMP	//FOREVER LOOP