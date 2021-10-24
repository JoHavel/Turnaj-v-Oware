# Turnaj v Oware
Vítejte na GitHub stránce témátu Oware středoškolského korespondenčního semináře [M&M](https://mam.mff.cuni.cz/).

Pravidla Oware a úvod k témátu najdete na stránkách [prvního čísla](https://mam.mff.cuni.cz/media/cislo/pdf/28/28-1.pdf).

## Turnaje
První turnaj proběhl 13. října 2021 a dopadl následovně (2 body za vítězství, 1 za remízu, 5+5 her každý s každým):
|          | Adam  | Daniel | Jiří  | Tomáš | Martin | Umístění |
|----------|-------|--------|-------|-------|--------|----------|
| Adam     |   X   |  16:4  | 18:2  | 20:0  |  20:0  |    1.    |
| Daniel   |  4:16 |    X   | 10:10 | 20:0  |  20:0  |    2.    |
| Jiří     |  2:18 |  10:10 |   X   | 20:0  |  20:0  |    3.    |
| Tomáš    |  0:20 |   0:20 |  0:20 |   X   |  20:0  |    4.    |
| Martin   |  0:20 |   0:20 |  0:20 |  0:20 |    X   |    5.    |

Další turnaj je plánován zhruba na 27. října 2021.

## Instalace
Jediné, co potřebujete je Python 3. Ten najdete např. na [oficiálních stránkách](https://www.python.org/downloads/).

Následně si stačí tento repozitář stáhnout (záložka `code` výše, položka `Download zip`), rozbalit do libovolné složky a spustit kliknutím na příslušný soubor, nebo z příkazové řádky (zvláště pokud chcete spouštět [oware/text.py](oware/text.py) s parametry) jako (po přesunutí se do složky `oware`) `python ….py`, například `python text.py -f` nebo `python text.py -s agents/nahodny.py agents/nejlepsi_po_mem.py`.
## Technické detaily
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

Poslední aktualizace 24. 10. 2021 (přidán první turnaj)
