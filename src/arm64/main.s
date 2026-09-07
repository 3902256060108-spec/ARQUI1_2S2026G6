.global _start



// CONSTANTES
.equ AT_FDCWD,   -100

.equ O_RDONLY,   0
.equ O_WRONLY,   1
.equ O_CREAT,    64
.equ O_TRUNC,    512

.equ SYS_OPENAT, 56
.equ SYS_CLOSE,  57
.equ SYS_READ,   63
.equ SYS_WRITE,  64
.equ SYS_EXIT,   93



// DATOS
.section .data

nombre_entrada:
    .asciz "datos.txt"

nombre_salida:
    .asciz "resultado.txt"


texto_max:
    .ascii "MAX="
.equ len_texto_max, . - texto_max

texto_min:
    .ascii "MIN="
.equ len_texto_min, . - texto_min

texto_avg:
    .ascii "AVG="
.equ len_texto_avg, . - texto_avg

texto_count:
    .ascii "COUNT="
.equ len_texto_count, . - texto_count


salto_linea:
    .ascii "\n"


mensaje_error_entrada:
    .ascii "Error: no se pudo abrir datos.txt\n"
.equ len_error_entrada, . - mensaje_error_entrada

mensaje_error_salida:
    .ascii "Error: no se pudo crear resultado.txt\n"
.equ len_error_salida, . - mensaje_error_salida

mensaje_sin_datos:
    .ascii "Error: datos.txt no contiene temperaturas\n"
.equ len_sin_datos, . - mensaje_sin_datos



// MEMORIA NO INICIALIZADA
.section .bss

.align 4

buffer_entrada:
    .skip 1024

buffer_numero:
    .skip 32



// CÓDIGO
.section .text



// INICIO
_start:

    
    // 1. ABRIR datos.txt 
    mov x0, #AT_FDCWD
    ldr x1, =nombre_entrada
    mov x2, #O_RDONLY
    mov x3, #0
    mov x8, #SYS_OPENAT
    svc #0

    cmp x0, #0
    b.lt error_entrada

    // x19 = descriptor del archivo de entrada
    mov x19, x0


    
    // 2. LEER datos.txt
    mov x0, x19
    ldr x1, =buffer_entrada
    mov x2, #1024
    mov x8, #SYS_READ
    svc #0

    cmp x0, #0
    b.lt error_lectura

    // x20 = cantidad de bytes leídos
    mov x20, x0


    
    // 3. CERRAR ARCHIVO DE ENTRADA
    mov x0, x19
    mov x8, #SYS_CLOSE
    svc #0


    
    // 4. PREPARAR REGISTROS
    
    // x21 = puntero actual dentro del buffer
    ldr x21, =buffer_entrada

    // x22 = cantidad de bytes restantes
    mov x22, x20

    // x23 = número actual
    mov x23, #0

    // x24 = COUNT
    mov x24, #0

    // x25 = SUMA
    mov x25, #0

    // x26 = MAX
    mov x26, #0

    // x27 = MIN
    mov x27, #0

    // x29 = bandera de fin de archivo
    // 0 = todavía no encontramos '$'
    // 1 = encontramos '$'
    mov x29, #0

    // x17 = bandera de número en construcción
    // 0 = no se han leído dígitos
    // 1 = existe un número pendiente
    mov x17, #0


    
    // 5. PROCESAR BUFFER

    b procesar_buffer




// PROCESAR BUFFER
procesar_buffer:

    // Si ya no quedan bytes, terminar.
    cmp x22, #0
    b.eq fin_procesamiento


    
    // LEER UN BYTE
    ldrb w0, [x21]

    // Avanzar puntero.
    add x21, x21, #1

    // Disminuir bytes restantes.
    sub x22, x22, #1



    // TERMINADOR '$'
    cmp w0, #'$'
    b.eq fin_archivo


    
    // SALTO DE LÍNEA
    cmp w0, #10
    b.ne verificar_retorno

    // Si no hay dígitos pendientes, la línea está vacía.
    cmp x17, #0
    b.eq procesar_buffer

    // Si sí hay un número pendiente, procesarlo.
    b fin_numero



// IGNORAR RETORNO DE CARRO
verificar_retorno:

    cmp w0, #13
    b.eq procesar_buffer



    // VALIDAR DÍGITO
    cmp w0, #'0'
    b.lt procesar_buffer

    cmp w0, #'9'
    b.gt procesar_buffer


    
    // MARCAR QUE EXISTE UN NÚMERO
    mov x17, #1



    // ASCII -> ENTERO
    sub w0, w0, #'0'



    // número = número * 10 + dígito   
    mov x1, #10

    mul x23, x23, x1

    add x23, x23, x0


    b procesar_buffer




// TERMINÓ UN NÚMERO
fin_numero:

    
    // SUMA
    add x25, x25, x23


    
    // PRIMER DATO
    cmp x24, #0
    b.ne comparar_max

    // Primer número:
    // inicializar MAX y MIN con el mismo valor.
    mov x26, x23
    mov x27, x23

    b numero_procesado




// COMPARAR MAX
comparar_max:

    cmp x23, x26
    b.le comparar_min

    // número_actual > MAX
    mov x26, x23




// COMPARAR MIN
comparar_min:

    cmp x23, x27
    b.ge numero_procesado

    // número_actual < MIN
    mov x27, x23




// DATO PROCESADO
numero_procesado:

    // COUNT++
    add x24, x24, #1

    // Reiniciar número actual.
    mov x23, #0

    // Ya no existe un número pendiente.
    mov x17, #0

    // Si llegamos aquí porque encontramos '$',
    // finalizar procesamiento.
    cmp x29, #1
    b.eq fin_procesamiento

    b procesar_buffer




// FIN DE ARCHIVO '$'
fin_archivo:

    // Marcar que encontramos el terminador.
    mov x29, #1

    // Si no existe ningún número pendiente,
    // terminar directamente.
    cmp x17, #0
    b.eq fin_procesamiento

    // Si existe un número pendiente,
    // procesarlo antes de terminar.
    b fin_numero




// FIN DE PROCESAMIENTO
fin_procesamiento:


    // ¿EXISTEN TEMPERATURAS?
    cmp x24, #0
    b.eq sin_datos



    // AVG = SUMA / COUNT
    udiv x28, x25, x24


    
    // CREAR resultado.txt
    mov x0, #AT_FDCWD
    ldr x1, =nombre_salida

    mov x2, #(O_WRONLY | O_CREAT | O_TRUNC)

    // Permisos 0644
    mov x3, #420

    mov x8, #SYS_OPENAT
    svc #0

    cmp x0, #0
    b.lt error_salida

    // x19 = descriptor del archivo resultado.txt
    mov x19, x0


    
    // ESCRIBIR MAX
    mov x0, x19
    ldr x1, =texto_max
    mov x2, #len_texto_max
    mov x8, #SYS_WRITE
    svc #0

    mov x0, x26
    bl escribir_numero

    bl escribir_salto


    
    // ESCRIBIR MIN
    mov x0, x19
    ldr x1, =texto_min
    mov x2, #len_texto_min
    mov x8, #SYS_WRITE
    svc #0

    mov x0, x27
    bl escribir_numero

    bl escribir_salto



    // ESCRIBIR AVG
    mov x0, x19
    ldr x1, =texto_avg
    mov x2, #len_texto_avg
    mov x8, #SYS_WRITE
    svc #0

    mov x0, x28
    bl escribir_numero

    bl escribir_salto


    
    // ESCRIBIR COUNT
    mov x0, x19
    ldr x1, =texto_count
    mov x2, #len_texto_count
    mov x8, #SYS_WRITE
    svc #0

    mov x0, x24
    bl escribir_numero

    bl escribir_salto


    
    // CERRAR resultado.txt
    mov x0, x19
    mov x8, #SYS_CLOSE
    svc #0


    b finalizar




escribir_numero:

    // Guardar dirección de retorno.
    mov x6, x30

    ldr x1, =buffer_numero

    // Ir casi al final del buffer.
    add x1, x1, #31

    // x2 = cantidad de caracteres.
    mov x2, #0


    
    // CASO ESPECIAL: NÚMERO 0
    cmp x0, #0
    b.ne convertir_numero

    mov w3, #'0'

    strb w3, [x1]

    mov x2, #1

    b escribir_buffer_numero




// CONVERTIR ENTERO -> ASCII
convertir_numero:

    mov x4, #10


conversion_loop:

    // x5 = cociente
    udiv x5, x0, x4

    // x3 = residuo
    // residuo = numero - cociente * 10
    msub x3, x5, x4, x0

    // residuo numérico -> ASCII
    add x3, x3, #'0'

    // Movernos una posición hacia atrás.
    sub x1, x1, #1

    // Guardar carácter.
    strb w3, [x1]

    // Incrementar longitud.
    add x2, x2, #1

    // Continuar usando el cociente.
    mov x0, x5

    cmp x0, #0
    b.ne conversion_loop




// ESCRIBIR BUFFER DEL NÚMERO
escribir_buffer_numero:

    mov x0, x19

    mov x8, #SYS_WRITE

    svc #0

    // Recuperar dirección de retorno.
    mov x30, x6

    ret




// ESCRIBIR SALTO DE LÍNEA
escribir_salto:

    mov x0, x19

    ldr x1, =salto_linea

    mov x2, #1

    mov x8, #SYS_WRITE

    svc #0

    ret



// ERROR AL ABRIR ENTRADA
error_entrada:

    mov x0, #2
    ldr x1, =mensaje_error_entrada
    mov x2, #len_error_entrada
    mov x8, #SYS_WRITE
    svc #0

    mov x0, #1
    mov x8, #SYS_EXIT
    svc #0




// ERROR DE LECTURA
error_lectura:

    // Cerrar archivo que ya estaba abierto.
    mov x0, x19
    mov x8, #SYS_CLOSE
    svc #0

    mov x0, #1
    mov x8, #SYS_EXIT
    svc #0




// ERROR AL CREAR SALIDA
error_salida:

    mov x0, #2
    ldr x1, =mensaje_error_salida
    mov x2, #len_error_salida
    mov x8, #SYS_WRITE
    svc #0

    mov x0, #1
    mov x8, #SYS_EXIT
    svc #0



// NO HAY TEMPERATURAS
sin_datos:

    
    mov x0, #AT_FDCWD
    ldr x1, =nombre_salida
    mov x2, #(O_WRONLY | O_CREAT | O_TRUNC)

    // Permisos 0644
    mov x3, #420

    mov x8, #SYS_OPENAT
    svc #0

    cmp x0, #0
    b.lt mostrar_error_sin_datos

    // Guardar descriptor.
    mov x19, x0

    // Cerrar inmediatamente.
    mov x0, x19
    mov x8, #SYS_CLOSE
    svc #0


mostrar_error_sin_datos:

    // Mostrar mensaje por stderr.
    mov x0, #2
    ldr x1, =mensaje_sin_datos
    mov x2, #len_sin_datos
    mov x8, #SYS_WRITE
    svc #0

    // Código de error especial: 2
    mov x0, #2
    mov x8, #SYS_EXIT
    svc #0




// FINALIZAR CORRECTAMENTE
finalizar:

    mov x0, #0

    mov x8, #SYS_EXIT

    svc #0
