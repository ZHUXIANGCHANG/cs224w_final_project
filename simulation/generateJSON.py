"""
@author Aaron Nagao

Usage: python generateJSON.py
Builds up an array "simulations" and writes it to simulationFile.json
"""

import itertools
import json

sl_countyToPopulation = {'Bo': 463668, 'Tonkolili': 347197, 'Kono': 335401, 'Koinadugu': 265758, 'Kenema': 497948, 'Pujehun': 228392, 'Kailahun': 358190, 'Moyamba': 260910, 'Bombali': 408390, 'Kambia': 270462, 'Bonthe': 129947, 'Port Loko': 453746}
guin_countyToPopulation = {'Dalaba': 136320, 'Lola': 175213, 'Dabola': 182951, 'Kindia': 438315, 'Siguiri': 695449, 'Yomou': 176664, 'Telimele': 283639, 'Coyah': 264164, 'Gueckedou': 291823, 'Beyla': 325482, 'Nzerekore': 396118, 'Kerouane': 211017, 'Dubreka': 328418, 'Macenta': 298282, 'Boffa': 211063, 'Pita': 277059, 'Conakry': 1667864, 'Kouroussa': 268224, 'Forecariah': 244649, 'Kissidougou': 283609}
lib_countyToPopulation = {'Bomi': 84119, 'Bong': 333481, 'Gbarpolu': 83388, 'Grand Bassa': 221693, 'Grand Cape Mount': 127076, 'Grand Gedeh': 125258, 'Grand Kru': 57913, 'Lofa': 276863, 'Margibi': 209923, 'Maryland': 135938, 'Montserrado': 1118241, 'Nimba': 462026, 'River Gee': 66789, 'RiverCess': 71509, 'Sinoe': 102391}

### Range of potential parameter values to try ###
# small-world rewire probability (smaller probability = closer to ring, increased diameter)
rewire_vals = [0.01, 0.003, 0.001] # 10/1000, 3/1000, 1/1000

# q = scaling factor, to get macro-level probability of a county infecting its neighbors
# Guinea: 200 real infections / 200K people = 1/1000, x q = probability of infecting neighbor
# but in our simulation, usually 2K infections / 200K people = 1/100 * q
sl_q_vals = [20, 55, 150, 400] # roughly powers of e
guin_q_vals = [20, 55, 150, 400]
lib_q_vals = [20, 55, 150, 400]

# beta = micro-level probability of a person moving from SUSCEPTIBLE to INFECTED
# daily risk for onward transmission ranges from 0.02-0.3: http://www.cdc.gov/mmwr/preview/mmwrhtml/su6303a1.htm#Appendix-tab1
sl_beta_vals = [0.02, 0.0319, 0.04] # Rivers: (b_i + b_h + b_f) * alpha = 0.0319
guin_beta_vals = [0.02, 0.03, 0.04] # should be less than liberia and sl (because Guinea had less-severe outbreak)
lib_beta_vals = [0.02, 0.04, 0.05925] # Rivers = 0.05925

# delta = micro-level probability of a person moving from INFECTED to RECOVERED
# much less sure about how to ballpark this parameter.
# Note: case fatality rate is around 0.74 guin, 0.48 sl, 0.71 lib (http://currents.plos.org/outbreaks/article/estimating-the-reproduction-number-of-zaire-ebolavirus-ebov-during-the-2014-outbreak-in-west-africa/)
sl_delta_vals = [0.75]
guin_delta_vals = [0.75]
lib_delta_vals = [0.75]

def main():
  simulations = []
  for (sl_q, sl_beta, sl_delta, rewireProb) in itertools.product(sl_q_vals, sl_beta_vals, sl_delta_vals, rewire_vals):
    simulation = {
      'countryName': 'Sierra Leone',
      'title': 'sl_q=%.0f,beta=%.4f,delta=%.2f,rewire=%.3f' % (sl_q, sl_beta, sl_delta, rewireProb),
      'q': sl_q,
      'beta': sl_beta,
      'delta': sl_delta,
      'countyGraphType': 'small world',
      'rewireProb': rewireProb,
      # ?? maybe should move population values to macro_graph/sl_labels.csv?
      'countiesToPopulation': sl_countyToPopulation # global var defined above: dict from countryName => population
    }
    simulations.append(simulation)

  for (guin_q, guin_beta, guin_delta, rewireProb) in itertools.product(guin_q_vals, guin_beta_vals, guin_delta_vals, rewire_vals):
    simulation = {
      'countryName': 'Guinea',
      'title': 'guin_q=%.0f,beta=%.4f,delta=%.2f,rewire=%.3f' % (guin_q, guin_beta, guin_delta, rewireProb),
      'q': guin_q,
      'beta': guin_beta,
      'delta': guin_delta,
      'countyGraphType': 'small world',
      'rewireProb': rewireProb,
      'countiesToPopulation': guin_countyToPopulation
    }
    simulations.append(simulation)

  for (lib_q, lib_beta, lib_delta, rewireProb) in itertools.product(lib_q_vals, lib_beta_vals, lib_delta_vals, rewire_vals):
    simulation = {
      'countryName': 'Liberia',
      'title': 'lib_q=%.0f,beta=%.4f,delta=%.2f,rewire=%.3f' % (lib_q, lib_beta, lib_delta, rewireProb),
      'q': lib_q,
      'beta': lib_beta,
      'delta': lib_delta,
      'countyGraphType': 'small world',
      'rewireProb': rewireProb,
      'countiesToPopulation': lib_countyToPopulation
    }
    simulations.append(simulation)

  with open('simulationFile.json', 'wb') as fp:
    json.dump(simulations, fp)

if __name__ == '__main__':
  main()
