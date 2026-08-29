import pygame
import random

pygame.init()

# ============================================================
# SETTINGS
# ============================================================

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
FPS = 60

SCREEN = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

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

target_person = None


# ============================================================
# FONTS
# ============================================================

FONT_MAIN = pygame.font.SysFont(
    "georgia",
    32
)

FONT_SMALL = pygame.font.SysFont(
    "georgia",
    20
)

FONT_STATUS = pygame.font.SysFont(
    "georgia",
    26,
    bold=True
)


# ============================================================
# PLAYER
# ============================================================

player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2

BASE_PLAYER_SPEED = 5
player_speed = BASE_PLAYER_SPEED

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60


# ------------------------------------------------------------
# PLAYER IMAGE
# ------------------------------------------------------------

player_image = pygame.image.load(
    "assets/player.jpg"
)

player_image = pygame.transform.scale(
    player_image,
    (PLAYER_WIDTH, PLAYER_HEIGHT)
)


# ============================================================
# STRESS STATUS
# ============================================================

current_stress_tier = None

popup_text = ""
popup_timer = 0

POPUP_DURATION = 180


# ============================================================
# STRESS TIER FUNCTION
# ============================================================

def get_stress_tier():

    if stress >= 100:
        return "MAX"

    elif stress >= 75:
        return "HIGH"

    elif stress >= 50:
        return "MEDIUM"

    elif stress >= 25:
        return "LOW"

    else:
        return "ZEN"


# ============================================================
# STRESS EFFECTS
# ============================================================

def apply_stress_effects():

    global player_speed

    tier = get_stress_tier()

    # --------------------------------------------------------
    # MAX STRESS
    # --------------------------------------------------------

    if tier == "MAX":

        player_speed = 3

    # --------------------------------------------------------
    # HIGH STRESS
    # --------------------------------------------------------

    elif tier == "HIGH":

        player_speed = 4

    # --------------------------------------------------------
    # MEDIUM STRESS
    # --------------------------------------------------------

    elif tier == "MEDIUM":

        player_speed = 5

    # --------------------------------------------------------
    # LOW STRESS
    # --------------------------------------------------------

    elif tier == "LOW":

        player_speed = 6

    # --------------------------------------------------------
    # ZEN
    # --------------------------------------------------------

    elif tier == "ZEN":

        player_speed = 7


# ============================================================
# STRESS POPUP
# ============================================================

def trigger_stress_popup():

    global popup_text
    global popup_timer

    tier = get_stress_tier()

    if tier == "MAX":

        popup_text = (
            "MAX STRESS! "
            "You're overwhelmed!"
        )

    elif tier == "HIGH":

        popup_text = (
            "HIGH STRESS — "
            "Movement slowed!"
        )

    elif tier == "MEDIUM":

        popup_text = (
            "STRESSED — "
            "Stay focused."
        )

    elif tier == "LOW":

        popup_text = (
            "CALM — "
            "Movement increased!"
        )

    elif tier == "ZEN":

        popup_text = (
            "ZEN MODE — "
            "Maximum movement speed!"
        )

    popup_timer = POPUP_DURATION


# ============================================================
# PLAYER UPDATE
# ============================================================

def update_player():

    global player_x
    global player_y
    global target_person
    global stress

    # Apply current stress effect
    apply_stress_effects()

    # ========================================================
    # CHASING SOMEONE
    # ========================================================

    if target_person is not None:

        target_x = (
            target_person.x
            + INTERN_WIDTH // 2
            - PLAYER_WIDTH // 2
        )

        # Move toward target
        if player_x < target_x:

            player_x += player_speed

        elif player_x > target_x:

            player_x -= player_speed

        # Player stays at same Y position
        # while chasing

        # ----------------------------------------------------
        # Check if caught
        # ----------------------------------------------------

        if abs(player_x - target_x) <= player_speed:

            player_x = target_x

            target_person.caught = True

            # ------------------------------------------------
            # Stress changes
            # ------------------------------------------------

            if target_person.has_badge:

                # Accidentally interrupted staff
                stress += 10

            else:

                # Successfully caught intern
                stress -= 5

            target_person = None

    # ========================================================
    # NORMAL MOVEMENT
    # ========================================================

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

    # ========================================================
    # KEEP PLAYER ON SCREEN
    # ========================================================

    player_x = max(
        0,
        min(
            player_x,
            SCREEN_WIDTH - PLAYER_WIDTH
        )
    )

    player_y = max(
        0,
        min(
            player_y,
            SCREEN_HEIGHT - PLAYER_HEIGHT
        )
    )


def draw_player():

    SCREEN.blit(
        player_image,
        (player_x, player_y)
    )


# ============================================================
# CUTSCENE
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

    # Clear screen
    SCREEN.fill(
        (251, 198, 207)
    )

    # Main text
    text = FONT_MAIN.render(
        lines[line_index],
        True,
        (255, 255, 255)
    )

    SCREEN.blit(
        text,
        (
            SCREEN_WIDTH // 2
            - text.get_width() // 2,

            SCREEN_HEIGHT // 2
        )
    )

    # Prompt
    prompt = FONT_SMALL.render(
        "Press SPACE to continue",
        True,
        (180, 180, 180)
    )

    SCREEN.blit(
        prompt,
        (
            SCREEN_WIDTH // 2
            - prompt.get_width() // 2,

            SCREEN_HEIGHT - 60
        )
    )


# ============================================================
# INTERNS / STAFF
# ============================================================

INTERN_WIDTH = 40
INTERN_HEIGHT = 60

spawn_timer = 0


# ============================================================
# DAY DIFFICULTY
# ============================================================

def get_spawn_interval():

    if day == 1:

        return 120

    elif day == 2:

        return 100

    elif day == 3:

        return 80

    elif day == 4:

        return 65

    else:

        return 50


def get_speed_range():

    if day == 1:

        return 1.5, 3.0

    elif day == 2:

        return 2.0, 3.5

    elif day == 3:

        return 2.5, 4.0

    elif day == 4:

        return 3.0, 4.5

    else:

        return 3.5, 5.0


# ============================================================
# INTERN CLASS
# ============================================================

class Intern:

    def __init__(
        self,
        x,
        y,
        has_badge
    ):

        self.x = x
        self.y = y

        self.has_badge = has_badge

        self.caught = False

        # ----------------------------------------------------
        # Movement
        # ----------------------------------------------------

        min_speed, max_speed = get_speed_range()

        self.speed = random.uniform(
            min_speed,
            max_speed
        )

        # ----------------------------------------------------
        # Pause system
        # ----------------------------------------------------

        self.walk_distance = random.randint(
            250,
            500
        )

        self.start_x = x

        self.pause_time = random.randint(
            60,
            120
        )

        self.pause_timer = 0

        self.has_paused = False

        self.state = "WALKING"

        # ----------------------------------------------------
        # Colour
        # ----------------------------------------------------

        if has_badge:

            # Staff
            self.color = (
                100,
                149,
                237
            )

        else:

            # Intern
            self.color = (
                121,
                186,
                236
            )


    def get_rect(self):

        return pygame.Rect(
            int(self.x),
            int(self.y),
            INTERN_WIDTH,
            INTERN_HEIGHT
        )


    def update(self):

        if self.caught:

            return

        # ====================================================
        # WALKING
        # ====================================================

        if self.state == "WALKING":

            self.x += self.speed

            if (
                not self.has_paused
                and self.x >= (
                    self.start_x
                    + self.walk_distance
                )
            ):

                self.state = "PAUSED"

                self.pause_timer = 0

        # ====================================================
        # PAUSED
        # ====================================================

        elif self.state == "PAUSED":

            self.pause_timer += 1

            if self.pause_timer >= self.pause_time:

                self.state = "WALKING"

                self.has_paused = True


    def draw(self):

        rect = self.get_rect()

        pygame.draw.rect(
            SCREEN,
            self.color,
            rect,
            border_radius=8
        )


# ============================================================
# SPAWN INTERN
# ============================================================

def spawn_intern():

    x = -INTERN_WIDTH

    y = 200

    new_rect = pygame.Rect(
        x,
        y,
        INTERN_WIDTH,
        INTERN_HEIGHT
    )

    overlapping = False

    # Check existing people
    for person in interns:

        if new_rect.colliderect(
            person.get_rect()
        ):

            overlapping = True

            break

    if overlapping:

        return

    # --------------------------------------------------------
    # 80% staff
    # 20% intern
    # --------------------------------------------------------

    has_badge = (
        random.random()
        < 0.80
    )

    interns.append(
        Intern(
            x,
            y,
            has_badge
        )
    )


# ============================================================
# CLICK ON INTERN
# ============================================================

def catch_intern(pos):

    global target_person

    # If already chasing someone,
    # don't select another person
    if target_person is not None:

        return

    for person in interns:

        if person.caught:

            continue

        if person.get_rect().collidepoint(pos):

            target_person = person

            break


# ============================================================
# UPDATE INTERNS
# ============================================================

def update_interns():

    global spawn_timer
    global stress
    global target_person

    # ========================================================
    # SPAWN
    # ========================================================

    spawn_timer += 1

    if (
        spawn_timer
        >= get_spawn_interval()
    ):

        spawn_timer = 0

        spawn_intern()


    # ========================================================
    # UPDATE PEOPLE
    # ========================================================

    for person in interns:

        if not person.caught:

            person.update()


    # ========================================================
    # PEOPLE LEAVE
    # ========================================================

    remaining_people = []

    for person in interns:

        # Don't remove target
        if person == target_person:

            remaining_people.append(
                person
            )

            continue

        # ----------------------------------------------------
        # Escaped
        # ----------------------------------------------------

        if person.x > SCREEN_WIDTH:

            # ONLY interns cause stress
            if not person.has_badge:

                stress += 5

            continue

        remaining_people.append(
            person
        )


    interns[:] = remaining_people


# ============================================================
# DRAW INTERNS
# ============================================================

def draw_interns():

    for person in interns:

        person.draw()


# ============================================================
# TOWER / MAP
# ============================================================

def update_tower():
    pass


def draw_tower():
    pass


# ============================================================
# SNACK SYSTEM
# ============================================================

def update_snacks():
    pass


def draw_snacks():
    pass


# ============================================================
# STRESS SYSTEM
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
    global current_stress_tier
    global popup_timer

    # --------------------------------------------------------
    # Clamp stress
    # --------------------------------------------------------

    stress = max(
        0,
        min(
            stress,
            100
        )
    )

    # --------------------------------------------------------
    # Determine tier
    # --------------------------------------------------------

    new_tier = get_stress_tier()

    # --------------------------------------------------------
    # First frame
    # --------------------------------------------------------

    if current_stress_tier is None:

        current_stress_tier = new_tier

    # --------------------------------------------------------
    # Tier changed
    # --------------------------------------------------------

    elif new_tier != current_stress_tier:

        current_stress_tier = new_tier

        trigger_stress_popup()

    # --------------------------------------------------------
    # Popup timer
    # --------------------------------------------------------

    if popup_timer > 0:

        popup_timer -= 1


# ============================================================
# DRAW STRESS BAR
# ============================================================

def draw_stress_bar():

    # --------------------------------------------------------
    # Label
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
    # Background
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
    # Filled section
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
    # Border
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
# DRAW STRESS POPUP
# ============================================================

def draw_stress_popup():

    if popup_timer <= 0:

        return

    # --------------------------------------------------------
    # Popup box
    # --------------------------------------------------------

    popup_width = 500
    popup_height = 80

    popup_x = (
        SCREEN_WIDTH // 2
        - popup_width // 2
    )

    popup_y = 80

    popup_rect = pygame.Rect(
        popup_x,
        popup_y,
        popup_width,
        popup_height
    )

    pygame.draw.rect(
        SCREEN,
        (50, 50, 50),
        popup_rect,
        border_radius=10
    )

    pygame.draw.rect(
        SCREEN,
        (255, 255, 255),
        popup_rect,
        2,
        border_radius=10
    )

    # --------------------------------------------------------
    # Popup text
    # --------------------------------------------------------

    text = FONT_STATUS.render(
        popup_text,
        True,
        (255, 255, 255)
    )

    SCREEN.blit(
        text,
        (
            SCREEN_WIDTH // 2
            - text.get_width() // 2,

            popup_y
            + popup_height // 2
            - text.get_height() // 2
        )
    )


# ============================================================
# DAY DISPLAY
# ============================================================

def draw_day():

    day_text = FONT_SMALL.render(
        f"DAY {day}",
        True,
        (255, 255, 255)
    )

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

    SCREEN.blit(
        day_text,
        (30, 25)
    )


# ============================================================
# DAY START POPUP
# ============================================================

def draw_day_info():

    if day == 1:

        info = "DAY 1 — The office is relatively calm."

    elif day == 2:

        info = "DAY 2 — More people are entering the office."

    elif day == 3:

        info = "DAY 3 — Everyone seems to be moving faster."

    elif day == 4:

        info = "DAY 4 — Things are getting chaotic."

    else:

        info = "DAY 5+ — Absolute office mayhem."


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

    # IMPORTANT:
    # Clear the screen every frame
    SCREEN.fill(
        (40, 90, 40)
    )

    # --------------------------------------------------------
    # Game objects
    # --------------------------------------------------------

    draw_tower()

    draw_snacks()

    draw_interns()

    draw_player()

    # --------------------------------------------------------
    # UI
    # --------------------------------------------------------

    draw_day()

    draw_stress_bar()

    draw_stress_popup()


# ============================================================
# ENDING
# ============================================================

def update_ending():
    pass


def draw_ending():

    SCREEN.fill(
        (20, 20, 20)
    )

    text = FONT_MAIN.render(
        "GAME OVER",
        True,
        (255, 255, 255)
    )

    SCREEN.blit(
        text,
        (
            SCREEN_WIDTH // 2
            - text.get_width() // 2,

            SCREEN_HEIGHT // 2
        )
    )


# ============================================================
# MAIN LOOP
# ============================================================

running = True

while running:

    # ========================================================
    # EVENTS
    # ========================================================

    for event in pygame.event.get():

        # ----------------------------------------------------
        # QUIT
        # ----------------------------------------------------

        if event.type == pygame.QUIT:

            running = False


        # ====================================================
        # INTRO
        # ====================================================

        if game_state == "INTRO":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    line_index += 1

                    if line_index >= len(lines):

                        game_state = "GAMEPLAY"


        # ====================================================
        # GAMEPLAY
        # ====================================================

        elif game_state == "GAMEPLAY":

            if event.type == pygame.MOUSEBUTTONDOWN:

                catch_intern(
                    event.pos
                )


    # ========================================================
    # UPDATE + DRAW
    # ========================================================

    if game_state == "INTRO":

        update_cutscene()

        draw_cutscene()


    elif game_state == "GAMEPLAY":

        update_gameplay()

        draw_gameplay()


    elif game_state == "ENDING":

        update_ending()

        draw_ending()


    # ========================================================
    # DISPLAY
    # ========================================================

    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()