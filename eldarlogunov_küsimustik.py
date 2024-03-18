def loe_küsimused_vastused(failinimi):
    küs_vas = {}
    with open(failinimi, "r", encoding="utf-8") as fail:
        for line in fail:
            n = line.find(":")
            küs_vas[line[:n].strip()] = line[n + 1:].strip()
    return küs_vas

def kirjuta_küsimused_vastused(failinimi, küs_vas):
    with open(failinimi, "w", encoding="utf-8") as fail:
        for küs, vas in küs_vas.items():
            fail.write(f"{küs}:{vas}\n")

def esita_küsimustik(küs_vas, küsitavate_arv):
    õiged_vastused = 0
    küsimustik_edukad = {}
    küsimustik_ebaõnnestunud = {}

    for i in range(küsitavate_arv):
        küs = list(küs_vas.keys())[i]
        oodatud_vastus = küs_vas[küs]

        vastus = input(f"{küs}\nSinu vastus: ").strip()

        if vastus.lower() == oodatud_vastus.lower():
            print("Õige!\n")
            õiged_vastused += 1
        else:
            print(f"Vale! Õige vastus on: {oodatud_vastus}\n")

        if i == küsitavate_arv - 1:
            print("Viktoriin lõppenud!")

    if õiged_vastused > küsitavate_arv // 2:
        küsimustik_edukad["Edukalt läbitud"] = õiged_vastused
    else:
        küsimustik_ebaõnnestunud["Edukalt läbitud"] = õiged_vastused

    return küsimustik_edukad, küsimustik_ebaõnnestunud

def kuvada_nimekirjad(edukad, ebaõnnestunud):
    if edukad:
        print("\nEdukalt läbitud:")
        for nimi, õiged in sorted(edukad.items()):
            print(f"{nimi}: {õiged} õiget vastust")
    if ebaõnnestunud:
        print("\nEbaõnnestunud:")
        for nimi, õiged in sorted(ebaõnnestunud.items()):
            print(f"{nimi}: {õiged} õiget vastust")

if __name__ == "__main__":
    failinimi = "küsimused_vastused.txt"
    küs_vas = loe_küsimused_vastused(failinimi)

    küsitavate_arv = int(input("Mitu küsimust soovid esitada? "))

    edukad, ebaõnnestunud = esita_küsimustik(küs_vas, küsitavate_arv)

    kirjuta_küsimused_vastused("õiged.txt", edukad)
    kirjuta_küsimused_vastused("valed.txt", ebaõnnestunud)

    kuvada_nimekirjad(edukad, ebaõnnestunud)
    
