#!/bin/bash



echo "nombre de simulation : "
read number_simulation
echo "starting simulations"
echo "--------------------------------------------------------------------------------------------------------------------------------------------------------------------"
for ((i = 0; i < $number_simulation; i++)); do
  echo "Simulation n°$i/$number_simulation"
  ./includes/Simulation1.py
  wait
  echo "--------------------------------------------------------------------------------------------------------------------------------------------------------------------"
done
