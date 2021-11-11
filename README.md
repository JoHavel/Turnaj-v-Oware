# Turnaj v Oware
Vítejte na GitHub stránce témátu Oware středoškolského korespondenčního semináře [M&M](https://mam.mff.cuni.cz/).

Pravidla Oware a úvod k témátu najdete na stránkách [prvního čísla](https://mam.mff.cuni.cz/media/cislo/pdf/28/28-1.pdf).

## Vypsané odměny
|        | Agamemnon (3b) | Bellerophon (2b) | Cadmus (3b) | Diomedes (3b) | Erechtheus (  ) |
|--------|----------------|------------------|-------------|---------------|-----------------|
| Adam   |     20:0       |      17:3        |    13:7     |      9:11     |                 |
| Jiří   |     20:0       |      16:4        |    13:7     |      8:12     |                 |
| Václav |     15:5       |      14:6        |    13:7     |      5:15     |                 |
| Daniel |     20:0       |      14:6        |     2:18    |      0:20     |                 |
| Tomáš  |     18:2       |      10:10       |     2:18    |      0:20     |                 |
| Martin |      8:12      |       0:20       |     0:20    |      0:20     |                 |

## Turnaje
První turnaj proběhl 13. října 2021 a dopadl následovně (2 body za vítězství, 1 za remízu, 5+5 her každý s každým):
|          | Adam  | Daniel | Jiří  | Tomáš | Martin | Umístění |
|----------|-------|--------|-------|-------|--------|----------|
| Adam     |   X   |  16:4  | 18:2  | 20:0  |  20:0  |    1.    |
| Daniel   |  4:16 |    X   | 10:10 | 20:0  |  20:0  |    2.    |
| Jiří     |  2:18 |  10:10 |   X   | 20:0  |  20:0  |    3.    |
| Tomáš    |  0:20 |   0:20 |  0:20 |   X   |  20:0  |    4.    |
| Martin   |  0:20 |   0:20 |  0:20 |  0:20 |    X   |    5.    |

Druhý turnaj proběhl 27. října 2021 a dopadl následovně:
|          | Adam  | Václav | Jiří  | Daniel | Tomáš | Martin | Umístění | Suma |
|----------|-------|--------|-------|--------|-------|--------|----------|------|
| Adam     |   X   |  12:8  |  9:11 |  20:0  | 20:0  |  20:0  |    1.    |  81  |
| Václav   |  8:12 |    X   | 14:6  |  19:1  | 20:0  |  10:10 |    2.    |  71  | 
| Jiří     | 11:9  |   6:14 |   X   |  12:8  | 20:0  |  20:0  |    3.    |  69  |
| Daniel   |  0:20 |   1:19 |  8:12 |    X   | 20:0  |  20:0  |    4.    |  49  |
| Tomáš    |  0:20 |   0:20 |  0:20 |   0:20 |   X   |  20:0  |    5.    |  20  |
| Martin   |  0:20 |  10:10 |  0:20 |   0:20 |  0:20 |    X   |    6.    |  10  |

Třetí turnaj proběhl 10. listopadu a zde jsou výsledky:
|        | Adam   | Jiří   | Václav | Daniel | Tomáš  | Martin | Umístění | Suma |
|--------|--------|--------|--------|--------|--------|--------|----------|------|
| Adam   |   X    | 11:9   | 14:6   | 18:2   | 16:4   | 20:0   |     1.   |  79  |
| Jiří   |  9:11  |   X    | 14:6   | 14:6   | 20:0   | 20:0   |     2.   |  77  |
| Václav |  6:14  |  6:14  |   X    | 16:4   | 20:0   | 10:10  |     3.   |  58  |
| Daniel |  2:18  |  6:14  |  4:16  |   X    | 10:10  | 20:0   |     4.   |  42  |
| Tomáš  |  4:16  |  0:20  |  0:20  | 10:10  |   X    | 20:0   |     5.   |  34  |
| Martin |  0:20  |  0:20  | 10:10  |  0:20  |  0:20  |   X    |     6.   |  10  |

Další turnaj je plánován zhruba na 24. listopadu 2021.

## Instalace
Jediné, co potřebujete je Python 3. Ten najdete např. na [oficiálních stránkách](https://www.python.org/downloads/).

Následně si stačí tento repozitář stáhnout (záložka `code` výše, položka `Download zip`), rozbalit do libovolné složky a spustit kliknutím na příslušný soubor, nebo z příkazové řádky (zvláště pokud chcete spouštět [oware/text.py](oware/text.py) s parametry) jako (po přesunutí se do složky `oware`) `python ….py`, například `python text.py -f` nebo `python text.py -s agents/nahodny.py agents/nejlepsi_po_mem.py`.
## Technické detaily
Jelikož máme velmi napilno a času moc není, tak nové funkce prozatím nepopisujeme v dokumentaci, ale jejich popis je přímo u nich v komentářích a dokumentaci Pythonu. Nové funkce jsou: `freeze` a `staw`.

Vaše řešení, které se skládá z **jednoho** souboru (<50MB) popsaného v [dokumentaci](dokumentace_user.pdf), odevzdávejte v odevzdávátku, které po přihlášení najdete na stránkách [M&M](https://mam.mff.cuni.cz/).

Tento soubor má obsahovat implementaci tzv. agenta, tj. skriptu, který sám hraje hru Oware. Nějaké jednoduché příklady takových skriptů najdete ve složce [oware/agents](oware/agents).

Mimo agenta můžete samozřejmě odevzdávat i popis, jak jste postupovali při jeho programování, nebo obecné nápady ke strategii. Pokud takový text sepíšete, orgové budou moc rádi a pravděpodobně vás odmění body navíc. 😉

Také si můžete hru vyzkoušet pomocí skriptů [oware/text.py](oware/text.py) a [oware/graphics.py](oware/graphics.py). I k těm najdete více v [dokumentaci](dokumentace_user.pdf).

V případě zájmu o to, jak toto celé funguje uvnitř, je něco málo napsáno v [programátorské dokumentaci](dokumentace_user.pdf), případně si můžete přečíst přímo zdrojové kódy.

# Povolení a zákazy

### Skript může:
- používat základní python (proměnné, funkce, třídy, základní moduly)
- ...

### Skript nemůže:
- komunikovat po síti
- zneužívat slabin a chyb programu (Pokud o nějakých víte, budu rád, když se ozvete na [jonas.havelka@volny.cz](mailto:jonas.havelka@volny.cz).)
- odchytávat obecnou Exception (tj. `except:` nebo `except BaseException:`) 
- ...

***[Turnajová část](/oware/tournament.py), povolení a zákazy se mohou (a pravděpodobně budou) měnit. [oware/text.py](oware/text.py), [oware/graphics.py](oware/graphics.py) a časový limit na tah se možná také změní. Zato to, jak má vypadat vaše řešení se na 99,9% měnit nebude (leda přidáním dalších featur na objekt game).***

Poslední aktualizace 10. 11. 2021 (aktualizovány souboje o odměny a třetí turnaj)
