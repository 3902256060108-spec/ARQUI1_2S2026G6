.global _start

.section .data
mensaje:
    .ascii "Hola desde ARM64\n"
longitud = . - mensaje

.section .text

_start:
    mov x0, #1
    ldr x1, =mensaje
    mov x2, #longitud
    mov x8, #64
    svc #0

    mov x0, #0
    mov x8, #93
    svc #0
    