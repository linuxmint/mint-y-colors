#!/usr/bin/python3

import webcolors, colorsys, sys, os

from gi.repository import Gio

COLORS = ["aqua", "blue", "brown", "grey", "orange", "pink", "purple", "red", "sand", "teal"]

def darken(red, green, blue, ratio):
    ratio = 1 - ratio
    return (round(red * ratio), round(green * ratio), round(blue * ratio))

def lighten(red, green, blue, ratio):
    ratio = 1 - ratio
    return [
            round(255 - (255 - red) * ratio),
            round(255 - (255 - green) * ratio),
            round(255 - (255 - blue) * ratio)
        ]
def usage():
    print ("Specify a color name and a value in HEX format.")
    print ("Example: ./make_theme.py blue 0000ff")
    sys.exit(1)


if not os.path.exists("mint-themes") or not os.path.exists("mint-y-icons"):
    print("mint-themes and mint-y-icons are missing.")
    print("Before running make_theme.py you need to get them with git")
    print("git clone https://github.com/linuxmint/mint-themes.git")
    print("git clone https://github.com/linuxmint/mint-y-icons.git")
    sys.exit(1)

if len(sys.argv) != 3:
    usage()

prog_name, color_name, color = sys.argv
color_name = color_name.lower()

if not color_name in COLORS:
    print("Unknown color: %s" % color_name)
    print("Valid color names are: %s" % ", ".join(COLORS))
    sys.exit(1)

if not color.startswith("#"):
    color = "#%s" % color

print ("--- Color 1 (BASE) ---")
rgb = webcolors.hex_to_rgb(color)
(red, green, blue) = rgb
print (rgb)
color1 = webcolors.rgb_to_hex(rgb)
print (color1)

# Color 2 (darken 10%)
print ("--- Color 2 (DARK) ---")
rgb = darken(red, green, blue, 0.1)
print (rgb)
color2 = webcolors.rgb_to_hex(rgb)
print (color2)

# Color 3 (lighten 33.3%)
print ("--- Color 3 (HOVER) ---")
rgb = lighten(red, green, blue, 0.333)
print (rgb)
color3 = webcolors.rgb_to_hex(rgb)
print (color3)

# Color 4 (darken 33.3%)
print ("--- Color 4 (PRESSED) ---")
rgb = darken(red, green, blue, 0.15)
print (rgb)
color4 = webcolors.rgb_to_hex(rgb)
print (color4)

# Color 5 (darken 5%)
print ("--- Color 5 (FOLDERS) ---")
rgb = darken(red, green, blue, 0.05)
print (rgb)
color4 = webcolors.rgb_to_hex(rgb)
print (color4)

os.system("rm *.deb")

# Generate theme
command = "sed -i '/colors1.*%s\"/c\y_hex_colors1[\"%s\"] = \"%s\"' mint-themes/constants.py" % (color_name.title(), color_name.title(), color1)
os.system(command)
command = "sed -i '/colors2.*%s\"/c\y_hex_colors2[\"%s\"] = \"%s\"' mint-themes/constants.py" % (color_name.title(), color_name.title(), color2)
os.system(command)
command = "sed -i '/colors3.*%s\"/c\y_hex_colors3[\"%s\"] = \"%s\"' mint-themes/constants.py" % (color_name.title(), color_name.title(), color3)
os.system(command)
command = "sed -i '/colors4.*%s\"/c\y_hex_colors4[\"%s\"] = \"%s\"' mint-themes/constants.py" % (color_name.title(), color_name.title(), color4)
os.system(command)
os.chdir("mint-themes")
os.system("./update-variations.py %s" % color_name.title())
os.system("dpkg-buildpackage")
os.chdir("..")

# Generate icon theme
value = color4.replace("#", "")
command = "sed -i '/%s\"/c\COLORS[\"%s\"] = \"%s\"' mint-y-icons/src/places/generate-color-variations.py" % (color_name, color_name, value)
os.system(command)
os.chdir("mint-y-icons/src/places/")
os.system("./generate-color-variations.py")
os.chdir("..")
os.system("./render_places.py %s" % color_name.title())
os.chdir("..")
os.system("dpkg-buildpackage")
os.chdir("..")

os.system("sudo dpkg -i *.deb")

settings = Gio.Settings(schema_id="org.cinnamon.desktop.interface")
settings.set_string("gtk-theme", "Mint-Y")
settings.set_string("icon-theme", "Mint-Y")
settings.set_string("gtk-theme", "Mint-Y-%s" % color_name.title())
settings.set_string("icon-theme", "Mint-Y-%s" % color_name.title())
settings = Gio.Settings(schema_id="org.cinnamon.theme")
settings.set_string("name", "Mint-Y-Dark")
settings.set_string("name", "Mint-Y-Dark-%s" % color_name.title())
