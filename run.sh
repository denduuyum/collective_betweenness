#!/bin/bash

names=("Bovine.txt" "Circuit.txt" "Ecoli.txt" "USAir97.txt" "humanDiseasome.txt" "Treni_Roma.txt" "EU_flights.txt" "openflights.txt" "yeast1.txt" "powergrid.txt" "OClinks.txt" "facebook.txt" "grqc.txt" "hepth.txt" "hepph.txt" "astroph.txt" "condmat.txt")

for i in "${!names[@]}"; do
    echo ${names[i]} >> corr_d1.out
    python3 corr.py ../network_betweenness/data/${names[i]} >> corr_d1.out
done
