"""
  ____          _____               _ _           _       
 |  _ \        |  __ \             (_) |         | |      
 | |_) |_   _  | |__) |_ _ _ __ _____| |__  _   _| |_ ___ 
 |  _ <| | | | |  ___/ _` | '__|_  / | '_ \| | | | __/ _ \
 | |_) | |_| | | |  | (_| | |   / /| | |_) | |_| | ||  __/
 |____/ \__, | |_|   \__,_|_|  /___|_|_.__/ \__, |\__\___|
         __/ |                               __/ |        
        |___/                               |___/         
    
____________________________________
/ Si necesitas ayuda, contáctame en \
\ https://parzibyte.me               /
 ------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
Creado por Parzibyte (https://parzibyte.me).
------------------------------------------------------------------------------------------------
            | IMPORTANTE |
Si vas a borrar este encabezado, considera:
Seguirme: https://parzibyte.me/blog/sigueme/
Y compartir mi blog con tus amigos
También tengo canal de YouTube: https://www.youtube.com/channel/UCroP4BTWjfM0CkGB6AFUoBg?sub_confirmation=1
Twitter: https://twitter.com/parzibyte
Facebook: https://facebook.com/parzibyte.fanpage
Instagram: https://instagram.com/parzibyte
Hacer una donación vía PayPal: https://paypal.me/LuisCabreraBenito
------------------------------------------------------------------------------------------------
"""
import random
import os
"""
Deshabilitar mensaje inicial de PyGame. Al final solo lo usamos para los sonidos
"""
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "sí"
import pygame

pygame.init()
pygame.mixer.init()

sonido_acertado = pygame.mixer.Sound("acertado.wav")
sonido_fallado = pygame.mixer.Sound("fallado.wav")

FILAS = 5
COLUMNAS = 5
MAR = " "
SUBMARINO = "S"  # Ocupa una celda
DESTRUCTOR = "D"  # Ocupa dos celdas
DESTRUCTOR_VERTICAL = "A"  # Ocupa dos celdas
DISPARO_FALLADO = "-"
DISPARO_ACERTADO = "*"
DISPAROS_INICIALES = 10
CANTIDAD_BARCOS_INICIALES = 8
JUGADOR_1 = "J1"
JUGADOR_2 = "J2"


def obtener_matriz_inicial():
    matriz = []
    for y in range(FILAS):
        # Agregamos un arreglo a la matriz, que sería una fila básicamente
        matriz.append([])
        for x in range(COLUMNAS):
            # Y luego agregamos una celda a esa fila. Por defecto lleva "Mar"
            matriz[y].append(MAR)
    return matriz


def incrementar_letra(letra):
    return chr(ord(letra)+1)


def imprimir_separador_horizontal():
    # Imprimir un renglón dependiendo de las columnas
    for _ in range(COLUMNAS+1):
        print("+---", end="")
    print("+")


def imprimir_fila_de_numeros():
    print("|   ", end="")
    for x in range(COLUMNAS):
        print(f"| {x+1} ", end="")
    print("|")


# Indica si una coordenada de la matriz está vacía
def es_mar(x, y, matriz):
    return matriz[y][x] == MAR


def coordenada_en_rango(x, y):
    return x >= 0 and x <= COLUMNAS-1 and y >= 0 and y <= FILAS-1


def colocar_e_imprimir_barcos(matriz, cantidad_barcos, jugador):
    # Dividimos y redondeamos a entero hacia abajo (ya que no podemos colocar una parte no entera de un barco)
    barcos_una_celda = cantidad_barcos//2
    barcos_dos_celdas_verticales = cantidad_barcos//4
    barcos_dos_celdas_horizontales = cantidad_barcos//4
    if jugador == JUGADOR_1:
        print("Imprimiendo barcos del jugador 1 ")
    else:
        print("Imprimiendo barcos del jugador 2 ")
    print(f"Barcos de una celda: {barcos_una_celda}\nBarcos verticales de dos celdas: {barcos_dos_celdas_verticales}\nBarcos horizontales de dos celdas: {barcos_dos_celdas_horizontales}\nTotal: {barcos_una_celda+barcos_dos_celdas_verticales+barcos_dos_celdas_horizontales}")
    # Primero colocamos los de dos celdas para que se acomoden bien
    matriz = colocar_barcos_de_dos_celdas_horizontal(
        barcos_dos_celdas_horizontales, DESTRUCTOR, matriz)
    matriz = colocar_barcos_de_dos_celdas_vertical(
        barcos_dos_celdas_verticales, DESTRUCTOR_VERTICAL, matriz)
    matriz = colocar_barcos_de_una_celda(barcos_una_celda, SUBMARINO, matriz)
    return matriz


def obtener_x_aleatoria():
    return random.randint(0, COLUMNAS-1)


def obtener_y_aleatoria():
    return random.randint(0, FILAS-1)


def colocar_barcos_de_una_celda(cantidad, tipo_barco, matriz):
    barcos_colocados = 0
    while True:
        x = obtener_x_aleatoria()
        y = obtener_y_aleatoria()
        if es_mar(x, y, matriz):
            matriz[y][x] = tipo_barco
            barcos_colocados += 1
        if barcos_colocados >= cantidad:
            break
    return matriz


def colocar_barcos_de_dos_celdas_horizontal(cantidad, tipo_barco, matriz):
    barcos_colocados = 0
    while True:
        x = obtener_x_aleatoria()
        y = obtener_y_aleatoria()
        x2 = x+1
        if coordenada_en_rango(x, y) and coordenada_en_rango(x2, y) and es_mar(x, y, matriz) and es_mar(x2, y, matriz):
            matriz[y][x] = tipo_barco
            matriz[y][x2] = tipo_barco
            barcos_colocados += 1
        if barcos_colocados >= cantidad:
            break
    return matriz


def colocar_barcos_de_dos_celdas_vertical(cantidad, tipo_barco, matriz):
    barcos_colocados = 0
    while True:
        x = obtener_x_aleatoria()
        y = obtener_y_aleatoria()
        y2 = y+1
        if coordenada_en_rango(x, y) and coordenada_en_rango(x, y2) and es_mar(x, y, matriz) and es_mar(x, y2, matriz):
            matriz[y][x] = tipo_barco
            matriz[y2][x] = tipo_barco
            barcos_colocados += 1
        if barcos_colocados >= cantidad:
            break
    return matriz


def imprimir_disparos_restantes(disparos_restantes, jugador):
    print(f"Disparos restantes de {jugador}: {disparos_restantes}")


def imprimir_matriz(matriz, deberia_mostrar_barcos, jugador):
    print(f"Este es el mar del jugador {jugador}: ")
    letra = "A"
    for y in range(FILAS):
        imprimir_separador_horizontal()
        print(f"| {letra} ", end="")
        for x in range(COLUMNAS):
            celda = matriz[y][x]
            valor_real = celda
            if not deberia_mostrar_barcos and valor_real != MAR and valor_real != DISPARO_FALLADO and valor_real != DISPARO_ACERTADO:
                valor_real = " "
            print(f"| {valor_real} ", end="")
        letra = incrementar_letra(letra)
        print("|",)  # Salto de línea
    imprimir_separador_horizontal()
    imprimir_fila_de_numeros()
    imprimir_separador_horizontal()


def solicitar_coordenadas(jugador):
    print(f"Solicitando coordenadas de disparo al jugador {jugador}")
    # Ciclo infinito. Se rompe cuando ingresan una fila correcta
    y = None
    x = None
    while True:
        letra_fila = input(
            "Ingresa la letra de la fila tal y como aparece en el tablero: ")
        # Necesitamos una letra de 1 carácter. Si no es de 1 carácter usamos continue para repetir este ciclo
        if len(letra_fila) != 1:
            print("Debes ingresar únicamente una letra")
            continue
        # Convertir la letra a un índice para acceder a la matriz
        # La A equivale al ASCII 65, la B al 66, etcétera. Para convertir la letra a índice
        # convertimos la letra a su ASCII y le restamos 65 (el 65 es el ASCII de la A, por lo que A es 0)
        y = ord(letra_fila) - 65
        # Verificar si es válida. En caso de que sí, rompemos el ciclo
        if coordenada_en_rango(0, y):
            break
        else:
            print("Fila inválida")
    # Hacemos lo mismo pero para la columna
    while True:
        try:
            x = int(input("Ingresa el número de columna: "))
            if coordenada_en_rango(x-1, 0):
                x = x-1  # Queremos el índice, así que restamos un 1 siempre
                break
            else:
                print("Columna inválida")
        except:
            print("Ingresa un número válido")

    return x, y


def disparar(x, y, matriz) -> bool:
    if es_mar(x, y, matriz):
        matriz[y][x] = DISPARO_FALLADO
        return False
    # Si ya había disparado antes, se le cuenta como falla igualmente
    elif matriz[y][x] == DISPARO_FALLADO or matriz[y][x] == DISPARO_ACERTADO:
        return False
    else:
        matriz[y][x] = DISPARO_ACERTADO
        return True


def oponente_de_jugador(jugador):
    if jugador == JUGADOR_1:
        return JUGADOR_2
    else:
        return JUGADOR_1


def todos_los_barcos_hundidos(matriz):
    for y in range(FILAS):
        for x in range(COLUMNAS):
            celda = matriz[y][x]
            # Si no es mar o un disparo, significa que todavía hay un barco por ahí
            if celda != MAR and celda != DISPARO_ACERTADO and celda != DISPARO_FALLADO:
                return False
    # Acabamos de recorrer toda la matriz y no regresamos en la línea anterior. Entonces todos los barcos han sido hundidos
    return True


def indicar_victoria(jugador):
    print(f"Fin del juego\nEl jugador {jugador} es el ganador")


def indicar_fracaso(jugador):
    print(
        f"Fin del juego\nEl jugador {jugador} pierde. Se han acabado sus disparos")


def imprimir_matrices_con_barcos(matriz_j1, matriz_j2):
    print("Mostrando ubicación de los barcos de ambos jugadores:")
    imprimir_matriz(matriz_j1, True, JUGADOR_1)
    imprimir_matriz(matriz_j2, True, JUGADOR_2)


def jugar():
    disparos_restantes_j1 = DISPAROS_INICIALES
    disparos_restantes_j2 = DISPAROS_INICIALES
    cantidad_barcos = 5
    matriz_j1, matriz_j2 = obtener_matriz_inicial(), obtener_matriz_inicial()
    matriz_j1 = colocar_e_imprimir_barcos(
        matriz_j1, cantidad_barcos, JUGADOR_1)
    matriz_j2 = colocar_e_imprimir_barcos(
        matriz_j2, cantidad_barcos, JUGADOR_2)
    turno_actual = JUGADOR_1
    print("===============")
    while True:
        print(f"Turno de {turno_actual}")
        disparos_restantes = disparos_restantes_j2
        if turno_actual == JUGADOR_1:
            disparos_restantes = disparos_restantes_j1
        imprimir_disparos_restantes(disparos_restantes, turno_actual)
        matriz_oponente = matriz_j1
        if turno_actual == JUGADOR_1:
            matriz_oponente = matriz_j2
        imprimir_matriz(matriz_oponente, False,
                        oponente_de_jugador(turno_actual))
        x, y = solicitar_coordenadas(turno_actual)
        acertado = disparar(x, y, matriz_oponente)
        if turno_actual == JUGADOR_1:
            disparos_restantes_j1 -= 1
        else:
            disparos_restantes_j2 -= 1

        imprimir_matriz(matriz_oponente, False,
                        oponente_de_jugador(turno_actual))
        if acertado:
            print("Disparo acertado")
            reproducir_sonido_acertado()
            if todos_los_barcos_hundidos(matriz_oponente):
                indicar_victoria(turno_actual)
                imprimir_matrices_con_barcos(matriz_j1, matriz_j2)
                break
        else:
            print("Disparo fallado")
            reproducir_sonido_error()
            if disparos_restantes-1 <= 0:
                indicar_fracaso(turno_actual)
                imprimir_matrices_con_barcos(matriz_j1, matriz_j2)
                break
            turno_actual = oponente_de_jugador(turno_actual)


def acerca_de():
    print("Programado por Luis Cabrera Benito a.k.a. Parzibyte")


def mostrar_menu():
    eleccion = ""
    while eleccion != "3":
        menu = """
1. Jugar
2. Acerca de
3. Salir
Elige: """
        eleccion = input(menu)
        if eleccion == "1":
            jugar()
        elif eleccion == "2":
            acerca_de()


def reproducir_sonido_acertado():
    pygame.mixer.Sound.play(sonido_acertado)


def reproducir_sonido_error():
    pygame.mixer.Sound.play(sonido_fallado)


mostrar_menu()
