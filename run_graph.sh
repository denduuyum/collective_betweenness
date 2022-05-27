#!/bin/bash

names=("Bovine.txt" "Circuit.txt" "Ecoli.txt" "USAir97.txt" "humanDiseasome.txt" "Treni_Roma.txt" "EU_flights.txt" "openflights.txt" "yeast1.txt" "powergrid.txt" "OClinks.txt" "facebook.txt" "grqc.txt" "hepth.txt" "hepph.txt" "astroph.txt" "condmat.txt")

lnames=("Bovine" "Circuit" "Ecoli" "USAir97" "humanDiseasome" "Treni_Roma" "EU_flights" "openflights" "yeast1" "powergrid" "OClinks" "facebook" "grqc" "hepth" "hepph" "astroph" "condmat")


for i in "${!names[@]}"; do
    echo ${names[i]} 
    python3.7 sir.py -T 100 -o ${lnames[i]}_d1.png -n ${lnames[i]}_d1 ../network_betweenness/data/${names[i]} 
done
