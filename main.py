import pygame
import random


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

        self.width = game.person_width
        self.height = game.person_height

        self.speed = random.uniform(
            1.5,
            3.0
        )

        self.state = "WALKING"

        self.dialogue = ""
        self.dialogue_timer = 0

        self.dialogue_duration = int(
            1.5 * game.fps
        )

    def get_rect(self):

        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )

    def update(self):

        if self.state == "WALKING":

            self.x += self.speed

        elif self.state == "DIALOGUE":

            self.dialogue_timer += 1

            if (
                self.dialogue_timer
                >= self.dialogue_duration
            ):

                self.state = "LEAVING"

        elif self.state == "LEAVING":

            self.y -= 5

    def draw(self, screen):

        screen.blit(
            self.image,
            (
                int(self.x),
                int(self.y)
            )
        )


class Game:

    def __init__(self):

        pygame.init()

        # Settings

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

        # Game state

        self.game_state = "INTRO"

        # Day system

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

        # Stress

        self.stress = 50
        self.last_stress_level = None

        # Player

        self.player_width = 60
        self.player_height = 90

        self.player_x = (
            self.screen_width // 2
        )

        self.player_y = (
            self.screen_height // 2
        )

        self.player_speed = 5

        # People

        self.person_width = 60
        self.person_height = 90

        self.people = []
        self.target_person = None

        self.spawn_timer = 0
        self.spawn_interval = 90

        # Backgrounds

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

            self.backgrounds.append(image)

        # Intern sprites

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

            self.intern_images.append(image)

        # Full-time worker sprites

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

            self.fulltime_images.append(image)

        # Player image

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

        # Fonts

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

        # Cutscene

        self.lines = [
            "In the Mokia Ottawa Office...",
            "...the towers are divided.",
            "Meet your office worker. Stress: rising.",
            "Work is piling up. The snack table is under threat.",
            "Defend your tower. Don't let those interns get to the snacks!"
        ]

        self.line_index = 0

        # Stress bar

        self.stress_bar_width = 250
        self.stress_bar_height = 25

        self.stress_bar_x = (
            self.screen_width
            - self.stress_bar_width
            - 30
        )

        self.stress_bar_y = 30

        # Stress popups

        self.stress_popup = ""
        self.stress_popup_timer = 0
        self.stress_popup_duration = 150

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

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                return False

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

            elif self.game_state == "GAMEPLAY":

                if (
                    event.type
                    == pygame.MOUSEBUTTONDOWN
                ):

                    if event.button == 1:

                        self.catch_person(
                            event.pos
                        )

            elif self.game_state == "ENDING":

                pass

        return True

    def update(self):

        if self.game_state == "INTRO":

            self.update_cutscene()

        elif self.game_state == "GAMEPLAY":

            self.update_gameplay()

        elif self.game_state == "ENDING":

            self.update_ending()

    def draw(self):

        if self.game_state == "INTRO":

            self.draw_cutscene()

        elif self.game_state == "GAMEPLAY":

            self.draw_gameplay()

        elif self.game_state == "ENDING":

            self.draw_ending()

    def update_cutscene(self):

        pass

    def draw_cutscene(self):

        self.screen.fill(
            (251, 198, 207)
        )

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

    def update_player(self):

        if self.target_person is not None:

            target_x = (
                self.target_person.x
                + self.person_width // 2
                - self.player_width // 2
            )

            if self.player_x < target_x:

                self.player_x += self.player_speed

            elif self.player_x > target_x:

                self.player_x -= self.player_speed

            if (
                abs(
                    self.player_x
                    - target_x
                )
                <= self.player_speed
            ):

                self.player_x = target_x

                person = self.target_person

                self.target_person = None

                person.state = "DIALOGUE"
                person.dialogue_timer = 0

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

        else:

            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:

                self.player_y -= self.player_speed

            if keys[pygame.K_s]:

                self.player_y += self.player_speed

            if keys[pygame.K_a]:

                self.player_x -= self.player_speed

            if keys[pygame.K_d]:

                self.player_x += self.player_speed

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

    def draw_player(self):

        self.screen.blit(
            self.player_image,
            (
                self.player_x,
                self.player_y
            )
        )

    def spawn_person(self):

        x = -self.person_width

        y = random.randint(
            170,
            300
        )

        is_intern = (
            random.random() < 0.20
        )

        if is_intern:

            image = random.choice(
                self.intern_images
            )

        else:

            image = random.choice(
                self.fulltime_images
            )

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

    def catch_person(self, pos):

        if self.target_person is not None:

            return

        for person in self.people:

            if person.state != "WALKING":

                continue

            if person.get_rect().collidepoint(pos):

                self.target_person = person

                break

    def update_people(self):

        self.spawn_timer += 1

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

        for person in self.people:

            person.update()

        remaining_people = []

        for person in self.people:

            if (
                person.state == "WALKING"
                and person.x > self.screen_width
            ):

                if person.is_intern:

                    self.stress += 5

                self.people_completed += 1

                continue

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

    def draw_people(self):

        for person in self.people:

            person.draw(
                self.screen
            )

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

    def update_tower(self):

        pass

    def draw_tower(self):

        pass

    def update_snacks(self):

        pass

    def draw_snacks(self):

        pass

    def get_stress_level(self):

        if self.stress >= 100:

            return "100"

        elif self.stress >= 75:

            return "75"

        elif self.stress >= 50:

            return "50"

        else:

            return "25"

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

    def update_stress(self):

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

        if self.stress_popup_timer > 0:

            self.stress_popup_timer -= 1

    def get_player_speed(self):

        if self.stress <= 25:

            return 6

        elif self.stress <= 50:

            return 5

        elif self.stress <= 75:

            return 4

        else:

            return 3

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

    def draw_stress_bar(self):

        stress_text = self.font_small.render(
            f"STRESS: {int(self.stress)}%",
            True,
            (0, 0, 0)
        )

        self.screen.blit(
            stress_text,
            (
                self.stress_bar_x,
                self.stress_bar_y - 25
            )
        )

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

        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            (
                self.stress_bar_x,
                self.stress_bar_y,
                self.stress_bar_width,
                self.stress_bar_height
            ),
            2
        )

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

        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            popup_rect,
            border_radius=12
        )

        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            popup_rect,
            2,
            border_radius=12
        )

        text = self.font_main.render(
            self.stress_popup,
            True,
            (0, 0, 0)
        )

        self.screen.blit(
            text,
            (
                self.screen_width // 2
                - text.get_width() // 2,
                popup_y + 27
            )
        )

    def start_new_day(self):

        if self.day >= self.max_day:

            self.game_state = "ENDING"

            return

        self.day += 1

        self.total_people_today = (
            self.interns_per_day[self.day]
        )

        self.people_completed = 0

        self.day_timer = (
            self.day_length
            * self.fps
        )

        self.spawn_timer = 0

        self.people.clear()

        self.target_person = None

        self.player_x = (
            self.screen_width // 2
        )

        self.player_y = (
            self.screen_height // 2
        )

        self.stress = 50
        self.last_stress_level = None

    def update_day_timer(self):

        self.day_timer -= 1

        if (
            self.day_timer <= 0
            or
            self.people_completed
            >= self.total_people_today
        ):

            self.start_new_day()

    def draw_day_info(self):

        day_text = self.font_small.render(
            f"DAY {self.day}",
            True,
            (0, 0, 0)
        )

        day_background = pygame.Rect(
            20,
            20,
            150,
            80
        )

        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            day_background,
            border_radius=8
        )

        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            day_background,
            2,
            border_radius=8
        )

        self.screen.blit(
            day_text,
            (30, 27)
        )

        people_left = (
            self.total_people_today
            - self.people_completed
        )

        people_text = self.font_tiny.render(
            f"PEOPLE LEFT: {people_left}/{self.total_people_today}",
            True,
            (0, 0, 0)
        )

        self.screen.blit(
            people_text,
            (30, 60)
        )

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
            (0, 0, 0)
        )

        self.screen.blit(
            time_text,
            (190, 25)
        )

        effect_text = self.font_tiny.render(
            self.get_stress_effect_text(),
            True,
            (0, 0, 0)
        )

        self.screen.blit(
            effect_text,
            (190, 55)
        )

    def update_gameplay(self):

        self.player_speed = (
            self.get_player_speed()
        )

        self.update_player()
        self.update_people()
        self.update_tower()
        self.update_snacks()
        self.update_stress()
        self.update_day_timer()

    def draw_gameplay(self):

        background = self.backgrounds[
            self.day - 1
        ]

        self.screen.blit(
            background,
            (0, 0)
        )

        self.draw_tower()
        self.draw_people()
        self.draw_player()
        self.draw_snacks()

        self.draw_day_info()
        self.draw_stress_bar()
        self.draw_stress_popup()

    def update_ending(self):

        pass

    def draw_ending(self):

        self.screen.fill(
            (30, 30, 50)
        )

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

        message = self.font_small.render(
            "You survived the Mokia Ottawa Office.",
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


def main():

    game = Game()

    game.run()


if __name__ == "__main__":

    main()
