# Project Portfolio

Static portfolio site. Project content lives in `make_data.py` (writes `data.json`). Edit it, then run:

    python3 make_data.py && python3 build.py

To add screenshots to a project, put images in an `img/` folder and add `images=["img/name.png"]` to that project's `add(...)` call. To link code, add `repo="https://github.com/..."`.

Add your headshot as `img/photo.jpg` (square works best) and run `python3 build.py`; it replaces the "EL" circle in the hero.
