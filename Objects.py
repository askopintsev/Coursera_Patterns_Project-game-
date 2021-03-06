from abc import ABC, abstractmethod
# import pygame
# import random


# def create_sprite(img, sprite_size):
#     icon = pygame.image.load(img).convert_alpha()
#     icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
#     sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
#     sprite.blit(icon, (0, 0))
#     return sprite


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


class AbstractObject(ABC):
    def __init__(self):
        pass

    def draw(self, display, sprite_size):
        display.blit(self.sprite, (sprite_size, sprite_size))


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.max_hp = None
        self.calc_max_hp()
        self.hp = self.max_hp

    def calc_max_hp(self):
        self.max_hp = 5 + self.stats["endurance"] * 2


class Enemy(Creature, Interactive):
    def __init__(self, icon, stats, xp, position, mob_type):
        self.sprite = icon
        self.stats = stats
        self.xp = xp
        self.position = position
        self.mob_type = mob_type

    def interact(self, engine, hero):
        if self.mob_type == 'rat':
            hero.hp -= 1
        elif self.mob_type == 'knight':
            hero.hp -= 2
        elif self.mob_type == 'naga':
            hero.hp -= 4
        elif self.mob_type == 'dragon':
            hero.hp -= 8
        hero.exp += self.xp
        while hero.level_up():
            engine.notify(f"Level up! Now you're level {hero.level}")


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [2, 2]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_hp()
            self.hp = self.max_hp
            return True


class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        pass


class Berserk(Effect):

    def apply_effect(self):
        self.stats["strength"] += 5
        self.stats["endurance"] += 5
        self.stats["intelligence"] -= 3


class Blessing(Effect):

    def apply_effect(self):
        self.stats["strength"] += 2
        self.stats["endurance"] += 2
        self.stats["intelligence"] += 2
        self.stats["luck"] += 2


class Weakness(Effect):

    def apply_effect(self):
        self.stats["strength"] -= 5
        self.stats["endurance"] -= 2
        self.stats["intelligence"] -= 1
