# potřebuje linux nebo WSL a nainstalovaný program make
# pro inicializaci se musí spustit build (ještě jsem se nedostal k tomu umožnit puštění i bez toho)
# poté se pomocí make vždy spočítají zápasy mezi novými a změněnými agenty a vypíše se výsledek
# kompletního (tj. i s nezměněnými agenty) turnaje do build/turnaj.txt.

# Agenti musí být ve složce agents/ a jejich výčet musí být napsán zde:
agents = nahodny.py nejlepsi_po_mem.py spravny_nahodny.py
crossproduct = $(foreach P,$(agents),$(addprefix $P__,$(agents)))
crossproductTXT = $(addsuffix .txt,$(crossproduct))
BUILDcrossproductTXT = $(addprefix build/,$(crossproductTXT))
N = 5

turnaj.txt: $(BUILDcrossproductTXT) oware.py
	./oware.py -G --Table $(addprefix agents/, $(agents)) > turnaj.txt
	$(eval x=$(shell cat build/history/counter.txt))
	cp turnaj.txt build/history/turnaj$(x).txt
	echo $(shell expr $(x) + 1) > build/history/counter.txt

build:
	mkdir build
	mkdir build/history
	echo 0 > build/history/counter.txt

# .SECONDEXPANSION for automatic prerequisites
.SECONDEXPANSION:
build/%.txt: $$(addprefix agents/,$$(subst __, ,$$(notdir $$(basename $$@)))) oware.py
	./oware.py -H --table -n $(N) $(addprefix agents/, $(subst __, ,$(notdir $(basename $@)))) > $@
