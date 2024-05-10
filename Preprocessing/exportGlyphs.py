import os
from fontforge import *

# Due to "python" reasons fontforge didnt install properly so I need to run this inside of fontforge it self
# but it exists "somewhere else" so instead directly folder paths for anyone else that wanted to follow along
fontDir = "K:/Self Projects/Ai Glyph Gen/Preprocessing/Raw Fonts/"
fontFinalLocation = "K:/Self Projects/Ai Glyph Gen/Preprocessing/Font Images/"

fontNames = ['Arizonia-Regular.ttf', 'Bonbon-Regular.ttf', 'Caveat-VariableFont_wght.ttf', 'ComforterBrush-Regular.ttf', 'CoveredByYourGrace-Regular.ttf', 'DancingScript-VariableFont_wght.ttf', 'Fasthand-Regular.ttf', 'Galada-Regular.ttf', 'Itim-Regular.ttf', 'Kings-Regular.ttf', 'Lemonada-VariableFont_wght.ttf', 'LiuJianMaoCao-Regular.ttf', 'MaShanZheng-Regular.ttf', 'Mynerve-Regular.ttf', 'NanumPenScript-Regular.ttf', 'PrincessSofia-Regular.ttf', 'Ranga-Regular.ttf', 'SlacksideOne-Regular.ttf', 'FZ KATAKATA.otf', 'NotoSerifTC-Regular.otf']
#fontNames = ['TW-Kai-98_1.ttf']

for fontName in fontNames:
    font = open(fontDir + fontName)
    processed = 0
    #Drop the file type for when we print the glyph
    printName = fontName.split(".")[0]
    for glyph in font:
        processed += 1
        if font[glyph].isWorthOutputting():
            font[glyph].export(fontFinalLocation + printName + str(processed) + ".png")
