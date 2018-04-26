#!/usr/bin/env python

import os
from os.path import expanduser
import random
import subprocess
import re
import sys
import fileinput

'''                                                                          
Create the dir ~/.config/termite/themes and place some random configs into it
Run this script via: python termite.py                          
Enjoy!                                                                       
'''                                                                          

splash = """\

       ▄▄▄▄▄▄     ▄ .▄    ▄▄▄ .    • ▄   ▄▄ ·.   ▀    ▄▄▄▄▄▄    ▄▄▄ .
        •██ ·    ██ ▐█    █ .▀·    ·██▄▐███ ▪   ██     •██      ▀▄.▀·
      ·  ▐█.▪·   ██▄ █  · █▀▀      ▐█ █▐▌▐█·    ▐█·   █ ▐█      █▀▀ ▄
       · ▐█▌·    █  ▐█    █ ▄▄▌ ·  ██ ██▌▐█▌ ·  ▐█▌     ▐█▌·    ▐█▄▄▌  ·
         ▀▀▀     ▀   █    █▀▀▀     ▀▀  █ ▀▀▀    ▀▀▀  ·  ▀▀▀  ·  ·  ·  

             1.              2.                3.                4. 
        _______________________________________________________________ 
       |                                                               |
      |   RANDOM   |   LIST THEMES   |   CHOOSE THEME   |  CHANGE FONT  |
       |_______________________________________________________________|

"""
#constants

#home directory
home = expanduser("~")  

#config directory
config = home + '/.config/termite/config' 

#get the current theme for printing

#random theme selected
theme = random.choice(os.listdir(home + '/.config/themite/themes/termite/'))

#Function for theme swapping
def theme_swap(t):
    f = open(config, 'r+')
    content = f.read()

    #grab the index range of the relevant part (the colors)
    start = content.index('[colors]')
    config_colors = content[start:]

    #opens the theme they selected
    t = open(t, 'r+')
    currentTheme = t.name[(t.name.index("config.") + 7):]
    tcontent = t.read()
    tstart = tcontent.index('[colors]')
    theme_colors = tcontent[tstart:]

    #with block to open and close the existing config file
    with open(config, 'r+') as swap:
        #remove the existing color options
        swap_content = swap.read()
        swap.seek(0)
        swap.truncate()
        #write the new theme colors onto the file
        swap.write(content.replace(config_colors, theme_colors) + "\n#" + currentTheme)

    return currentTheme

def main():
    subprocess.check_call(['clear'])
    current = open(config, "r")
    lineList = current.readlines()
    current.close()
    currentTheme = lineList[len(lineList) - 1]
    currentTheme = currentTheme[1:]    
    themite = input(splash + "\nCurrent theme: " + currentTheme + "\n" )
    themite = input(splash)

    #Random
    if themite == "1":
        #get the theme dir, append the randomly selected theme and create path
        theme_dir = home + '/.config/themite/themes/termite/'
        #clear the screen, and call the color.sh script
        theme_swap(theme_dir + theme)
        subprocess.check_call(['clear'])
        subprocess.call('~/.config/themite/color.sh', shell=True)
        print("Current theme: " + theme_swap(theme_dir + theme))


    #List
    elif themite == "2":
        List = os.listdir(home + '/.config/themite/themes/termite/')
        print("\n")

        for filename in List:
            m = re.search('(?<=config.)\w+', filename)
            if m:
                print(m.group(0))
        temp = input("\nPress ENTER to continue")
        main()

    #Choose theme
    elif themite == "3":
        List = os.listdir(home + '/.config/themite/themes/termite/')
        
        for filename in List:
            m = re.search('(?<=config.)\w+', filename)
            if m:
                print(m.group(0))


        #take user input and give it as an argument for the theme swap method
        theme_dir = home + '/.config/themite/themes/termite/'
        theme_swap(theme_dir + "config." + input("Theme: "))
        #reset the terminal so changes occur immediately, and run color script
        theme_dir = home + '/.config/themite/themes/termite/config.'
        theme_swap(theme_dir + input("Theme: "))
        subprocess.check_call(['clear'])
        subprocess.call('~/.config/themite/color.sh', shell=True)
    
    elif themite == "4":
        #feel like this part can be improved somewhat - maybe provide a list of the system installed fonts?
        font = 'font = '
        new_font = "font = " + input('Font <Name> <Size>:')
        x = fileinput.input(files=config, inplace=1)
        for line in x:
            if font in line:
                line = new_font
            print(line.strip())
        x.close()
    #Display current theme

main()

#exit from termite, and reopen
subprocess.check_call(['killall', '-USR1', 'termite'])
