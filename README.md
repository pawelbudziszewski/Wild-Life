# Wild-Life
## Interactive Game of Life
This is my small lockdown-weekend project: my tribute to [John Horton Conway](https://en.wikipedia.org/wiki/John_Horton_Conway) - an interactive version of Life Game.
I always wondered, how fun it would be to be able modify life's world in the runtime. So here it is: use your mouse to add new life forms.

Video demonstration:

[![Watch the video](https://img.youtube.com/vi/WSkPuXGfMSo/hqdefault.jpg)](https://youtu.be/WSkPuXGfMSo)

### What you need:

-	Python 3.8 or newer (should work on 3.6+, but I didn't test it)
-	Numpy (`pip install numpy`)
- Scipy (`pip install scipy`)
-	OpenCV (`pip install opencv-python`)

It should run on any system where you can install Python with modules listed above, however I tested it only on Windows.

### How to run it:
Run `python3.exe wild_life.py` (or equivalent on your system)

### How to use it:

-	Mouse-click anywhere to insert species
-	Mouse-click on the species list in the bottom to select species to be inserted
-	`1`, `2`, `3`, `4` keys to change color map
-	`Esc` to exit

All configuration parameters are stored in the first part of wild_life.py file.

## Bonus: minimal code - 154 bytes

The [minimal_code](minimal_code) folder contains shortest python implementation I was able to create. It's fully functional (though not interactive), with OpenCV visualisation, very fast. In only `154 bytes` of code :)

Hit `Esc` to exit.

## Copyright
Copyright 2021, 2022 [Paweł Budziszewski](https://github.com/pawelbudziszewski)
