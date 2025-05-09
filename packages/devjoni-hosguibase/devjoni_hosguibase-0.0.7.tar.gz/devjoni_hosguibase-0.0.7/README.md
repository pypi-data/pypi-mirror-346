# Hosguibase - A multi-backend GUI toolkit

Hosguibase a toolkit for making graphical user interfaces using Python
Hosguibase uses other toolkits
as its backends, which allow programs to look native on many platforms.
Some backends may have qualities that make them better suited
for certain tasks.

Hosguibase does not aim to expose all or even many
functionalities of its backends. On the contrary, we look for a
minimal feature set that can be used to create acceptable applications.
This minimalism is to ease the workload needed to
maintain multiple backends.
You can use the features of a backend directly but this
will likely lock you down to that specific backend (which may not be
bad at all).

Hosguibase is developed by DEV Joni since 2023. Currently,
the project is in an early stage not recommended
for production.


## Installing

```
pip install devjoni-hosguibase
```

## API Overview

### Widgets

- MainWindow - The main window
- FrameWidget - Containment and partitioning
- TextWidget - Non-editable text (label)
- ButtonWidget - Clickable -> command
- SliderWidget - Slidable (scale)
- EntryWidget - Single-line editable text
- EditorWidget - Multiline editable text
- DropdownWidget - Selection (optionmenu)
- ImageWidget - Shows an image

The API resembles tkinter. When creating a new widget,
you specify its parent and then make the widget appear
on the screen by using the grid method.

### A hello world example

```python
import devjoni.guibase as gb

app = gb.MainWindow()
app.title = "My graphical program"
app.geometry = "small"

hello = gb.TextWidget(app)
hello.grid(row=0, column=0)

hello.set(text='Hello world!')

app.run()
```

## Supported Backends

Default backend: tkinter

- tkinter : The GUI toolkit based on tcl/tk that comes with Python
- gtk3/4 (via gi): A toolkit used for example by GNOME
- p3d : Panda3D - The open-source 3D rendering engine

The backend is currently selected with flags to the program.


### Tkinter backend (default)

Launching

```
python myprogram.py --tk
```

### GTK backends

Requirements

```
pip install PyGObject
```

Launching version 3
```
python myprogram.py --gtk3
```

or version 4

```
python myprogram.py --gtk4
```

### Panda3D backend

Requirements

```
pip install Panda3D
```

Launching

```
python myprogram.py --p3d
```


## Current Limitations

- Only grid layout engine supported (no free placement of widgets)
- Playing videos or 3D graphics not straighforward
- No dedicated touch or joystick support


## Contributing

### Reporting Issues

Please feel free to report any bugs or issues in our bug tracker in Github:

[https://github.com/devjonix/hosguibase/issues](https://github.com/devjonix/hosguibase/issues)

### Pull Requests

Despite commercial backing this is a true open-source project.
We appriciate any inputs to the project as GitHub pull requests.
