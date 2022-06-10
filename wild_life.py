"""Wild Life
An interactive version of Conway’s Life Game, written in Python. 

Source and description:
   https://github.com/pawelbudziszewski/Wild-Life

Copyright 2021, 2022 Paweł Budziszewski


This is an interactive version of Conway’s Life Game, written in Python. 
It allows placing different life forms using mouse while game is running.

How to run it:
On Windows just execute 'python3.exe wild_life.py'
In theory this code should run fine also on Linux, but I did not test it.

How use it:
 - Mouse-click anywhere to insert species
 - Mouse-click on the species list in the bottom to select species to 
   be inserted
 - [1], [2], [3], [4] keys to change color map
 - [Esc] to exit


Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import time
import random

import numpy as np
import cv2
from scipy.signal import convolve2d

import life_forms


## ----- Configuration parameters -----

# Size of the world (number of grid cells)
WIDTH=600
HEIGHT=300

# Magnification - each cell will be displayed as NxN pixels.
N=2

# Do we want to wrap the world? If yes, everything that moves outside
# of the border will appear at opposite border.
WRAP_WORLD = False

# Dying life cells leaves shadows. FADE_COEFFICIENT determines,
# how long this shadow will last. Greater value - longer shadow
# lifetime. Value of 0.0 means no shadows.
# This value should be larger or equal to 0 and lower than 1 - other
# values are technically possible, but may give awkward results (have 
# fun testing).
FADE_COEFFICIENT = 0.6

# Color maps we can use
COLOR_MAPS = [cv2.COLORMAP_BONE,
              cv2.COLORMAP_HOT,
              cv2.COLORMAP_OCEAN,
              cv2.COLORMAP_PINK
             ]
# Initial color map
INITIAL_COLOR_MAP = 0

# Life forms to be used in menu (see life_forms.py)
SPECIES_MENU_ITEMS = [
              life_forms.GOSPER_GLIDER_GUN,
              life_forms.GLIDERS,
              life_forms.TURTLE_R,
              life_forms.BLIMKER_PUFFER,
              life_forms.KOK_GALAXY,
              life_forms.PULSAR,
              life_forms.BLANK,
              ]
# Initially selected life form
INITIAL_SPECIES_MENU_ITEM = 0

## ----- Configuration end -----


class WildLife:
    """ Life class"""

    def __init__(self):
        self.W = WIDTH
        self.H = HEIGHT
        self.N = N

        self.current_species = INITIAL_SPECIES_MENU_ITEM

        # This will be our arena
        self.world = np.zeros([self.H,self.W])
        # Arena transformed into image to be displayed
        self.world_img=np.ones([self.H,self.W])*0.5

        self.color_map_id = INITIAL_COLOR_MAP

        # Convolution kernel (for counting neighbours)
        self.conv_kernel = np.ones((3, 3))
        self.conv_kernel[1,1] = 0

        self.generate_menu()


    def generate_image(self):
        """ Generate OpenCV image based on game's world and menu
        """
        img = self.world_img*-1+1
        remapped = cv2.applyColorMap((img*255).astype(np.uint8), COLOR_MAPS[self.color_map_id])
        remapped = np.vstack((remapped,self.menu))
        if self.N>1:
            remapped=remapped.repeat(self.N, axis=0).repeat(self.N, axis=1)
        return remapped


    def life_step(self):
        """ One step of life cycle
        """
        if WRAP_WORLD:
            boundary = 'wrap'
        else:
            boundary = 'fill'
        neighbors_count = convolve2d(self.world, self.conv_kernel, mode='same', boundary=boundary)
        self.world = (neighbors_count==3) | ((self.world==1) & (neighbors_count==2))

        self.world_img *= FADE_COEFFICIENT
        self.world_img += self.world


    def add_species(self, y, x, species, arena=None, center = True):
        """ Add life form to grid

        Keyword arguments:
        x, y -- where to place the species
        species -- 2D Nupmy array containing species definition
                   (0 - empty space, 1 - life cell)
        arena -- array on which species will be placed. If not provided,
                 self.world will be used
        center -- do x, y coordinates describe center of
                  the species (True), or upper-left corner (False)
        """

        if arena is None:
            arena = self.world

        (h,w) = species.shape
        if center:
            y-=h//2
            x-=w//2

        if y<0:
            y = 2
        if x<0:
            x = 2
        if y+h>=arena.shape[0]:
            y = arena.shape[0]-h
        if x+w>=arena.shape[1]:
            x = arena.shape[1]-w

        arena[y:y+species.shape[0], x:x+species.shape[1]] = species


    def generate_aquarium(self, coords, density=0.15):
        """ Generate rectangular aquarium with randomally placed life 
        cells

        Keyword arguments:
        coords -- list of 4 values describing coordinates of
                  upper left and lower right corners: (x1, y1, x2, y2)
        density -- coefficient describing how many grid cells will be
                   filled in: 0 - none, 1 - all
        """

        aquarium = (np.random.rand(coords[3]-coords[1], coords[2]-coords[0]) < density)
        self.world[coords[1]:coords[3], coords[0]:coords[2]] = aquarium.astype(int)


    def generate_menu(self):
        """ Generate menu with list of species
        """

        max_w = max([item.shape[1] for item in SPECIES_MENU_ITEMS])
        max_h = max([item.shape[0] for item in SPECIES_MENU_ITEMS])

        self.menu_items_coordinates = []
        self.menu = np.ones([max_h+5,self.W])*0.05

        w = max_w//2+2
        h = max_h//2+2
        bgr=np.zeros((max_h+2,max_w+2))
        bgr_border=np.ones((max_h+4,max_w+4))*0.5
        bgr_border[1:-1,1:-1] = 0.0

        for i, item in enumerate(SPECIES_MENU_ITEMS):
            if i==self.current_species:
                self.add_species(h,i*(max_w+4)+w, bgr_border, arena = self.menu)
            else:
                self.add_species(h,i*(max_w+4)+w, bgr, arena = self.menu)
            self.add_species(h,i*(max_w+4)+w, item, arena = self.menu)

            coords = (i*(max_w+4),(i+1)*(max_w+4))
            self.menu_items_coordinates.append(coords)
        self.menu = self.menu*-1+1
        self.menu = cv2.applyColorMap((self.menu*255).astype(np.uint8), COLOR_MAPS[self.color_map_id])


    def _click_menu(self, y, x):
        """ Process clicking on the menu

        Internal method
        """

        for i,coords in enumerate(self.menu_items_coordinates):
            if coords[1]>=x>=coords[0]:
                self.current_species = i
        self.generate_menu()


    def click(self, event, x, y, flags, param):
        """ Event to be connected with OpenCV click
        Usage:
        cv2.setMouseCallback(window_name, life_object.click)

        Keyword arguments:
        event -- OpenCV event
        x, y -- screen-space coordinates of mouse click
        flags, param -- other OpenCV callback parameters
        """
        if event == cv2.EVENT_LBUTTONDOWN :
            if y//self.N > self.H:
                self._click_menu(y//self.N-self.H, x//self.N)
            else:
                self.add_species(y//self.N, x//self.N, SPECIES_MENU_ITEMS[self.current_species])


    def get_population(self):
        """ Return current population
        """
        return np.sum(self.world)


print("Starting the journey of your life!")

life = WildLife()
life.generate_aquarium(coords=(0, int(HEIGHT*0.7), WIDTH-1, HEIGHT-1))

cv2.namedWindow('Wild Life')
cv2.setMouseCallback('Wild Life', life.click)

info_str=""

# This is a list of last fps values (initially zeros). Mean value
# will be displayed. Make it larger to have smoother fps display.
# Size of 1 will give real-time readings.
fps_history=np.zeros((80))

start_time=time.time()

# Uncomment to wait for a key before app starts
#cv2.waitKey()

while cv2.getWindowProperty('Wild Life', cv2.WND_PROP_VISIBLE) >= 1:

    life.life_step()
    out=life.generate_image()

    pos = (out.shape[1]-250, out.shape[0]-10)
    out = cv2.putText(out, info_str, org=pos, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.45,
        color=(150,100,100), thickness=1, lineType=cv2.LINE_AA)
    cv2.imshow("Wild Life", out)

    # Hit Esc to exit
    k = cv2.waitKey(1)
    if k%256 == 27:
        break
      
    # Hit number keys (1..0) to change color maps
    n=k%256-49
    if 0<=n<len(COLOR_MAPS):
        life.color_map_id=n

    # Going too fast? Want to see what's happening? Add sleep here
    #time.sleep(0.2)

    fps = 1.0/(time.time()-start_time)
    start_time=time.time()
    fps_history = np.delete(fps_history, 0)
    fps_history = np.append(fps_history,[fps])
    info_str=f"population: {life.get_population()}  fps: {np.mean(fps_history):.1f}"

# Uncomment to wait for a key on exit before main windows dies
#cv2.waitKey()
cv2.destroyAllWindows()
