import random

class Domanda:
    # Si tratta di un costruttore (OOP)
    def __init__(self, testo, difficolta, risposta_corretta, risposte_errate):
        self.testo = testo
        self.difficolta = difficolta
        self.risposta_corretta = risposta_corretta
        self.risposte_errate = risposte_errate

    # Un metodo che definisce come la domanda viene stampata/posta
    def __str__(self):
        return f"{self.testo} (Difficoltà: {self.difficolta})\nRisposta corretta: {self.risposta_corretta}\nRisposte errate: {', '.join(self.risposte_errate)}"

def carica_domande(file_path): # apro il file in modalità lettura
    domande = []
    with open(file_path, 'r') as file:
        lines = file.readlines() # leggo tutte le righe e le memorizzo in una lista
    i = 0
    while i < len(lines):
        if lines[i].strip()=="":
            i += 1
            continue
        testo = lines[i].strip()
        difficolta = int(lines[i+1].strip())
        risposta_corretta = lines[i + 2].strip()
        risposte_errate = [lines[i + 3].strip(),
                           lines[i + 4].strip(),
                           lines[i + 5].strip()]
        domande.append(Domanda(testo, difficolta, risposta_corretta, risposte_errate))
        i +=7

    return domande

def gioca_trivia(domande):
    livello_corrente = 0
    punteggio = 0
    while True:
        domande_livello = [d for d in domande if d.difficolta == livello_corrente]
        if not domande_livello:
            break

        domanda = random.choice(domande_livello)
        risposte = [domanda.risposta_corretta] + domanda.risposte_errate
        random.shuffle(risposte)

        print(f"Livello {livello_corrente}) {domanda.testo}")
        for i, risposta in enumerate(risposte):
            print(f"\t{i + 1}. {risposta}")

        risposta_utente = int(input("Inserisci la risposta: ")) - 1
        if risposte[risposta_utente] == domanda.risposta_corretta:
            print("Risposta corretta!")
            punteggio += 1
            livello_corrente += 1
        else:
            print(f"Risposta sbagliata! La risposta corretta era: {domanda.risposta_corretta}")
            break

    print(f"Hai totalizzato {punteggio} punti!")
    nickname = input("Inserisci il tuo nickname: ")
    return nickname, punteggio

def salva_punteggi(file_path, nickname, punteggio):
    punteggi = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        #divido la linea in due parti (nick e punti) e li aggiungo come tupla
        # alla lista punteggi
        for line in lines:
            parts = line.split()
            if len(parts) ==2:
                nome, punti = parts
                punteggi.append((nome, int(punti)))

    # Allego il nuovo punteggio
    punteggi.append((nickname, punteggio))
    # Ordino i punteggi in ordine decrescente
    punteggi.sort(key=lambda x: x[1], reverse=True)

    # Scrivo i punteggi nella lista
    with open(file_path, 'w') as file: # Apro il file in modalità scrittura
        for nome, punti in punteggi:
            file.write(f"{nome} {punti}\n")

def main():
    domande = carica_domande('domande.txt')
    nickname, punteggio = gioca_trivia(domande)
    salva_punteggi('punti.txt', nickname, punteggio)
    verifica_punteggi('punti.txt')

def verifica_punteggi(file_path):
    print("Contenuto del file punti.txt:")
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                print(line.strip())
    except FileNotFoundError:
        print("Il file punti.txt non esiste.")

if __name__ == "__main__":
    main()


