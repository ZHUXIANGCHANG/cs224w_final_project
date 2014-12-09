set title "guin_q=2000,beta=0.0300,delta=0.90"
set key top left
set grid
set xdata time
set timefmt "%Y-%m-%d"
set terminal png size 1000,800
set output "guin_q=2000,beta=0.0300,delta=0.90.png"
plot "Conakry.tab" using 1:2 title "Conakry" with lines,"Gueckedou.tab" using 1:2 title "Gueckedou" with lines,"Macenta.tab" using 1:2 title "Macenta" with lines,"Dabola.tab" using 1:2 title "Dabola" with lines,"Kissidougou.tab" using 1:2 title "Kissidougou" with lines,"Telimele.tab" using 1:2 title "Telimele" with lines,"Boffa.tab" using 1:2 title "Boffa" with lines,"Kouroussa.tab" using 1:2 title "Kouroussa" with lines,"Siguiri.tab" using 1:2 title "Siguiri" with lines,"Pita.tab" using 1:2 title "Pita" with lines,"Nzerekore.tab" using 1:2 title "Nzerekore" with lines,"Yomou.tab" using 1:2 title "Yomou" with lines,"Dubreka.tab" using 1:2 title "Dubreka" with lines,"Forecariah.tab" using 1:2 title "Forecariah" with lines,"Kerouane.tab" using 1:2 title "Kerouane" with lines,"Coyah.tab" using 1:2 title "Coyah" with lines,"Dalaba.tab" using 1:2 title "Dalaba" with lines,"Beyla.tab" using 1:2 title "Beyla" with lines,"Kindia.tab" using 1:2 title "Kindia" with lines,"Lola.tab" using 1:2 title "Lola" with lines
