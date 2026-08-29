import pygame
import random

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
stress = 50

interns = []
snacks = []


# ============================================================
# FONTS
# ============================================================

FONT_MAIN = pygame.font.SysFont("georgia", 32)
FONT_SMALL = pygame.font.SysFont("georgia", 20)


# ============================================================
# PLAYER / OFFICE WORKER
# ============================================================

player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2
player_speed = 5

target_person = None

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
    global target_person, stress

    # --------------------------------------------------------
    # CHASING AN INTERN
    # --------------------------------------------------------

    if target_person is not None:

        # Target the center of the intern
        target_x = (
            target_person.x
            + INTERN_WIDTH // 2
            - PLAYER_WIDTH // 2
        )

        # Move left or right toward them
        if player_x < target_x:
            player_x += player_speed

        elif player_x > target_x:
            player_x -= player_speed

        # Player stays at their current Y position
        # while chasing

        # Check if player reached the person
        if abs(player_x - target_x) <= player_speed:

            player_x = target_x

            # Catch the person
            target_person.caught = True

            # Change stress depending on who was caught
            if target_person.has_badge:
                stress += 10
            else:
                stress -= 5

            # Stop chasing
            target_person = None

    # --------------------------------------------------------
    # NORMAL MOVEMENT
    # --------------------------------------------------------

    else:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            player_y -= player_speed

        if keys[pygame.K_s]:
            player_y += player_speed

        if keys[pygame.K_a]:
            player_x -= player_speed

        if keys[pygame.K_d]:
            player_x += player_speed

    # --------------------------------------------------------
    # KEEP PLAYER INSIDE SCREEN
    # --------------------------------------------------------

    player_x = max(
        0,
        min(player_x, SCREEN_WIDTH - PLAYER_WIDTH)
    )

    player_y = max(
        0,
        min(player_y, SCREEN_HEIGHT - PLAYER_HEIGHT)
    )


def draw_player():
    SCREEN.blit(
        player_image,
        (player_x, player_y)
    )


# ============================================================
# CUTSCENES
# ============================================================

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

    # Clear the screen
    SCREEN.fill((251, 198, 207))

    # Main text
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

    # Continue prompt
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

INTERN_WIDTH = 40
INTERN_HEIGHT = 60

spawn_timer = 0
spawn_interval = 90


class Intern:

    def __init__(self, x, y, has_badge):

        self.x = x
        self.y = y

        self.has_badge = has_badge
        self.caught = False

        self.lifetime = 0

        # How long this person stays on screen
        self.max_lifetime = random.randint(180, 360)

        # Staff = blue
        # Intern = lighter blue
        self.color = (
            (100, 149, 237)
            if has_badge
            else (121, 186, 236)
        )


    def get_rect(self):

        return pygame.Rect(
            self.x,
            self.y,
            INTERN_WIDTH,
            INTERN_HEIGHT
        )


    def draw(self):

        rect = self.get_rect()

        pygame.draw.rect(
            SCREEN,
            self.color,
            rect,
            border_radius=8
        )


def spawn_intern():

    while True:

        x = random.randint(
            50,
            SCREEN_WIDTH - INTERN_WIDTH - 50
        )

        # Currently everyone spawns near the top
        y = 200

        new_rect = pygame.Rect(
            x,
            y,
            INTERN_WIDTH,
            INTERN_HEIGHT
        )

        overlapping = False

        # Make sure the new person doesn't overlap
        # an existing person
        for person in interns:

            if new_rect.colliderect(
                person.get_rect()
            ):

                overlapping = True
                break

        if not overlapping:

            # 80% chance of being staff
            has_badge = random.random() < 0.80

            interns.append(
                Intern(
                    x,
                    y,
                    has_badge
                )
            )

            return


def catch_intern(pos):

    global target_person

    for person in interns:

        if person.caught:
            continue

        if person.get_rect().collidepoint(pos):

            # Tell the player to follow this person
            target_person = person

            # Don't mark them as caught yet.
            # They get caught when the player reaches them.
            break


def update_interns():

    global spawn_timer
    global stress
    global target_person

    # --------------------------------------------------------
    # SPAWN PEOPLE
    # --------------------------------------------------------

    spawn_timer += 1

    if spawn_timer >= spawn_interval:

        spawn_timer = 0

        spawn_intern()


    # --------------------------------------------------------
    # UPDATE PEOPLE
    # --------------------------------------------------------

    for person in interns:

        if person.caught:
            continue

        person.lifetime += 1

        # Person leaves when their timer expires.
        #
        # Don't let the person being chased disappear.
        if (
            person.lifetime >= person.max_lifetime
            and person != target_person
        ):

            # Escaped interns increase stress
            if not person.has_badge:
                stress += 5

            # Staff leaving does not change stress

            person.caught = True


    # --------------------------------------------------------
    # REMOVE CAUGHT / ESCAPED PEOPLE
    # --------------------------------------------------------

    interns[:] = [
        person
        for person in interns
        if not person.caught
    ]


def draw_interns():

    for person in interns:
        person.draw()


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

STRESS_BAR_X = (
    SCREEN_WIDTH
    - STRESS_BAR_WIDTH
    - 30
)

STRESS_BAR_Y = 30


def update_stress():

    global stress

    # Keep stress between 0 and 100
    stress = max(
        0,
        min(stress, 100)
    )


def draw_stress_bar():

    # --------------------------------------------------------
    # STRESS LABEL
    # --------------------------------------------------------

    stress_text = FONT_SMALL.render(
        f"STRESS: {int(stress)}%",
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

    # --------------------------------------------------------
    # BAR BACKGROUND
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # FILLED PART
    # --------------------------------------------------------

    filled_width = int(
        STRESS_BAR_WIDTH
        * (stress / 100)
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

    # --------------------------------------------------------
    # BORDER
    # --------------------------------------------------------

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

    # Clear previous frame
    SCREEN.fill((40, 90, 40))

    # Draw game objects
    draw_tower()
    draw_snacks()
    draw_interns()
    draw_player()

    # ========================================================
    # DAY DISPLAY — TOP LEFT
    # ========================================================

    day_text = FONT_SMALL.render(
        f"DAY {day}",
        True,
        (255, 255, 255)
    )

    # Background behind day
    day_background = pygame.Rect(
        20,
        20,
        day_text.get_width() + 20,
        day_text.get_height() + 10
    )

    pygame.draw.rect(
        SCREEN,
        (50, 50, 50),
        day_background
    )

    # Day text
    SCREEN.blit(
        day_text,
        (30, 25)
    )

    # ========================================================
    # STRESS BAR — TOP RIGHT
    # ========================================================

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

        # Quit
        if event.type == pygame.QUIT:
            running = False


        # ====================================================
        # INTRO CONTROLS
        # ====================================================

        if game_state == "INTRO":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    line_index += 1

                    # Finished intro
                    if line_index >= len(lines):

                        game_state = "GAMEPLAY"


        # ====================================================
        # GAMEPLAY CONTROLS
        # ====================================================

        elif game_state == "GAMEPLAY":

            if event.type == pygame.MOUSEBUTTONDOWN:

                catch_intern(event.pos)


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
