"""Sokoban: the classic puzzle game.

© Reuben Thomas <rrt@sc3d.org> 2025
Released under the GPL version 3, or (at your option) any later version.
"""

import os
import warnings
from enum import StrEnum, auto

from chambercourt.game import Game


# Placeholder for gettext
def _(message: str) -> str:
    return message


# Import pygame, suppressing extra messages that it prints on startup.
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from pygame import Color, Vector2


class Tile(StrEnum):
    """An enumeration representing the available map tiles."""

    FLOOR = auto()
    OUTSIDE = auto()
    WALL = auto()
    DIAMOND = auto()
    TARGET = auto()
    DIAMOND_ON_TARGET = auto()
    HERO_ON_TARGET = auto()
    HERO = auto()


class SokobanGame(Game[Tile]):
    def __init__(self) -> None:
        super().__init__(
            "sokoban",
            Tile,
            Tile.HERO,
            Tile.FLOOR,
            Tile.WALL,
        )

    @staticmethod
    def description() -> str:
        return _("Push the diamonds on to the targets.")

    @staticmethod
    def instructions() -> str:
        # fmt: off
        # TRANSLATORS: Please keep this text wrapped to 40 characters. The font
        # used in-game is lacking many glyphs, so please test it with your
        # language and let me know if I need to add glyphs.
        return _("""\
Push the diamonds on to the targets.
""")
        # fmt: on

    screen_size = (2560, 2048)
    window_size = (2048, 2048)
    default_background_colour = Color(0, 0, 0)
    window_scale = 1
    font_scale = 8

    def init_game(self) -> None:
        for x in range(self.level_width):
            for y in range(self.level_height):
                block = self.get(Vector2(x, y))
                if block in (Tile.HERO, Tile.HERO_ON_TARGET):
                    self.hero.position = Vector2(x, y)
                    self.set(
                        self.hero.position,
                        Tile.FLOOR if block == Tile.HERO else Tile.TARGET,
                    )

    def can_move(self, velocity: Vector2) -> bool:
        newpos = self.hero.position + velocity
        block = self.get(newpos)
        if block in (Tile.FLOOR, Tile.TARGET):
            return True
        if block in (Tile.DIAMOND, Tile.DIAMOND_ON_TARGET):
            new_rockpos = self.hero.position + velocity * 2
            return self.get(new_rockpos) in (Tile.FLOOR, Tile.TARGET)
        return False

    def do_play(self) -> None:
        newpos = self.hero.position + self.hero.velocity
        block = self.get(newpos)
        if block in (Tile.DIAMOND, Tile.DIAMOND_ON_TARGET):
            new_diamond_pos = newpos + self.hero.velocity
            new_pos_block = self.get(new_diamond_pos)
            self.set(
                new_diamond_pos,
                Tile.DIAMOND if new_pos_block == Tile.FLOOR else Tile.DIAMOND_ON_TARGET,
            )
            self.set(newpos, Tile.FLOOR if block == Tile.DIAMOND else Tile.TARGET)

    def show_status(self) -> None:
        self.print_screen(
            (0, 0),
            _("Level {}").format(self.level),
            width=self.surface.get_width(),
            align="center",
            color="grey",
        )
        column_width = 500
        self.print_screen(
            (32, 2), _("Moves"), width=column_width, align="center", color="grey"
        )
        self.print_screen(
            (32, 3), str(self.moves), width=column_width, align="center"
        )

    def finished(self) -> bool:
        for y in range(self.level_height):
            for x in range(self.level_width):
                if self.get(Vector2(x, y)) == Tile.DIAMOND:
                    return False
        return True
