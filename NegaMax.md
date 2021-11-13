# Úvod do hraní her pro počítače


Pojďme se zamyslet nad tím, jak bychom mohli naučit počítač hrát Oware.
Lidi se snažili naučit stroje hrát šachy ještě před vynálezem počítačů,
takže máme spoustu nápadů, kterými se můžeme inspirovat.
Oware, stejně jako šachy, je v mnoha ohledech hra jednoduchá pro počítače:
máme kompletní přehled o stavu hry, nejsou přítomné žádné náhodné prvky
a hrají jenom dva hráči přímo proti sobě…

V tomto témátku nebudeme moc zabíhat do formalismů.
Pokud chcete zjistit víc o teorii her, podívejte se na témátko Hry provázející nás celý 26. ročník.


## Kde vlastně jsem?

První věc, co by počítač měl umět, je zjistit, v jak dobré pozici se nachází.
Pak už bude snadné poznat dobré tahy (to jsou ty, co vedou do lepších pozic)
a odtud už nějak celou hru zvládneme vyhrát. Jednoduché, ne?

Problém je, že měřit, jak dobrá daná pozice je, je těžké.
Umíme na konci hry poznat, kdo vyhrál, ale čím dál konec hry je,
tím mlhavější je naše představa o stavu hry.
V šachu se hráči koukají třeba na to, kolik figurek komu zbývá na šachovnici.
V Oware máme ještě přímočařejší metodu – můžeme se koukat na skóre.


> Rozšiřující problém 1:
>
> Skóre v Oware je dvojice čísel vyjadřující počty sklizených semínek.
> Zamyslete se, jak dobré je které z následujících skóre pro prvního hráče.
> Jak byste je uspořádali? Proč?
>
> 10:10, 15:20, 20:15, 10:15, 15:10, 25:10, 25:20, 30:10



Koukáním na skóre rozhodně nedokážeme určit výhodnost pozice dokonale,
ale i přibližný odhad se ukáže být dosti užitečným.
Tomuto ohodnocení situace se říká heuristika
a tradičně se vyhraným hrám přiřazuje hodnota plus nekonečno,
prohraným hrám mínus nekonečno,
a ještě nerozhodnutým hrám se připisují hodnoty někde mezi těmito extrémy.


> Rozšiřující problém 2:
>
> Jak by mohla vypadat heuristika pro Oware lepší než jen koukání na skóre?


## Kam chci jít?

Pokud už tušíme jak ohodnotit situaci, zbývá nám „jenom“ najít dobrý tah.
Tohle je myšlenka, kterou jste mohli vidět v agentovi `nejlepsi_po_mem`,
ač ten používal velmi jednoduchou heuristiku.
Naše heuristiky nejsou taky nijak dokonalé, budeme se tedy muset snažit
poznat dobrý tah nějak lépe.

Snad se shodneme na tom, že pokud existuje tah do výrazně lepší pozice,
tak naše aktuální pozice asi není moc špatná.
Naopak pokud všechny tahy vedou do špatných pozic, tak na tom asi nejsme dobře.
Pokud jsme na tahu, tak vybereme tah, který vede do pro nás nejvýhodnější pozice.
Heuristické ohodnocení této pozice by tedy mělo odpovídat maximu
z ohodnocení pozic, do kterých se umíme dostat jedním tahem.
Tuto myšlenku budeme chtít pořádně rozvinout,
ale na to se nejdříve musíme vcítit do role našeho soupeře.

Náš soupeř se snaží vyhrát, tedy abychom my prohráli.
Je-li na tahu, vybere tah vedoucí do pro nás nejhorší možné pozice.
Heuristické ohodnocení pozice, kde je na tahu soupeř, by tudíž mělo odpovídat
minimu z ohodnocení pozic, do kterých nás umí soupeř dostat jedním tahem.
Pokud se tedy pokusíme dohlédnout dále do budoucnosti,
tak ohodnocení naší aktuální pozice by mělo odpovídat ohodnocení
nejlepší z pozic, do kterých se umíme dostat jedním tahem,
a ohodnocení těchto pozic by naopak mělo odpovídat ohodnocení nejhorších pozic,
do kterých je nás poté schopen dostat soupeř.
Této myšlence se říká [MiniMax](https://en.wikipedia.org/wiki/Minimax), protože se střídají kroky, kde dochází k
maximalizování a minimalizování heuristiky.

Ještě než se ale pustíme do programování, pojďme si ukázat jeden elegantní trik.
Soupeřova snaha minimalizovat naši heuristiku se dá také popsat jako snaha
maximalizovat jeho heuristiku, která je k té naší opačná.
V praxi dokonce heuristiky tradičně bývají takové,
aby ohodnocení dané pozice oběma hráči se sečetla na nulu.
Tohle je nejen celkem rozumný způsob jak o heuristice uvažovat,
ale také vede k algoritmu známému jako NegaMax.

NegaMaxové ohodnocení naší aktuální pozice je tedy maximum z našich ohodnocení
pozic, do kterých se umíme dostat jedním tahem. Naše ohodnocení těchto pozic
je pak vždy negace soupeřova ohodnocení, kde soupeř se řídí stejným algoritmem.

Oware je příliš složitá hra na to, abychom dohlédli ze začátku až na její konec.
Snažit se dopracovat se NegaMaxem až k vyhraným či prohraným situacím by trvalo
příliš dlouho. Počty možných pozic rostou exponenciálně. Pořád je ale možné
nahlédnout několik tahů do budoucnosti a tam situaci ohodnotit heuristikou.
Zkuste to! V závislosti na rychlosti vašich programů byste měli vidět
asi tak pět tahů do budoucnosti a zvládnout porazit Agamemnona
a možná i Bellerophona.

## Co bude příště?

Příště se podíváme na několik pokročilejších triků
jak dohlédnout ještě dál do budoucnosti
a tím vylepšit svůj program natolik, aby se mohl utkat s Diomedem.
