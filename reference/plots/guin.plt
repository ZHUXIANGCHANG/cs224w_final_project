set title "Cumulative confirmed cases in Guinea by County"
set key top left
set grid
set xdata time
set timefmt "%Y-%m-%d"
set terminal png size 1000,800
set output "guin.png"
plot "guin_Coyah.tab" using 1:2 title "Coyah" with lines,"guin_Lola.tab" using 1:2 title "Lola" with lines,"guin_Dabola.tab" using 1:2 title "Dabola" with lines,"guin_Kerouane.tab" using 1:2 title "Kerouane" with lines,"guin_Dinguiraye.tab" using 1:2 title "Dinguiraye" with lines,"guin_Dalaba.tab" using 1:2 title "Dalaba" with lines,"guin_Gueckedou.tab" using 1:2 title "Gueckedou" with lines,"guin_Kouroussa.tab" using 1:2 title "Kouroussa" with lines,"guin_Beyla.tab" using 1:2 title "Beyla" with lines,"guin_Nzerekore.tab" using 1:2 title "Nzerekore" with lines,"guin_Siguiri.tab" using 1:2 title "Siguiri" with lines,"guin_Conakry.tab" using 1:2 title "Conakry" with lines,"guin_Dubreka.tab" using 1:2 title "Dubreka" with lines,"guin_Macenta.tab" using 1:2 title "Macenta" with lines,"guin_Boffa.tab" using 1:2 title "Boffa" with lines,"guin_Pita.tab" using 1:2 title "Pita" with lines,"guin_Yomou.tab" using 1:2 title "Yomou" with lines,"guin_Telimele.tab" using 1:2 title "Telimele" with lines,"guin_Forecariah.tab" using 1:2 title "Forecariah" with lines,"guin_Kindia.tab" using 1:2 title "Kindia" with lines,"guin_Kissidougou.tab" using 1:2 title "Kissidougou" with lines
