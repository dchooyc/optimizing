# Why pointers
The fastest way to pass data across two variables is using pointers.

The reason is that on the underlying level of the programming language, using pointers requires lesser instructions in assembly than swapping two values without using pointers.

The difference in performance is significant when the data being passed across the two variables is a larger data structure.

To test the difference in performance, install golang and run ```go run pointers.go``` or simply run ```./pointers```. The first line to be printed shows the time taken when using pointers and the second line shows the time take without using pointers. On average for the size of the test data generated, on my machine using pointers takes about 10ms while without using pointers takes about 16ms.

The generated assembly code of the go program can be found by running ```go tool objdump -S pointers``` or by looking in the generated-assembly.txt file.

The speed difference for using pointers vs without using pointers seems to correspond to the number of lines generated for the function in assembly.

Here is the assembly code for the ```swapWithPointers``` function. (26 lines)
```
		swapWithPointers(&a, &b)
  0x4853f9		90			NOPL			
	temp := *a
  0x4853fa		488dbc2438010000	LEAQ 0x138(SP), DI	
  0x485402		488db42418030000	LEAQ 0x318(SP), SI	
  0x48540a		48896c24f0		MOVQ BP, -0x10(SP)	
  0x48540f		488d6c24f0		LEAQ -0x10(SP), BP	
  0x485414		e8b393fdff		CALL 0x45e7cc		
  0x485419		488b6d00		MOVQ 0(BP), BP		
	*a = *b
  0x48541d		488dbc2418030000	LEAQ 0x318(SP), DI	
  0x485425		488db424f8010000	LEAQ 0x1f8(SP), SI	
  0x48542d		660f1f840000000000	NOPW 0(AX)(AX*1)	
  0x485436		660f1f840000000000	NOPW 0(AX)(AX*1)	
  0x48543f		90			NOPL			
  0x485440		48896c24f0		MOVQ BP, -0x10(SP)	
  0x485445		488d6c24f0		LEAQ -0x10(SP), BP	
  0x48544a		e87d93fdff		CALL 0x45e7cc		
  0x48544f		488b6d00		MOVQ 0(BP), BP		
	*b = temp
  0x485453		488dbc24f8010000	LEAQ 0x1f8(SP), DI	
  0x48545b		488db42438010000	LEAQ 0x138(SP), SI	
  0x485463		48896c24f0		MOVQ BP, -0x10(SP)	
  0x485468		488d6c24f0		LEAQ -0x10(SP), BP	
  0x48546d		e85a93fdff		CALL 0x45e7cc		
  0x485472		488b6d00		MOVQ 0(BP), BP	
```

Here is the assembly code for the ```swapWithoutPointers``` function. (45 lines)
```
		a, b = swapWithoutPointers(a, b)
  0x485593		488dbc2458020000	LEAQ 0x258(SP), DI	
  0x48559b		488db424b8020000	LEAQ 0x2b8(SP), SI	
  0x4855a3		48896c24f0		MOVQ BP, -0x10(SP)	
  0x4855a8		488d6c24f0		LEAQ -0x10(SP), BP	
  0x4855ad		e81a92fdff		CALL 0x45e7cc		
  0x4855b2		488b6d00		MOVQ 0(BP), BP		
  0x4855b6		488dbc24d8000000	LEAQ 0xd8(SP), DI	
  0x4855be		488db42498010000	LEAQ 0x198(SP), SI	
  0x4855c6		48896c24f0		MOVQ BP, -0x10(SP)	
  0x4855cb		488d6c24f0		LEAQ -0x10(SP), BP	
  0x4855d0		e8f791fdff		CALL 0x45e7cc		
  0x4855d5		488b6d00		MOVQ 0(BP), BP		
  0x4855d9		488d7c2478		LEAQ 0x78(SP), DI	
  0x4855de		488db42458020000	LEAQ 0x258(SP), SI	
  0x4855e6		48896c24f0		MOVQ BP, -0x10(SP)	
  0x4855eb		488d6c24f0		LEAQ -0x10(SP), BP	
  0x4855f0		e8d791fdff		CALL 0x45e7cc		
  0x4855f5		488b6d00		MOVQ 0(BP), BP		
  0x4855f9		488dbc24d8030000	LEAQ 0x3d8(SP), DI	
  0x485601		488db424d8000000	LEAQ 0xd8(SP), SI	
  0x485609		48896c24f0		MOVQ BP, -0x10(SP)	
  0x48560e		488d6c24f0		LEAQ -0x10(SP), BP	
  0x485613		e8b491fdff		CALL 0x45e7cc		
  0x485618		488b6d00		MOVQ 0(BP), BP		
  0x48561c		488dbc2478030000	LEAQ 0x378(SP), DI	
  0x485624		488d742478		LEAQ 0x78(SP), SI	
  0x485629		48896c24f0		MOVQ BP, -0x10(SP)	
  0x48562e		488d6c24f0		LEAQ -0x10(SP), BP	
  0x485633		e89491fdff		CALL 0x45e7cc		
  0x485638		488b6d00		MOVQ 0(BP), BP		
  0x48563c		488dbc24b8020000	LEAQ 0x2b8(SP), DI	
  0x485644		488db424d8030000	LEAQ 0x3d8(SP), SI	
  0x48564c		48896c24f0		MOVQ BP, -0x10(SP)	
  0x485651		488d6c24f0		LEAQ -0x10(SP), BP	
  0x485656		e87191fdff		CALL 0x45e7cc		
  0x48565b		488b6d00		MOVQ 0(BP), BP		
  0x48565f		488dbc2498010000	LEAQ 0x198(SP), DI	
  0x485667		488db42478030000	LEAQ 0x378(SP), SI	
  0x48566f		660f1f840000000000	NOPW 0(AX)(AX*1)	
  0x485678		0f1f840000000000	NOPL 0(AX)(AX*1)	
  0x485680		48896c24f0		MOVQ BP, -0x10(SP)	
  0x485685		488d6c24f0		LEAQ -0x10(SP), BP	
  0x48568a		e83d91fdff		CALL 0x45e7cc		
  0x48568f		488b6d00		MOVQ 0(BP), BP	
```