#!/usr/bin/env python

import pyautogui
import time

class Land():
    def __init__(self, x, y, corn):
        self.pos = [x, y]
        self.corn = corn
        self.plant = [x + 260, y + 160]

chicken_food_timer = 0
corn_timer = 0
chicken_timer = 0
chicken_food_in_progress = False
chicken_in_progress = False

class ChickenCoop():
    def __init__(self, x, y, eggs):
        self.pos = [x, y]
        self.eggs = eggs
        self.produce = [x + 260, y + 160]

class Mill():
    def __init__(self, x, y):
        self.pos = [x, y]
        self.prod = [x + 260, y + 160]
        self.chicken_food = [x - 190, y + 279]

lands = []

#RESOURCES
corn = 484
chicken_food = 490
eggs = 0

#GAINS
corn1 = 16
corn2 = 15
corn3 = 15

egg1 = 27

#POSITIONS
mon_width = 1920

lands.append(Land(mon_width + 630, 564, corn=16))
lands.append(Land(mon_width + 512, 618, corn=15))
lands.append(Land(mon_width + 597, 659, corn=15))

chicken_coops = []
chicken_coops.append(ChickenCoop(mon_width + 776, 445, egg1))
chicken_coops.append(ChickenCoop(mon_width + 734, 509, egg1))

mill = Mill(mon_width + 625, 486)

def move_and_click(pos):
    pyautogui.moveTo(pos[0], pos[1], 0.5)
    pyautogui.click()

def harvest_corn():
    global corn

    for land in lands:
        move_and_click(land.pos)
        corn += land.corn


def plant_corn():
    for land in lands:
        move_and_click(land.pos)
        move_and_click(land.plant)

    global corn_timer
    corn_timer = 0

def start_chicken_food():
    move_and_click(mill.pos)

    move_and_click(mill.chicken_food)
    move_and_click(mill.prod)

    global corn
    corn -= 161
    global chicken_food_timer
    chicken_food_timer = 0
    global chicken_food_in_progress
    chicken_food_in_progress = True

def get_chicken_food():
    move_and_click(mill.pos)
    chicken_food_in_progress = False

    global chicken_food
    chicken_food += 70

def start_chicken():
    global chicken_food

    for coop in chicken_coops:
        move_and_click(coop.pos)
        move_and_click(coop.produce)
        chicken_food -= 10

    global chicken_in_progress
    chicken_in_progress = True
    global chicken_timer
    chicken_timer = 0

def harvest_chicken():
    global eggs

    for coop in chicken_coops:
        move_and_click(coop.pos)
        eggs += 27

    global chicken_in_progress
    chicken_in_progress = False

chicken_food_time = 11 * 60 + 12
corn_time = 120
chicken_time = 6 * 60 + 30

plant_corn()
while True:
    if corn > 161 and not chicken_food_in_progress:
        start_chicken_food()

    if chicken_food > len(chicken_coops) * 10 and not chicken_in_progress:
        start_chicken()

    if chicken_food_timer == chicken_food_time:
        get_chicken_food()
    elif chicken_food_in_progress:
        chicken_food_timer += 1
        if chicken_food_timer % 10 == 0:
            print('Harvesting chicken food in: %d seconds' % (chicken_food_time - chicken_food_timer))

    if corn_timer == corn_time:
        harvest_corn()
        plant_corn()
    else:
        corn_timer += 1
        if corn_timer % 10 == 0:
            print('Harvesting and planting corn in: %d seconds' % (corn_time - corn_timer))

    if chicken_timer == chicken_time and chicken_in_progress:
        harvest_chicken()
    elif chicken_in_progress:
        chicken_timer += 1
        if chicken_timer % 10 == 0:
            print('Harvesting chicken in: %d seconds' % (chicken_time - chicken_timer))

    time.sleep(1)
