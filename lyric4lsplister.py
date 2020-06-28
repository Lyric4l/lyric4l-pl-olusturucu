import argparse
import configparser
import csv
import functools
import gzip
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

__author__ = "lyric4l"
__license__ = "GPL"
__version__ = "v1 beta"

CONFIG = {}


def read_config(filename):

    if os.path.isfile(filename):


        config = configparser.ConfigParser()
        config.read(filename)

        CONFIG["global"] = {
            "years": config.get("years", "years").split(","),
            "chars": config.get("specialchars", "chars").split(","),
            "numfrom": config.getint("nums", "from"),
            "numto": config.getint("nums", "to"),
            "wcfrom": config.getint("nums", "wcfrom"),
            "wcto": config.getint("nums", "wcto"),
            "threshold": config.getint("nums", "threshold"),
            "alectourl": config.get("alecto", "alectourl"),
            "dicturl": config.get("downloader", "dicturl"),
        }

        leet = functools.partial(config.get, "leet")
        leetc = {}
        letters = {"a", "i", "e", "t", "o", "s", "g", "z"}

        for letter in letters:
            leetc[letter] = config.get("leet", letter)

        CONFIG["LEET"] = leetc

        return True

    else:
        print(filename + " adında config dosyası yok")
        sys.exit("siktirip gidiliyor")

        return False


def make_leet(x):
    for letter, leetletter in CONFIG["LEET"].items():
        x = x.replace(letter, leetletter)
    return x


def concats(seq, start, stop):
    for mystr in seq:
        for num in range(start, stop):
            yield mystr + str(num)


def komb(seq, start, special=""):
    for mystr in seq:
        for mystr1 in start:
            yield mystr + special + mystr1




def print_to_file(filename, unique_list_finished):
    f = open(filename, "w")
    unique_list_finished.sort()
    f.write(os.linesep.join(unique_list_finished))
    f.close()
    f = open(filename, "r")
    lines = 0
    for line in f:
        lines += 1
    f.close()
    print(
        "[+] sözcükler kaydediliyo: \033[1;31m"
        + filename
        + "\033[1;m,  \033[1;31m"
        + str(lines)
        + " words.\033[1;m"
    )
    print(
        "[+] gerekli ayarlamaları yapıyorum \033[1;31m"
        + filename
        + "\033[1;m deniyorum"
    )


def print_cow():
    print(" ___________ ")
    print("      \                     # kullanıcı")
    print("       \   \033[1;31m,__,\033[1;m             # sifre")
    print("        \  \033[1;31m(\033[1;moo\033[1;31m)____\033[1;m         # profilize edici")
    print("           \033[1;31m(__)    )\ \033[1;m  ")
    print(
        "           \033[1;31m   ||--|| \033[1;m\033[05m*\033[25m\033[1;m      [ lyric4l | lyric4l.me ]"
    )




def improve_dictionary(file_to_open):

    kombinacija = {}
    komb_unique = {}

    if not os.path.isfile(file_to_open):
        exit("hata: " + file_to_open + " dosyası yok")

    chars = CONFIG["global"]["chars"]
    years = CONFIG["global"]["years"]
    numfrom = CONFIG["global"]["numfrom"]
    numto = CONFIG["global"]["numto"]

    fajl = open(file_to_open, "r")
    listic = fajl.readlines()
    listica = []
    for x in listic:
        listica += x.split()

    print("\r\n      *************************************************")
    print("      *                    \033[1;31muyarı\033[1;m                 *")
    print("      *         cok buyuk bir worldist hazirliyon haci         *")
    print("      *       valla adami ayakta hoplatirlar benden demesi      *")
    print("      *************************************************\r\n")

    conts = input(
        "> bütün kelimeleri birlesik yaziyim mi? Y/[N]: "
    ).lower()

    if conts == "y" and len(listic) > CONFIG["global"]["threshold"]:
        print(
            "\r\n[-] birlestirilcek maksimum kelime sayisi: "
            + str(CONFIG["global"]["threshold"])
        )
        print("[-] arttircaksan sayiyi config dosyasina elles\r\n")
        conts = input(
            "> tüm kelimeleri birlestiriyim mi Y/[N]: "
        ).lower()

    cont = [""]
    if conts == "y":
        for cont1 in listica:
            for cont2 in listica:
                if listica.index(cont1) != listica.index(cont2):
                    cont.append(cont1 + cont2)

    spechars = [""]
    spechars1 = input(
        "> sifrelerin sonuna abuk subuk karakterler ekliyim mi Y/[N]: "
    ).lower()
    if spechars1 == "y":
        for spec1 in chars:
            spechars.append(spec1)
            for spec2 in chars:
                spechars.append(spec1 + spec2)
                for spec3 in chars:
                    spechars.append(spec1 + spec2 + spec3)

    randnum = input(
        "> sifrelerin sonuna abuk subuk rakamlar ekliyim mi Y/[N]:"
    ).lower()
    leetmode = input("> leet mod istiyon mu? (i.e. leet = 1337) Y/[N]: ").lower()

    # init
    for i in range(6):
        kombinacija[i] = [""]

    kombinacija[0] = list(komb(listica, years))
    if conts == "y":
        kombinacija[1] = list(komb(cont, years))
    if spechars1 == "y":
        kombinacija[2] = list(komb(listica, spechars))
        if conts == "y":
            kombinacija[3] = list(komb(cont, spechars))
    if randnum == "y":
        kombinacija[4] = list(concats(listica, numfrom, numto))
        if conts == "y":
            kombinacija[5] = list(concats(cont, numfrom, numto))

    print("\r\n[+] bi liste cikartiyom az bekle...")

    print("[+] listeyi duzenliyorum...")

    for i in range(6):
        komb_unique[i] = list(dict.fromkeys(kombinacija[i]).keys())

    komb_unique[6] = list(dict.fromkeys(listica).keys())
    komb_unique[7] = list(dict.fromkeys(cont).keys())


    uniqlist = []
    for i in range(8):
        uniqlist += komb_unique[i]

    unique_lista = list(dict.fromkeys(uniqlist).keys())
    unique_leet = []
    if leetmode == "y":
        for (
            x
        ) in (
            unique_lista
        ):  
            x = make_leet(x) 
            unique_leet.append(x)

    unique_list = unique_lista + unique_leet

    unique_list_finished = []

    unique_list_finished = [
        x
        for x in unique_list
        if len(x) > CONFIG["global"]["wcfrom"] and len(x) < CONFIG["global"]["wcto"]
    ]

    print_to_file(file_to_open + ".lyric4lsplister.txt", unique_list_finished)

    fajl.close()


def interactive():

    print("\r\n[+] heklenecek adamla ilgili az bilgi verele")
    print("[+] eger bi sikim bilmiyosan entera bas atla\r\n")



    profile = {}

    name = input("> First Name: ").lower()
    while len(name) == 0 or name == " " or name == "  " or name == "   ":
        print("\r\n[-] bi isim gir be birader")
        name = input("> isim: ").lower()
    profile["name"] = str(name)

    profile["surname"] = input("> soyisim: ").lower()
    profile["nick"] = input("> nicki: ").lower()
    birthdate = input("> dogum gunu (DDMMYYYY): ")
    while len(birthdate) != 0 and len(birthdate) != 8:
        print("\r\n[-] dogum gununu belirttigim formatta gir mal misin aq")
        birthdate = input("> dogum gunu (DDMMYYYY): ")
    profile["birthdate"] = str(birthdate)

    print("\r\n")

    profile["wife"] = input("> sevgilisinin adi : ").lower()
    profile["wifen"] = input("> sevgilisinin nicki: ").lower()
    wifeb = input("> sevgilisinin dogum tarihi (DDMMYYYY): ")
    while len(wifeb) != 0 and len(wifeb) != 8:
        print("\r\n[-] belirttigim formatta gir bak sikicem dalagini")
        wifeb = input("> sevgilisinin dogum tarihi (DDMMYYYY): ")
    profile["wifeb"] = str(wifeb)
    print("\r\n")

    profile["kid"] = input("> cocugunun ismi: ").lower()
    profile["kidn"] = input("> cocugunun nicki: ").lower()
    kidb = input("> cocugunun dogum tarihi (DDMMYYYY): ")
    while len(kidb) != 0 and len(kidb) != 8:
        print("\r\n[-] lan olm sunu duzgun gir")
        kidb = input("> cocugunun dogum gunu (DDMMYYYY): ")
    profile["kidb"] = str(kidb)
    print("\r\n")

    profile["pet"] = input("> hayvaninin ismi: ").lower()
    profile["company"] = input("> sehrinin ismi: ").lower()
    print("\r\n")

    profile["words"] = [""]
    words1 = input(
        "> baska bi kelime eklemek istiyon mu Y/[N]: "
    ).lower()
    words2 = ""
    if words1 == "y":
        words2 = input(
            "> bak simdi birden fazla girceksen deneme,deneme1,deneme2 diye gircen tmm mi hadi bakim "
        ).replace(" ", "")
    profile["words"] = words2.split(",")

    profile["spechars1"] = input(
        "> kelimelerin sonuna sikimsonik harfler falan ekliyim mi Y/[N]: "
    ).lower()

    profile["randnum"] = input(
        "> kelimelerin sonuna falan rakamlar ekliyim mi Y/[N]:"
    ).lower()
    profile["leetmode"] = input("> leet mod acilsin mi (i.e. leet = 1337) Y/[N]: ").lower()

    generate_wordlist_from_profile(profile) 


def generate_wordlist_from_profile(profile):
    """ Generates a wordlist from a given profile """

    chars = CONFIG["global"]["chars"]
    years = CONFIG["global"]["years"]
    numfrom = CONFIG["global"]["numfrom"]
    numto = CONFIG["global"]["numto"]

    profile["spechars"] = []

    if profile["spechars1"] == "y":
        for spec1 in chars:
            profile["spechars"].append(spec1)
            for spec2 in chars:
                profile["spechars"].append(spec1 + spec2)
                for spec3 in chars:
                    profile["spechars"].append(spec1 + spec2 + spec3)

    print("\r\n[+] hazirliyorum...")



    birthdate_yy = profile["birthdate"][-2:]
    birthdate_yyy = profile["birthdate"][-3:]
    birthdate_yyyy = profile["birthdate"][-4:]
    birthdate_xd = profile["birthdate"][1:2]
    birthdate_xm = profile["birthdate"][3:4]
    birthdate_dd = profile["birthdate"][:2]
    birthdate_mm = profile["birthdate"][2:4]

    wifeb_yy = profile["wifeb"][-2:]
    wifeb_yyy = profile["wifeb"][-3:]
    wifeb_yyyy = profile["wifeb"][-4:]
    wifeb_xd = profile["wifeb"][1:2]
    wifeb_xm = profile["wifeb"][3:4]
    wifeb_dd = profile["wifeb"][:2]
    wifeb_mm = profile["wifeb"][2:4]

    kidb_yy = profile["kidb"][-2:]
    kidb_yyy = profile["kidb"][-3:]
    kidb_yyyy = profile["kidb"][-4:]
    kidb_xd = profile["kidb"][1:2]
    kidb_xm = profile["kidb"][3:4]
    kidb_dd = profile["kidb"][:2]
    kidb_mm = profile["kidb"][2:4]


    nameup = profile["name"].title()
    surnameup = profile["surname"].title()
    nickup = profile["nick"].title()
    wifeup = profile["wife"].title()
    wifenup = profile["wifen"].title()
    kidup = profile["kid"].title()
    kidnup = profile["kidn"].title()
    petup = profile["pet"].title()
    companyup = profile["company"].title()

    wordsup = []
    wordsup = list(map(str.title, profile["words"]))

    word = profile["words"] + wordsup


    rev_name = profile["name"][::-1]
    rev_nameup = nameup[::-1]
    rev_nick = profile["nick"][::-1]
    rev_nickup = nickup[::-1]
    rev_wife = profile["wife"][::-1]
    rev_wifeup = wifeup[::-1]
    rev_kid = profile["kid"][::-1]
    rev_kidup = kidup[::-1]

    reverse = [
        rev_name,
        rev_nameup,
        rev_nick,
        rev_nickup,
        rev_wife,
        rev_wifeup,
        rev_kid,
        rev_kidup,
    ]
    rev_n = [rev_name, rev_nameup, rev_nick, rev_nickup]
    rev_w = [rev_wife, rev_wifeup]
    rev_k = [rev_kid, rev_kidup]


    bds = [
        birthdate_yy,
        birthdate_yyy,
        birthdate_yyyy,
        birthdate_xd,
        birthdate_xm,
        birthdate_dd,
        birthdate_mm,
    ]

    bdss = []

    for bds1 in bds:
        bdss.append(bds1)
        for bds2 in bds:
            if bds.index(bds1) != bds.index(bds2):
                bdss.append(bds1 + bds2)
                for bds3 in bds:
                    if (
                        bds.index(bds1) != bds.index(bds2)
                        and bds.index(bds2) != bds.index(bds3)
                        and bds.index(bds1) != bds.index(bds3)
                    ):
                        bdss.append(bds1 + bds2 + bds3)

    wbds = [wifeb_yy, wifeb_yyy, wifeb_yyyy, wifeb_xd, wifeb_xm, wifeb_dd, wifeb_mm]

    wbdss = []

    for wbds1 in wbds:
        wbdss.append(wbds1)
        for wbds2 in wbds:
            if wbds.index(wbds1) != wbds.index(wbds2):
                wbdss.append(wbds1 + wbds2)
                for wbds3 in wbds:
                    if (
                        wbds.index(wbds1) != wbds.index(wbds2)
                        and wbds.index(wbds2) != wbds.index(wbds3)
                        and wbds.index(wbds1) != wbds.index(wbds3)
                    ):
                        wbdss.append(wbds1 + wbds2 + wbds3)

    kbds = [kidb_yy, kidb_yyy, kidb_yyyy, kidb_xd, kidb_xm, kidb_dd, kidb_mm]

    kbdss = []

    for kbds1 in kbds:
        kbdss.append(kbds1)
        for kbds2 in kbds:
            if kbds.index(kbds1) != kbds.index(kbds2):
                kbdss.append(kbds1 + kbds2)
                for kbds3 in kbds:
                    if (
                        kbds.index(kbds1) != kbds.index(kbds2)
                        and kbds.index(kbds2) != kbds.index(kbds3)
                        and kbds.index(kbds1) != kbds.index(kbds3)
                    ):
                        kbdss.append(kbds1 + kbds2 + kbds3)


    kombinaac = [profile["pet"], petup, profile["company"], companyup]

    kombina = [
        profile["name"],
        profile["surname"],
        profile["nick"],
        nameup,
        surnameup,
        nickup,
    ]

    kombinaw = [
        profile["wife"],
        profile["wifen"],
        wifeup,
        wifenup,
        profile["surname"],
        surnameup,
    ]

    kombinak = [
        profile["kid"],
        profile["kidn"],
        kidup,
        kidnup,
        profile["surname"],
        surnameup,
    ]

    kombinaa = []
    for kombina1 in kombina:
        kombinaa.append(kombina1)
        for kombina2 in kombina:
            if kombina.index(kombina1) != kombina.index(kombina2) and kombina.index(
                kombina1.title()
            ) != kombina.index(kombina2.title()):
                kombinaa.append(kombina1 + kombina2)

    kombinaaw = []
    for kombina1 in kombinaw:
        kombinaaw.append(kombina1)
        for kombina2 in kombinaw:
            if kombinaw.index(kombina1) != kombinaw.index(kombina2) and kombinaw.index(
                kombina1.title()
            ) != kombinaw.index(kombina2.title()):
                kombinaaw.append(kombina1 + kombina2)

    kombinaak = []
    for kombina1 in kombinak:
        kombinaak.append(kombina1)
        for kombina2 in kombinak:
            if kombinak.index(kombina1) != kombinak.index(kombina2) and kombinak.index(
                kombina1.title()
            ) != kombinak.index(kombina2.title()):
                kombinaak.append(kombina1 + kombina2)

    kombi = {}
    kombi[1] = list(komb(kombinaa, bdss))
    kombi[1] += list(komb(kombinaa, bdss, "_"))
    kombi[2] = list(komb(kombinaaw, wbdss))
    kombi[2] += list(komb(kombinaaw, wbdss, "_"))
    kombi[3] = list(komb(kombinaak, kbdss))
    kombi[3] += list(komb(kombinaak, kbdss, "_"))
    kombi[4] = list(komb(kombinaa, years))
    kombi[4] += list(komb(kombinaa, years, "_"))
    kombi[5] = list(komb(kombinaac, years))
    kombi[5] += list(komb(kombinaac, years, "_"))
    kombi[6] = list(komb(kombinaaw, years))
    kombi[6] += list(komb(kombinaaw, years, "_"))
    kombi[7] = list(komb(kombinaak, years))
    kombi[7] += list(komb(kombinaak, years, "_"))
    kombi[8] = list(komb(word, bdss))
    kombi[8] += list(komb(word, bdss, "_"))
    kombi[9] = list(komb(word, wbdss))
    kombi[9] += list(komb(word, wbdss, "_"))
    kombi[10] = list(komb(word, kbdss))
    kombi[10] += list(komb(word, kbdss, "_"))
    kombi[11] = list(komb(word, years))
    kombi[11] += list(komb(word, years, "_"))
    kombi[12] = [""]
    kombi[13] = [""]
    kombi[14] = [""]
    kombi[15] = [""]
    kombi[16] = [""]
    kombi[21] = [""]
    if profile["randnum"] == "y":
        kombi[12] = list(concats(word, numfrom, numto))
        kombi[13] = list(concats(kombinaa, numfrom, numto))
        kombi[14] = list(concats(kombinaac, numfrom, numto))
        kombi[15] = list(concats(kombinaaw, numfrom, numto))
        kombi[16] = list(concats(kombinaak, numfrom, numto))
        kombi[21] = list(concats(reverse, numfrom, numto))
    kombi[17] = list(komb(reverse, years))
    kombi[17] += list(komb(reverse, years, "_"))
    kombi[18] = list(komb(rev_w, wbdss))
    kombi[18] += list(komb(rev_w, wbdss, "_"))
    kombi[19] = list(komb(rev_k, kbdss))
    kombi[19] += list(komb(rev_k, kbdss, "_"))
    kombi[20] = list(komb(rev_n, bdss))
    kombi[20] += list(komb(rev_n, bdss, "_"))
    komb001 = [""]
    komb002 = [""]
    komb003 = [""]
    komb004 = [""]
    komb005 = [""]
    komb006 = [""]
    if len(profile["spechars"]) > 0:
        komb001 = list(komb(kombinaa, profile["spechars"]))
        komb002 = list(komb(kombinaac, profile["spechars"]))
        komb003 = list(komb(kombinaaw, profile["spechars"]))
        komb004 = list(komb(kombinaak, profile["spechars"]))
        komb005 = list(komb(word, profile["spechars"]))
        komb006 = list(komb(reverse, profile["spechars"]))

    print("[+] son duzenlemeler...")

    komb_unique = {}
    for i in range(1, 22):
        komb_unique[i] = list(dict.fromkeys(kombi[i]).keys())

    komb_unique01 = list(dict.fromkeys(kombinaa).keys())
    komb_unique02 = list(dict.fromkeys(kombinaac).keys())
    komb_unique03 = list(dict.fromkeys(kombinaaw).keys())
    komb_unique04 = list(dict.fromkeys(kombinaak).keys())
    komb_unique05 = list(dict.fromkeys(word).keys())
    komb_unique07 = list(dict.fromkeys(komb001).keys())
    komb_unique08 = list(dict.fromkeys(komb002).keys())
    komb_unique09 = list(dict.fromkeys(komb003).keys())
    komb_unique010 = list(dict.fromkeys(komb004).keys())
    komb_unique011 = list(dict.fromkeys(komb005).keys())
    komb_unique012 = list(dict.fromkeys(komb006).keys())

    uniqlist = (
        bdss
        + wbdss
        + kbdss
        + reverse
        + komb_unique01
        + komb_unique02
        + komb_unique03
        + komb_unique04
        + komb_unique05
    )

    for i in range(1, 21):
        uniqlist += komb_unique[i]

    uniqlist += (
        komb_unique07
        + komb_unique08
        + komb_unique09
        + komb_unique010
        + komb_unique011
        + komb_unique012
    )
    unique_lista = list(dict.fromkeys(uniqlist).keys())
    unique_leet = []
    if profile["leetmode"] == "y":
        for (
            x
        ) in (
            unique_lista
        ):  

            x = make_leet(x) 
            unique_leet.append(x)

    unique_list = unique_lista + unique_leet

    unique_list_finished = []
    unique_list_finished = [
        x
        for x in unique_list
        if len(x) < CONFIG["global"]["wcto"] and len(x) > CONFIG["global"]["wcfrom"]
    ]

    print_to_file(profile["name"] + ".txt", unique_list_finished)


def download_http(url, targetfile):
    print("[+] " + targetfile + " dosyasini " + url + " linkinden indiriyom ")
    webFile = urllib.request.urlopen(url)
    localFile = open(targetfile, "wb")
    localFile.write(webFile.read())
    webFile.close()
    localFile.close()


def alectodb_download():

    url = CONFIG["global"]["alectourl"]

    print("\r\n[+] bir sey kontrol ediyom 1sn")

    targetfile = "alectodb.csv.gz"

    if not os.path.isfile(targetfile):

        download_http(url, targetfile)

    f = gzip.open(targetfile, "rt")

    data = csv.reader(f)

    usernames = []
    passwords = []
    for row in data:
        usernames.append(row[5])
        passwords.append(row[6])
    gus = list(set(usernames))
    gpa = list(set(passwords))
    gus.sort()
    gpa.sort()

    print(
        "\r\n[+] bir seyler yapiyom 1sn\r\n[+] heh bitti."
    )
    f = open("alectodb-usernames.txt", "w")
    f.write(os.linesep.join(gus))
    f.close()

    f = open("alectodb-passwords.txt", "w")
    f.write(os.linesep.join(gpa))
    f.close()


def download_wordlist():

    print("	\r\n	hangisini indircen knk sec\r\n")

    print("     1   Moby            14      french          27      places")
    print("     2   afrikaans       15      german          28      polish")
    print("     3   american        16      hindi           29      random")
    print("     4   aussie          17      hungarian       30      religion")
    print("     5   chinese         18      italian         31      russian")
    print("     6   computer        19      japanese        32      science")
    print("     7   croatian        20      latin           33      spanish")
    print("     8   czech           21      literature      34      swahili")
    print("     9   danish          22      movieTV         35      swedish")
    print("    10   databases       23      music           36      turkish")
    print("    11   dictionaries    24      names           37      yiddish")
    print("    12   dutch           25      net             38      exit program")
    print("    13   finnish         26      norwegian       \r\n")
    print(
        "	\r\n	dosyalar bak burdan indirilcek: "
        + CONFIG["global"]["dicturl"]
    )
    print(
        "	\r\n	indirince -w parametresiyle kullancan ha\r\n"
    )

    filedown = input("> numara gir: ")
    filedown.isdigit()
    while filedown.isdigit() == 0:
        print("\r\n[-] napiyon mal ")
        filedown = input("> numara gir: ")
    filedown = str(filedown)
    while int(filedown) > 38 or int(filedown) < 0:
        print("\r\n[-] mal misin ")
        filedown = input("> numara gir ")
    filedown = str(filedown)

    download_wordlist_http(filedown)
    return filedown


def download_wordlist_http(filedown):

    mkdir_if_not_exists("dictionaries")

    arguments = {
        1: (
            "Moby",
            (
                "mhyph.tar.gz",
                "mlang.tar.gz",
                "moby.tar.gz",
                "mpos.tar.gz",
                "mpron.tar.gz",
                "mthes.tar.gz",
                "mwords.tar.gz",
            ),
        ),
        2: ("afrikaans", ("afr_dbf.zip",)),
        3: ("american", ("dic-0294.tar.gz",)),
        4: ("aussie", ("oz.gz",)),
        5: ("chinese", ("chinese.gz",)),
        6: (
            "computer",
            (
                "Domains.gz",
                "Dosref.gz",
                "Ftpsites.gz",
                "Jargon.gz",
                "common-passwords.txt.gz",
                "etc-hosts.gz",
                "foldoc.gz",
                "language-list.gz",
                "unix.gz",
            ),
        ),
        7: ("croatian", ("croatian.gz",)),
        8: ("czech", ("czech-wordlist-ascii-cstug-novak.gz",)),
        9: ("danish", ("danish.words.gz", "dansk.zip")),
        10: (
            "databases",
            ("acronyms.gz", "att800.gz", "computer-companies.gz", "world_heritage.gz"),
        ),
        11: (
            "dictionaries",
            (
                "Antworth.gz",
                "CRL.words.gz",
                "Roget.words.gz",
                "Unabr.dict.gz",
                "Unix.dict.gz",
                "englex-dict.gz",
                "knuth_britsh.gz",
                "knuth_words.gz",
                "pocket-dic.gz",
                "shakesp-glossary.gz",
                "special.eng.gz",
                "words-english.gz",
            ),
        ),
        12: ("dutch", ("words.dutch.gz",)),
        13: (
            "finnish",
            ("finnish.gz", "firstnames.finnish.gz", "words.finnish.FAQ.gz"),
        ),
        14: ("french", ("dico.gz",)),
        15: ("german", ("deutsch.dic.gz", "germanl.gz", "words.german.gz")),
        16: ("hindi", ("hindu-names.gz",)),
        17: ("hungarian", ("hungarian.gz",)),
        18: ("italian", ("words.italian.gz",)),
        19: ("japanese", ("words.japanese.gz",)),
        20: ("latin", ("wordlist.aug.gz",)),
        21: (
            "literature",
            (
                "LCarrol.gz",
                "Paradise.Lost.gz",
                "aeneid.gz",
                "arthur.gz",
                "cartoon.gz",
                "cartoons-olivier.gz",
                "charlemagne.gz",
                "fable.gz",
                "iliad.gz",
                "myths-legends.gz",
                "odyssey.gz",
                "sf.gz",
                "shakespeare.gz",
                "tolkien.words.gz",
            ),
        ),
        22: ("movieTV", ("Movies.gz", "Python.gz", "Trek.gz")),
        23: (
            "music",
            (
                "music-classical.gz",
                "music-country.gz",
                "music-jazz.gz",
                "music-other.gz",
                "music-rock.gz",
                "music-shows.gz",
                "rock-groups.gz",
            ),
        ),
        24: (
            "names",
            (
                "ASSurnames.gz",
                "Congress.gz",
                "Family-Names.gz",
                "Given-Names.gz",
                "actor-givenname.gz",
                "actor-surname.gz",
                "cis-givenname.gz",
                "cis-surname.gz",
                "crl-names.gz",
                "famous.gz",
                "fast-names.gz",
                "female-names-kantr.gz",
                "female-names.gz",
                "givennames-ol.gz",
                "male-names-kantr.gz",
                "male-names.gz",
                "movie-characters.gz",
                "names.french.gz",
                "names.hp.gz",
                "other-names.gz",
                "shakesp-names.gz",
                "surnames-ol.gz",
                "surnames.finnish.gz",
                "usenet-names.gz",
            ),
        ),
        25: (
            "net",
            (
                "hosts-txt.gz",
                "inet-machines.gz",
                "usenet-loginids.gz",
                "usenet-machines.gz",
                "uunet-sites.gz",
            ),
        ),
        26: ("norwegian", ("words.norwegian.gz",)),
        27: (
            "places",
            (
                "Colleges.gz",
                "US-counties.gz",
                "World.factbook.gz",
                "Zipcodes.gz",
                "places.gz",
            ),
        ),
        28: ("polish", ("words.polish.gz",)),
        29: (
            "random",
            (
                "Ethnologue.gz",
                "abbr.gz",
                "chars.gz",
                "dogs.gz",
                "drugs.gz",
                "junk.gz",
                "numbers.gz",
                "phrases.gz",
                "sports.gz",
                "statistics.gz",
            ),
        ),
        30: ("religion", ("Koran.gz", "kjbible.gz", "norse.gz")),
        31: ("russian", ("russian.lst.gz", "russian_words.koi8.gz")),
        32: (
            "science",
            (
                "Acr-diagnosis.gz",
                "Algae.gz",
                "Bacteria.gz",
                "Fungi.gz",
                "Microalgae.gz",
                "Viruses.gz",
                "asteroids.gz",
                "biology.gz",
                "tech.gz",
            ),
        ),
        33: ("spanish", ("words.spanish.gz",)),
        34: ("swahili", ("swahili.gz",)),
        35: ("swedish", ("words.swedish.gz",)),
        36: ("turkish", ("turkish.dict.gz",)),
        37: ("yiddish", ("yiddish.gz",)),
    }


    intfiledown = int(filedown)

    if intfiledown in arguments:

        dire = "dictionaries/" + arguments[intfiledown][0] + "/"
        mkdir_if_not_exists(dire)
        files_to_download = arguments[intfiledown][1]

        for fi in files_to_download:
            url = CONFIG["global"]["dicturl"] + arguments[intfiledown][0] + "/" + fi
            tgt = dire + fi
            download_http(url, tgt)

        print("[+]  " + dire + " aha buraya kaydettim")

    else:
        print("[-] gidiyorum hadi by")


def mkdir_if_not_exists(dire):
    if not os.path.isdir(dire):
        os.mkdir(dire)


def main():

    read_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.cfg"))

    parser = get_parser()
    args = parser.parse_args()

    if not args.quiet:
        print_cow()

    if args.version:
        version()
    elif args.interactive:
        interactive()
    elif args.download_wordlist:
        download_wordlist()
    elif args.alecto:
        alectodb_download()
    elif args.improve:
        improve_dictionary(args.improve)
    else:
        parser.print_help()

def get_parser():
    parser = argparse.ArgumentParser(description="lyric4l pl lister v1 falan hic keyfim yok yazamıyom")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="iste profilize ederken interaktif sorular olayı",
    )
    group.add_argument(
        "-w",
        dest="improve",
        metavar="FILENAME",
        help="iste pl listin varsa onu daha iyi yapıyo bu komut"
    )
    group.add_argument(
        "-l",
        dest="download_wordlist",
        action="store_true",
        help="hazir olan pl leri indiriyosun",
    )
    group.add_argument(
        "-a",
        dest="alecto",
        action="store_true",
        help="bunu siktir et ya kullanma calismiyo zaten"
    )
    group.add_argument(
        "-v", "--version", action="store_true", help="versiyonu gosterio ama beceremedim calismiyo"
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="bu da sessiz mod internetten arakladim da bu da calismiyo glb"
    )

    return parser


if __name__ == "__main__":
    main()
