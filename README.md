# EasyDict
The first open source translator which is completely open with dictionary data too. The homepage is http://easydict.jiri.one. On this page you can also try the search results, which will be the same as in the app (however, the web application does not use TinyDB+orjson as a backend, but uses RethinkDB - the source data is the same). 
**The application is at an early stage of development, but the features and dictionaries that have already been implemented work very well.**

## What is it

EasyDict is a simple translator that will translate, typically, one word in one language into another language. This translator has several, sometimes unique, features. 

1. It is written in Python.
2. It uses the fastest json implementation for storing dictionaries - [orjson](https://github.com/ijl/orjson) (own orjson storage for [TinyDB](https://tinydb.readthedocs.io)).
3. The user interface is written in [PyGObject](https://pygobject.readthedocs.io) (GTK3.0).
4. The application starts hidden in tray and tapping tray brings up the main application window - [xapp](https://github.com/linuxmint/xapp) library is used.
5. If you have the main application window displayed, it is displayed on top and overlays all other windows. In this mode, the app monitors the clipboard and automatically translates the words you copy into it.
6. You can use either a whole word search or a full-text.

## Currently available dictionaries
Currently only Czech-English and English-Czech dictionaries are available. This dictionary data comes from the http://svobodneslovniky.cz project (the dictionary data is therefore governed by the GNU/FDL license).

Screenshots
---


| Welcome Screen| Search Screen |
| -------- | -------- |
| ![](https://i.imgur.com/aTeNxq7.png)     | ![](https://i.imgur.com/tWvsQeQ.png)     |

How to install it and use it
---
Because, the app is writen in Python, you can simply install from PyPi:
`pip install easydict-gtk`
and run it with:
`easydict-gtk`
The second option to install easydict-gtk is to use Flatpak:
`flatpak install -y one.jiri.easydict-gtk`
and run it with:
`flatpak run one.jiri.easydict-gtk`
Note: In Flatpak version is not supported tray icon, if you need tray, you have to use classic version from PyPi or from source code.

Dependencies:
---
Everything should be automatically installed by pip: tinydb, orjson, pycairo, PyGObject

To-Do-List
---
- [X] get the homepage https://easydict.jiri.one back online
- [ ] create tests for backend
- [ ] add the possibility to use other dictionaries
- [ ] optimize the application for touch control so that it can be run on Phosh - https://puri.sm/projects/phosh/ using libhandy - https://gitlab.gnome.org/GNOME/libhandy
- [X] ? maybe swith to poetry
- [X] create FlatPak package and publish it on FlatHub
- [ ] create ArchLinux package an publish it on AUR
- [ ] ...
