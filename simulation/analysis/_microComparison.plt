counties = "Bo Bombali Bonthe Kailahun Kambia Kenema Koinadugu Kono Moyamba Port_Loko Pujehun Tonkolili"

do for [county in counties] {

    set title county.', Sierra Leone: Actual vs. Simulation'
    set key top left
    set grid
    set xdata time
    set timefmt "%Y-%m-%d"
    set terminal png size 1000,800
    set output county.'_microComparison.png'

    set ytics autofreq tc lt 1
    set ylabel 'Number of cases'
    set y2tics autofreq tc lt 2

    plot '../../reference/plots/sl_'.county.'.tab' using 1:2 title "Actual" with lines linetype 1, '../filesOfInterest/secondRun/sl_q=400,beta=0.0200,delta=0.70,rewire=0.010_2014-12-07_02-09-32/'.county.'.tab' using 1:2 title "Simulated" with lines linetype 2 axes x1y2

}