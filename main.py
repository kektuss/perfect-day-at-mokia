import pygame

# ============================================================
# SETTINGS
# ============================================================

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
FPS = 60

# ============================================================
# GAME STATE
# ============================================================

game_state = "INTRO"

day = 1
stress = 100

interns = []
snacks = []


# ============================================================
# CUTSCENES
# ============================================================

def update_cutscene():
    pass


def draw_cutscene():
    pass


# ============================================================
# PLAYER / OFFICE WORKER
# ============================================================

def update_player():
    pass


def draw_player():
    pass


# ============================================================
# INTERNS — FRIEND
# ============================================================

def update_interns():
    pass


def draw_interns():
    pass


# ============================================================
# TOWER / MAP — YOU
# ============================================================

def update_tower():
    pass


def draw_tower():
    pass


# ============================================================
# SNACK SYSTEM — YOU
# ============================================================

def update_snacks():
    pass


def draw_snacks():
    pass


# ============================================================
# STRESS SYSTEM — YOU
# ============================================================

def update_stress():
    pass


def draw_stress_bar():
    pass


# ============================================================
# GAMEPLAY
# ============================================================

def update_gameplay():
    update_player()
    update_interns()
    update_tower()
    update_snacks()
    update_stress()


def draw_gameplay():
    draw_tower()
    draw_snacks()
    draw_interns()
    draw_player()
    draw_stress_bar()


# ============================================================
# ENDING
# ============================================================

def update_ending():
    pass


def draw_ending():
    pass


# ============================================================
# MAIN LOOP
# ============================================================

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == "INTRO":
        update_cutscene()
        draw_cutscene()

    elif game_state == "GAMEPLAY":
        update_gameplay()
        draw_gameplay()

    elif game_state == "ENDING":
        update_ending()
        draw_ending()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()