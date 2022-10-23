#start UT

#LUMEVÄRK
#siin on 
# Image definitions for snow particles:
image solid_snow_small = Transform(Solid("FFF", xysize=(3, 3)), rotate=45)
image solid_snow_normal = Transform(Solid("FFF", xysize=(5, 5)), rotate=45)
image solid_snow_large = Transform(Solid("FFF", xysize=(7, 7)), rotate=45)

# Definition for Snowing UDD:
image snowing = Fixed(
    Snowing("solid_snow_large", speed=(5.0, 5.8), slow_start=(7, (0.6, 0.9))),
    Snowing("solid_snow_normal", speed=(4.8, 5.2), slow_start=(7, (0.8, 1.2))),
    Snowing("solid_snow_small", speed=(4.3, 4.7), slow_start=(5, (0.5, 0.7))))

# This bit is required for the Snowing effect:
transform particle(d, delay, startpos, endpos, speed):
    subpixel True
    pause delay
    d
    pos startpos
    linear speed pos endpos

init python:
    class Snowing(renpy.Displayable, NoRollback):
        def __init__(self, d, interval=(0.2, 0.3), start_pos=((-200, config.screen_width), 0), end_pos=({"offset": (100, 200)}, config.screen_height), speed=4.0, slow_start=False, transform=particle, **kwargs):
            """Creates a 'stream' of displayable...
            
            @params:
            -d: Anything that can shown in Ren'Py.
            -interval: Time to wait before adding a new particle. Expects a tuple with two floats.
            -start_pos: x, y starting positions. This expects a tuple of two elements containing either a tuple or an int each.
            -end_pos: x, y end positions. Same rule as above but in addition a dict can be used, in such a case:
                *empty dict will result in straight movement
                *a dict containing an "offset" key will offset the ending position by the value. Expects an int or a tuple of two ints. Default is (100, 200) and attempts to simulate a slight wind to the right (east).
            -speed: A time before particle eaches the end_pos. Expects float or a tuple of floats.
            -slow_start: If not the default False, this will expect a tuple of (time, (new_interval_min, new_interval_max)):
                *This will override the normal interval when the Displayable is first shown for the "time" seconds with the new_interval.
            -transform: ATL function to use for the particles.
                
            The idea behind the design is to enable large amounts of the same displayable guided by instructions from a specified ATL function to
            reach end_pos from start_pos in speed amount of seconds (randomized if needs be). For any rotation, "fluff" or any additional effects different ATL funcs with parallel can be used to achieve the desired effect.
            """
            super(Snowing, self).__init__(**kwargs)
            self.d = renpy.easy.displayable(d)
            self.interval = interval
            self.start_pos = start_pos
            self.end_pos = end_pos
            self.speed = speed
            self.slow_start = slow_start
            self.transform = transform
            
            self.next = 0
            self.shown = {}
        
        def render(self, width, height, st, at):
                
            rp = store.renpy
                
            if not st:
                self.next = 0
                self.shown = {}
                
            render = rp.Render(width, height)
            
            if self.next <= st:
                speed = rp.random.uniform(self.speed[0], self.speed[1])  if isinstance(self.speed, (list, tuple)) else self.speed
                    
                posx = self.start_pos[0]
                posx = rp.random.randint(posx[0], posx[1]) if isinstance(posx, (list, tuple)) else posx
                
                posy = self.start_pos[1]
                posy = rp.random.randint(posy[0], posy[1]) if isinstance(posy, (list, tuple)) else posy
                
                endposx = self.end_pos[0]
                if isinstance(endposx, dict):
                    offset = endposx.get("offset", 0)
                    endposx = posx + rp.random.randint(offset[0], offset[1]) if isinstance(offset, (list, tuple)) else offset
                else:
                    endposx = rp.random.randint(endposx[0], endposx[1]) if isinstance(endposx, (list, tuple)) else endposx
                
                endposy = self.end_pos[1]
                if isinstance(endposy, dict):
                    offset = endposy.get("offset", 0)
                    endposy = posy + randint.randint(offset[0], offset[1]) if isinstance(offset, (list, tuple)) else offset
                else:
                    endposy = rp.random.randint(endposy[0], endposy[1]) if isinstance(endposy, (list, tuple)) else endposy
                
                self.shown[st + speed] = self.transform(self.d, st, (posx, posy), (endposx, endposy), speed)
                if self.slow_start and st < self.slow_start[0]:
                    interval = self.slow_start[1]
                    self.next = st + rp.random.uniform(interval[0], interval[1])
                else:
                    self.next = st + rp.random.uniform(self.interval[0], self.interval[1])
            
            for d in self.shown.keys():
                if d < st:
                    del(self.shown[d])
                else:
                    d = self.shown[d]
                    render.blit(d.render(width, height, st, at), (d.xpos, d.ypos))
                    
            rp.redraw(self, 0)
            
            return render
            
        def visit(self):
            return [self.d]
            
#SÄDELUS
transform particle(d, delay, speed=1.0, around=(config.screen_width/2, config.screen_height/2), angle=0, radius=200):
    d
    pause delay
    subpixel True
    around around
    radius 0
    linear speed radius radius angle angle

init python:
    class ParticleBurst(renpy.Displayable):
        def __init__(self, displayable, interval=(0.02, 0.04), speed=(0.15, 0.3), around=(config.screen_width/2, config.screen_height/2), angle=(0, 360), radius=(50, 75), particles=None, mouse_sparkle_mode=False, **kwargs):
            """Creates a burst of displayable...
            
            @params:
            - displayable: Anything that can be shown in Ren'Py (expects a single displayable or a container of displayable to randomly draw from).
            - interval: Time between bursts in seconds (expects a tuple with two floats to get randoms between them).
            - speed: Speed of the particle (same rule as above).
            - angle: Area delimiter (expects a tuple with two integers to get randoms between them) with full circle burst by default. (0, 180) for example will limit the burst only upwards creating sort of a fountain.
            - radius: Distance delimiter (same rule as above).
            - around: Position of the displayable (expects a tuple with x/y integers). Burst will be focused around this position.
            - particles: Amount of particle to go through, endless by default.
            - mouse_sparkle_mode: Focuses the burst around a mouse poiner overriding "around" property.
            
            This is far better customizable than the original ParticleBurst and is much easier to expand further if an required..
            """
            super(ParticleBurst, self).__init__(**kwargs)
            self.d = [renpy.easy.displayable(d) for d in displayable] if isinstance(displayable, (set, list, tuple)) else [renpy.easy.displayable(displayable)]
            self.interval = interval
            self.speed = speed
            self.around = around
            self.angle = angle
            self.radius = radius
            self.particles = particles
            self.msm = mouse_sparkle_mode
        
        def render(self, width, height, st, at):
                
            rp = store.renpy
                
            if not st:
                self.next = 0
                self.particle = 0
                self.shown = {}
                
            render = rp.Render(width, height)
            
            if not (self.particles and self.particle >= self.particles) and self.next <= st:
                speed = rp.random.uniform(self.speed[0], self.speed[1])
                angle = rp.random.randrange(self.angle[0], self.angle[1])
                radius = rp.random.randrange(self.radius[0], self.radius[1])
                if not self.msm:
                    self.shown[st + speed] = particle(rp.random.choice(self.d), st, speed, self.around, angle, radius)
                else:
                    self.shown[st + speed] = particle(rp.random.choice(self.d), st, speed, rp.get_mouse_pos(), angle, radius)
                self.next = st + rp.random.uniform(self.interval[0], self.interval[1])
                if self.particles:
                    self.particle = self.particle + 1
            
            for d in self.shown.keys():
                if d < st:
                    del(self.shown[d])
                else:
                    d = self.shown[d]
                    render.blit(d.render(width, height, st, at), (d.xpos, d.ypos))
                    
            rp.redraw(self, 0)
            
            return render

        def visit(self):
            return self.d
            
           
# Code above can be ignored, this is what you need:
image boom = ParticleBurst([Solid("#%06x"%renpy.random.randint(0, 0xFFFFFF), xysize=(5, 5)) for i in xrange(50)], mouse_sparkle_mode=True)

# Simpler setup could be:
# image starburst = ParticleBurst("star.png")
# or even:
# image starburst = ParticleBurst("star")
# if you have an image called "star.png" in game/images/ folder or image star had been previously defined.
            
#charas
define k = Character("Karoliine")
define kes = Character("???")

#transitions
define fadehold = Fade(0.5, 1.0, 0.5)
define dissolve = Dissolve(0.2)

#images
#karu
image karu 4w1 = im.Scale("karu_4thwall1.png", 440,650)
image karu 4w2 = im.Scale("karu_4thwall2.png", 440,650)
image karu aha = im.Scale("karu_aha.png", 450,700)
image karu anger = im.Scale("karu_angery.png", 420,630)
image karu appi = im.Scale("karu_appi.png", 500,630)
image karu appi flip = im.Scale("karu_appi_flip.png", 470,630)
image karu boi1 = im.Scale("karu_boi1.png", 450,630)
image karu boi2 = im.Scale("karu_boi2.png", 450,630)
image karu doit = im.Scale("karu_doittoem.png", 460,640)
image karu doubt = im.Scale("karu_doubt.png", 470,640)
image karu doubt flip = im.Scale("karu_doubt_flip.png", 470,640)
image karu e1 = im.Scale("karu_eee1.png", 390,640)
image karu e2 = im.Scale("karu_eee2.png", 390,640)
image karu explain = im.Scale("karu_exblain.png", 390,630)
image karu fear = im.Scale("karu_fear.png", 360,630)
image karu fight1 = im.Scale("karu_fight1.png", 430,630)
image karu fight2 = im.Scale("karu_fight2.png", 480,640)
image karu load = im.Scale("karu_loading.png", 370,650)
image karu load flip = im.Scale("karu_loading_flip.png", 370,650)
image karu misasja = im.Scale("karu_misasja.png", 390,630)
image karu mmh = im.Scale("karu_mmh.png", 420,630)
image karu mmno = im.Scale("karu_mmno.png", 390,650)
image karu mv1 = im.Scale("karu_mv1.png", 350,630)
image karu mv2 = im.Scale("karu_mv2.png", 340,640)     
image karu smile = im.Scale("karu_smile.png", 370,620)
image karu think = im.Scale("karu_think.png", 450,660)
image karu wave = im.Scale("karu_wave.png", 370,650)
image karu yell = im.Scale("karu_yell.png", 390,630)

#enemy
image gl bro = im.Scale("glasses_bro.png", 380,630)
image gl bye1 = im.Scale("glasses_bye1.png", 380,630)
image gl bye2 = im.Scale("glasses_bye2.png", 380,630)
image gl eheh = im.Scale("glasses_eheh.png", 350,640)
image gl huh1 = im.Scale("glasses_huh1.png", 380,630)
image gl huh2 = im.Scale("glasses_huh2.png", 380,630)
image gl laugh1 = im.Scale("glasses_laugh1.png", 380,640)
image gl laugh2 = im.Scale("glasses_laugh2.png", 390,640)
image gl pardon = im.Scale("glasses_pardon.png", 380,630)
image gl power = im.Scale("glasses_power.png", 390,640)
image gl think = im.Scale("glasses_think.png", 390,640)

#taust
image bg uugu = im.Scale("bg_uugu.jpg", 1280,720)
image bg rnnak = im.Scale("bg_rnnak.jpg", 1280,720)
image bg rnnak bad = im.Scale("bg_rnnak_bad.jpg", 1280,720)
image black = "#000"
image bg void = im.Scale("bg_void.jpg", 1280,720)
image bg woods = im.Scale("bg_woods3.jpg", 1280,720)
image bg raamat = im.Scale("bg_rmtk.jpg", 1280,720)
image bg raamat bad1 = im.Scale("bg_rmtk_bad1.jpg", 1280,720)
image bg raamat bad2 = im.Scale("bg_rmtk_bad2.jpg", 1280,720)
image bg raamat bad3 = im.Scale("bg_rmtk_bad3.jpg", 1280,720)
image bg kool = im.Scale("bg_kool.jpg", 1280,720)
image bg kool bad1 = im.Scale("bg_kool_bad1.jpg", 1280,720)
image bg kool bad2 = im.Scale("bg_kool_bad2.jpg", 1280,720)
image bg kool bad3 = im.Scale("bg_kool_bad3.jpg", 1280,720)
image bg dust = im.Scale("bg_dust.png", 1280,720)
image bg later = im.Scale("bg_later.jpg", 1280,720)
image bg cliff = im.Scale("bg_cliff.jpg", 1280,720)
image bg heart = im.Scale("bg_heart.png", 1280,720)

#lisad
image arvuti kalad base = im.Scale("arvuti_follow.jpg", 170,130)
image arvuti kalad rotated = Transform("arvuti kalad base", rotate=9)
image arvuti roosa base = im.Scale("arvuti_power.jpg", 170,130)
image arvuti roosa rotated = Transform("arvuti roosa base", rotate=9)
image arvuti muru base = im.Scale("arvuti_bliss.jpg", 170,130)
image arvuti muru rotated = Transform("arvuti muru base", rotate=9)
image arvuti meri base = im.Scale("arvuti_azul.jpg", 170,130)
image arvuti meri rotated = Transform("arvuti meri base", rotate=9)
image arvuti hai base = im.Scale("arvuti_sark.jpg", 170,130)
image arvuti hai rotated = Transform("arvuti hai base", rotate=9)
image hai = im.Scale("im_sark.png", 300,300)
image hai bad1 = im.Scale("im_sark_bad1.png", 300,300)
image hai bad2 =im.Scale("im_sark_bad2.png", 300,300)
image star = "star.png"

image athena = im.Scale("statue_athena.png", 500,600)
image athena bad1 = im.Scale("statue_athena_bad1.png", 500,600)
image athena bad2 = im.Scale("statue_athena_bad2.png", 500,600)
image athlete = im.Scale("statue_athlete.png", 300,500)
image athlete bad1= im.Scale("statue_athlete_bad1.png", 300,500)
image athlete bad2 = im.Scale("statue_athlete_bad2.png", 300,500)
image anubis = im.Scale("statue_anubis.gif", 250,200)
image anubis bad1= im.Scale("statue_anubis_bad1.gif", 250,200)
image anubis bad2= im.Scale("statue_anubis_bad2.gif", 250,200)
    
transform lock:
        rotate 0
        linear 0.0 rotate 30
        block:
            linear 0.75 rotate -30
            linear 0.65 rotate 25
            linear 0.60 rotate -25
            linear 0.55 rotate 20
            linear 0.50 rotate -20
            linear 0.45 rotate 15
            linear 0.35 rotate -15
            linear 0.30 rotate 10
            linear 0.25 rotate -10
            linear 0.20 rotate 5
            linear 0.15 rotate -5
            linear 0.1 rotate 0 
    
init:
    $ arvutiekraan = Position(xpos=215, xanchor=0, ypos=380, yanchor=0)
    $ peeking = Position(xpos=-100, xanchor=0, ypos=150, yanchor=0)
    $ nub = Position(xpos=400, xanchor=0, ypos=220, yanchor=0)
    $ athle = Position(xpos=20, xanchor=0, ypos=200, yanchor=0)
    $ athe = Position(xpos=900, xanchor=0, ypos=140, yanchor=0)
   
init python:
    config.debug_sound = True
    
init python:
    import random
    
#START
label start:
    
    scene bg uugu
    with fade
    play music "Karu_2.wav" fadein 1
    show karu fight1
    with dissolve
    k"Tere tulemast minu mängu!"
    show karu think
    with dissolve
    k"Olen loonud selle praktilise tööna 12. klassi lõpetamiseks."
    show karu wave
    with dissolve
    k"Loodan, et see on meelt lahutav."
    show karu think
    with dissolve
    k"Vaatame kohe mis edasi tuleb!"
    show karu aha
    with dissolve
    k"Siit tuleb mängujuhend!"
    k"Kui sa tead, kuidas selliseid mänge mängida, siis pole viga, see juhend on lühike."
    show karu explain
    with dissolve
    k"1. samm: vajuta (vasakut) hiireklahvi või tühikut klaviatuuril, et liikuda edasi teksti lugemisel."
    k"2. samm: saad vahel teha valikuid nagu see-"
    
    menu:
      
          "ee":
          
              jump choice1_ee
          
          "oo":
          
              jump choice1_oo
          
              
label choice1_ee:
    show karu fight1
    with dissolve
    k"oo!"
    
    jump contin
    
label choice1_oo:
    show karu fight2
    with dissolve
    k"ee!"
    
    jump contin
    
label contin:
    show karu smile
    with dissolve
    k"-mis mõjutavad mängu käiku."
    k"Tubli! "
    k"Põhimõtteliselt see on kõik, mida on vaja selle mängu mängimiseks. Läheme edasi peaosa juurde!"
    stop music fadeout 1
    
    window hide
    scene black with fadehold
    centered "{size=+40}1. UNENÄGU{/size}"
    centered "{size=+40}KÜBERRÜNNAK{/size}"
    
    scene bg rnnak
    show arvuti kalad rotated at arvutiekraan
    with fade
    show karu 4w2
    with dissolve
    play music "windowsxp.wav" fadein 1
    window show
    k"(Võib-olla märkate, et see taust on väga hooletult kokku klopsitud.)"
    show karu 4w1
    with dissolve
    k"(See on selline, kuna see kujutab minu killustunud ja hägusaid mälestusi mu lapsepõlvest.)"
    show karu mmno
    with dissolve
    k"(KINDLASTI MITTE sellepärast, et mul ei ole ühtegi head pilti sellest toast, mis on nüüd hoopis teistsugune.)"
    k"{cps=15}(...Igatahes...){/cps}"
    show karu wave
    with dissolve
    k"Nii! Tere tulemast minu unemaastikule!"
    show karu think
    with dissolve
    k"Hetkel viibime ühes minu lapsepõlve unenäos, mis oli seotud meie koduarvuti taustapildiga."
    show arvuti roosa rotated at arvutiekraan with Dissolve(.5)
    show karu load
    with dissolve
    k"Windows XP-l on väga spetsiifilised taustapildid ja ma mäletan neid üsna hästi."
    show arvuti muru rotated at arvutiekraan with Dissolve(.5)
    show karu fear
    with dissolve
    k"Mu õudusunenägu oli aga seotud ühe hirmsa haikala taustapildiga."
    stop music fadeout 1
    show arvuti meri rotated at arvutiekraan with Dissolve(.5)
    pause 0.5
    window hide 
    show arvuti hai rotated at arvutiekraan with Dissolve(1.5)
    
    play sound "shark.wav"
    show hai at arvutiekraan with dissolve
    pause .5
    show karu appi
    with dissolve
    pause .5
    k"oiei"
    window hide
    hide karu appi with moveoutright  
    
    hide hai with moveoutright
    play sound "punch.opus"
    with hpunch
    pause 1.0
    play sound "shark.wav"
    show karu appi flip with moveinright
    hide karu appi flip with moveoutleft
    show hai with moveinright
    play sound "white_noise.wav" fadein 1
    show hai bad1
    with dissolve
    pause 0.5
    show hai bad2
    with dissolve
    pause 0.5
    show bg rnnak bad
    with dissolve
    stop sound fadeout 1
    
    scene bg void with pushright
    pause 1.0
    show karu fear at peeking
    with moveinleft
    pause .5
    window show
    k"Kas ta on läinud?"
    show karu e2 at center with move
    k"{cps=10}...{/cps}"
    show karu e1
    with dissolve
    k"{cps=5}...{/cps}"
    show karu mv2
    with dissolve
    k"Pean tunnistama, et mul pole halli aimugi mis see oli."
    show karu load
    with dissolve
    k"Kui ma seda und päriselt nägin, tuli hai arvutist välja"
    k"aga see kindlalt ei hakanud mind niimoodi taga ajama."
    show karu doit
    with dissolve
    k"Väga kahtlane..."
    
    show karu 4w1
    with dissolve
    k"Kuid! Liigume edasi."
    k"Hetkel oleme unenägudevahelises alas. Siit võib minna ükskõik kuhu!"
    show karu think
    with dissolve
    k"Millist unenägu sooviksid nüüd külastada?"
    
    menu:
        
        "Mahajäetud majas olev raamatukogu":
         jump choice2_rmt
         
        "Muhu koolimaja saal":
         jump choice2_kool
         
label choice2_rmt:
    
    k"Davai!"
    window hide
    scene black with fadehold
    centered "{size=+40}2. UNENÄGU{/size}"
    centered "{size=+40}RAAMATUKOGU{/size}"
    scene bg woods
    with fade
    show snowing
    pause 1.0
    show karu mmh
    with dissolve
    window show
    k"Oi mul on liiga vähe riideid selle unenäo jaoks."
    show karu 4w1
    with dissolve
    k"Ma nägin seda und tegelt päris ammu, vau."
    show karu 4w2
    with dissolve
    play sound "snow_steps.wav" fadein 1
    k"Nii, selles unenäos kõndisin ma läbi lumetormi."
    k"Olin enda kodu lähedal metsas."
    show karu mv1
    with dissolve
    k"Ma ei näinud mitte midagi, täielik pimedus!"
    show karu fight2
    with dissolve
    k"Siis aga tuli ette raske uks, mis kuulus mu küla mahajäetud majale ja ma sain tormi käest minema."
    play sound "door_open.wav"
    
    scene bg raamat
    with fade
    show karu boi1
    with dissolve
    k"Leidsin eest raamatukogu!"
    show karu boi2
    with dissolve
    k"Mis muidugi nägi välja nagu, noh{cps=5}...{/cps} {w}raamatukogu."
    k"Mitte lihtsalt hunnik raamatuid."
    show karu doubt
    with dissolve
    k"Hiljem sain teada, et samal pool, kus ma seda unes olin näinud,"
    show karu misasja
    with dissolve
    k"oli ka päriselt kunagi olnud raamatukogu!"
    k"Miks ma sellist prohvetlikku und nägin?"
    show karu fear
    with dissolve
    k"Kes teab?"
    show karu think
    with dissolve
    k"Muidu lõppes uni selles kohas ära-"
    window hide
    play music "koerapolka.wav" fadein 1
    pause 2.0
    show karu load
    with dissolve
    window show
    k"Mida?"
    show karu fear
    with dissolve
    k"Mis toimub??"
    stop music fadeout 1
    play sound "gasp_sound.mp3"
    show gl power at left
    with dissolve
    kes"Hei!"
    window hide
    show karu appi at right with move
    with dissolve
    pause 0.5
    show karu fear
    with dissolve
    window show
    k"Appi kes sa oled??"
    show gl eheh
    with dissolve
    kes"Seda ei pea ei sina ega mängija teadma."
    show karu anger
    with dissolve
    k"Sa ei ole osa mu unenäost, sa saad aru mis toimub."
    show gl pardon
    show karu fight2
    with dissolve
    k"Mis sa oled ja kuidas sa siia said??"
    pause 1.0
    show gl laugh1
    with dissolve
    kes"Hahahahahah."
    show karu mmno
    show gl laugh2
    with dissolve
    kes"HAHAHAHAHAHAH!"
    show karu e2
    show gl power
    with dissolve
    kes"Mina olen su minevik!"
    show gl think
    with dissolve
    kes"Ja su tulevik {cps=5}...{/cps}"
    show karu boi2
    show gl bye1
    with dissolve
    kes"Lol tšauki"
    show gl bye2
    with dissolve
    hide gl bye2
    with moveoutleft
    
    show karu mv1
    with dissolve
    k"Mida."
    window hide
    play sound "white_noise.wav" fadein 3
    show bg raamat bad1
    show karu mmh at center with move
    with dissolve
    k"Me peame siit leebet tõmbama."
    show bg raamat bad2
    show karu appi
    with dissolve
    k"KOHE!"
    hide karu appi with moveoutright
    show bg raamat bad3
    with dissolve
    stop sound fadeout 1
    jump converge
    
label choice2_kool:
    k"Lähme!"
    window hide
    scene black with fadehold
    centered "{size=+40}2. UNENÄGU{/size}"
    centered "{size=+40}KOOLIMAJA{/size}"
    scene bg kool
    with fade
    play sound "chatter.wav" fadein 1
    show karu smile
    with dissolve
    k"Oh!"
    k"See on tegelt üsna hiljutine unenägu."
    show karu 4w1
    with dissolve
    k"Ma ja mu sõbrad läksime mu eelmise kooli saali"
    k"kus näidati igasuguseid mütoloogiaga seotud kujusid."
    window hide
    show athena at athe behind karu
    with dissolve
    pause 0.5
    show athlete at athle behind karu
    with dissolve
    pause 0.5
    show anubis at nub behind karu
    with dissolve
    pause 1.0
    show karu doubt at left with move
    with dissolve
    pause 0.5
    show karu doubt flip at right with move
    with dissolve
    pause 0.5
    show karu doubt at center with move
    with dissolve
    show karu smile
    with dissolve
    k"No vot!"
    k"Milline näitus."
    stop sound fadeout 1
    show karu boi1
    with dissolve
    k"Siis saime me harjutada tantse ja laule,"
    k"mida olime tulevase aktuse jaoks õppinud."
    show karu think
    with dissolve
    k"Minu laul oli üks mida ma päriselt ka laulda oskan."
    show athena bad1 with dissolve:
        xpos 700 ypos 50
        lock
    show karu explain
    with dissolve
    k"Selle nimi on 'This is home' ja-"
    show athlete bad1 with dissolve:
        xpos -50 ypos 120
        lock
    show karu load
    with dissolve
    k"Ah?"
    k"Mis toimub?"
    show karu load flip
    with dissolve
    play sound "gasp_sound.mp3"
    show gl power at left
    with dissolve
    kes"Hei!"
    window hide
    show karu appi at right with move
    with dissolve
    pause 0.5
    show karu fear
    with dissolve
    window show
    k"Kes sa oled??"
    show gl pardon
    with dissolve
    kes"Sa tahaks teada jah."
    show karu mv1
    with dissolve
    k"{cps=10}...{/cps}"
    show karu misasja
    with dissolve
    k"Jah! Ma tahangi teada!"
    show gl laugh1
    with dissolve
    kes"Nooooo kui sa nii koledasti küsid:"
    show gl power
    with dissolve
    kes"Ma olen su päästja!"
    show gl bro
    with dissolve
    kes"Ja su hukutaja{cps=10}...{/cps}"
    show karu e1
    show gl bye1
    with dissolve
    kes"Mu töö siin on tehtud"
    show gl bye2
    with dissolve
    hide gl bye2
    with moveoutleft
    
    show karu misasja
    with dissolve
    k"Aga sa ei teinudki midagi!?!"
    play sound "white_noise.wav" fadein 1
    show bg kool bad1
    show karu mmh at center with move
    with dissolve
    
    show bg kool bad2
    show athena bad2
    show athlete bad2
    show anubis bad1
    with dissolve
    k"Okei miskit halba toimub, ma arvan et läheme minema."
    show bg kool bad3
    show anubis bad2
    show karu appi
    with dissolve
    k"NÜÜD!"
    window hide
    hide karu appi with moveoutright
    stop sound fadeout 1
    jump converge
    
label converge:    
    scene bg void with pushleft
    show karu mv2 at center
    with dissolve
    pause 1.0
    show karu mmno
    with dissolve
    window show
    k"See mis ta seal lõpus ütles oli nii üledramatiseeritud."
    show karu anger
    with dissolve
    k"Aga nüüd ma tean!"
    k"Tema on see, kes mu unenägusid moonutab!"
    window hide
    show karu think
    with dissolve
    pause 1.5
    show karu aha
    with dissolve
    window show
    k"HEI!"
    k"SINA! {w} KOLM KÜSIMÄRKI!"
    show karu yell
    with dissolve
    k"TULE VÄLJA!"
    window hide
    
    play sound "gasp_sound.mp3"
    show gl think at left
    with dissolve
    show karu appi at right with move
    with dissolve
    show karu mmno
    with dissolve
    window show
    k"Kas sa PEAD ehmatama niimoodi?"
    show gl pardon
    with dissolve
    kes"Absoluutselt."
    show karu doubt
    with dissolve
    k"Kuidas sa üldse saad minu unenägusid muuta?"
    show karu explain
    show gl laugh1
    with dissolve
    k"MINA kontrollin aju!"
    show gl bro
    with dissolve
    kes"No ütleme nii et,"
    show karu load
    show gl eheh
    with dissolve
    kes"mul on see võime."
    show gl pardon
    with dissolve
    k"Miks mitte seda kasutada?"
    show gl laugh2
    show karu mv1
    with dissolve
    k"Täielik jama."
    show karu mmno
    with dissolve
    k"Mida ma teen?"
    
    show karu doit
    with dissolve
    
    menu:
        
         "Räägi läbi.":
          jump choice3_labi
        
         "Eemalda ta.":
          jump choice3_eemalda
        
label choice3_labi:
    show karu boi1
    with dissolve
    k"Okei."
    k"Sa oled osa minust onju?"
    show gl think
    with dissolve
    kes"Enda arust küll{cps=10}...{/cps}"
    show karu aha
    with dissolve
    k"Ärme kakle!"
    k"Teeme pigem koostööd."
    window hide
    show karu boi1
    show gl huh1
    with dissolve
    pause 1.0
    show gl huh2
    with dissolve
    pause 1.0
    show gl power
    with dissolve
    kes"Okidoki!"
    show karu smile
    show gl power
    with dissolve
    k"Jee!"
    window hide
    play music "Karuuuuuuuuuu.wav" fadein 1
   
    scene bg void
    with fade
    show karu smile:
        xalign 0.75
        yalign 1.0
    show gl power:
        xalign 0.25
        yalign 1.0
    with dissolve
    show boom
    k"Voh! Natuke sädelust ja kõik saab korda."
    kes"Tundub nii."
    show karu e1
    with dissolve
    k"Ma eeldan siis, et sa oled seotud mu loovusega?"
    k"Kuna sinu mõjutusel muutusid mu unenäod."
    show gl eheh
    with dissolve
    kes"Jep! Võid kutsuda mind Kujutlusvõimeks!"
    show karu smile
    with dissolve
    k"Teeme nii."
    show gl power
    with dissolve
    "Kujutlusvõime" "Tore, et saime koos midagi luua."
    show gl laugh1
    with dissolve
    "Kujutlusvõime" "Meil on üksteist vaja, et olla täielik inimene!"
    show karu wave
    with dissolve
    k"No siis on väga tore, et me ära leppisime."
    pause 1.0
   
    window hide
    scene black with fadehold
    centered "{size=+40}HEA LÕPP:{/size}"
    centered "{size=+40}MEELERAHU{/size}"
    centered "{size=+30}Mängi uuesti?{/size}"
    
    menu:
        "JAH":
            jump start
        "EI":
            jump end
    
label choice3_eemalda:
    show karu anger
    with dissolve
    k"Jah, just, need on minu mõtted!"
    show gl huh1
    with dissolve
    k"Sul pole õigust nendega mässata!"
    window hide
    show karu fight2
    show gl huh2
    with dissolve
    pause 0.5
    show karu fight2 at left
    play audio "punch.opus"
    hide karu fight2
    hide gl bye2
    with moveoutleft
    play audio "punch.opus"
    pause 0.5
    show karu doubt flip with moveinleft
    show karu boi2 at center
    with dissolve
    window show
    k"Oeh."
    play music "FEAR_KARUUUUUUUUUU.wav" fadein 1
    show karu fight1
    with dissolve
    k"Nii, nüüd on rahu majas."
    
    window hide
    scene black with fadehold
    pause 0.5
    scene bg later with fadehold
    pause 0.5
    scene bg dust
    with fade
    show karu fight1
    with dissolve
    window show
    k"Oeh."
    k"Ma ei jaksa enam midagi luua."
    k"Mul pole tahtmist ühtegi loomingulist asja enam teha."
    k"See lõpp on ka nii tühi ja igav."
    k"Tundub nagu mingi osa minust oleks puudu{cps=10}...{/cps}"
    k"Loodan et nautisid seda ekskursiooni mu unenägudesse,"
    k"vaatamata sellele, et selle küsimärgiga pidime kokku puutuma."
    pause 1.0
    k"Ma ei usu et ma rohkem midagi sellist teen."
    window hide
    scene black with fadehold
    centered "{size=+40}HALB LÕPP:{/size}"
    centered "{size=+40}INSPIRATSIOONIKAOTUS{/size}"
    centered "{size=+30}Mängi uuesti?{/size}"
    
    menu:
        "JAH":
            jump start
        "EI":
            jump end
label end:
    stop music fadeout 1
    scene black with fadehold
    pause 0.5
    scene bg cliff
    with fade
    play music "Karu_2.wav" fadein 1
    show karu wave
    with dissolve
    k"Hei!"
    k"Aitäh, et mängisid minu mängu!"
    k"See on mu esimene suurem projekt."
    show karu smile
    with dissolve
    k"Loodan et nautisid selle mängimist!"
    show karu wave
    with dissolve
    k"Ilusat päeva/õhtut!"
    
    scene bg heart
    with fade
    stop music fadeout 1
    pause 3.0
    
return
