import pygame, sys, time
from pygame.locals import *
from pygame_functions import *

## Colores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

screenSize(1280,720)
pygame.init()
pygame.mixer.init()
print("orlandi.dev - hello world")
pygame.display.set_caption("Landi")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Fondo
#setBackgroundImage("background.jpg")
setBackgroundImage("background2.png")

# Personaje
character = makeSprite("SteamMan_walk.png", 6)
characterAttack1 = makeSprite("SteamMan_attack1.png", 6)
transformSprite(character, 360, 2.0)
transformSprite(characterAttack1, 0, 2.0)
showSprite(character)
xPos = 50
yPos = 520
xSpeed = 0
ySpeed = 0
running = True
moveSprite(character, xPos, yPos)

nextFrame = clock()
frame = 0

frame_duration = 60  # Duración de cada frame en milisegundos
next_frame_time = clock() + frame_duration
is_attacking_z = False  # Variable para rastrear si se está atacando con "Z"
is_attacking_x = False  # Variable para rastrear si se está atacando con "X"
current_sprite = "walk"  # Sprite actual
z_key_pressed = False  # Variable para rastrear si la tecla "Z" está presionada
x_key_pressed = False  # Variable para rastrear si la tecla "X" está presionada
character_transformed = False  # Variable para rastrear si el personaje está transformado
prev_z_key_pressed = False  # Variable para rastrear si la tecla "Z" estaba presionada previamente

# Variables de salto
ySpeed = 0
is_jumping = False
jump_power = -12  # Ajusta la fuerza de salto según tus necesidades
gravity = 1    # Ajusta la gravedad según tus necesidades


while running:

    if (clock() > nextFrame):
        frame = (frame + 1) % 6
        nextFrame += 60

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                z_key_pressed = True
            elif event.key == pygame.K_x:
                x_key_pressed = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                z_key_pressed = False
                transformSprite(character, 360, 2.0, True, False)
                prev_z_key_pressed = True
            elif event.key == pygame.K_x:
                x_key_pressed = False



    if keyPressed("right"):
        xSpeed = 8
        if keyPressed("up") and not is_jumping:
            ySpeed = jump_power
            is_jumping = True

    elif keyPressed("left"):
        xSpeed = -8
        if keyPressed("up") and not is_jumping:
            ySpeed = jump_power
            is_jumping = True

    elif keyPressed("up") and not is_jumping:
        ySpeed = jump_power
        is_jumping = True
    else:
        xSpeed = 0

     # Aplicar gravedad
    ySpeed += gravity

    # Mover al personaje verticalmente
    yPos += ySpeed

    if (yPos <= 50 or yPos >= 521) and not (xPos > 690 and xPos < 840):
        yPos = 520
        ySpeed = 0
        gravity = 1.0
        is_jumping = False


    # Verificar si la tecla Z está presionada
    if keyPressed("z"):
        xSpeed = -0.0001
        is_attacking_z = True
        changeSpriteImage(characterAttack1, 0 * 6 + frame)
        transformSprite(characterAttack1, 360, 2.0, True, False)
    else:
        is_attacking_z = False

    if keyPressed("x"):
        xSpeed = 0.0001
        is_attacking_x = True
        changeSpriteImage(characterAttack1, 0 * 6 + frame)
    else:
        is_attacking_x = False

    # Cambiar el sprite y aplicar la transformación
    if clock() > next_frame_time:
        frame = (frame + 1) % 6

        if is_attacking_z:
            if current_sprite != "attack1_z" and current_sprite != "attack1_x":
                xSpeed = 0
                gravity = 1
                hideSprite(character)
                moveSprite(characterAttack1, xPos, yPos)
                showSprite(characterAttack1)
                current_sprite = "attack1_z"
        elif is_attacking_x:
            if current_sprite != "attack1_x" and current_sprite != "attack1_z":
                xSpeed = 0
                gravity = 1
                hideSprite(character)
                moveSprite(characterAttack1, xPos, yPos)
                showSprite(characterAttack1)
                current_sprite = "attack1_x"
        else:
            if current_sprite != "walk":
                xSpeed = -2
                hideSprite(characterAttack1)
                changeSpriteImage(character, 0 * 6 + frame)
                if current_sprite == "attack1_z":
                    transformSprite(character, 360, 2.0, True, False)
                moveSprite(character, xPos, yPos)
                showSprite(character)
                current_sprite = "attack1_z"
                current_sprite = "attack1_x"
                current_sprite = "walk"

        if xSpeed > 0 and is_attacking_z == False and is_attacking_x == False:
            changeSpriteImage(character, 0 * 6 + frame)

            # Verifica si la tecla "Z" estaba presionada previamente y aplica la transformación
            if prev_z_key_pressed and not character_transformed:
                transformSprite(character, 360, 2.0, True, False)
                character_transformed = True

        elif xSpeed < 0 and is_attacking_z == False and is_attacking_x == False:
            changeSpriteImage(character, 0 * 6 + frame)
            transformSprite(character, 360, 2.0, True, False)

            # Verifica si la tecla "Z" estaba presionada previamente y aplica la transformación
            if prev_z_key_pressed and not character_transformed:
                transformSprite(character, 360, 2.0, True, False)
                character_transformed = True

        next_frame_time = clock() + frame_duration

    xPos += xSpeed
    if xPos > 1270:
        xPos = -50
    elif xPos < -50:
        xPos = 1270

    yPos += ySpeed
    if yPos > 710:
        yPos = -50
    elif yPos < -50:
        yPos = 710

    moveSprite(character, xPos, yPos)
    moveSprite(characterAttack1, xPos, yPos)
    tick(30)

endWait()