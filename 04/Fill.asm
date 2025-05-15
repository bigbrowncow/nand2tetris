// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.

//infite loop
(LOOP)
//test for keydown
@KBD
D=M
@keydown
D;JGT
@LOOP
0;JMP

(keydown)
//@SCREEN
//turns first 16 pixels black
//M=-1

//turns first 16,320 pixels black
@16320
D=A
(bl)
@SCREEN
A=D+A
D=D-1
M=-1
@bl
D;JGE




(LOOP2)
@KBD
D=M
@keyup
D;JEQ
@LOOP2
0;JMP

(keyup)
//turns first 16,320 pixels black
@16320
D=A
(wh)
@SCREEN
A=D+A
D=D-1
M=0
@wh
D;JGE


//screen is 512 x 255
//so each row is 64 bytes... we need to do this 16,320 times!


//need to check for release and turn screen white


@LOOP
D;JMP


@END
(END)
0;JMP
