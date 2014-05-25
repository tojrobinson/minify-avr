.def tmp = r16

.macro push_macro 
   push tmp
.endmacro

.macro pop_macro
   pop tmp
.endmacro

.cseg
.org 0x0

rjmp main

foo:
   push_macro
   ldi tmp, 42
   pop_macro
   ret

main:
   rcall foo

   idle: rjmp idle
