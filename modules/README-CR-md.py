# Prompt for HH LL Indicator


Erstelle einen Highest High (HH) und Lowest Low (LL) Indikator.

Ein HH liegt vor, wenn nach einer grünen Kerze unmittelbar zwei rote Kerzen nacheinander auftreten.
Kontrolliere die letzten 10 Kerzen und setze bei dem größten Docht die Markierung HH im Pandas-DataFrame.

Für das LL gilt: Nach einer roten Kerze, wenn zwei unmittelbar grüne Kerzen nacheinander erscheinen,
kontrolliere die letzten 10 Kerzen.
Setze das LL bei dem tiefsten Docht und trage es als LL in die Pandas-Reihe ein.