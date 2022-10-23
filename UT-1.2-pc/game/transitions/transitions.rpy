# All the images in the folder work for 1920x1080 sized games.
# Please resize them if your game size is smaller, to match the size of your own game.

# Once you have added the transitions folder to your games "game" folder
# you can use any of the transitions here!

# To use them you just need to do the same as when you use "dissolve" or "fade"
# Just type the name of the transition you want instead.
# "with dottrans2" will use the transition called "dottrans2"

# all of these are named the same as the image file by default, aside from the eye transitions.
# You can change any of the names for these transitions to make it easier for
# you to remember by changing what it says right after the "$" before the "=" sign.

init:
    $ cloudtrans = ImageDissolve("transitions/cloudtrans.png", 2.0, 16)
    $ cloudtrans2 = ImageDissolve("transitions/cloudtrans2.png", 2.0, 16)
    $ slashtrans = ImageDissolve("transitions/slashtrans.png", 1.0, 16)
    $ slashtrans2 = ImageDissolve("transitions/slashtrans2.png", 1.0, 16)
    $ stormtrans = ImageDissolve("transitions/stormtrans.png", 1.0, 10)
    $ stormtrans2 = ImageDissolve("transitions/stormtrans2.png", 1.0, 10)
    $ blindstrans = ImageDissolve("transitions/blindstrans.png", 1.0, 20)
    $ blindstrans2 = ImageDissolve("transitions/blindstrans2.png", 1.0, 20)
    $ checkertrans = ImageDissolve("transitions/checkertrans.png", 1.0, 20)
    $ checkertrans2 = ImageDissolve("transitions/checkertrans2.png", 1.0, 20)
    $ dottrans = ImageDissolve("transitions/dottrans.png", 1.5, 16)
    $ dottrans2 = ImageDissolve("transitions/dottrans2.png", 1.5, 16)
    $ swirltrans = ImageDissolve("transitions/swirltrans.png", 2.0, 20)
    $ cuttrans = ImageDissolve("transitions/cuttrans.png", 1.5, 16)
    $ cuttrans2 = ImageDissolve("transitions/cuttrans2.png", 1.5, 16)
    $ snowtrans = ImageDissolve("transitions/snowtrans.png", 2.0, 20)
    $ snowtrans2 = ImageDissolve("transitions/snowtrans2.png", 2.0, 20)
    $ noisetrans = ImageDissolve("transitions/noisetrans.png", 2.0, 20)
    $ scaletrans = ImageDissolve("transitions/scaletrans.png", 2.0, 20)
    $ brokehtrans = ImageDissolve("transitions/brokehtrans.png", 2.0, 20)
    $ paintingtrans = ImageDissolve("transitions/paintingtrans.png", 3.0, 20)
    $ treetrans = ImageDissolve("transitions/treetrans.png", 3.0, 20)
    $ crosstrans = ImageDissolve("transitions/crosstrans.png", 2.0, 20)
    $ crosstrans2 = ImageDissolve("transitions/crosstrans2.png", 2.0, 20)
    $ dimondtrans = ImageDissolve("transitions/dimondtrans.png", 2.0, 20)

    # These eye ones can be used alone, or if you use them together you can
    # create an animation of an eye flickering open. Feel free to mess around
    # with the numbers to make it work for you!

    $ openeye1 = ImageDissolve("transitions/myeyetrans.png", 2.0, 20)
    $ closeeye1 = ImageDissolve("transitions/myeyetrans2.png", 2.0, 20)
    $ openeye2 = ImageDissolve("transitions/myeyetrans.png", 1.0, 20)
    $ closeeye2 = ImageDissolve("transitions/myeyetrans2.png", 1.0, 20)
    $ openeye3 = ImageDissolve("transitions/myeyetrans.png", 4.0, 20)

# Instructions to make the eye animation.

    # Start the scene with a black background
    ## scene black
    ## with fade (or the transition you want to use)

    # You can add a timed pause if you don't want the
    # eye to start opening right away.
    ## pause 0.6

    # When you use the openeye transitions you want the
    # scene the character will see when they open their eyes.
    ## scene fallentree
    ## show ava happy
    ## with openeye1

    # Then use your black background when you use the closeeye transition.
    ## scene black
    ## with closeeye1


# Example:
# you just need to remove the hashtags(#) and
# add the names of your background images and character.

    ## scene black
    ## with fade
    ## pause 0.6
    ## scene fallentree
    ## show ava happy
    ## with openeye1
    ## scene black
    ## with closeeye1
    ## scene fallentree
    ## show ava happy
    ## with openeye2
    ## scene black
    ## with closeeye2
    ## scene fallentree
    ## show ava happy
    ## with openeye3

# Feel free to contact LimitElta on twitter or itch.io if you need help! :)
