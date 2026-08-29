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

# ------------------------------------------------------------
# DAY SYSTEM
# ------------------------------------------------------------

DAY_LENGTH = 60  # seconds

INTERNS_PER_DAY = {
    1: 5,
    2: 7,
    3: 9,
    4: 12,
    5: 15
}

total_interns_today = INTERNS_PER_DAY[day]
interns_completed = 0

day_timer = DAY_LENGTH * FPS


# ============================================================
# LISTS / TARGET
# ============================================================

interns = []

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

FONT_TINY = pygame.font.SysFont(
    "georgia",
    16
)


# ============================================================
# PLAYER / OFFICE WORKER
# ============================================================

player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2

player_speed = 5

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
# PLAYER UPDATE
# ============================================================

def update_player():

    global player_x
    global player_y
    global target_person
    global stress

    # ========================================================
    # CHASING SOMEONE
    # ========================================================

    if target_person is not None:

        # Follow their X position
        target_x = (
            target_person.x
            + INTERN_WIDTH // 2
            - PLAYER_WIDTH // 2
        )

        # Move toward them
        if player_x < target_x:

            player_x += player_speed

        elif player_x > target_x:

            player_x -= player_speed

        # Keep player at their current Y position
        # while chasing.

        # ----------------------------------------------------
        # CONFRONTATION
        # ----------------------------------------------------

        if abs(player_x - target_x) <= player_speed:

            player_x = target_x

            person = target_person

            # =================================================
            # IMPORTANT BUG FIX
            # =================================================
            #
            # Clear target_person IMMEDIATELY.
            #
            # Previously, target_person stayed assigned while
            # the dialogue was happening, so this code ran
            # repeatedly every frame.
            #
            target_person = None

            # Put person into dialogue state
            person.state = "DIALOGUE"
            person.dialogue_timer = 0

            # -------------------------------------------------
            # STAFF
            # -------------------------------------------------

            if person.has_badge:

                stress += 10

                person.dialogue = random.choice([
                    "I'm WORKING!",
                    "Do I look like an intern to you?",
                    "Excuse me?!",
                    "I have a meeting!",
                    "Can you not?!"
                ])

            # -------------------------------------------------
            # ACTUAL INTERN
            # -------------------------------------------------

            else:

                stress -= 5

                person.dialogue = random.choice([
                    "Wait—what?!",
                    "I was just getting snacks...",
                    "Okay okay, I'm leaving!",
                    "You caught me!",
                    "Fine! I'm going!"
                ])

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


# ============================================================
# DRAW PLAYER
# ============================================================

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
    "Defend your tower. Don't let those interns get to the snacks!"
]

line_index = 0


def update_cutscene():
    pass


def draw_cutscene():

    SCREEN.fill(
        (251, 198, 207)
    )

    # --------------------------------------------------------
    # MAIN TEXT
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # PROMPT
    # --------------------------------------------------------

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

# Lower = more frequent spawning
spawn_interval = 90


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

        # ----------------------------------------------------
        # MOVEMENT
        # ----------------------------------------------------

        self.speed = random.uniform(
            1.5,
            3.0
        )

        # ----------------------------------------------------
        # STATE
        # ----------------------------------------------------

        self.state = "WALKING"

        # WALKING
        # DIALOGUE
        # LEAVING

        # ----------------------------------------------------
        # DIALOGUE
        # ----------------------------------------------------

        self.dialogue = ""

        self.dialogue_timer = 0

        # 1.5 seconds
        self.dialogue_duration = int(
            1.5 * FPS
        )

        # ----------------------------------------------------
        # COLOUR
        # ----------------------------------------------------

        # Staff = blue
        # Intern = lighter blue

        self.color = (
            (100, 149, 237)
            if has_badge
            else (121, 186, 236)
        )

    # ========================================================
    # RECTANGLE
    # ========================================================

    def get_rect(self):

        return pygame.Rect(
            int(self.x),
            int(self.y),
            INTERN_WIDTH,
            INTERN_HEIGHT
        )

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self):

        # ----------------------------------------------------
        # WALKING
        # ----------------------------------------------------

        if self.state == "WALKING":

            self.x += self.speed

        # ----------------------------------------------------
        # DIALOGUE
        # ----------------------------------------------------

        elif self.state == "DIALOGUE":

            self.dialogue_timer += 1

            if (
                self.dialogue_timer
                >= self.dialogue_duration
            ):

                self.state = "LEAVING"

        # ----------------------------------------------------
        # LEAVING
        # ----------------------------------------------------

        elif self.state == "LEAVING":

            # Move upward
            self.y -= 5

    # ========================================================
    # DRAW
    # ========================================================

    def draw(self):

        rect = self.get_rect()

        pygame.draw.rect(
            SCREEN,
            self.color,
            rect,
            border_radius=8
        )

        # ----------------------------------------------------
        # STAFF BADGE
        # ----------------------------------------------------

        if self.has_badge:

            pygame.draw.circle(
                SCREEN,
                (255, 215, 0),
                (
                    int(self.x + 10),
                    int(self.y + 10)
                ),
                5
            )


# ============================================================
# SPAWN INTERN
# ============================================================

def spawn_intern():

    # Spawn from left side
    x = -INTERN_WIDTH

    # Random vertical position
    y = random.randint(
        170,
        300
    )

    # 80% staff
    # 20% actual intern

    has_badge = (
        random.random() < 0.80
    )

    interns.append(
        Intern(
            x,
            y,
            has_badge
        )
    )


# ============================================================
# CLICK / CONFRONT WORKER
# ============================================================

def catch_intern(pos):

    global target_person

    # Don't select someone while already chasing
    if target_person is not None:
        return

    for person in interns:

        # Only walking workers can be clicked
        if person.state != "WALKING":
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
    global interns_completed

    # ========================================================
    # SPAWN
    # ========================================================

    spawn_timer += 1

    # Only spawn until today's quota is reached
    if (
        len(interns)
        + interns_completed
        < total_interns_today
    ):

        if spawn_timer >= spawn_interval:

            spawn_timer = 0

            spawn_intern()

    # ========================================================
    # UPDATE PEOPLE
    # ========================================================

    for person in interns:

        person.update()

    # ========================================================
    # REMOVE PEOPLE
    # ========================================================

    remaining_people = []

    for person in interns:

        # ----------------------------------------------------
        # ESCAPED THROUGH RIGHT SIDE
        # ----------------------------------------------------

        if (
            person.state == "WALKING"
            and person.x > SCREEN_WIDTH
        ):

            # Only actual interns increase stress
            if not person.has_badge:

                stress += 5

            interns_completed += 1

            continue

        # ----------------------------------------------------
        # LEFT THROUGH TOP AFTER CONFRONTATION
        # ----------------------------------------------------

        if (
            person.state == "LEAVING"
            and person.y + INTERN_HEIGHT < 0
        ):

            interns_completed += 1

            continue

        remaining_people.append(person)

    interns[:] = remaining_people


# ============================================================
# DRAW INTERNS
# ============================================================

def draw_interns():

    for person in interns:

        person.draw()

        # ====================================================
        # DIALOGUE BOX
        # ====================================================

        if person.state == "DIALOGUE":

            dialogue_width = 320
            dialogue_height = 85

            dialogue_x = (
                person.x
                + INTERN_WIDTH // 2
                - dialogue_width // 2
            )

            dialogue_y = (
                person.y - 100
            )

            # Keep box on screen

            dialogue_x = max(
                10,
                min(
                    dialogue_x,
                    SCREEN_WIDTH
                    - dialogue_width
                    - 10
                )
            )

            dialogue_y = max(
                80,
                dialogue_y
            )

            dialogue_rect = pygame.Rect(
                int(dialogue_x),
                int(dialogue_y),
                dialogue_width,
                dialogue_height
            )

            # ------------------------------------------------
            # BOX
            # ------------------------------------------------

            pygame.draw.rect(
                SCREEN,
                (255, 255, 255),
                dialogue_rect,
                border_radius=10
            )

            pygame.draw.rect(
                SCREEN,
                (40, 40, 40),
                dialogue_rect,
                2,
                border_radius=10
            )

            # ------------------------------------------------
            # TEXT
            # ------------------------------------------------

            dialogue_text = FONT_TINY.render(
                person.dialogue,
                True,
                (40, 40, 40)
            )

            SCREEN.blit(
                dialogue_text,
                (
                    dialogue_x + 15,
                    dialogue_y + 30
                )
            )


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


# ============================================================
# STRESS POPUPS
# ============================================================

stress_popup = ""

stress_popup_timer = 0

STRESS_POPUP_DURATION = 150

last_stress_level = None


# ============================================================
# GET STRESS LEVEL
# ============================================================

def get_stress_level():

    if stress >= 100:

        return "100"

    elif stress >= 75:

        return "75"

    elif stress >= 50:

        return "50"

    else:

        return "25"


# ============================================================
# TRIGGER POPUP
# ============================================================

def trigger_stress_popup(level):

    global stress_popup
    global stress_popup_timer

    if level == "100":

        stress_popup = (
            "MAX STRESS! You're overwhelmed!"
        )

    elif level == "75":

        stress_popup = (
            "HIGH STRESS! Things are getting hectic."
        )

    elif level == "50":

        stress_popup = (
            "STEADY. Keep your cool."
        )

    elif level == "25":

        stress_popup = (
            "LOW STRESS! You're feeling relaxed."
        )

    stress_popup_timer = (
        STRESS_POPUP_DURATION
    )


# ============================================================
# UPDATE STRESS
# ============================================================

def update_stress():

    global stress
    global stress_popup_timer
    global last_stress_level

    # Keep stress between 0 and 100

    stress = max(
        0,
        min(
            stress,
            100
        )
    )

    current_level = (
        get_stress_level()
    )

    # Trigger popup when entering
    # a different stress range

    if (
        current_level
        != last_stress_level
    ):

        trigger_stress_popup(
            current_level
        )

        last_stress_level = (
            current_level
        )

    # Popup countdown

    if stress_popup_timer > 0:

        stress_popup_timer -= 1


# ============================================================
# STRESS BUFFS / DEBUFFS
# ============================================================

def get_player_speed():

    # --------------------------------------------------------
    # 0-25%
    # CALM BUFF
    # --------------------------------------------------------

    if stress <= 25:

        return 6

    # --------------------------------------------------------
    # 26-50%
    # NORMAL
    # --------------------------------------------------------

    elif stress <= 50:

        return 5

    # --------------------------------------------------------
    # 51-75%
    # STRESSED
    # --------------------------------------------------------

    elif stress <= 75:

        return 4

    # --------------------------------------------------------
    # 76-100%
    # OVERWHELMED
    # --------------------------------------------------------

    else:

        return 3


def get_stress_effect_text():

    if stress <= 25:

        return (
            "BUFF: Calm - movement speed increased"
        )

    elif stress <= 50:

        return (
            "STATUS: Normal"
        )

    elif stress <= 75:

        return (
            "DEBUFF: Stressed - movement slowed"
        )

    else:

        return (
            "DEBUFF: OVERWHELMED - movement greatly slowed"
        )


# ============================================================
# DRAW STRESS BAR
# ============================================================

def draw_stress_bar():

    # --------------------------------------------------------
    # LABEL
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
    # BACKGROUND
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
    # FILLED BAR
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
# DRAW STRESS POPUP
# ============================================================

def draw_stress_popup():

    if stress_popup_timer <= 0:
        return

    popup_width = 600
    popup_height = 90

    popup_x = (
        SCREEN_WIDTH // 2
        - popup_width // 2
    )

    popup_y = 120

    popup_rect = pygame.Rect(
        popup_x,
        popup_y,
        popup_width,
        popup_height
    )

    # Background
    pygame.draw.rect(
        SCREEN,
        (40, 40, 40),
        popup_rect,
        border_radius=12
    )

    # Border
    pygame.draw.rect(
        SCREEN,
        (255, 255, 255),
        popup_rect,
        2,
        border_radius=12
    )

    # Text
    text = FONT_MAIN.render(
        stress_popup,
        True,
        (255, 255, 255)
    )

    SCREEN.blit(
        text,
        (
            SCREEN_WIDTH // 2
            - text.get_width() // 2,
            popup_y + 27
        )
    )


# ============================================================
# DAY SYSTEM
# ============================================================

def start_new_day():

    global day
    global stress
    global day_timer
    global total_interns_today
    global interns_completed
    global spawn_timer
    global player_x
    global player_y
    global target_person
    global last_stress_level

    day += 1

    # --------------------------------------------------------
    # NO MORE DAYS
    # --------------------------------------------------------

    if day not in INTERNS_PER_DAY:

        game_state_change_to_ending()

        return

    # --------------------------------------------------------
    # NEW DAY VALUES
    # --------------------------------------------------------

    total_interns_today = (
        INTERNS_PER_DAY[day]
    )

    interns_completed = 0

    day_timer = (
        DAY_LENGTH * FPS
    )

    spawn_timer = 0

    interns.clear()

    target_person = None

    # --------------------------------------------------------
    # RESET PLAYER
    # --------------------------------------------------------

    player_x = (
        SCREEN_WIDTH // 2
    )

    player_y = (
        SCREEN_HEIGHT // 2
    )

    # --------------------------------------------------------
    # RESET STRESS
    # --------------------------------------------------------

    stress = 50

    last_stress_level = None


# ============================================================
# GO TO ENDING
# ============================================================

def game_state_change_to_ending():

    global game_state

    game_state = "ENDING"


# ============================================================
# DAY TIMER
# ============================================================

def update_day_timer():

    global day_timer

    day_timer -= 1

    # Day ends when:
    #
    # 1. Time runs out
    #
    # OR
    #
    # 2. All workers have been dealt with

    if (
        day_timer <= 0
        or
        interns_completed
        >= total_interns_today
    ):

        start_new_day()


# ============================================================
# DAY INFORMATION
# ============================================================

def draw_day_info():

    # --------------------------------------------------------
    # DAY
    # --------------------------------------------------------

    day_text = FONT_SMALL.render(
        f"DAY {day}",
        True,
        (255, 255, 255)
    )

    day_background = pygame.Rect(
        20,
        20,
        150,
        80
    )

    pygame.draw.rect(
        SCREEN,
        (50, 50, 50),
        day_background,
        border_radius=8
    )

    SCREEN.blit(
        day_text,
        (30, 27)
    )

    # --------------------------------------------------------
    # INTERNS LEFT
    # --------------------------------------------------------

    interns_left = (
        total_interns_today
        - interns_completed
    )

    interns_text = FONT_TINY.render(
        f"INTERNS LEFT: {interns_left}/{total_interns_today}",
        True,
        (255, 255, 255)
    )

    SCREEN.blit(
        interns_text,
        (30, 60)
    )

    # --------------------------------------------------------
    # TIME
    # --------------------------------------------------------

    seconds_left = max(
        0,
        day_timer // FPS
    )

    minutes = (
        seconds_left // 60
    )

    seconds = (
        seconds_left % 60
    )

    time_text = FONT_TINY.render(
        f"TIME: {minutes}:{seconds:02d}",
        True,
        (255, 255, 255)
    )

    SCREEN.blit(
        time_text,
        (190, 25)
    )

    # --------------------------------------------------------
    # STRESS EFFECT
    # --------------------------------------------------------

    effect_text = FONT_TINY.render(
        get_stress_effect_text(),
        True,
        (255, 255, 255)
    )

    SCREEN.blit(
        effect_text,
        (190, 55)
    )


# ============================================================
# GAMEPLAY
# ============================================================

def update_gameplay():

    global player_speed

    # Stress determines movement speed

    player_speed = (
        get_player_speed()
    )

    update_player()

    update_interns()

    update_tower()

    update_snacks()

    update_stress()

    update_day_timer()


# ============================================================
# DRAW GAMEPLAY
# ============================================================

def draw_gameplay():

    # ========================================================
    # CLEAR ENTIRE SCREEN
    # ========================================================

    SCREEN.fill(
        (40, 90, 40)
    )

    # ========================================================
    # GAME OBJECTS
    # ========================================================

    draw_tower()

    draw_interns()

    draw_player()

    draw_snacks()

    # ========================================================
    # UI
    # ========================================================

    draw_day_info()

    draw_stress_bar()

    draw_stress_popup()


# ============================================================
# ENDING
# ============================================================

def update_ending():
    pass


def draw_ending():

    SCREEN.fill(
        (30, 30, 50)
    )

    title = FONT_MAIN.render(
        "THE WORKDAY IS OVER",
        True,
        (255, 255, 255)
    )

    SCREEN.blit(
        title,
        (
            SCREEN_WIDTH // 2
            - title.get_width() // 2,
            250
        )
    )

    message = FONT_SMALL.render(
        "You survived the Nokia Ottawa Office.",
        True,
        (255, 255, 255)
    )

    SCREEN.blit(
        message,
        (
            SCREEN_WIDTH // 2
            - message.get_width() // 2,
            310
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

        # ----------------------------------------------------
        # INTRO
        # ----------------------------------------------------

        if game_state == "INTRO":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    line_index += 1

                    if line_index >= len(lines):

                        game_state = "GAMEPLAY"

                        day_timer = (
                            DAY_LENGTH * FPS
                        )

        # ----------------------------------------------------
        # GAMEPLAY
        # ----------------------------------------------------

        elif game_state == "GAMEPLAY":

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

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
