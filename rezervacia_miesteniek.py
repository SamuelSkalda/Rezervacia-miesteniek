import tkinter
canvas = tkinter.Canvas(width=600, height=300, bg='white')
canvas.pack()

pocetradov=10 #pocet radov resp. stlpcov
VEL=40 #velkost podla ktorej sa vykresluju policka
busx, busy= 50, 50
s=[0]*40 #zoznam kde si ukladám či je miesto obsadené alebo nie
obsadene=0 #premena na pocitanie obsadenych miest
ulicka=20 #premena na pocitanie volnych miest v ulicke
                            
def zafarbi(sedadlo,farba): #funkcia na zafarbenie policka
    canvas.itemconfig('sedadlo_'+str(sedadlo), fill=farba) #upravuje/meni farbu policka
    
def kresli(x, y, pocet): #funkcia na vykreslovanie policok
    cislo = 0 # premena na cislo v policku
    for i in range(pocet): #forcyklus pocet opakovani podla poctu stlpcov
        for j in range(4): #vnoreny forcyklus pocet opakovani podla poctu riadkov 
            cislo += 1 #pripocitavanie aby sa zvacsovalo cislo sedadla
            canvas.create_rectangle(x+i*VEL, y+j*VEL,
                                   x+(i+1)*VEL-10, y+(j+1)*VEL-10,fill='green',
                                   tags='sedadlo_'+str(cislo)) #vykreslenie policok a zafarbenie vsetkych na zeleno + otagovanie sedadiel podla cisla sedalda 
            canvas.create_text(x+i*VEL+VEL/2-5, y+j*VEL+VEL/2-5, text=cislo) #vypisanie textu v strede policka
            canvas.create_text(100, 230, text='Počet voľných: '+str(40-obsadene), tags='obs') #prve vypisanie volnych miest
            canvas.create_text(107, 250, text='Počet obsadených: '+str(obsadene), tags='obs') #prve vypisanie obsadenych miest
            canvas.create_text(130, 270, text='Počet voľných pri uličke: '+str(ulicka), tags='obs') #prve vypisanie volnych miest pri ulicke

def klik(event): #funkcia pre kliknutie lavim tlacitkom na mysi
    global obsadene, ulicka #globalne premene
    if(busx < event.x < busx + VEL * pocetradov and
       busy < event.y < busy + VEL * 4): #podmienka na urcenie miesta kde uzivatel klikol
        ix = (event.x - busx) // VEL
        iy = (event.y - busy) // VEL
        sedadlo = ix * 4 + iy + 1 #vypocitanie cisla sedadla kde uzivatel klikol
        if s[sedadlo-1] == 0: #podmienka na zistenie ci je miesto volne alebo nie
            zafarbi(sedadlo, 'red') #volanie funkcie zafarbi s parametrami cislo sedadla a farby zafarbenia
            obsadene += 1 #pripocitanie obsadeneho miesta
            s[sedadlo-1] = 1 #zmena na obsadene v zozname 1 = obsadene, 0 = volne
            cislo=0 #pomocna premena do forcyklu na prejdenie cisiel sedadiel
            for i in range(10): 
                for j in range(4): #cykly na prejdenie vsetkych riadkov a stlpcov
                    cislo += 1
                    if cislo == sedadlo and j+1 < 4 and j+1 > 1: #podmienka na zistenie ci je sedadlo pri ulicke
                        ulicka -= 1 #odcitanie z volnych miest pri ulicke
        else:
            zafarbi(sedadlo, 'green') #volanie funkcie zafarbi s parametrami cislo sedadla a farby zafarbenia
            obsadene -= 1 #odcitanie z obsadenych sedadiel takze sa uvolnilo
            s[sedadlo-1] = 0 #nastavenie v zozname na volne miesto
            cislo = 0 #pomocna premena do forcyklu na prejdenie cisiel sedadiel
            for i in range(10):
                for j in range(4): #cykly na prejdenie vsetkych riadkov a stlpcov
                    cislo += 1
                    if cislo == sedadlo and j+1 < 4 and j+1 > 1: #podmienka na zistenie ci je sedadlo pri ulicke
                        ulicka += 1 #pripocitanie k volnym miestam pri ulicke
    canvas.delete('obs') #vymazanie textu
    canvas.create_text(100, 230, text='Počet voľných: '+str(40-obsadene), tags='obs') #vypisovanie volnych miest
    canvas.create_text(107, 250, text='Počet obsadených: '+str(obsadene), tags='obs') #vypisovanie obsadenych miest
    canvas.create_text(130, 270, text='Počet voľných pri uličke: '+str(ulicka), tags='obs') #vypisovanie volnych pri ulicke

def save(): #funkcia na ulozenie rozlozenia a obsadenosti do textoveho suboru
    subor = open('rezervacia.txt', 'w') #vytvorenie suboru na zapisanie
    for i in range(4): #forcyklus riadky
        riadok = ' ' #zaciatok riadku
        cislo = i+1 #cislo riadku
        for j in range(10): #forcyklus stlpce
            if s[cislo-1] == 1: #podmienka na zistenie zo zoznamu ci je sedadlo obsadene alebo nie
                riadok=riadok+'X  ' #ak je obsadene prida sa do riadku X
            else:
                riadok=riadok+str(cislo)+' ' #ak je volne tak sa do riadku prida cislo sedadla
            cislo+=4 #do premenej sa pripocita +4 lebo zapisujem po riadkoch a tam sa cisla zvacsuju o 4
        subor.write(riadok+'\n') #zapisanie riadku do suboru a posunutie do dalsieho riadku
    subor.close() #uzatvorenie suboru
                
    

kresli(busx, busy, pocetradov) #volanie funkcie kresli
canvas.bind('<Button-1>', klik) #bindovanie laveho tlacitka na mysi s volanim funkcie ktora sa vykona pri kliknuti
button = tkinter.Button(text='save', command=save) #vytvorenie tlacitka na ulozenie do suboru
button.pack()