

## Typy dat
Dělíme na numerická a kategoriální

### Numerická
 * Matematická - dají se s nimi dělat mat. operace
 * Kdo ví jaké jsou ty ostatní


### Kategoriální
* Nominální - nedaji se moc porovnávat
* Ordinálni - daji se porovnat

## Data Matrix
Řádky a sloupce, sloupce můžeme nazývat atributy.
Objekty jsou jakoby řádky v matici.

Jeden řádek matice reprezentuje bod v dimenzi, např. dimenze 2d bude rovina, 3d bude prostor, 4d bod v dimenzi 4.

Sloupec bude reprezentovat vektor, s dimenzí N.
Práci s maticemi můžeme reprezentovat jako práci s body v prostoru.

S bodama v prostoru můžeme vidět blízkost bodů, skupiny těch bodů, tzv. shluky, odchylky, body které se liší něčím od ostatních *(outlier)*.

Do prostoru si uděláme souřadný systém zavedením os, 1 pro každou dimenzi, které se protnou v jednom bodu 
a každá osa bude mít i své měřítko. Kartézský souřadnicový systém má osy na sebe kolmé a
mají stejné měřítko.

Jakýkoliv bod lze vyjádřit jako lineární kombinaci bázových vektorů prostoru.

Skalárním součinem lze určit vzdálenost dvou vektorů.
Podobnost měříme kosínovou podobnost, která je v intervalu od 0 do 1.

Toto jsou míry, míry si jsou symetrické.

* Rozptyl - vzdálenost bodů od průměru 
* Mean, Průměr matice - průměr ze všech bodů

### Centered Data Matrix
Počátek souřadnicového systému přesuneme na průměr

### Linární ne/závislost
Sloupce, které jsou lineárně závislé na ostatních se dá vynechat, má to spojitost
s hodností (rank) matice.


# Nástroje analýzy

### Aritmetický průměr
kvadratický, geometrický, harmonický
* rozptyl,
* (relativní) standardní odchylky (deviation), 
* confidence interval (interval spolehlivosti) - říká např. pro 150 záznámu a spočítám jejich průměr, jak je ten průměr důvěrný, +-průměr, který by se spočítal i na jiné sadě

### Median
quantile (quartile), interquartile range, outlier, boxplot

### Statistická distribuce
normal distribution, (cumulative) distribution function

### Korelace

Korelace je číslo od -1 do 1 mezi atributy. Pokud atributy dostatečně korelují, v budoucí analýze mi stačí použít pouze jeden atribut,
a druhý vypustit, protože spolu korelují.

Spearmanova nebo Pearsonova metoda pro výpočet korelace

### Pravděpodobnostní funkce

Jestliže X je diskrétní hodnota, tak součet všech pravděpodobností se musí rovnat 1.
#### Bernoulli distribuce (pokusy)
Pokud je hodnota menší než 7, tak se jedná o malý lístek, jinak je to velký lístek.
Pravděpodobnosti jsou pak jen 2, malý lístek nebo velký lístek

##### Binomická distribuce

Např. sáhnu 10 do klouboku, kolikrát se stane, že vytáhnu 2 lístky, které budou velké.

Funkce hustoty, která se počítá s integrálem, kde výsledek integrálu všech pravděpodobnostních hodnot také musí být rovna 1

## Distribuce
Normální rozdělení pro sloupeček je vzorec viz slidy.

**Na 4. cvičení pro každý sloupec atributů udělat 
empirickou a normální distribuci a porovnat grafy.
Rozdělí interval na jednotlivé části (mini-interval) a spočítá se
kolik hodnot spadá do daného miní-intervalu. Tím se dostane sloupcový graf.**

Kumulativní distribuce, jak teoretické tak i empirické

