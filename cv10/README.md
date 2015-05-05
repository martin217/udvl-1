Cvičenie 10
==========

**Riešenie odovzdávajte podľa
[pokynov na konci tohoto zadania](#technické-detaily-riešenia)
do Štvrtka 14.5. 23:59:59.**

Súbory potrebné pre toto cvičenie si môžete stiahnúť ako jeden zip
[`cv10.zip`](https://github.com/FMFI-UK-1-AIN-411/udvl/archive/cv10.zip).

## Predikátová logika

Zapíšte v prvorádovej logike nasledovné tvrdenia (ak sú v zátvorke uvedené
konkrétne predikáty, použitie tie):

1. Potme je každá krava čierna.

1. Niet ruže bez tŕňa. (`ruza(x)`, `trn(x)`, `ma(x,y)`)

1. Niet na svete nikoho, kto by bol vždy šťastný. (`stastny(kto, kedy)`)

1. Vrana k vrane sadá.

1. `G` je kompletný graf. (`vrcholGrafu(graf,vrchol)`,
   `hranaGrafu(graf,vrchol1,vrchol2)`)

1. Lež večná meno toho nech ovenčí sláva,  
   kto seba v obeť svätú za svoj národ dáva.

Rozhodnite a zdôvodnite ktoré z nasledovných tvrdení sú pravdivé a ktoré nie:

1. Nech `φ` je prvorádová formula bez kvantifikátorov. Ak vo `φ` nahradíme
   všetky premenné za konštanty, dostaneme výrokovologickú formulu.

1. Nech `F` je splniteľná výrokovologická formula. Vyrobíme z nej prvorádovú
   formulu `Φ` tak, že každú výrokovologickú premennú `a` zmeníme na unárny
   predikát `a(x)` a "pred" celú formulu pridáme `∀x`. Teda napríklad formula
   `((a∧b)→(b∨a))` sa zmení na `∀x((a(x)∧b(x))→(b(x)∨a(x)))`.  Potom `Φ` je
   tiež splniteľná formula.

1. Nech `Φ` je prvorádová formula bez kvantifikátorov, premenných a funkčných
   symbolov (môže obsahovať konštanty).  Výrokovologickú formulu `F` vytvoríme
   tak, že všetky predikáty tvaru
   <code>P(c<sub>1</sub>,c<sub>2</sub>,...,c<sub>n</sub>)</code> vo `Φ`
   nahradíme výrokovologickou premennou
   <code>P\_c<sub>1</sub>\_c<sub>2</sub>\_...\_c<sub>n</sub></code>.
   Ak `Φ` bola splniteľná formula, tak `F` je tiež splniteľná.

1. Existuje formula pravdivá v práve jednej štruktúre.


## Hamiltonovská kružnica (4b)

Pomocou SAT solveru nájdite hamiltonovskú kružnicu v orientovanom grafe.

Implementujte triedu `HamiltonianCycle` s metódou `find` s jediným argumentom
`edges`, maticou susednosti: dvojrozmerné pole n x n bool-ov popisujúce hrany v
grafe: ak je v i-tom riadku na j-tom mieste `True`, tak z i do j vedie hrana
(vrcholy sú číslované od 0). Metóda vráti ako výsledok pole n čísel,
postupnosť vrcholov na kružnici, ak kružnica existuje, alebo prázdne pole, ak
kružnica neexistuje.


Potrebujeme zistiť či sa dajú vrcholy grafu usporiadať do takej postupnosti, že
vždy ide hrana z i-teho do (i+1)-teho vrcholu v tejto postupnosti. Potrebujeme
teda uhhádnuť, ktorý vrchol bude na ktorej pozícii v tejto postupnosti
(zabezpečiť, ze pre kažú pozíciu vyberieme práve jeden vrchol) a zabezpečiť že
za sebou idúce vrcholy sú sppojené hranou správnym smerom (ak nie je v grafe
hrana z a do b, nesmú byť a a b na nejakých pozíciách i a i+1).

Jedna z možností je mať premenné `v_pos_i`, ktoré budú
pravdivé práve vtedy ak vrchol `i` je na pozicii `pos`. Potom stačí:

- zabezpečiť, že je to postuponosť neopakujúcich sa vrcholov (dlžky N):
  - pre každé `pos` aspoň jedno z `v_pos_i` je pravdivé
    (na každej pozícii je aspoň jeden vrchol)
  - pre každé `pos` nie sú dve rôzne `v_pos_i` `v_pos_j` pravdivé naraz
    (nie sú dva vrholy na tej istej pozícii)
  - pre každé `i` nie sú dve rôzne `v_pos1_i` `v_pos2_i` pravdivé naraz
    (nie je jeden vrchol na dvoch rôznych pozíciách)
- zabezpečiť, že za sebou idúce vrholy sú spojené hranou, teda, ak sú v
  postupnosti za sebou, tak musia byť spojené hranou, resp (obmena) ak nie je
  hrana z i do j, tak nemôžu byť za sebou:
  - ak nie je v grafe hrana z `i` do `j`, tak pre každé `pos` nesmú platiť
    `v_pos_i` a `v_(pos+1)_j` (naraz), plus samozrejme aj pre poslendý a prvý,
    aby to bola kružnica.

Trošku nepekná vec na tomto zakódovaní / riešení je, že potrebujeme generovať
klauzy (alebo pomocné premenné) pre každú dvojicu vrcholov, medzi ktorými nie
je hrana. Plus netreba zabúdať, že pracujeme s orientovaným grafom.


## Technické detaily riešenia

Riešenie odovzdajte do vetvy `cv10` v adresári `cv10`.

Odovzdajte súbor `ham.py` v ktorom je implementovaná trieda `HamiltonianCycle`
s metódou `find`. Program `cv10test.py` musí s vašou knižnicou korektne zbehnúť.

Ak chcete v pythone použiť knižnicu z [examples/sat](../examples/sat), nemusíte
si ju kopírovať do aktuálne adresára, stačí ak na začiatok svojej knižnice
pridáte:
```python
import os
import sys
sys.path[0:0] = [os.path.join(sys.path[0], '../examples/sat')]
import sat
```

Odovzdávanie riešení v iných jazykoch konzultujte s cvičiacimi.
