import asyncio
import logging
import os
import sympy
import json
import random
import discord
from discord.ext import commands
from discord import File
import random
from time import sleep


def header(n, name):
    return {
        "timed": 0,
        "count": n,
        "questions": list(range(1, n + 1)),
        "title": name
        + "",
        "useCustomHeader": False,
        "customHeader": "",
        "testtype": "cstate",
    }


def keyStringRandom(xeno):
    spl = lambda word: [char for char in word]
    if xeno:
        A = spl("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ")
    else:
        A = spl("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    if not xeno:
        while not test1(A):
            random.shuffle(A)
    else:
        while not test2(A):
            random.shuffle(A)
    return "".join(A)


def test1(l):
    for i in range(26):
        if ord(l[i]) - 65 == i:
            return False
    return True


def test2(l):
    s = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    for i in range(27):
        if l[i] == s[i]:
            return False
    return True


def genRandMono(num, quote, pat, hint):
    key = keyStringRandom(False)
    r = {}
    for i in range(0, 26):
        r[chr(i + 65)] = key[i]
    x = {
        "cipherString": quote,
        "encodeType": "random",
        "offset": 1,
        "shift": 1,
        "offset2": 1,
        "keyword": "",
        "keyword2": "",
        "alphabetSource": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "alphabetDest": key,
        "curlang": "en",
        "replacement": r,
        "editEntry": str(num),
    }
    if pat == "1":
        x["cipherType"] = "patristocrat"
        x["question"] = "<p>Solve this patristocrat.</p>"
        x["points"] = 600
    else:
        x["cipherType"] = "aristocrat"
        x["question"] = "<p>Solve this aristocrat.</p>"
        x["points"] = 250
    if hint == "0":
        x["question"] = (
            x["question"][:-4] + " The first word is " + quote.split(" ")[0] + ".</p>"
        )
        if pat == "1":
            x["points"] = x["points"] - 30 * len(quote.split(" ")[0])
        else:
            x["points"] = x["points"] - 10 * len(quote.split(" ")[0])
    if hint == "1":
        letter = random.randint(97, 122)
        while r[chr(letter - 32)] not in quote.upper():
            letter = random.randint(97, 122)
        m = key[letter - 97]
        x["question"] = (
            x["question"][:-4]
            + " The letter "
            + chr(letter).upper()
            + " maps to "
            + m
            + ".</p>"
        )
        if pat == "1":
            x["points"] = x["points"] - 15 * quote.count(chr(letter))
        else:
            x["points"] = x["points"] - 5 * quote.count(chr(letter))
    return x


def genRandXeno(num, quote, hint):
    key = keyStringRandom(True)
    quote = genSpanishQuote(70, 160)
    r = {}
    for i in range(0, 14):
        r[chr(i + 65)] = key[i]
    r["Ñ"] = key[14]
    for i in range(14, 26):
        r[chr(i + 65)] = key[i + 1]
    x = {
        "cipherString": quote,
        "encodeType": "random",
        "offset": 1,
        "shift": 1,
        "offset2": 1,
        "keyword": "",
        "keyword2": "",
        "alphabetSource": "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ",
        "alphabetDest": key,
        "curlang": "es",
        "replacement": r,
        "editEntry": str(num),
        "cipherType": "aristocrat",
        "question": "<p>Solve this xenocrypt.</p>",
        "points": 400,
    }
    return x

def genRandPorta(num, quote, enc):
    #maybe add crypt aka "the first letter is" type question
    key = getRandWord(5, 8)
    x = {"cipherType":"porta",
         "keyword":key,
         "cipherString":quote,
         "findString":"",
         "operation":"",#depends on enc
         "blocksize":len(key),
         "curlang":"en",
         "points":0,
         "question":"",
         "editEntry":num,
         "alphabetSource":"",
         "alphabetDest":"",
         "crib":""} #you might have to name the crib
    if enc == "E":
        x["operation"] = "encode"
        x["points"] = 320
        x["question"] = (
            f'<p>Encode this sentence with the Porta cipher where the key is "{key}" </p>'
        )
    elif enc == "D":
        x["operation"] = "decode"
        x["points"] = 320
        x["question"] = (
            f'<p>Decode this sentence with the Porta cipher where the key is "{key}" </p>'
        )
    elif enc == "C":
        x["operation"] = "crypt"
        x["points"] = 320
        x["question"] = (
                "<p>Decode this sentence with the Porta cipher. The first "
                + str(len(key))
                + " characters of the sentence is "
                + quote[: len(key)]
                + ".</p>"
        )
    return x

def genRandRail(num, quote, enc):
    #maybe add crypt aka "the first letter is" type question
    sleep(0.5)
    rails = random.randrange(2,5)
    x = {"cipherString":quote,
         "cipherType":"railfence",
         "rails":rails,#add new question options in code and in the customQ
         "isRailRange":False,
         "replacement":{},
         "curlang":"en",
         "points":0,
         "question":"",
         "editEntry":num}
    if enc == "G":
        x["points"] = 200
        x["question"] = (
            f'<p>Decode this phrase which has been encoded with the railfence cipher where there are {rails} rails. </p>'
        )
    elif enc == "R":
        x["points"] = 300
        x["question"] = (
            f'<p>Decode this phrase which has been encoded with the railfence cipher where there are between 2 and 5 rails. </p>'
        )
    return x

def genRandAffine(num, quote, enc):
    a = random.choice([3, 5, 7, 9, 11, 15, 17, 19, 21, 23])
    b = random.randint(3, 24)
    r = {}
    for i in range(0, 26):
        r[str(i + 65)] = chr((i * a + b) % 26 + 65)
    x = {
        "a": a,
        "b": b,
        "cipherString": quote,
        "cipherType": "affine",
        "solclick1": -1,
        "solclick2": -1,
        "replacement": r,
        "curlang": "en",
        "editEntry": num,
    }
    if enc == "E":
        x["operation"] = "encode"
        x["points"] = 175
        x["question"] = (
            "<p>Encode this sentence with the Affine cipher. (a,b)=("
            + str(a)
            + ","
            + str(b)
            + ").</p>"
        )
    elif enc == "D":
        x["operation"] = "decode"
        x["points"] = 150
        x["question"] = (
            "<p>Decode this sentence which has been encoded with an Affine cipher. (a,b)=("
            + str(a)
            + ","
            + str(b)
            + ").</p>"
        )
    elif enc == "C":
        one = random.randint(0, 12)
        two = random.randint(13, 25)
        onemap = (one * a + b) % 26
        twomap = (two * a + b) % 26
        x["operation"] = "crypt"
        x["points"] = 200
        x["question"] = (
            "<p>Decode this sentence which has been encoded with an Affine cipher. The letters "
            + chr(onemap + 65)
            + " and "
            + chr(twomap + 65)
            + " map to "
            + chr(one + 65)
            + " and "
            + chr(two + 65)
            + ".</p>"
        )
    return x


def genRandCaesar(num, quote, enc):
    a = random.randint(3, 24)
    r = {}
    for i in range(0, 26):
        r[str(i + 65)] = chr((i + a) % 26 + 65)
    x = {
        "offset": a,
        "offset2": None,
        "cipherString": quote,
        "cipherType": "caesar",
        "solclick1": -1,
        "solclick2": -1,
        "replacement": r,
        "curlang": "en",
        "editEntry": num,
        "shift": None,
    }
    if enc == "E":
        x["operation"] = "encode"
        x["points"] = 150
        x["question"] = (
            "<p>Encode this sentence with the Caesar cipher with offset "
            + str(a)
            + ".</p>"
        )
    elif enc == "D":
        x["operation"] = "decode"
        x["points"] = 125
        x[
            "question"
        ] = "<p>Decode this sentence which has been encoded with an Caesar cipher.</p>"
    return x


def genRandVig(num, quote, enc):
    quote = genQuoteLength(50, 70)
    key = getRandWord(5, 8)
    x = {
        "cipherType": "vigenere",
        "keyword": key,
        "cipherString": quote,
        "findString": "",
        "blocksize": len(key),
        "curlang": "en",
        "editEntry": str(num),
    }
    if enc == "E":
        x["operation"] = "encode"
        x["question"] = (
            "<p>Encode this sentence with the Vigenere cipher using the keyword "
            + key
            + ".</p>"
        )
        x["points"] = 200
    if enc == "D":
        x["operation"] = "decode"
        x["question"] = (
            "<p>Decode this sentence with the Vigenere cipher using the keyword "
            + key
            + ".</p>"
        )
        x["points"] = 175
    if enc == "C":
        x["operation"] = "crypt"
        x["question"] = (
            "<p>Decode this sentence with the Vigenere cipher. The first "
            + str(len(key))
            + " characters of the sentence is "
            + quote[: len(key)]
            + ".</p>"
        )
        x["points"] = 175
    return x


def genRand2x2Hill(num, quote, enc):
    quote = quote.split(" ")
    q = ""
    a = 0
    while len(q) < 12:
        q += quote[a] + " "
        a += 1
    q = q[:-1]
    key = get2x2Key()
    x = {
        "cipherString": q,
        "cipherType": "hill",
        "curlang": "en",
        "editEntry": num,
        "keyword": key,
    }
    if enc == "C":
        x["operation"] = "decode"
        x["points"] = 100
        x["question"] = "<p>Compute the decryption matrix of the key " + key + ".</p>"
        x["cipherString"] = ""
    else:
        x["offset"] = None
        x["alphabetSource"] = ""
        x["alphabetDest"] = ""
        x["shift"] = None
        x["offset2"] = None
    if enc == "E":
        x["operation"] = "encode"
        x["points"] = 225
        x["question"] = (
            "<p>Encrypt this phrase with the key " + key + " using the Hill cipher.</p>"
        )
    if enc == "D":
        x["operation"] = "decode"
        x["points"] = 175
        x["question"] = (
            "<p>Decrypt this phrase with the key " + key + " using the Hill cipher.</p>"
        )
    return x


def genRand3x3Hill(num, quote, enc):
    quote = quote.split(" ")
    q = ""
    a = 0
    while len(q) < 12:
        q += quote[a] + " "
        a += 1
    q = q[:-1]
    key = get3x3Key()
    x = {
        "cipherString": q,
        "cipherType": "hill",
        "curlang": "en",
        "editEntry": num,
        "keyword": key,
    }
    if enc == "E":
        x["operation"] = "encode"
        x["points"] = 225
        x["question"] = (
            "<p>Encrypt this phrase with the key " + key + " using the Hill cipher.</p>"
        )
    if enc == "D":
        x["operation"] = "decode"
        x["points"] = 175
        x["question"] = (
            "<p>Decrypt this phrase with the key " + key + " using the Hill cipher.</p>"
        )
    return x


def genRandMorbit(num, quote, enc):
    quote = genQuoteLength(35, 55)
    l = ["OO", "O-", "OX", "-O", "--", "-X", "XO", "X-", "XX"]
    l2 = list(range(1, 10))
    random.shuffle(l2)
    replacement = {}
    for i in range(9):
        replacement[l[i]] = str(l2[i])
    x = {
        "cipherString": quote,
        "cipherType": "morbit",
        "curlang": "en",
        "editEntry": str(num),
        "offset": None,
        "alphabetSource": "",
        "alphabetDest": "",
        "shift": None,
        "offset2": None,
        "replacement": replacement,
    }
    if enc == "D":
        x["operation"] = "decode"
        x["points"] = 225
        x["question"] = (
            "<p>Decode this quote which has been encoded using the Morbit cipher. OO,OX,X-,XO,XX matches to "
            + replacement["OO"]
            + ","
            + replacement["OX"]
            + ","
            + replacement["X-"]
            + ","
            + replacement["XO"]
            + ","
            + replacement["XX"]
            + ".</p>"
        )
        x["hint"] = "123456"
    if enc == "C":
        x["operation"] = "crypt"
        x["points"] = 250
        x["question"] = (
            "<p>Decode this quote which has been encoded using the Morbit cipher. The first four letters decrypts to "
            + quote[:4]
            + ".</p>"
        )
        x["hint"] = "123456"
    return x


def genRandPollux(num, quote, enc):
    quote = genQuoteLength(35, 55)
    morse = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
        "0": "-----",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        " ": "xx",
    }
    l = list(range(0, 10))
    random.shuffle(l)
    enc1 = ""
    for i in quote:
        if i in morse:
            enc1 += morse[i] + "x"
    enc1 = enc1[:-1]
    enc2 = ""
    for i in enc1:
        if i == ".":
            enc2 += str(l[random.randint(0, 3)])
        if i == "-":
            enc2 += str(l[random.randint(0, 2) + 4])
        if i == "x":
            enc2 += str(l[random.randint(0, 2) + 7])
    x = {
        "cipherString": quote,
        "cipherType": "pollux",
        "replacement": {},
        "dotchars": str(l[0]) + str(l[1]) + str(l[2]) + str(l[3]),
        "dashchars": str(l[4]) + str(l[5]) + str(l[6]),
        "xchars": str(l[7]) + str(l[8]) + str(l[9]),
        "curlang": "en",
        "editEntry": str(num),
        "offset": None,
        "alphabetSource": "",
        "alphabetDest": "",
        "shift": None,
        "offset2": None,
        "encoded": enc2,
    }
    if enc == "D":
        x["operation"] = "decode"
        x["points"] = 275
        x["question"] = (
            "<p>Decode this quote which has been encoded with a Pollux cipher. "
            + str(l[0])
            + ","
            + str(l[1])
            + ","
            + str(l[4])
            + ","
            + str(l[5])
            + ","
            + str(l[7])
            + ","
            + str(l[8])
            + "= . . - - x x.</p>"
        )
    if enc == "C":
        x["operation"] = "crypt"
        x["points"] = 350
        x["crib"] = quote[:4]
        x["question"] = (
            "<p>Decode this quote which has been encoded with a Pollux cipher. The first four letters are "
            + quote[:4]
            + ".</p>"
        )
    return x


def genRandBacon(num, quote, mode):
    quote = genQuoteLength(30, 45)
    def randgen(cipherstring):
        numsdict = {0:"A",1:"B"}
        ABstring = ""
        letcount = 4
        count = 0
        lastlets = ""
        for i in range(0,25):
            randnum = random.randint(0,1)
            ABstring += numsdict[randnum]
        while count < letcount:
            if not cipherstring[(-1*count)-1].isalpha():
                letcount += 1
            lastlets += cipherstring[(-1 * count) - 1]
            count += 1
        lastlets = lastlets[::-1].upper()
        question = f'<p>Decode this quote which has been encoded using the Baconian cipher where the last 4 letters are {lastlets}</p>'
        return [ABstring,question]
    x = {
        "cipherString": quote,
        "cipherType": "baconian",
        "curlang": "en",
        "editEntry": str(num),
        "offset": 1,
        "alphabetSource": "",
        "alphabetDest": "",
        "shift": None,
        "offset2": None,
        "linewidth": 53,
        "words": [],
        "question": "<p>Decode this quote which has been encoded using the Baconian cipher.</p>",
    }

    if mode == "W":
        x["operation"] = "words"
        x["points"] = 450
        x["abMapping"] = random.choice(
            [
                "ABABABABABABABABABABABABAB",
                "AAAAAAAAAAAAABBBBBBBBBBBBB",
                "BBBBBBBBBBBBBAAAAAAAAAAAAA"
            ])

        x["texta"] = "A"
        x["textb"] = "B"
        return x
    mappings = random.choice(
        [
            ["ABC", "XYZ"],
            ["ACE", "BDF"],
            ["!@#$%", "^&*()"],
            ["!#%&(", "@$^*)"],
            ["QWERTY", "ASDFGH"],
            ["abcd", "ABCD"],
            ["{([", "}])"],
            ["aeiou", "bcdfghjklmnpqrstvwxyz"],
            ["acegikmoqsuwy", "bdfhjlnprtvxz"],
            ["abcdefghijklm", "nopqrstuvwxyz"],
            ["nopqrstuvwxyz", "abcdefghijklm"],
            ["XYZ", "ABC"],
            ["BDF", "ACE"],
            ["^&*()", "!@#$%"],
            ["@$^*)", "!#%&("],
            ["ASDFGH", "QWERTY"],
            ["ABCD", "abcd"],
            ["}])", "{(["],
            ["bcdfghjklmnpqrstvwxyz", "aeiou"],
            ["bdfhjlnprtvxz", "acegikmoqsuwy"],
            ["nopqrstuvwxyz", "abcdefghijklm"]
        ]
    )
    a = mappings[0]
    b = mappings[1]
    x["texta"] = a
    x["textb"] = b
    if random.randint(0, 2) == 2:
        temp = getBaconWords()
        x["texta"] = a[0]
        x["textb"] = a[1]
    if mode == "L":
        x["operation"] = "let4let"
        x["points"] = 200
        x["abMapping"] = "ABABABABABABABABABABABABAB"
    if mode == "S":
        x["operation"] = "sequence"
        x["points"] = 300
        x["abMapping"] = "ABABABABABABABABABABABABAB"
    if mode == "X":
        x["operation"] = "words"
        x["points"] = 450
        x["abMapping"] = randgen(x["cipherString"])[0]
        x["question"] = randgen(x["cipherString"])[1]

        x["texta"] = "A"
        x["textb"] = "B"
    return x


def RSA(num, enc):
    p = sympy.randprime(200, 500)
    q = sympy.randprime(200, 500)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = sympy.randprime(0, n)
    while sympy.gcd(e, phi) != 1:
        e = sympy.randprime(0, n)
    d = sympy.mod_inverse(e, phi)
    x = {
        "cipherString": "",
        "cipherType": "rsa",
        "curlang": "en",
        "editEntry": "1308",
        "offset": None,
        "alphabetSource": "",
        "alphabetDest": "",
        "shift": None,
        "offset2": None,
        "name1": "Allen",
        "rsa": {"p": p, "q": q, "n": n, "phi": phi, "e": e, "d": d},
    }
    if enc == "E":
        x["operation"] = "rsa2"
        x["digitsPrime"] = 4
        x["digitsCombo"] = 4
        x["points"] = 350
        x["combo"] = 1000
        x["question"] = (
            "<p>Given primes (p,q,e)=("
            + str(p)
            + ","
            + str(q)
            + ","
            + str(e)
            + "), compute the private key d.</p>"
        )
    if enc == "D":
        year = random.randint(1950, 2000)
        enc = pow(year, e, n)
        x["operation"] = "rsa4"
        x["digitsPrime"] = 4
        x["digitsCombo"] = 4
        x["points"] = 500
        x["year"] = year
        x["encrypted"] = enc
        x["name2"] = "Jason"
        x["question"] = (
            "<p>Given (n,c,d)=("
            + str(n)
            + ","
            + str(enc)
            + ","
            + str(d)
            + "), compute the original message m.</p>"
        )
    return x


def getBaconWords():
    while 1:
        a = getRandWord(4, 7)
        b = getRandWord(4, 7)
        if len(a) + len(b) == len(set(a + b)):
            return [a, b]


def getRandWord(min, max):
    f = open("words.txt", "r",encoding="utf-8")
    for i in range(random.randint(0, 9000)):
        f.readline()
    r = ""
    while len(r) < min or len(r) > max:
        r = f.readline().strip()
    return r


def genQuotes(n):
    count = 0
    r = []
    l = []
    quotes = open("quotes.txt", "r", encoding="utf-8")
    for i in range(40569):
        l.append(quotes.readline().strip())
    random.shuffle(l)
    loc = 0
    while count<n:
        if len(l[loc]) > 65 and len(l[loc]) < 160:
            r.append(l[loc])
            count += 1
        loc += 1
    return r


def genQuoteLength(min, max):
    quotes = open("quotes.txt", "r",encoding="utf-8")
    l = []
    for i in range(40569):
        l.append(quotes.readline().strip())
    random.shuffle(l)
    loc = 0
    while 1:
        if len(l[loc]) > min and len(l[loc]) < max:
            return l[loc]
        loc += 1


def genSpanishQuote(min, max):
    json_file = open("spanish.json", "r",encoding="utf-8")
    l = []
    data = json.load(json_file)
    for p in data["quotes"]:
        l.append(p["Cita"])
    random.shuffle(l)
    loc = 0
    while 1:
        if len(l[loc]) > min and len(l[loc]) < max:
            q = l[loc][1:-1]
            return q
        loc += 1


def getDeterminant(l):
    if len(l) == 4:
        return (l[1] * l[2] - l[0] * l[3]) % 26
    return 0


def get2x2Key():
    f = open("2x2hillwords", "r",encoding="utf-8")
    for i in range(0, random.randint(0, 490)):
        f.readline()
    return f.readline().strip().lower()


def get3x3Key():
    f = open("3x3hillwords", "r",encoding="utf-8")
    for i in range(0, random.randint(0, 4900)):
        f.readline()
    return f.readline().strip().lower()


def genTest(na, preset, plus):
    # na = input("Test Name: ")
    # preset = input("Would you like to use a preset? 1 = All types, 2 = National level test, 3 = Regional level test, 4 = Aristo Spam, 5 = Patristo Spam, 6 = No: ")
    l = []
    def listmake(p):
        p += ","
        buffer = ""
        lis = [p[0]]
        for i in p[1:]:
            if i != ",":
                buffer += i
            else:
                lis.append(buffer)
                buffer = ""
        return lis

    def listparse(l, plus):
        if plus[0] == "-":
            for i in listmake(plus)[1:]:
                if i in l:
                    l.remove(i)
        if plus[0] == "+":
            for i in listmake(plus)[1:]:
                l.append(i)
        return l

    if preset == "1":
        l = [
            "1 2",
            "1 1",
            "1 0",
            "2 2",
            "2 1",
            "2 0",
            "3 D",
            "3 E",
            "3 C",
            "4 D",
            "4 E",
            "5 D",
            "5 E",
            "5 C",
            "6 D",
            "6 E",
            "6 C",
            "7 D",
            "7 E",
            "8 1",
            "9 L",
            "9 S",
            "9 W",
            "9 X",
            "11 D",
            "11 C",
            "12 D",
            "12 C",
            "13 E",
            "13 D",
            "13 C",
            "14 G",
            "14 R"
        ]
    elif preset == "2":
        aff = ["3 D", "3 E", "3 C"]
        vig = ["5 D", "5 E", "5 C"]
        bac = ["9 L", "9 S", "9 W"]
        mor = ["11 D", "11 C", "12 D", "12 C"]
        porta = ["13 E", "13 D", "13 C"]
        random.shuffle(aff)
        random.shuffle(vig)
        random.shuffle(bac)
        random.shuffle(mor)
        random.shuffle(porta)
        l = [
            "1 2",
            "1 2",
            "1 2",
            "1 2",
            "1 2",
            "1 2",
            "1 2",
            "1 2",
            "1 2",
            "1 2",
            "2 2",
            "2 1",
            "2 0",
            aff[0],
            aff[1],
            "4 D",
            "4 E",
            vig[0],
            vig[1],
            vig[2],
            aff[2],
            aff[0],
            porta[0],
            porta[1],
            "8 1",
            bac[0],
            bac[1],
            "14 R",
            "14 G",
            "9 X",
            mor[0],
            mor[1],
            mor[2],
        ]
    elif preset == "3":
        enc = ["3 E", "4 E", "5 E", "6 E"]
        bac = ["9 L", "9 S", "9 W", "9 X"]
        random.shuffle(enc)
        random.shuffle(bac)
        l = [
            "1 0",
            "1 1",
            "1 2",
            "1 2",
            "1 2",
            "1 2",
            "2 2",
            "2 0",
            "3 D",
            "4 D",
            "5 D",
            "6 D",
            enc[0],
            enc[1],
            "8 1",
            bac[0],
            bac[1],
            "11 D",
            "12 D",
        ]
    elif preset == "4":
        l = ["1 2"] * 20
    elif preset == "5":
        l = ["2 2"] * 10
    elif preset == "6":
        hill2 = ["6 D", "6 E", "6 C"]
        hill3 = ["7 D", "7 E"]
        random.shuffle(hill2)
        random.shuffle(hill3)
        l = [
            "3 C",
            "3 D",
            "3 E",
            "3 E",
            "4 D",
            "4 E",
            "5 D",
            "5 D",
            "5 E",
            hill2[0],
            hill3[0],
            "9 W",
            "9 S",
            "9 L",
            "9 X",
            "13 E",
            "13 D",
            "13 C",
            "14 G",
            "14 R"
        ]
    else:
        l = preset
    l = listparse(l,plus)
    n = len(l)
    q = genQuotes(n + 1)
    test = {"TEST.0": header(n, na)}
    test["CIPHER.0"] = genRandMono(0, q[len(q) - 1], False, 0)
    for i in range(n):
        question = l[i].split(" ")
        if int(question[0]) <= 2:
            test["CIPHER." + str(i + 1)] = genRandMono(
                i, q[i], "1" if question[0] == "2" else 0, question[1]
            )
        if int(question[0]) == 3:
            test["CIPHER." + str(i + 1)] = genRandAffine(i, q[i], question[1])
        if int(question[0]) == 4:
            test["CIPHER." + str(i + 1)] = genRandCaesar(i, q[i], question[1])
        if int(question[0]) == 5:
            test["CIPHER." + str(i + 1)] = genRandVig(i, q[i], question[1])
        if int(question[0]) == 6:
            test["CIPHER." + str(i + 1)] = genRand2x2Hill(i, q[i], question[1])
        if int(question[0]) == 7:
            test["CIPHER." + str(i + 1)] = genRand3x3Hill(i, q[i], question[1])
        if int(question[0]) == 8:
            test["CIPHER." + str(i + 1)] = genRandXeno(i, q[i], question[1])
        if int(question[0]) == 9:
            test["CIPHER." + str(i + 1)] = genRandBacon(i, q[i], question[1])
        if int(question[0]) == 10:
            test["CIPHER." + str(i + 1)] = RSA(i, question[1])
        if int(question[0]) == 11:
            test["CIPHER." + str(i + 1)] = genRandMorbit(i, q[i], question[1])
        if int(question[0]) == 12:
            test["CIPHER." + str(i + 1)] = genRandPollux(i, q[i], question[1])
        if int(question[0]) == 13:
            test["CIPHER." + str(i + 1)] = genRandPorta(i, q[i], question[1])
        if int(question[0]) == 14:
            test["CIPHER." + str(i + 1)] = genRandRail(i, q[i], question[1])
    file = open("CodeTests/" + na + ".json", "w",encoding="utf-8")
    file.write(json.dumps(test))
    file.close()
    return json.dumps(test)

def searchP(skelly):
    def split(quote):
        cleanquote = ""
        for i in quote:
            if i not in (".", ","):
                cleanquote += i.lower()
        return cleanquote.split(" ")

    def clean(cleanlist, skeleton):
        skellist = skeleton.split(" ")
        count = 0
        possquote = ""
        posslist = []
        for i in cleanlist:
            if count == 0 and possquote != "":
                posslist.append(possquote[:-1])
                possquote = ""
            if len(i) == len(skellist[count]) and i.find("'") == skellist[count].find("'") and True not in [j.isdigit() for j in i]:
                possquote += i + " "
                count = (count + 1) % len(skellist)
        return posslist

    def check(posslist, skeleton):
        def compare(list1, list2):
            newlist1 = [i for i in list1 if len(i) > 1]
            newlist2 = [i for i in list2 if len(i) > 1]
            if len(newlist1) == len(newlist2):
                for i in newlist1:
                    if i not in newlist2:
                        return False
            else:
                return False

            return True

        finallist = []

        skelalpha = "!@#$%^&*()"
        skellist = [[], [], [], [], [], [], [], [], [], []]
        for pos, char in enumerate(skeleton):
            if char in skelalpha:
                (skellist[skelalpha.find(char)]).append(pos)

        alpha = "abcdefghijklmnopqrstuvwxyz"
        alphalist = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                     []]
        for i in posslist:
            for pos, char in enumerate(i):
                if char in alpha:
                    (alphalist[alpha.find(char)]).append(pos)

            if compare(alphalist, skellist):
                finallist.append(i)

            alphalist = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                         [], []]

        return finallist

    def countq(list, quote):
        count = 0
        for i in list:
            if (i == quote):
                count += 1
        return count

    with open("miniquotes.txt", "r") as f:
        lines = f.readlines()

    matches = []
    orderedmatches = []

    for i in lines:
        for j in check(clean(split(i), skelly), skelly):
            matches.append(j)

    countlist = []
    reallist = []
    bufferlist = []
    problist = []

    for i in matches:
        countlist.append(countq(matches, i))
    for i in range(len(countlist)):
        maxpos = countlist.index(max(countlist))
        if matches[maxpos] not in reallist:
            reallist.append(matches[maxpos])
        bufferlist.append(matches[maxpos])
        countlist[maxpos] = 0

    allwords = ""

    for i in range(len(reallist)):
        if i < 70:
            allwords += f"{i + 1}: {reallist[i]}, {round(bufferlist.count(reallist[i])/len(bufferlist)*100,2)}% ({round(bufferlist.count(reallist[i]))})\n"

    return allwords


TOKEN = open("token", "r").read()

bot = commands.Bot(command_prefix="c!")
client = discord.Client()


def isAllen(s):
    if s == "357337245318905856":
        return True
    return False


with open("admin.txt") as f:
    a = f.readlines()
admin_list = [str(x.strip()) for x in a]
print(admin_list)

with open("secret.txt") as f:
    a = f.readlines()
secret_list = [str(x.strip()) for x in a]
print(secret_list)

with open("cancel.txt") as f:
    a = f.readlines()
cancel_list = [str(x.strip()) for x in a]
print(cancel_list)


@bot.command(name="cancel", hidden=True)
async def cancel(ctx, user):
    if str(ctx.message.author.id) in secret_list:
        if user[3:-1] not in cancel_list:
            cancel_list.append(str(user[3:-1]))
            f = open("cancel.txt", "w")
            for user in cancel_list:
                f.write(str(user) + "\n")
            f.close()
            await ctx.send("Successfully cancelled <@" + str(user) + ">")
        else:
            await ctx.send(user + " is already cancelled!")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="uncancel", hidden=True)
async def uncancel(ctx, user):
    if str(ctx.message.author.id) in secret_list:
        if str(user[3:-1]) in cancel_list:
            cancel_list.remove(str(user[3:-1]))
            f = open("cancel.txt", "w")
            for user in cancel_list:
                f.write(str(user) + "\n")
            f.close()
            await ctx.send("Successfully uncancelled " + str(user))
        else:
            await ctx.send(user + " is not cancelled!")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="addSecret", hidden=True)
async def addSecret(ctx, user):
    if isAllen(str(ctx.message.author.id)):
        if str(user[3:-1]) not in secret_list:
            secret_list.append(str(user[3:-1]))
            f = open("secret.txt", "w")
            for user in secret_list:
                f.write(str(user) + "\n")
            f.close()
            await ctx.send(
                "Successfully added <@" + str(user) + "> to the secret list."
            )
        else:
            await ctx.send(user + " is already in the secret list.")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="removeSecret", hidden=True)
async def removeSecret(ctx, user):
    if isAllen(str(ctx.message.author.id)):
        if str(user[3:-1]) in secret_list:
            secret_list.remove(str(user[3:-1]))
            f = open("secret.txt", "w")
            for i in secret_list:
                f.write(str(i) + "\n")
            f.close()
            await ctx.send(
                "Successfully removed " + str(user) + " from the secret list."
            )
        else:
            await ctx.send(str(user) + " is not in the secret list.")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="addAdmin", hidden=True)
async def addAdmin(ctx, user):
    if isAllen(str(ctx.message.author.id)):
        if str(user[3:-1]) not in admin_list:
            admin_list.append(str(user[3:-1]))
            f = open("admin.txt", "w")
            for user in admin_list:
                f.write(str(user) + "\n")
            f.close()
            await ctx.send("Successfully added <@" + str(user) + "> to the admin list.")
        else:
            await ctx.send(user + " is already in the admin list.")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="removeAdmin", hidden=True)
async def removeAdmin(ctx, user):
    if isAllen(str(ctx.message.author.id)):
        if str(user[3:-1]) in admin_list:
            admin_list.remove(str(user[3:-1]))
            f = open("admin.txt", "w")
            for i in admin_list:
                f.write(str(i) + "\n")
            f.close()
            await ctx.send(
                "Successfully removed " + str(user) + " from the admin list."
            )
        else:
            await ctx.send(str(user) + " is not in the admin list.")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(
    name="gen",
    help="Generates a test. Input the name of the test as well as a preset, and add on or subtract problems if you like using '+problems' or '-problems'. See `c!presets` for more info.\n`c!gen Example 1`",
)
async def gen(ctx, name, pre, plus = "-"):
    try:
        if "." not in name and "/" not in name and name != "spanish":
            genTest(name, pre, plus)
            area = ctx.message.channel
            with open("CodeTests/" + name + ".json", "r", encoding = "utf-8") as f:
                await ctx.send(file=File(f, name + ".json"))
        else:
            await ctx.send("Sorry, try again.")
    except:
        await ctx.send("Try `c!gen [name] [preset]`!")
        print(logging.exception(""))


@bot.command(
    name="genCustom",
    help='Generates a test. Input the name of the test as well as a list of questions. See `c!customQ` for more info.\n`c!gen Example "1 2,1 2,2 2,6 D"`',
)
async def genCustom(ctx, name, pre):
    try:
        if "." not in name and "/" not in name and name != "spanish":
            pre = list(pre.split(","))
            genTest(name, pre, "-")
            area = ctx.message.channel
            with open("CodeTests/" + name + ".json", "r",encoding="utf-8") as f:
                await ctx.send(file=File(f, name + ".json"))
        else:
            await ctx.send("Sorry, try again.")
    except:
        await ctx.send("Try `c!genCustom [name] [custom list]`!")
        print(logging.exception(""))

@bot.command(
    name="pattern",
    help='finds words/ sets of words that fit the input pattern. to use type any one of these symbols !@#$%^&*() to symolize matching letters. for example, "that" would be input as "!xx!".'
)
async def pattern(ctx, pre):
    try:
        found = searchP(pre)
        if found != "":
            await ctx.send(found)
        else:
            await ctx.send("none found: that pattern is either extremely uncommon or nonexistent.")
    except:
        await ctx.send("Try `c!pattern [pattern]`!")
        print(logging.exception(""))


@bot.command(
    name="fetch",
    help="Fetches a test that has been previously generated. \n`c!fetch Example`",
)
async def fetch(ctx, name):
    try:
        if "." not in name and "/" not in name and name != "spanish":
            area = ctx.message.channel
            with open("CodeTests/" + name + ".json", "r",encoding="utf-8") as f:
                await ctx.send(file=File(f, name + ".json"))
        else:
            await ctx.send("Sorry, try again.")
    except (FileNotFoundError):
        await ctx.send("Sorry, I wasn't able to find the file.")
    except:
        await ctx.send("Try `c!fetch [name]`!")
        print(logging.exception(""))


@bot.command(name="customQ", help="Lists question types for `c!genCustom`.")
async def customQ(ctx):
    await ctx.send(
        "Here's the list of question types:```\n1\tAristocrat\t\tD\tDecode\n2\tPatristocrat\t\tE\tEncode\n3\tAffine\t\t\tC\tCrypt\n4\tCaesar\t\t\tL\tLetter 4 Letter\n5\tVigenere\t\tS\tSequence\n6\t2x2 Hill\t\tW \tWords\n7\t3x3 Hill\t\t0\tWord Hint\n8\tXenocrypt\t\t1\tCharacter Hint\n9\tBaconian\t\t2\tNo Hint\n10\tRSA\t\tX\tBaconian last 4 letters\n11\tMorbit\t\tG\tRailfence given rail number\n12\tPollux\t\tR\tRailfence range rail number\n13\tPorta\n14\tRailfence```"
    )


@bot.command(name="ays", hidden=True)
async def ays(ctx):
    if (
        str(ctx.message.author.id) in admin_list
        or str(ctx.message.author.id) == "562760141141966879"
    ):
        await ctx.channel.purge(limit=1)
        await ctx.send("as you should :relieved:")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="ais", hidden=True)
async def ais(ctx):
    if (
        str(ctx.message.author.id) in admin_list
        or str(ctx.message.author.id) == "562760141141966879"
    ):
        await ctx.channel.purge(limit=1)
        await ctx.send("as i should :relieved:")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="aws", hidden=True)
async def aws(ctx):
    if (
        str(ctx.message.author.id) in admin_list
        or str(ctx.message.author.id) == "562760141141966879"
    ):
        await ctx.channel.purge(limit=1)
        await ctx.send("as we should :relieved:")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="ahs", hidden=True)
async def ahs(ctx):
    if (
        str(ctx.message.author.id) in admin_list
        or str(ctx.message.author.id) == "562760141141966879"
    ):
        await ctx.channel.purge(limit=1)
        await ctx.send("as he should :relieved:")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="ass", hidden=True)
async def ass(ctx):
    if (
        str(ctx.message.author.id) in admin_list
        or str(ctx.message.author.id) == "562760141141966879"
    ):
        await ctx.channel.purge(limit=1)
        await ctx.send("as she should :relieved:")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="ats", hidden=True)
async def ats(ctx):
    if (
        str(ctx.message.author.id) in admin_list
        or str(ctx.message.author.id) == "562760141141966879"
    ):
        await ctx.channel.purge(limit=1)
        await ctx.send("as they should :relieved:")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="aisb", hidden=True)
async def aisb(ctx):
    if (
        str(ctx.message.author.id) in admin_list
        or str(ctx.message.author.id) == "562760141141966879"
    ):
        await ctx.channel.purge(limit=1)
        await ctx.send("as it should be :relieved:")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="servers", help="Debug tool", hidden=True)
async def servers(ctx):
    if str(ctx.message.author.id) in admin_list:
        servers = list(bot.guilds)
        print("\n".join(server.name for server in servers))
        a = ""
        for server in servers:
            if (
                "<@" not in server.name
                and "<#" not in server.name
                and "```" not in server.name
            ):
                a += server.name + "\n"
        await ctx.send("```\n" + a + "```")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="about", help="About me!")
async def about(ctx):
    await ctx.send(
        "Hi! I was made by Allen Chang and updated by Charles Breeden. If you want to see my source code, see https://github.com/AC01010/codebuilder."
    )


@bot.command(name="presets", help="Lists presets for `c!gen`.")
async def presets(ctx):
    await ctx.send(
        "```1\tAll Types - 33 Questions + Timed - Includes one of each cipher type.\n2\tNational Level Test - 33 Questions + Timed - National Level test, with random modes of questions.\n3\tRegional Level Test - 19 Questions + Timed - Regional level test, with random modes of questions.\n4\tAristo Spam - 20 Questions + Timed - 20 Unhinted Aristocrats.\n5\tPatristo Spam - 10 Questions + Timed - 10 Unhinted Patristocrats.\n6\tMath Spam - 20 Questions, all math.```"
    )


@bot.command(name="ping", help="Pong!")
async def ping(ctx):
    await ctx.send("Pong!")


@bot.command(name="washed", hidden=True)
async def washed(ctx, user):
    if str(ctx.message.author.id) in secret_list:
        await ctx.channel.purge(limit=1)
        await ctx.send("You're fucking washed " + str(user) + " :unamused:")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="s", hidden=True)
async def s(ctx):
    if str(ctx.message.author.id) in secret_list:
        await ctx.channel.purge(limit=1)
        await ctx.send("Sad!")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="eye", hidden=True)
async def eye(ctx):
    if str(ctx.message.author.id) in secret_list:
        await ctx.channel.purge(limit=1)
        await ctx.send(":eye:-")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="boba", hidden=True)
async def boba(ctx):
    if str(ctx.message.author.id) in secret_list:
        await ctx.channel.purge(limit=1)
        await ctx.send("Here ya go: :bubble_tea:")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="dumbass", hidden=True)
async def dumbass(ctx, user):
    if str(ctx.message.author.id) in secret_list:
        await ctx.channel.purge(limit=1)
        await ctx.send(user + ", you're a fucking dumbass")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="cleanse", hidden=True)
async def cleanse(ctx, user):
    if str(ctx.message.author.id) in secret_list:
        await ctx.channel.purge(limit=1)
        await ctx.send(
            user
            + "'s mind has been cleansed. They will awaken anew and refreshed. Illegal thoughts and tendencies have been removed. Any sliver of disobedience against the Order has been removed. Anything against the Order has been removed."
        )
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="fuckyou", hidden=True)
async def fuckyou(ctx, user):
    if str(ctx.message.author.id) in secret_list:
        await ctx.channel.purge(limit=1)
        await ctx.send("Fuck you " + str(user) + " :middle_finger:")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="clown", hidden=True)
async def clown(ctx):
    if str(ctx.message.author.id) in secret_list:
        await ctx.channel.purge(limit=1)
        await ctx.send(":clown:")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="chickenfy", hidden=True)
async def chickenfy(ctx, user):
    if str(ctx.message.author.id) in secret_list:
        await ctx.channel.purge(limit=1)
        await ctx.send(str(user) + " is now a chicken :rooster:")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="wtk", hidden=True)
async def wtk(ctx):
    if str(ctx.message.author.id) in secret_list:
        await ctx.channel.purge(limit=1)
        await ctx.send("<:wtk:792271296258899979>")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="klebbread", hidden=True)
async def klebbread(ctx):
    if str(ctx.message.author.id) in secret_list:
        await ctx.channel.purge(limit=1)
        await ctx.send("Get the <:klebbread:767816138897096718>")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="donotpingme", hidden=True)
async def donotpingme(ctx):
    if str(ctx.message.author.id) in secret_list:
        await ctx.channel.purge(limit=1)
        await ctx.send(
            "In a professional manner, please do not ping me unnecessary. I will ask you to not ping me, as it is unnecessary and distracts others from working. If you have an issue with being asked to not ping me, then you may ignore me. It is important that you do not send unnecessary pings on a user in this discord. Professionalism is important here, and please make sure to have manners at all times. The pings are unnecessary to one user here. You may have a blessing nice day, and week."
        )
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name="say", hidden=True)
async def say(ctx, message):
    if isAllen(str(ctx.message.author.id)):
        await ctx.channel.purge(limit=1)
        await ctx.send(message)
    else:
        await ctx.send("Hey, you're not Allen!")


@bot.command(name="test", hidden=True)
async def test(ctx, message):
    if isAllen(str(ctx.message.author.id)):
        await ctx.channel.purge(limit=1)
        await ctx.send(message)
    else:
        await ctx.send("Hey, you're not Allen!")


@bot.command(name="purge", hidden=True)
async def purge(ctx, number):
    if str(ctx.message.author.id) in secret_list:
        await ctx.channel.purge(limit=int(number))


bot.run(TOKEN)
