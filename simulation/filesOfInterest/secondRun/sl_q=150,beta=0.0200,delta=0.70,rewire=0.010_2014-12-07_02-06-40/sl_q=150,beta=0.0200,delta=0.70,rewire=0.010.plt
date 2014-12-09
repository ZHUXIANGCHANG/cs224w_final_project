set title "sl_q=150,beta=0.0200,delta=0.70,rewire=0.010"
set key top left
set grid
set xdata time
set timefmt "%Y-%m-%d"
set terminal png size 1000,800
set output "sl_q=150,beta=0.0200,delta=0.70,rewire=0.010.png"
plot "Kailahun.tab" using 1:2 title "Kailahun" with lines,"Kenema.tab" using 1:2 title "Kenema" with lines,"Kono.tab" using 1:2 title "Kono" with lines,"Kambia.tab" using 1:2 title "Kambia" with lines,"Koinadugu.tab" using 1:2 title "Koinadugu" with lines,"Bombali.tab" using 1:2 title "Bombali" with lines,"Tonkolili.tab" using 1:2 title "Tonkolili" with lines,"Port_Loko.tab" using 1:2 title "Port Loko" with lines,"Pujehun.tab" using 1:2 title "Pujehun" with lines,"Bo.tab" using 1:2 title "Bo" with lines,"Moyamba.tab" using 1:2 title "Moyamba" with lines,"Bonthe.tab" using 1:2 title "Bonthe" with lines
