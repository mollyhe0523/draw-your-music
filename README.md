# Draw your music
To launch the program, simply run the "run.py" in the code folder.

## Introduction
This program allows you to create music by drawing.

You can first decide the tonality/style of the music:
![tonality](https://github.com/mollyhe0523/draw-your-music/raw/master/demo/tonality.png)

Then draw lines to create music with choices of 4 musical instruments:
![toolbar](https://github.com/mollyhe0523/draw-your-music/raw/master/demo/toolbar.png)
![canvas](https://github.com/mollyhe0523/draw-your-music/raw/master/demo/canvas.jpg)

## Demo
Click [here](https://mollyhwy.com/archives/251).

## Technical Explanation

### Technical Diagram
![diagram](https://github.com/mollyhe0523/draw-your-music/raw/master/demo/diagram.png)

### Python Library Used
- GUI-- tkinter
- Synthesis-- pretty_midi

### Task Breakdown
__Molly -- GUI__
1. Get and set user's choice of tonality/style:
  ```Python
  def clicked(key, major):
      global mykey, mymajor, west
      tonality = Label(root,text = "Generating music at "+key+" "+major+"!")
      tonality.grid(column=2)
      mykey = key
      mymajor = major
      west = True
      if ma_or_mi.get() == "Chinese" or ma_or_mi.get() == "Japanese":
          west = False
          eastern_canvas()
      else:
          western_canvas()
      show_toolbar()
  ```
2. Let the user draw on the canvas while synchronously collecting every points drawn:
  ```Python
  def w_draw(event):
      global mylist,color, i
      x, y = event.x, event.y
      if 40<=x<=1240 and 20<=y<=510:
          mylist.append((x-40,510-y,color))
          if canvas.old_coords:
              x1, y1 = canvas.old_coords
              if x!= x1 and y == y1:
                  if x>x1:
                      for i in range(1,x-x1,2):
                          mylist.append((x1+i-40,510-y,color))
                  else:
                      for i in range(1,x1-x,2):
                          mylist.append((x+i-40,510-y,color))
              elif x == x1 and y != y1:
                  if y>y1:
                      for i in range(1,y-y1,2):
                          mylist.append((x-40,510-(y1+i),color))
                  else:
                      for i in range(1,y1-y,2):
                          mylist.append((x-40,510-(y+i),color))
              i = canvas.create_line(x, y, x1, y1, width=8, fill = color)
              print(i)
          canvas.old_coords = x, y
  ```
3. Bind left mouse click with draw and reset:
  ```Python
  drawing.bind('<B1-Motion>', w_draw)
  drawing.bind('<ButtonRelease-1>', reset_coords)
  ```

__Sophia -- Analysis & Synthesis__
1. Encoding keys and tonality with midi key notation:
  ```Python
  def key_library(key):
      library={"C": 12,"D":14, "E":16, "F": 17, "G":19, "A": 21, "B": 23}
      return library[key]

  def major_library(key_name):
      library={"major":[0,2,4,5,7,9,11],"natural_minor":[0,2,3,5,7,8,10], \
               "harmonic_minor":[0,2,3,5,7,8,11],"melodic_minor":[0,2,3,5,7,9,11], \
               "Chinese":[0,2,4,7,9],"Japanese": [0,2,3,7,8]}
      return library[key_name]
  ```
2.

### Future goals
- More __flexibility__ at user’s end: speed, velocity, volume, start and end of each note.
- More __accuracy__ over the translation between image and piano roll.
- More __controllability__: make the drawing itself easier + add recall/eraser function.
- __Longer__: support drawing longer pieces of music
