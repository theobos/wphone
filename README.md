# WPhone

**WPhone** is de Python-versie van de eerste Wonderfoon, die was geschreven in Go voor de Raspberry Pi (zie **wonderfoon-1.1.pdf** voor bouwinstructies). Deze variant is niet meer te vinden op de websites www.wonderfoon.nl en www.wonderfoon.eu, maar is vervangen door Wonderfoons die kant en klaar te koop zijn, of varianten waarvan het zelf bouwen wat minder bewerkelijk is. 
De Python-versie is eenvoudiger dan de versie in Go: er is maar één configuratie-bestand en er is geen build nodig.

WPhone werkt met alle T65-modellen waar uit de draaischijf of het toetsenbord alleen een rode, blauwe en gele draad komen.

### Configuratie

De WPhone kent maar één configuratie-bestand, **wphone.config**, dat als volgt wordt uitgeleverd:

```json
{
 "off-hook"        :  16,
 "red"             :  19,
 "blue"            :  26,	
 "max-wait"        :  2,
 "polling-interval":  0.02,
 "music-dir"       : "music",
 "music-player"    : "mplayer",
 "led"             :  18  
}
```
#### off-hook

De naam van de GPIO-pin die signaleert of de hoorn op de haak ligt; 16 betekent GPIO16. Bij het oppakken van de hoorn klinkt de kiestoon.

#### red

Het nummer van de GPIO-pin waar de rode draad aan vast is gemaakt; 19 betekent GPIO19.

#### blue

Het nummer van de GPIO-pin waar de rode draad aan vast is gemaakt; 26 betekent GPIO26.

#### max-wait

De tijd (in seconden, eventueel met decimalen) die wordt gewacht tot het langzaamste cijfer, '0', is gedraaid. Deze tijd kan per T65-model verschillen. Bij een hoge waarde duurt het lang voordat de gekozen muziek gaat spelen.

#### polling-interval

De tijd (in seconden, eventueel met decimalen) tussen de opeenvolgende keren dat de GPIO-pinnen red en blue worden gelezen.

#### music-dir

In **music-dir** staan de audio-files. De eerste 9 files (gesorteerd op naam) horen bij cijfer 1 t/m 9, de tiende bij cijfer 0. De geluidsformaten moeten wel door de gekozen **music-player** afgespeeld kunnen worden. De namen van de audio-files hoeven aan geen enkele conventie te voldoen en worden nergens geconfigureerd, maar voor de sortering kan het handig zijn om de naam met een getal (01 t/m 10) te beginnen.
Deze directory kan absoluut of relatief aan de installatie-directory van WPhone zijn.

#### music-player

Het commando om de muziek af te spelen. De default, **mplayer**, speelt alle (on)bekende muziek-formaten af.

#### led

Het nummer van de GPIO-pin waaraan de LED is vast gemaakt; 18 betekent GPIO18. Deze LED gaat aan zodra de Raspberry Pi is opgestart.

### Opmerkingen

De gele draad moet aan één van de GND GPIO-pinnen vast zijn gemaakt maar hoeft niet geconfigureerd te worden.

### Installatie & Starten
Kopieer alle bestanden naar dezelfde directory, bijvoorbeeld **/home/pi/wphone**.
Voor testen & experimenteren kan de WPhone als volgt gestart worden:

```bash
cd /home/pi/wphone
./wphone-start.sh
```

### Automatisch starten
De WPhone kan automatisch gestart worden. In dit geval is WPhone geïnstalleerd in **/home/pi/wphone**.

Voeg aan bestand **/etc/rc.local** de volgende regel toe (vlak voor de regel met **exit 0**):

```bash
cd /home/pi/wphone
rm -f nohup.out; nohup wphone-start.sh &
```

Zodra de Rasperry Pi is gestart, gebeurt het volgende:
 
- De LED gaat aan
- Trompetgeschal
- Afluisteren van draaischijf of toetsenbord begint
