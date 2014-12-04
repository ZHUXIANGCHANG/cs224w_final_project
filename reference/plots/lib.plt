set title "Cumulative confirmed cases in Liberia by County"
set key top left
set grid
set xdata time
set timefmt "%Y-%m-%d"
set terminal png size 1000,800
set output "lib.png"
plot "lib_Bomi.tab" using 1:2 title "Bomi" with lines,"lib_Grand_Gedeh.tab" using 1:2 title "Grand Gedeh" with lines,"lib_Grand_Bassa.tab" using 1:2 title "Grand Bassa" with lines,"lib_Margibi.tab" using 1:2 title "Margibi" with lines,"lib_Grand_Kru.tab" using 1:2 title "Grand Kru" with lines,"lib_Montserrado.tab" using 1:2 title "Montserrado" with lines,"lib_Nimba.tab" using 1:2 title "Nimba" with lines,"lib_Gbarpolu.tab" using 1:2 title "Gbarpolu" with lines,"lib_Sinoe.tab" using 1:2 title "Sinoe" with lines,"lib_River_Gee.tab" using 1:2 title "River Gee" with lines,"lib_Grand_Cape_Mount.tab" using 1:2 title "Grand Cape Mount" with lines,"lib_Lofa.tab" using 1:2 title "Lofa" with lines,"lib_Bong.tab" using 1:2 title "Bong" with lines,"lib_RiverCess.tab" using 1:2 title "RiverCess" with lines,"lib_Maryland.tab" using 1:2 title "Maryland" with lines
