import pygame as pg
from noise import snoise2


class Speech:
    def __init__(self, speech: str = "Bonjour!", sounds: dict = {}):
        self.speech = speech
        self.sounds = sounds

        self.pos = 0
        self.dt = 0.0
        self.waiting = 0.0
        self.finished = False
    
    def update(self, dt: int = 16, tick: int = 0):
        if not self.finished:
            if self.waiting <= 0.0:
                self.dt += dt * 0.005 + (snoise2(tick * 0.0005, 0) + 1.0) * 0.25

                if int(self.dt) != self.pos:
                    # Next character
                    self.pos = int(self.dt)
                    if self.pos >= len(self.speech):
                        self.finished = True
                    
                    else:
                        char = self.speech[self.pos].lower()

                        # Play the sound
                        if char in self.sounds:
                            self.sounds[char].play()

                        # Mark a pause at next character
                        if char in ["!", "?", ".", ",", "\n"]:
                            self.waiting = 0.35
                        elif char in [" "]:
                            self.waiting = 0.03
                
            else:
                self.waiting -= dt * 0.001
    
    def render(
        self,
        surf: pg.Surface,
        x: int = 0,
        y: int = 0,
        color: pg.Color = (255, 255, 255),
        line_height: int = 18,
        font: pg.font.Font | None = None,
        width: int = 80
    ):
        # Speech lines
        for i, l in enumerate(self.wrap_text(self.speech[:self.pos], width)):
            text_surf = font.render(l, True, color)
            surf.blit(text_surf, (x, y + line_height * i))

    @staticmethod
    def get_wrap_line(text: str, width: int):
        # New line at line jump
        for i in range(min(width, len(text))):
            if text[i] == "\n":
                return text[:i], i + 1
        
        j = width
        if j < len(text):
            # Truncate
            while text[j] != " ":
                j -= 1
            
            j += 1
            return text[:j], j
        
        else:
            # Rest
            return text, len(text)

    def wrap_text(self, text: str, width: int = 80):
        while text:
            l, i = self.get_wrap_line(text, width)
            text = text[i:]
            yield l
