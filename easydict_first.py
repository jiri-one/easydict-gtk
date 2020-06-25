import gi

gi.require_version("Gtk", "3.0")
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2
from html_generator import CreateHtml


from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw, ImageFont

import pymongo
import re

myclient = pymongo.MongoClient("mongodb://192.168.222.20:27017/")
mydb = myclient["dicts"]
mycol = mydb["eng-cze"]
myquery =  { "eng": { "$regex": "\^*ass\$*" } }
mydoc = mycol.find(myquery)

def create_image():
    # Generate an image and draw a pattern
    font = ImageFont.truetype("/usr/share/fonts/liberation/LiberationSans-Regular.ttf", 69)
    img = Image.new("RGB", (100, 100), "white")
    img.putalpha(0)
    d = ImageDraw.Draw(img)
    d.text((0,0), "ED", font=font, fill='red')

    return img

html = CreateHtml(mydoc).html_string
           
class Handler:
    def onXButton(self, *args):
        window.hide()
        return True

    def onButtonPressed(self, button):
        print("Hello World!")
        
    def onFulltextClicked(self, button):
        return button.get_active()

def alternate():
    if window.props.visible:
        window.hide()
    else:
        window.show()

builder = Gtk.Builder()
builder.add_from_file("easydict.glade")
builder.connect_signals(Handler())
webview = WebKit2.WebView()

box_dict = builder.get_object("box_dicts") #scrolled window
box_dict.add(webview)

webview.load_html(html)

window = builder.get_object("window")
window.props.visible = False
window.set_keep_above(False)
window.show_all()

my_menu = menu(item(text="Show EasyDict", action=alternate, default = True))
icon = icon('EasyBright', create_image(), menu=my_menu)
icon.run()

Gtk.main()
