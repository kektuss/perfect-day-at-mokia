
import pygame

pygame.init()

# ============================================================
# SETTINGS
# ============================================================

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
FPS = 60

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mokia")

clock = pygame.time.Clock()


# ============================================================
# GAME STATE
# ============================================================

game_state = "INTRO"

day = 1
stress = 100

interns = []
snacks = []


# ============================================================
# PLAYER / OFFICE WORKER
# ============================================================

# Player properties
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2
player_speed = 5

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

# Load player image
player_image = pygame.image.load("assets/player.jpg")

# Resize player image
player_image = pygame.transform.scale(
    player_image,
    (PLAYER_WIDTH, PLAYER_HEIGHT)
)


def update_player():
    global player_x, player_y

    keys = pygame.key.get_pressed()

    # Movement
    if keys[pygame.K_w]:
        player_y -= player_speed

    if keys[pygame.K_s]:
        player_y += player_speed

    if keys[pygame.K_a]:
        player_x -= player_speed

    if keys[pygame.K_d]:
        player_x += player_speed

    # Keep player inside the screen
    player_x = max(0, min(player_x, SCREEN_WIDTH - PLAYER_WIDTH))
    player_y = max(0, min(player_y, SCREEN_HEIGHT - PLAYER_HEIGHT))


def draw_player():
    SCREEN.blit(player_image, (player_x, player_y))


# ============================================================
# CUTSCENES
# ============================================================

FONT_MAIN = pygame.font.SysFont("georgia", 32)
FONT_SMALL = pygame.font.SysFont("georgia", 20)

lines = [
    "In the Nokia Ottawa Office...",
    "...the towers are divided.",
    "Meet your office worker. Stress: rising.",
    "Work is piling up. The snack table is under threat.",
    "Defend your tower. Don't let those interns get to the snacks!",
]

line_index = 0


def update_cutscene():
    pass


def draw_cutscene():
    # Clear the screen before drawing the cutscene
    SCREEN.fill((251, 198, 207))

    text = FONT_MAIN.render(
        lines[line_index],
        True,
        (255, 255, 255)
    )

    SCREEN.blit(
        text,
        (
            SCREEN_WIDTH // 2 - text.get_width() // 2,
            SCREEN_HEIGHT // 2
        )
    )

    prompt = FONT_SMALL.render(
        "Press SPACE to continue",
        True,
        (180, 180, 180)
    )

    SCREEN.blit(
        prompt,
        (
            SCREEN_WIDTH // 2 - prompt.get_width() // 2,
            SCREEN_HEIGHT - 60
        )
    )


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

STRESS_BAR_WIDTH = 250
STRESS_BAR_HEIGHT = 25

STRESS_BAR_X = SCREEN_WIDTH - STRESS_BAR_WIDTH - 30
STRESS_BAR_Y = 30


def update_stress():
    global stress

    # Keep stress between 0 and 100
    stress = max(0, min(stress, 100))


def draw_stress_bar():

    # Stress label
    stress_text = FONT_SMALL.render(
        f"STRESS: {stress}%",
        True,
        (255, 255, 255)
    )

    SCREEN.blit(
        stress_text,
        (
            STRESS_BAR_X,
            STRESS_BAR_Y - 25
        )
    )

    # Background of the bar
    pygame.draw.rect(
        SCREEN,
        (70, 70, 70),
        (
            STRESS_BAR_X,
            STRESS_BAR_Y,
            STRESS_BAR_WIDTH,
            STRESS_BAR_HEIGHT
        )
    )

    # Filled portion of the bar
    filled_width = int(
        STRESS_BAR_WIDTH * (stress / 100)
    )

    pygame.draw.rect(
        SCREEN,
        (220, 70, 70),
        (
            STRESS_BAR_X,
            STRESS_BAR_Y,
            filled_width,
            STRESS_BAR_HEIGHT
        )
    )

    # Border
    pygame.draw.rect(
        SCREEN,
        (255, 255, 255),
        (
            STRESS_BAR_X,
            STRESS_BAR_Y,
            STRESS_BAR_WIDTH,
            STRESS_BAR_HEIGHT
        ),
        2
    )


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
    # Clear the previous frame
    SCREEN.fill((40, 90, 40))

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

running = True

while running:

    # --------------------------------------------------------
    # EVENTS
    # --------------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Cutscene controls
        if game_state == "INTRO":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    line_index += 1

                    # Finished all cutscene lines
                    if line_index >= len(lines):
                        game_state = "GAMEPLAY"


    # --------------------------------------------------------
    # UPDATE + DRAW
    # --------------------------------------------------------

    if game_state == "INTRO":

        update_cutscene()
        draw_cutscene()

    elif game_state == "GAMEPLAY":

        update_gameplay()
        draw_gameplay()

    elif game_state == "ENDING":

        update_ending()
        draw_ending()


    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
