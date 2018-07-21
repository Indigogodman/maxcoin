#!/bin/bash
# create multiresolution windows icon
ICON_SRC=../../src/qt/res/icons/supermaxcoin.png
ICON_DST=../../src/qt/res/icons/supermaxcoin.ico
convert ${ICON_SRC} -resize 16x16 supermaxcoin-16.png
convert ${ICON_SRC} -resize 32x32 supermaxcoin-32.png
convert ${ICON_SRC} -resize 48x48 supermaxcoin-48.png
convert supermaxcoin-16.png supermaxcoin-32.png supermaxcoin-48.png ${ICON_DST}

