# Copyright (C) 2025 <UTN FRA>
#
# Author: Facundo Falcone <f.falcone@sistemas-utnfra.com.ar>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame as pg
from .button import Button
from .game_sound import GameSound

class ButtonSound(Button):
    
    def __init__(self, x, y, text, screen, font_path: str, sound_path: str, color: tuple = (255,0,0), font_size = 25, on_click = None, on_click_param = None):
        super().__init__(x, y, text, screen, font_path, color, font_size, on_click, on_click_param)
        self.click_option_sfx = GameSound()
        self.sound_path = sound_path
        
    def button_pressed(self):
        """
        This function checks if a button is pressed and triggers an action when it is clicked.
        """
        mouse_pos = pg.mouse.get_pos()
        
        if self.rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0] == 1:
                pg.time.delay(300)
                self.on_click(self.on_click_param)
                self.click_option_sfx.play_sound(self.sound_path)
                
    def draw(self):
        super().draw()
    
    def update(self):
        """
        The `update` function in Python calls the `draw` and `button_pressed` methods.
        """
        super().update()