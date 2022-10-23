## This file contains options that can be changed to customize your game.
##
## Lines beginning with two '#' marks are comments, and you shouldn't uncomment
## them. Lines beginning with a single '#' mark are commented-out code, and you
## may want to uncomment them when appropriate.


## Basics ######################################################################

## A human-readable name of the game. This is used to set the default window
## title, and shows up in the interface and error reports.
##
## The _() surrounding the string marks it as eligible for translation.

define config.name = _("U.NET.US")


## Determines if the title given above is shown on the main menu screen. Set
## this to False to hide the title.

define gui.show_name = True


## The version of the game.

define config.version = "1.2"


## Text that is placed on the game's about screen. To insert a blank line
## between paragraphs, write \n\n.

define gui.about = __("""\
U.NET.US on loodud Orissaare Gümnaasiumi 12. klassi praktilise töö käigus.
Autor: Karoliine Kaljuste

ALLIKAD:
Laenatud kood:
{a=https://tinyurl.com/wmj2rtb/}Lumesadu{/a} ja {a=https://tinyurl.com/wj6xgt8}Värvikeeris{/a} - Autor foorumi Lemmasoft kasutaja xela

Pildid:
{a=https://tjkelly.com/blog/windows-xp-desktop-backgrounds/}Windows XP taustapildid{/a}
{a=https://wall.alphacoders.com/big.php?i=170031}Haikala{/a} - üleslaadija darkness
{a=https://www.transparenttextures.com/}Peamenüü taust{/a}
{a=https://tinyurl.com/tbe5x9a}'346 minutes later'{/a]}
{a=https://tinyurl.com/un65mpv}'Puud lume lähedal'{/a} - Autor Francesco Paggiaro, leheküljel Pexels
{a=https://tinyurl.com/upc2mwj}Anubise kuju{/a}
{a=https://tinyurl.com/sfyy2n8}Ateena kuju{/a}
{a=https://tinyurl.com/su7c3ge}Pükstega Taaveti kuju{/a}

Audio:
Muusikapalade 'FEAR_KARUUUUUUUUUU.mp3', 'Karu_2.mp3' ja 'Karuuuuuuuuuu.mp3' Autor Kaitlyn “firebitch” Le
{a=https://en.wikipedia.org/wiki/File:Der_Flohwalzer.wav}'Der Flohwalzer' ehk Koerapolka{/a} - üleslaadija Nunh-huh
{a=http://robbi-985.homeip.net/blog/?page_id=81}'Music using ONLY sounds from Windows XP and 98!'{/a} ({a=https://www.youtube.com/watch?v=dsU3B0W3TMs&gl=GB}YouTube{/a}) - Autor Robbi-985/Something Unreal
Heliefektid leheküljelt {a=https://freesound.org/}Freesound{/a}

""")


## A short name for the game used for executables and directories in the built
## distribution. This must be ASCII-only, and must not contain spaces, colons,
## or semicolons.

define build.name = "UT"


## Sounds and music ############################################################

## These three variables control which mixers are shown to the player by
## default. Setting one of these to False will hide the appropriate mixer.

define config.has_sound = True
define config.has_music = True
define config.has_voice = True


## To allow the user to play a test sound on the sound or voice channel,
## uncomment a line below and use it to set a sample sound to play.

# define config.sample_sound = "sample-sound.ogg"
# define config.sample_voice = "sample-voice.ogg"


## Uncomment the following line to set an audio file that will be played while
## the player is at the main menu. This file will continue playing into the
## game, until it is stopped or another file is played.

define config.main_menu_music = "Karuuuuuuuuuu.wav"

## Transitions #################################################################
##
## These variables set transitions that are used when certain events occur.
## Each variable should be set to a transition, or None to indicate that no
## transition should be used.

## Entering or exiting the game menu.

define config.enter_transition = dissolve
define config.exit_transition = dissolve


## A transition that is used after a game has been loaded.

define config.after_load_transition = dissolve


## Used when entering the main menu after the game has ended.

define config.end_game_transition = dissolve


## A variable to set the transition used when the game starts does not exist.
## Instead, use a with statement after showing the initial scene.


## Window management ###########################################################
##
## This controls when the dialogue window is displayed. If "show", it is always
## displayed. If "hide", it is only displayed when dialogue is present. If
## "auto", the window is hidden before scene statements and shown again once
## dialogue is displayed.
##
## After the game has started, this can be changed with the "window show",
## "window hide", and "window auto" statements.

define config.window = "auto"


## Transitions used to show and hide the dialogue window

define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)


## Preference defaults #########################################################

## Controls the default text speed. The default, 0, is infinite, while any other
## number is the number of characters per second to type out.

default preferences.text_cps = 0


## The default auto-forward delay. Larger numbers lead to longer waits, with 0
## to 30 being the valid range.

default preferences.afm_time = 15


## Save directory ##############################################################
##
## Controls the platform-specific place Ren'Py will place the save files for
## this game. The save files will be placed in:
##
## Windows: %APPDATA\RenPy\<config.save_directory>
##
## Macintosh: $HOME/Library/RenPy/<config.save_directory>
##
## Linux: $HOME/.renpy/<config.save_directory>
##
## This generally should not be changed, and if it is, should always be a
## literal string, not an expression.

define config.save_directory = "UT-1566125401"


## Icon ########################################################################
##
## The icon displayed on the taskbar or dock.

define config.window_icon = "gui/thought-bubble-md.png"


## Build configuration #########################################################
##
## This section controls how Ren'Py turns your project into distribution files.

init python:

    ## The following functions take file patterns. File patterns are case-
    ## insensitive, and matched against the path relative to the base directory,
    ## with and without a leading /. If multiple patterns match, the first is
    ## used.
    ##
    ## In a pattern:
    ##
    ## / is the directory separator.
    ##
    ## * matches all characters, except the directory separator.
    ##
    ## ** matches all characters, including the directory separator.
    ##
    ## For example, "*.txt" matches txt files in the base directory, "game/
    ## **.ogg" matches ogg files in the game directory or any of its
    ## subdirectories, and "**.psd" matches psd files anywhere in the project.

    ## Classify files as None to exclude them from the built distributions.

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    ## To archive files, classify them as 'archive'.

    # build.classify('game/**.png', 'archive')
    # build.classify('game/**.jpg', 'archive')

    ## Files matching documentation patterns are duplicated in a mac app build,
    ## so they appear in both the app and the zip file.

    build.documentation('*.html')
    build.documentation('*.txt')

## A Google Play license key is required to download expansion files and perform
## in-app purchases. It can be found on the "Services & APIs" page of the Google
## Play developer console.

# define build.google_play_key = "..."


## The username and project name associated with an itch.io project, separated
## by a slash.

# define build.itch_project = "renpytom/test-project"
