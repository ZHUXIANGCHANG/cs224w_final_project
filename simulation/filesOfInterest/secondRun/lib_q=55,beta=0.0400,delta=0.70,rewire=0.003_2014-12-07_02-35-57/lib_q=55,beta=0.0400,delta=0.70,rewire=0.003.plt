set title "lib_q=55,beta=0.0400,delta=0.70,rewire=0.003"
set key top left
set grid
set xdata time
set timefmt "%Y-%m-%d"
set terminal png size 1000,800
set output "lib_q=55,beta=0.0400,delta=0.70,rewire=0.003.png"
plot "Bomi.tab" using 1:2 title "Bomi" with lines,"Bong.tab" using 1:2 title "Bong" with lines,"Gbarpolu.tab" using 1:2 title "Gbarpolu" with lines,"Grand_Bassa.tab" using 1:2 title "Grand Bassa" with lines,"Grand_Cape_Mount.tab" using 1:2 title "Grand Cape Mount" with lines,"Grand_Gedeh.tab" using 1:2 title "Grand Gedeh" with lines,"Grand_Kru.tab" using 1:2 title "Grand Kru" with lines,"Lofa.tab" using 1:2 title "Lofa" with lines,"Margibi.tab" using 1:2 title "Margibi" with lines,"Maryland.tab" using 1:2 title "Maryland" with lines,"Montserrado.tab" using 1:2 title "Montserrado" with lines,"Nimba.tab" using 1:2 title "Nimba" with lines,"River_Gee.tab" using 1:2 title "River Gee" with lines,"RiverCess.tab" using 1:2 title "RiverCess" with lines,"Sinoe.tab" using 1:2 title "Sinoe" with lines
