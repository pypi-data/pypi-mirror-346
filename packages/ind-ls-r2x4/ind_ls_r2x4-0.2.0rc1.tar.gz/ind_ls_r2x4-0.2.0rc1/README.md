Driver package for the R2X4 light source from [Industrialise](www.industrialise.be).

# Installation
The package can be installed from the wheel file:
```bash
pip install ls_r2x4-0.2.0-py3-none-any.whl
```

There is an optional Qt based widget available, next to a tkinter based one.
The Qt widget uses `QtPy` to abstract the Qt backend. The package can be installed with:

```bash
pip install qtpy
```

The actual Qt backend needs to be installed separately. For example, to use the PySide2 backend:

```bash
pip install PySide2
```

QtPy5 and PySide6 are also supported. Checkout the `QtPy` [documentation](https://pypi.org/project/QtPy/) for information on which version of backend 
is supported by which version of `QtPy`.

There is also a `R2X4Panel` available for use in [Gamma Desk](https://pypi.org/project/gamma-desk/) which makes use of the Qt widget. Check the 
`ls_r2x4.gui.gdesk_panel` module for more information. To install Gamma Desk:
    
```bash
pip install gamma-desk
```

# Usage
## Demo

A demo is started when the package is run as a script:
```bash
python -m ls_r2x4
```

These top level scripts are available when the python environment is active:

  - `r2x4_gui_tkinter` : Start the GUI using the tkinter backend.
  - `r2x4_gui_qt`: Start the GUI using a Qt backend. This is needs pyqt or pyside to be installed!
  - `r2x4_demo`: Start the same demo as when the package is run as a script.

More demo scripts are available in the ls_r2x4.demo.demo module.

For jupyter lab users there is also a demo jupyter notebook available in the ls_r2x4.demo folder.

## Programming API

The main class to use is the `LightSourceR2X4` class. It is located in the ls_r2x4.r2x4 module.

```python
from ls_r2x4.r2x4 import LightSourceR2X4
ls = LightSourceR2X4()
```

A serial port name can be passed to the constructor, if left None it will try to find the correct port automatically.

Once the instance is created, the light source can be controlled using the methods and attributes of the class.

```python
import time
ls.triggering_force_a_channels()
ls.blue_a.value = 5  # set the blue a channel to 5%
ls.red_b.value = 3  # set the red b channel to 3%
time.sleep(2)
ls.triggering_force_b_channels()
time.sleep(1)
ls.blue_a.value = 0  # turn back off
ls.red_b.value = 0
```

Checkout the demo scripts for more examples.
