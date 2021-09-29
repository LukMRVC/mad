

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
