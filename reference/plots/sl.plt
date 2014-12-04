set title "Cumulative confirmed cases in Sierra Leone by County"
set key top left
set grid
set xdata time
set timefmt "%Y-%m-%d"
set terminal png size 1000,800
set output "sl.png"
plot "sl_Kailahun.tab" using 1:2 title "Kailahun" with lines,"sl_Kenema.tab" using 1:2 title "Kenema" with lines,"sl_Kono.tab" using 1:2 title "Kono" with lines,"sl_Kambia.tab" using 1:2 title "Kambia" with lines,"sl_Koinadugu.tab" using 1:2 title "Koinadugu" with lines,"sl_Bombali.tab" using 1:2 title "Bombali" with lines,"sl_Tonkolili.tab" using 1:2 title "Tonkolili" with lines,"sl_Port_Loko.tab" using 1:2 title "Port Loko" with lines,"sl_Pujehun.tab" using 1:2 title "Pujehun" with lines,"sl_Bo.tab" using 1:2 title "Bo" with lines,"sl_Moyamba.tab" using 1:2 title "Moyamba" with lines,"sl_Bonthe.tab" using 1:2 title "Bonthe" with lines
