import pygame

# Inicializar pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Error Léxico")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Fuente
font = pygame.font.Font(None, 36)

def mostrar_error_lexico(mensaje):
    running = True
    while running:
        screen.fill(WHITE)  # Fondo blanco

        # Renderizar mensaje de error
        error_text = font.render("Error Léxico:", True, RED)
        message_text = font.render(mensaje, True, RED)

        # Dibujar en la pantalla
        screen.blit(error_text, (50, 150))
        screen.blit(message_text, (50, 200))

        pygame.display.flip()

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Cerrar la ventana
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # Presionar Enter para salir
                running = False

    pygame.quit()

# Ejemplo de uso con un mensaje de error
# mostrar_error_lexico("Símbolo inesperado en la línea 3")
