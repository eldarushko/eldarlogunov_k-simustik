import smtplib
import ssl
from email.message import EmailMessage
from email.mime.image import MIMEImage
import imghdr

def saada_email_with_results(result_email, edukad, ebaõnnestunud, pilt_path):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "eldar565z.logunov@gmail.com"
    password = input("Sisestage oma parool: ")

    msg = EmailMessage()
    msg["Subject"] = "Testi tulemused"
    msg["From"] = sender_email
    msg["To"] = result_email

    content = "Testi tulemused:\n\n"
    if edukad:
        content += "Edukalt läbitud testid:\n"
        for nimi, õiged in edukad.items():
            content += f"{nimi}: {õiged} õiged vastused\n"
        content += "\n"
    if ebaõnnestunud:
        content += "Ebaedukalt testid:\n"
        for nimi, õiged in ebaõnnestunud.items():
            content += f"{nimi}: {õiged} õiged vastused\n"
        content += "\n"

    msg.set_content(content)

    if pilt_path:
        with open(pilt_path, "rb") as fpilt:
            img_data = fpilt.read()

        image_type = imghdr.what(None, img_data)
        if image_type is None:
            print("Pildi tüüpi ei õnnestunud kindlaks määrata.")
        else:
            img_part = MIMEImage(img_data, name=pilt_path, _subtype=image_type)
            msg.add_attachment(img_part)

    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls(context=context)
        server.login(sender_email, password)
        server.send_message(msg)
        print("Tulemused edukalt saadetud!")
    except Exception as e:
        print("Viga tulemusega saatmisel:", e)
    finally:
        server.quit()

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
        for nimi, õiged in edukad.items():
            print(f"{nimi}: {õiged} õiget vastust")
    if ebaõnnestunud:
        print("\nEbaõnnestunud:")
        for nimi, õiged in ebaõnnestunud.items():
            print(f"{nimi}: {õiged} õiget vastust")

if __name__ == "__main__":
    failinimi = "küsimused_vastused.txt"
    küs_vas = loe_küsimused_vastused(failinimi)

    result_email = input("Siseta emaili aadress, et tulemused saata: ")
    küsitavate_arv = int(input("Kui palju küsimustele te tahate vastata? "))

    edukad, ebaõnnestunud = esita_küsimustik(küs_vas, küsitavate_arv)

    kirjuta_küsimused_vastused("õiged.txt", edukad)
    kirjuta_küsimused_vastused("valed.txt", ebaõnnestunud)

    kuvada_nimekirjad(edukad, ebaõnnestunud)

    pilt_path = input("Sisestage pildi tee, kui soovite saata pildi: ")
    saada_email_with_results(result_email, edukad, ebaõnnestunud, pilt_path)