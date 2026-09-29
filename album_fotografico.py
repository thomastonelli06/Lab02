import csv
from operator import itemgetter
from ctypes import memset

#provaprova
def carica_da_file(file_path):

    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    try:

        # Apro il CSV in lettura e uso csv.reader per separare i campi di ogni riga.
        infile = open(file_path, "r")
        reader = csv.reader(infile)
        elenco_foto = []
        for row in reader:
            elenco_foto.append(row)
        infile.close()

        lista_anni = {}
        # Salto l intestazione e ricavo l anno di ogni foto.
        for lista in elenco_foto[1:]:
            anno = int(lista[4].strip())
            # Creo una lista quando incontro un anno nuovo
            if anno not in lista_anni:
                lista_anni[anno] = []
            lista_anni[anno].append(lista)

        return lista_anni

    except FileNotFoundError:
        return None




def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    if mese < 1 or mese > 12:
        return None
    # Cerco il codice nelle foto di tutti gli anni per evitare duplicati.
    for lista_foto in album.values():
        for foto in lista_foto:
            if foto[0] == codice:
                return None

    foto = [codice, titolo, autore, mese, anno]

    # Apro il CSV per controllare i codici già registrati
    try:
        infile = open(file_path, "r")
        reader = csv.reader(infile)
        elenco_foto = []
        for row in reader:
            elenco_foto.append(row)
            # Raccolgo i codici delle righe lette, saltando l'intestazione
            codici = []
            for lista in elenco_foto[1:]:
                if lista[0] not in codici:
                    codici.append(lista[0])
        # Scrivo la foto soltanto se il codice non è già nel file
        if codice not in codici:

            with open(file_path, "a") as outfile:
                outfile.write(f"{codice},{titolo},{autore},{mese},{anno}\n")
            # Creo l'anno nell'album se ancora non esiste
            if anno not in album:
                album[anno] = []
            # Aggiorno l'album dopo aver scritto la riga nel CSV
            album[anno].append(foto)
            return foto


    except (FileNotFoundError, ValueError):
        return None






def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    # itero le foto conservate nei vari anni
    for lista_foto in album.values():
        for foto in lista_foto:
            # Tolgo gli spazi e converto mese e anno in testo, se sono numeri
            codice_foto = foto[0].strip()
            titolo = foto[1].strip()
            autore = foto[2].strip()
            mese = str(foto[3]).strip()
            anno_foto = str(foto[4]).strip()

            if codice.strip() == codice_foto:
                return  f"{codice_foto}, {titolo}, {autore}, {mese}, {anno_foto}"


    return None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    # Controllo se l'anno esiste
    if anno not in album:
        return None
    # Ordino le foto usando il titolo
    foto_ordinate = sorted(album[anno], key=itemgetter(1))
    # prendo solo i titoli delle foto ordinate
    titoli = [foto[1] for foto in foto_ordinate]

    return titoli



def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
