scacchiera=[
    0, 0, 0,
    0, 0, 0,
    0, 0, 0 # 0 = spazio vuoto, 1 = X, 2 = O
]

turno=1 #1=X, 2=O
colore_bot=0
def valuta_matto(scacchiera):

    if scacchiera[0]==scacchiera[1]==scacchiera[2]:
        return scacchiera[0]
    elif scacchiera[3]==scacchiera[4]==scacchiera[5]:
        return scacchiera[3]
    elif scacchiera[6]==scacchiera[7]==scacchiera[8]:
        return scacchiera[6]
    
    elif scacchiera[0]==scacchiera[3]==scacchiera[6]:
        return scacchiera[0]
    elif scacchiera[1]==scacchiera[4]==scacchiera[7]:
        return scacchiera[1]
    elif scacchiera[2]==scacchiera[5]==scacchiera[8]:
        return scacchiera[2]
    
    elif scacchiera[0]==scacchiera[4]==scacchiera[8]:
        return scacchiera[0]
    elif scacchiera[2]==scacchiera[4]==scacchiera[6]:
        return scacchiera[2]
    else:
        return 0

def ritocca_scacchiera(scacchiera):
    scacc_pul=''
    contatore=1
    for n in scacchiera:
        if n==0:
            scacc_pul+='. '
        elif n==1:
            scacc_pul+='X '
        else:
            scacc_pul+='O '
        if contatore%3==0:
            scacc_pul+='\n'
        contatore+=1
    return scacc_pul

def muovi(mossa, scacchiera, turno):
    if turno%2!=0:
        if scacchiera[mossa]==0:
            scacchiera[mossa]=1
        else:
            print("Mossa sbagliata!")
            return 0
    else:
        if scacchiera[mossa]==0:
            scacchiera[mossa]=2
        else:
            print("Mossa sbagliata!")
            return 0
    return scacchiera
ciao=0

def analizza(scacchiera, colore_bot):
    valutazione=0
    matto = valuta_matto(scacchiera)
    if matto == colore_bot:
        valutazione+=1000
    else:
        valutazione-=1000
    if scacchiera[4]==colore_bot:
        valutazione+=30
    elif colore_bot in [scacchiera[0], scacchiera[2], scacchiera[6], scacchiera[8]]:
        valutazione+=20
    elif colore_bot in [scacchiera[1], scacchiera[3], scacchiera[5], scacchiera[7]]:
        valutazione+=10
    for i in range(3):
        
        colonna = [scacchiera[i], scacchiera[i+3], scacchiera[i+6]]
        colore_avversario=0 

        if colore_bot==1: 
            colore_avversario=2 
        else: 
            colore_avversario=1

        if colonna.count(colore_bot) == 2 and colonna.count(0) == 1:
            valutazione += 100 
        if colonna.count(colore_avversario) == 2 and colonna.count(colore_bot) == 1: # Dovrebbe incentivare a bloccare l'avversiario
            valutazione += 120 
        
        colore_avversario = 1 if colore_bot == 2 else 2
        if colonna.count(colore_avversario) == 2 and colonna.count(0) == 1:
            valutazione -= 1000

    for i in range(0, 9, 3):

        riga = [scacchiera[i], scacchiera[i+1], scacchiera[i+2]]
        if riga.count(colore_bot) == 2 and riga.count(0) == 1:
            valutazione += 100
        if riga.count(colore_avversario) == 2 and riga.count(colore_bot) == 1: # Dovrebbe incentivare a bloccare l'avversiario
            valutazione += 120 
        if riga.count(colore_avversario) == 2 and riga.count(0) == 1:
            valutazione -= 1000
    for i in range(2):
        diagonale1=[scacchiera[0], scacchiera[4], scacchiera[8]]
        diagonale2=[scacchiera[2], scacchiera[4], scacchiera[6]]
        if diagonale1.count(colore_bot) == 2 and diagonale1.count(0) == 1:
            valutazione += 100
        if diagonale1.count(colore_avversario) == 2 and diagonale1.count(colore_bot) == 1: # Dovrebbe incentivare a bloccare l'avversiario
            valutazione += 120 
        if diagonale1.count(colore_avversario) == 2 and diagonale1.count(0) == 1:
            valutazione -= 1000

        if diagonale2.count(colore_bot) == 2 and diagonale2.count(0) == 1:
            valutazione += 100
        if diagonale2.count(colore_avversario) == 2 and diagonale2.count(colore_bot) == 1: # Dovrebbe incentivare a bloccare l'avversiario
            valutazione += 120 
        if diagonale2.count(colore_avversario) == 2 and diagonale2.count(0) == 1:
            valutazione -= 1000
    return valutazione + 1000# per qualche motivo ritornava sempre val - 1000...

def motore(scacchiera):
    mosse={}
    for j in range(9):
        if scacchiera[j] == 0:
            scacchiera_ipotetica=scacchiera.copy()
            scacchiera_ipotetica[j]=colore_bot
            
            # CORREZIONE: Assegna un valore iniziale a mosse[j] basato sulla tua prima mossa
            mosse[j] = analizza(scacchiera_ipotetica, colore_bot)
            
            for i in range(9):
                if scacchiera_ipotetica[i]==0:
                    scacchiera_futura=scacchiera_ipotetica.copy()
                    scacchiera_futura[i]= (1 if colore_bot == 2 else 2) # Avversario
                    valutazione=analizza(scacchiera_futura, colore_bot)
                    
                    # Ora questo controllo funziona perché mosse[j] ha una base numerica da confrontare!
                    if valutazione < mosse[j]: 
                        mosse[j] = valutazione 
    chiave_max = max(mosse, key=mosse.get)
    print(f"Il motore sceglie la casella: {chiave_max}")
    return chiave_max

contatore=1
nmosse=0

colore_bot_str=input("Che segno vuoi essere? (O o X, non 0!) ").lower()
if colore_bot_str=='x':
    colore_bot=2
elif colore_bot_str=='o':
    colore_bot=1



while ciao not in [1,2]:
    if nmosse < 9:
        if contatore==1:
            print("Turno delle X!, ", end='')
        else:
            print("Turno delle O!, ", end='')

        if contatore==colore_bot:
            print("il turno del motore")
            mossa=motore(scacchiera)
            nmosse+=1

            risultato=muovi(mossa,scacchiera,turno)

        else:
            print("il tuo turno!")
            mossa=input("La tua mossa: ")
            try:
                mossa=int(mossa)-1
            except ValueError:
                print("mossa non valida!")
                continue
            nmosse+=1

            risultato=muovi(mossa,scacchiera,turno)
        if risultato==0:
            break
        print(risultato)
        val=analizza(scacchiera, colore_bot)

        print(f"Valutazione: {val}")

        ciao=valuta_matto(scacchiera)
        if ciao==0:
            print("Tutto bene!")
        elif ciao==1:
            print("Matto per le X!")
        else:
            print("Matto per le O!")
        turno+=1
        scacchiera_ritoccata= ritocca_scacchiera(scacchiera)
        print(scacchiera_ritoccata)
        if contatore==1:
            contatore+=1
        else:
            contatore-=1
    else:
        print("Patta!")
        break