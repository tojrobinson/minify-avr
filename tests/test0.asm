.include "m64def.inc"

.def tmp = r16
.def tmp_2 =           r17

.equ LONG_VALUE_NAME = 7

rjmp main
; newest func
main:
   ldi tmp, LONG_VALUE_NAME

; load addr of some_string into tmp and tmp_2
  ld tmp, low(some_string)

ld tmp_2, high(some_string)

; wait
      idle:
   rjmp idle



; my pro string yo
some_string: .db "taco sammich some_string", 0

