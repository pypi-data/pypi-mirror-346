#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

# #############################################################################
# RESET
# #############################################################################

# [0m  reset; clears all colors and styles (to white on black)
export RESET='\x1b[0m'
export NOCOLOR=$RESET
export DEFAULT=$RESET
export DEFAULT_COLOR=$RESET

# #############################################################################
# FOREGROUND
# #############################################################################

# [30m set foreground color to black
# black='\e[0;30m'
# grey='\e[1;30m'
# ='\e[2;30m'
# ='\e[3;30m'
# ='\e[4;30m'
export BLACK='\x1b[0;30m'
export GREY='\x1b[1;30m'
export BLACK2='\x1b[2;30m'
export BLACK3='\x1b[3;30m'
export BLACK4='\x1b[4;30m'
export FAINT='\x1b[2m'

# [37m set foreground color to white
# gray light='\e[0;37m'
# blanc='\e[1;37m'
export GREY_LIGHT='\x1b[0;37m'
export WHITE='\x1b[1;37m'

# [32m set foreground color to green
# green dark='\e[0;32m'
# green light='\e[1;32m'
export GREEN='\x1b[32m'

# [31m set foreground color to red
# rougefonce='\e[0;31m'
# rose='\e[1;31m'
export RED='\x1b[31m'
export PINK='\x2b[31m'

# [33m set foreground color to yellow
# orange='\e[0;33m'
# yellow='\e[1;33m'
export YELLOW='\x1b[33m'
# export ORANGE='\x2b[33m'

# [34m set foreground color to blue
# blue dark='\e[0;34m'
# blue light='\e[1;34m'
export BLUE='\x1b[34m'

# [35m set foreground color to magenta (purple)
# magenta darke='\e[0;35m'
# magenta light='\e[1;35m'

# [36m set foreground color to cyan
# cyan dark='\e[0;36m'
# cyan light='\e[1;36m'

# [38m set foreground color to ???

# [39m set foreground color to default (white)

# #############################################################################
# BACKGROUND
# #############################################################################

# [40m set background color to black
export WHITE_BCK='\x1b[7m'
# export WHITE_BCK='\x1b[47m\x1b[40m'

# [41m set background color to red
export RED_BCK='\x1b[41m'

# [42m set background color to green
export GREEN_BCK='\x1b[42m'

# [43m set background color to yellow
export YELLOW_BCK='\x1b[43m'$GREY

# [44m set background color to blue
export BLUE_BCK='\x1b[44m'

# [45m set background color to magenta (purple)

# [46m set background color to cyan

# [47m set background color to white

# [48m set background color to ???

# [49m set background color to default (black)

# #############################################################################
# ALT
# #############################################################################

# [1m  bold on
# [22m bold off
export BOLD='\x1b[1m'
export NOBOLD='\x1b[22m'
# [3m  italics on
# [23m italics off
# [4m  underline on
# [24m underline off
# [7m  inverse on; reverses foreground & background colors
# [27m inverse off
# [9m  strikethrough on
# [29m strikethrough off

# #############################################################################
# MOVEMENT
# #############################################################################

export CURSOR_UP='\e[1A'

# #############################################################################
# LOG
# #############################################################################

export OK=$GREEN
export WARN=$YELLOW
export ERR=$RED

# #############################################################################
# LOG PREAMPLE
# #############################################################################

export MESSAGE_OK=$OK'[OK]'$RESET
export MESSAGE_WARN=$WARN'[WARN]'$RESET
export MESSAGE_ERR=$ERR'[ERROR]'$RESET
