import pygame
import random


# ============================================================
# PERSON CLASS
# ============================================================

class Person:

    def __init__(
        self,
        x,
        y,
        is_intern,
        image,
        game
    ):

        self.x = x
        self.y = y

        self.is_intern = is_intern

        self.image = image

        # ----------------------------------------------------
        # SIZE
        # ----------------------------------------------------

        self.width = game.person_width
        self.height = game.person_height

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

        self.dialogue_duration = int(
            1.5 * game.fps
        )

    # ========================================================
    # GET RECTANGLE
    # ========================================================

    def get_rect(self):

        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
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

    def draw(self, screen):

        screen.blit(
            self.image,
            (
                int(self.x),
                int(self.y)
            )
        )


# ============================================================
# GAME CLASS
# ============================================================

class Game:

    def __init__(self):

        # ====================================================
        # PYGAME
        # ====================================================

        pygame.init()

        # ====================================================
        # SETTINGS
        # ====================================================

        self.screen_width = 1080
        self.screen_height = 720

        self.fps = 60

        self.screen = pygame.display.set_mode(
            (
                self.screen_width,
                self.screen_height
            )
        )

        pygame.display.set_caption(
            "Mokia"
        )

        self.clock = pygame.time.Clock()

        # ====================================================
        # GAME STATE
        # ====================================================

        self.game_state = "INTRO"

        # ====================================================
        # DAY SYSTEM
        # ====================================================

        self.day_length = 60

        self.day = 1

        self.max_day = 5

        self.day_timer = (
            self.day_length * self.fps
        )

        self.interns_per_day = {
            1: 5,
            2: 7,
            3: 9,
            4: 12,
            5: 15
        }

        self.total_people_today = (
            self.interns_per_day[self.day]
        )

        self.people_completed = 0

        # ====================================================
        # STRESS
        # ====================================================

        self.stress = 50

        self.last_stress_level = None

        # ====================================================
        # PLAYER
        # ====================================================

        self.player_width = 40
        self.player_height = 60

        self.player_x = (
            self.screen_width // 2
        )

        self.player_y = (
            self.screen_height // 2
        )

        self.player_speed = 5

        # ====================================================
        # PEOPLE
        # ====================================================

        self.person_width = 40
        self.person_height = 60

        self.people = []

        self.target_person = None

        self.spawn_timer = 0

        self.spawn_interval = 90

        # ====================================================
        # BACKGROUNDS
        # ====================================================

        self.backgrounds = []

        for number in range(1, 6):

            image = pygame.image.load(
                f"assets/bg{number}.png"
            ).convert()

            image = pygame.transform.scale(
                image,
                (
                    self.screen_width,
                    self.screen_height
                )
            )

            self.backgrounds.append(
                image
            )

        # ====================================================
        # INTERN SPRITES
        # ====================================================

        self.intern_images = []

        for number in range(1, 5):

            image = pygame.image.load(
                f"assets/intern{number}.png"
            ).convert_alpha()

            image = pygame.transform.scale(
                image,
                (
                    self.person_width,
                    self.person_height
                )
            )

            self.intern_images.append(
                image
            )

        # ====================================================
        # FULL-TIME SPRITES
        # ====================================================

        self.fulltime_images = []

        for number in range(1, 3):

            image = pygame.image.load(
                f"assets/fulltime{number}.webp"
            ).convert_alpha()

            image = pygame.transform.scale(
                image,
                (
                    self.person_width,
                    self.person_height
                )
            )

            self.fulltime_images.append(
                image
            )

        # ====================================================
        # PLAYER IMAGE
        # ====================================================

        self.player_image = pygame.image.load(
            "assets/player.jpg"
        ).convert()

        self.player_image = pygame.transform.scale(
            self.player_image,
            (
                self.player_width,
                self.player_height
            )
        )

        # ====================================================
        # FONTS
        # ====================================================

        self.font_main = pygame.font.SysFont(
            "georgia",
            32
        )

        self.font_small = pygame.font.SysFont(
            "georgia",
            20
        )

        self.font_tiny = pygame.font.SysFont(
            "georgia",
            16
        )

        # ====================================================
        # CUTSCENE
        # ====================================================

        self.lines = [
            "In the Nokia Ottawa Office...",
            "...the towers are divided.",
            "Meet your office worker. Stress: rising.",
            "Work is piling up. The snack table is under threat.",
            "Defend your tower. Don't let those interns get to the snacks!"
        ]

        self.line_index = 0

        # ====================================================
        # STRESS BAR
        # ====================================================

        self.stress_bar_width = 250
        self.stress_bar_height = 25

        self.stress_bar_x = (
            self.screen_width
            - self.stress_bar_width
            - 30
        )

        self.stress_bar_y = 30

        # ====================================================
        # STRESS POPUPS
        # ====================================================

        self.stress_popup = ""

        self.stress_popup_timer = 0

        self.stress_popup_duration = 150

    # ========================================================
    # RUN GAME
    # ========================================================

    def run(self):

        running = True

        while running:

            running = self.handle_events()

            self.update()

            self.draw()

            pygame.display.flip()

            self.clock.tick(
                self.fps
            )

        pygame.quit()

    # ========================================================
    # EVENTS
    # ========================================================

    def handle_events(self):

        for event in pygame.event.get():

            # ------------------------------------------------
            # QUIT
            # ------------------------------------------------

            if event.type == pygame.QUIT:

                return False

            # ------------------------------------------------
            # INTRO
            # ------------------------------------------------

            if self.game_state == "INTRO":

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:

                        self.line_index += 1

                        if (
                            self.line_index
                            >= len(self.lines)
                        ):

                            self.game_state = "GAMEPLAY"

                            self.day_timer = (
                                self.day_length
                                * self.fps
                            )

            # ------------------------------------------------
            # GAMEPLAY
            # ------------------------------------------------

            elif self.game_state == "GAMEPLAY":

                if (
                    event.type
                    == pygame.MOUSEBUTTONDOWN
                ):

                    if event.button == 1:

                        self.catch_person(
                            event.pos
                        )

            # ------------------------------------------------
            # ENDING
            # ------------------------------------------------

            elif self.game_state == "ENDING":

                pass

        return True

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self):

        if self.game_state == "INTRO":

            self.update_cutscene()

        elif self.game_state == "GAMEPLAY":

            self.update_gameplay()

        elif self.game_state == "ENDING":

            self.update_ending()

    # ========================================================
    # DRAW
    # ========================================================

    def draw(self):

        if self.game_state == "INTRO":

            self.draw_cutscene()

        elif self.game_state == "GAMEPLAY":

            self.draw_gameplay()

        elif self.game_state == "ENDING":

            self.draw_ending()

    # ========================================================
    # CUTSCENE
    # ========================================================

    def update_cutscene(self):

        pass

    def draw_cutscene(self):

        self.screen.fill(
            (251, 198, 207)
        )

        # ----------------------------------------------------
        # MAIN TEXT
        # ----------------------------------------------------

        text = self.font_main.render(
            self.lines[self.line_index],
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            text,
            (
                self.screen_width // 2
                - text.get_width() // 2,
                self.screen_height // 2
            )
        )

        # ----------------------------------------------------
        # PROMPT
        # ----------------------------------------------------

        prompt = self.font_small.render(
            "Press SPACE to continue",
            True,
            (180, 180, 180)
        )

        self.screen.blit(
            prompt,
            (
                self.screen_width // 2
                - prompt.get_width() // 2,
                self.screen_height - 60
            )
        )

    # ========================================================
    # PLAYER
    # ========================================================

    def update_player(self):

        # ====================================================
        # CHASING SOMEONE
        # ====================================================

        if self.target_person is not None:

            target_x = (
                self.target_person.x
                + self.person_width // 2
                - self.player_width // 2
            )

            # ------------------------------------------------
            # MOVE TOWARD PERSON
            # ------------------------------------------------

            if self.player_x < target_x:

                self.player_x += (
                    self.player_speed
                )

            elif self.player_x > target_x:

                self.player_x -= (
                    self.player_speed
                )

            # ------------------------------------------------
            # CONFRONTATION
            # ------------------------------------------------

            if (
                abs(
                    self.player_x
                    - target_x
                )
                <= self.player_speed
            ):

                self.player_x = target_x

                person = self.target_person

                # Clear target immediately
                self.target_person = None

                # Put person into dialogue
                person.state = "DIALOGUE"

                person.dialogue_timer = 0

                # ============================================
                # FULL-TIME WORKER
                # ============================================

                if not person.is_intern:

                    self.stress += 10

                    person.dialogue = random.choice(
                        [
                            "I'm WORKING!",
                            "Do I look like an intern to you?",
                            "Excuse me?!",
                            "I have a meeting!",
                            "Can you not?!"
                        ]
                    )

                # ============================================
                # ACTUAL INTERN
                # ============================================

                else:

                    self.stress -= 5

                    person.dialogue = random.choice(
                        [
                            "Wait—what?!",
                            "I was just getting snacks...",
                            "Okay okay, I'm leaving!",
                            "You caught me!",
                            "Fine! I'm going!"
                        ]
                    )

        # ====================================================
        # NORMAL MOVEMENT
        # ====================================================

        else:

            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:

                self.player_y -= (
                    self.player_speed
                )

            if keys[pygame.K_s]:

                self.player_y += (
                    self.player_speed
                )

            if keys[pygame.K_a]:

                self.player_x -= (
                    self.player_speed
                )

            if keys[pygame.K_d]:

                self.player_x += (
                    self.player_speed
                )

        # ====================================================
        # KEEP PLAYER ON SCREEN
        # ====================================================

        self.player_x = max(
            0,
            min(
                self.player_x,
                self.screen_width
                - self.player_width
            )
        )

        self.player_y = max(
            0,
            min(
                self.player_y,
                self.screen_height
                - self.player_height
            )
        )

    # ========================================================
    # DRAW PLAYER
    # ========================================================

    def draw_player(self):

        self.screen.blit(
            self.player_image,
            (
                self.player_x,
                self.player_y
            )
        )

    # ========================================================
    # SPAWN PERSON
    # ========================================================

    def spawn_person(self):

        # ----------------------------------------------------
        # SPAWN FROM LEFT SIDE
        # ----------------------------------------------------

        x = -self.person_width

        # ----------------------------------------------------
        # RANDOM VERTICAL POSITION
        # ----------------------------------------------------

        y = random.randint(
            170,
            300
        )

        # ----------------------------------------------------
        # RANDOM TYPE
        # ----------------------------------------------------
        #
        # 80% = full-time worker
        # 20% = intern
        #
        # ----------------------------------------------------

        is_intern = (
            random.random() < 0.20
        )

        # ----------------------------------------------------
        # RANDOM SPRITE
        # ----------------------------------------------------

        if is_intern:

            image = random.choice(
                self.intern_images
            )

        else:

            image = random.choice(
                self.fulltime_images
            )

        # ----------------------------------------------------
        # CREATE PERSON
        # ----------------------------------------------------

        person = Person(
            x,
            y,
            is_intern,
            image,
            self
        )

        self.people.append(
            person
        )

    # ========================================================
    # CATCH PERSON
    # ========================================================

    def catch_person(self, pos):

        # Don't select someone while already chasing
        if self.target_person is not None:

            return

        for person in self.people:

            # Only walking people can be clicked
            if person.state != "WALKING":

                continue

            if person.get_rect().collidepoint(pos):

                self.target_person = person

                break

    # ========================================================
    # UPDATE PEOPLE
    # ========================================================

    def update_people(self):

        # ====================================================
        # SPAWN
        # ====================================================

        self.spawn_timer += 1

        # Only spawn until today's quota is reached
        if (
            len(self.people)
            + self.people_completed
            < self.total_people_today
        ):

            if (
                self.spawn_timer
                >= self.spawn_interval
            ):

                self.spawn_timer = 0

                self.spawn_person()

        # ====================================================
        # UPDATE PEOPLE
        # ====================================================

        for person in self.people:

            person.update()

        # ====================================================
        # REMOVE PEOPLE
        # ====================================================

        remaining_people = []

        for person in self.people:

            # ------------------------------------------------
            # ESCAPED THROUGH RIGHT SIDE
            # ------------------------------------------------

            if (
                person.state == "WALKING"
                and person.x > self.screen_width
            ):

                # Only actual interns increase stress
                if person.is_intern:

                    self.stress += 5

                self.people_completed += 1

                continue

            # ------------------------------------------------
            # LEFT THROUGH TOP AFTER CONFRONTATION
            # ------------------------------------------------

            if (
                person.state == "LEAVING"
                and person.y + self.person_height < 0
            ):

                self.people_completed += 1

                continue

            remaining_people.append(
                person
            )

        self.people = remaining_people

    # ========================================================
    # DRAW PEOPLE
    # ========================================================

    def draw_people(self):

        for person in self.people:

            person.draw(
                self.screen
            )

            # =================================================
            # DIALOGUE BOX
            # =================================================

            if person.state == "DIALOGUE":

                dialogue_width = 320
                dialogue_height = 85

                dialogue_x = (
                    person.x
                    + self.person_width // 2
                    - dialogue_width // 2
                )

                dialogue_y = (
                    person.y - 100
                )

                # ------------------------------------------------
                # KEEP BOX ON SCREEN
                # ------------------------------------------------

                dialogue_x = max(
                    10,
                    min(
                        dialogue_x,
                        self.screen_width
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
                    self.screen,
                    (255, 255, 255),
                    dialogue_rect,
                    border_radius=10
                )

                pygame.draw.rect(
                    self.screen,
                    (40, 40, 40),
                    dialogue_rect,
                    2,
                    border_radius=10
                )

                # ------------------------------------------------
                # TEXT
                # ------------------------------------------------

                dialogue_text = self.font_tiny.render(
                    person.dialogue,
                    True,
                    (40, 40, 40)
                )

                self.screen.blit(
                    dialogue_text,
                    (
                        dialogue_x + 15,
                        dialogue_y + 30
                    )
                )

    # ========================================================
    # TOWER / MAP
    # ========================================================

    def update_tower(self):

        pass

    def draw_tower(self):

        pass

    # ========================================================
    # SNACK SYSTEM
    # ========================================================

    def update_snacks(self):

        pass

    def draw_snacks(self):

        pass

    # ========================================================
    # STRESS LEVEL
    # ========================================================

    def get_stress_level(self):

        if self.stress >= 100:

            return "100"

        elif self.stress >= 75:

            return "75"

        elif self.stress >= 50:

            return "50"

        else:

            return "25"

    # ========================================================
    # STRESS POPUP
    # ========================================================

    def trigger_stress_popup(self, level):

        if level == "100":

            self.stress_popup = (
                "MAX STRESS! You're overwhelmed!"
            )

        elif level == "75":

            self.stress_popup = (
                "HIGH STRESS! Things are getting hectic."
            )

        elif level == "50":

            self.stress_popup = (
                "STEADY. Keep your cool."
            )

        elif level == "25":

            self.stress_popup = (
                "LOW STRESS! You're feeling relaxed."
            )

        self.stress_popup_timer = (
            self.stress_popup_duration
        )

    # ========================================================
    # UPDATE STRESS
    # ========================================================

    def update_stress(self):

        # Keep stress between 0 and 100

        self.stress = max(
            0,
            min(
                self.stress,
                100
            )
        )

        current_level = (
            self.get_stress_level()
        )

        # ----------------------------------------------------
        # TRIGGER POPUP WHEN ENTERING
        # DIFFERENT STRESS RANGE
        # ----------------------------------------------------

        if (
            current_level
            != self.last_stress_level
        ):

            self.trigger_stress_popup(
                current_level
            )

            self.last_stress_level = (
                current_level
            )

        # ----------------------------------------------------
        # POPUP COUNTDOWN
        # ----------------------------------------------------

        if self.stress_popup_timer > 0:

            self.stress_popup_timer -= 1

    # ========================================================
    # PLAYER SPEED
    # ========================================================

    def get_player_speed(self):

        # ----------------------------------------------------
        # 0-25%
        # CALM BUFF
        # ----------------------------------------------------

        if self.stress <= 25:

            return 6

        # ----------------------------------------------------
        # 26-50%
        # NORMAL
        # ----------------------------------------------------

        elif self.stress <= 50:

            return 5

        # ----------------------------------------------------
        # 51-75%
        # STRESSED
        # ----------------------------------------------------

        elif self.stress <= 75:

            return 4

        # ----------------------------------------------------
        # 76-100%
        # OVERWHELMED
        # ----------------------------------------------------

        else:

            return 3

    # ========================================================
    # STRESS EFFECT TEXT
    # ========================================================

    def get_stress_effect_text(self):

        if self.stress <= 25:

            return (
                "BUFF: Calm - movement speed increased"
            )

        elif self.stress <= 50:

            return (
                "STATUS: Normal"
            )

        elif self.stress <= 75:

            return (
                "DEBUFF: Stressed - movement slowed"
            )

        else:

            return (
                "DEBUFF: OVERWHELMED - movement greatly slowed"
            )

    # ========================================================
    # DRAW STRESS BAR
    # ========================================================

    def draw_stress_bar(self):

        # ----------------------------------------------------
        # LABEL
        # ----------------------------------------------------

        stress_text = self.font_small.render(
            f"STRESS: {int(self.stress)}%",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            stress_text,
            (
                self.stress_bar_x,
                self.stress_bar_y - 25
            )
        )

        # ----------------------------------------------------
        # BACKGROUND
        # ----------------------------------------------------

        pygame.draw.rect(
            self.screen,
            (70, 70, 70),
            (
                self.stress_bar_x,
                self.stress_bar_y,
                self.stress_bar_width,
                self.stress_bar_height
            )
        )

        # ----------------------------------------------------
        # FILLED BAR
        # ----------------------------------------------------

        filled_width = int(
            self.stress_bar_width
            * (self.stress / 100)
        )

        pygame.draw.rect(
            self.screen,
            (220, 70, 70),
            (
                self.stress_bar_x,
                self.stress_bar_y,
                filled_width,
                self.stress_bar_height
            )
        )

        # ----------------------------------------------------
        # BORDER
        # ----------------------------------------------------

        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            (
                self.stress_bar_x,
                self.stress_bar_y,
                self.stress_bar_width,
                self.stress_bar_height
            ),
            2
        )

    # ========================================================
    # DRAW STRESS POPUP
    # ========================================================

    def draw_stress_popup(self):

        if self.stress_popup_timer <= 0:

            return

        popup_width = 600
        popup_height = 90

        popup_x = (
            self.screen_width // 2
            - popup_width // 2
        )

        popup_y = 120

        popup_rect = pygame.Rect(
            popup_x,
            popup_y,
            popup_width,
            popup_height
        )

        # ----------------------------------------------------
        # BACKGROUND
        # ----------------------------------------------------

        pygame.draw.rect(
            self.screen,
            (40, 40, 40),
            popup_rect,
            border_radius=12
        )

        # ----------------------------------------------------
        # BORDER
        # ----------------------------------------------------

        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            popup_rect,
            2,
            border_radius=12
        )

        # ----------------------------------------------------
        # TEXT
        # ----------------------------------------------------

        text = self.font_main.render(
            self.stress_popup,
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            text,
            (
                self.screen_width // 2
                - text.get_width() // 2,
                popup_y + 27
            )
        )

    # ========================================================
    # START NEW DAY
    # ========================================================

    def start_new_day(self):

        # ----------------------------------------------------
        # IF DAY 5 IS FINISHED
        # GAME ENDS
        # ----------------------------------------------------

        if self.day >= self.max_day:

            self.game_state = "ENDING"

            return

        # ----------------------------------------------------
        # INCREASE DAY
        # ----------------------------------------------------

        self.day += 1

        # ----------------------------------------------------
        # NEW DAY VALUES
        # ----------------------------------------------------

        self.total_people_today = (
            self.interns_per_day[self.day]
        )

        self.people_completed = 0

        self.day_timer = (
            self.day_length
            * self.fps
        )

        self.spawn_timer = 0

        # ----------------------------------------------------
        # CLEAR PEOPLE
        # ----------------------------------------------------

        self.people.clear()

        self.target_person = None

        # ----------------------------------------------------
        # RESET PLAYER
        # ----------------------------------------------------

        self.player_x = (
            self.screen_width // 2
        )

        self.player_y = (
            self.screen_height // 2
        )

        # ----------------------------------------------------
        # RESET STRESS
        # ----------------------------------------------------

        self.stress = 50

        self.last_stress_level = None

    # ========================================================
    # UPDATE DAY TIMER
    # ========================================================

    def update_day_timer(self):

        self.day_timer -= 1

        # ----------------------------------------------------
        # DAY ENDS WHEN:
        #
        # 1. TIME RUNS OUT
        #
        # OR
        #
        # 2. ALL PEOPLE HAVE BEEN DEALT WITH
        # ----------------------------------------------------

        if (
            self.day_timer <= 0
            or
            self.people_completed
            >= self.total_people_today
        ):

            self.start_new_day()

    # ========================================================
    # DAY INFORMATION
    # ========================================================

    def draw_day_info(self):

        # ----------------------------------------------------
        # DAY
        # ----------------------------------------------------

        day_text = self.font_small.render(
            f"DAY {self.day}",
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
            self.screen,
            (50, 50, 50),
            day_background,
            border_radius=8
        )

        self.screen.blit(
            day_text,
            (30, 27)
        )

        # ----------------------------------------------------
        # PEOPLE LEFT
        # ----------------------------------------------------

        people_left = (
            self.total_people_today
            - self.people_completed
        )

        people_text = self.font_tiny.render(
            f"PEOPLE LEFT: {people_left}/{self.total_people_today}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            people_text,
            (30, 60)
        )

        # ----------------------------------------------------
        # TIME
        # ----------------------------------------------------

        seconds_left = max(
            0,
            self.day_timer // self.fps
        )

        minutes = (
            seconds_left // 60
        )

        seconds = (
            seconds_left % 60
        )

        time_text = self.font_tiny.render(
            f"TIME: {minutes}:{seconds:02d}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            time_text,
            (190, 25)
        )

        # ----------------------------------------------------
        # STRESS EFFECT
        # ----------------------------------------------------

        effect_text = self.font_tiny.render(
            self.get_stress_effect_text(),
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            effect_text,
            (190, 55)
        )

    # ========================================================
    # GAMEPLAY UPDATE
    # ========================================================

    def update_gameplay(self):

        # Stress determines movement speed

        self.player_speed = (
            self.get_player_speed()
        )

        self.update_player()

        self.update_people()

        self.update_tower()

        self.update_snacks()

        self.update_stress()

        self.update_day_timer()

    # ========================================================
    # GAMEPLAY DRAW
    # ========================================================

    def draw_gameplay(self):

        # ====================================================
        # BACKGROUND
        # ====================================================
        #
        # Day 1 = backgrounds[0]
        # Day 2 = backgrounds[1]
        # ...
        # Day 5 = backgrounds[4]
        #
        # ====================================================

        background = self.backgrounds[
            self.day - 1
        ]

        self.screen.blit(
            background,
            (0, 0)
        )

        # ====================================================
        # GAME OBJECTS
        # ====================================================

        self.draw_tower()

        self.draw_people()

        self.draw_player()

        self.draw_snacks()

        # ====================================================
        # UI
        # ====================================================

        self.draw_day_info()

        self.draw_stress_bar()

        self.draw_stress_popup()

    # ========================================================
    # ENDING
    # ========================================================

    def update_ending(self):

        pass

    def draw_ending(self):

        self.screen.fill(
            (30, 30, 50)
        )

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title = self.font_main.render(
            "THE WORKDAY IS OVER",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            title,
            (
                self.screen_width // 2
                - title.get_width() // 2,
                250
            )
        )

        # ----------------------------------------------------
        # MESSAGE
        # ----------------------------------------------------

        message = self.font_small.render(
            "You survived the Nokia Ottawa Office.",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            message,
            (
                self.screen_width // 2
                - message.get_width() // 2,
                310
            )
        )


# ============================================================
# START GAME
# ============================================================

def main():

    game = Game()

    game.run()


if __name__ == "__main__":

    main()
