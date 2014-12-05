"""
@author Aaron Nagao

Usage: python generateJSON.py
Builds up an array "simulations" and writes it to simulationFile.json
"""

import itertools
import json

sl_countyToPopulation = {'Bo': 463668, 'Tonkolili': 347197, 'Kono': 335401, 'Koinadugu': 265758, 'Kenema': 497948, 'Pujehun': 228392, 'Kailahun': 358190, 'Moyamba': 260910, 'Bombali': 408390, 'Kambia': 270462, 'Bonthe': 129947, 'Port Loko': 453746}
guin_countyToPopulation = {'Dalaba': 136320, 'Lola': 175213, 'Dabola': 182951, 'Kindia': 438315, 'Siguiri': 695449, 'Yomou': 176664, 'Telimele': 283639, 'Coyah': 264164, 'Gueckedou': 291823, 'Beyla': 325482, 'Nzerekore': 396118, 'Kerouane': 211017, 'Dubreka': 328418, 'Macenta': 298282, 'Boffa': 211063, 'Pita': 277059, 'Conakry': 1667864, 'Kouroussa': 268224, 'Forecariah': 244649, 'Kissidougou': 283609}
lib_countyToPopulation = {'Bomi': 84119, 'Bong': 333481, 'Gbarpolu': 83388, 'Grand Bassa': 221693, 'Grand Cape Mount': 127076, 'Grand Gedeh': 125258, 'Grand Kru': 57913, 'Lofa': 276863, 'Margibi': 209923, 'Maryland': 135938, 'Montserrado': 1118241, 'Nimba': 462026, 'River Gee': 66789, 'Rivercess': 71509, 'Sinoe': 102391}

### Range of potential parameter values to try ###
# q = scaling factor, to get macro-level probability of a county infecting its neighbors
sl_q_vals = [2000]
guin_q_vals = [2000]
lib_q_vals = [2000]

# beta = micro-level probability of a person moving from SUSCEPTIBLE to INFECTED
sl_beta_vals = [0.0319] # Rivers: (b_i + b_h + b_f) * alpha
guin_beta_vals = [0.025, 0.03] # should be less than liberia and sl (because Guinea had less-severe outbreak)
lib_beta_vals = [0.05925] # Rivers

# delta = micro-level probability of a person moving from INFECTED to RECOVERED
# much less sure about how to ballpark this parameter
sl_delta_vals = [0.6, 0.7, 0.8, 0.9]
guin_delta_vals = [0.6, 0.7, 0.8, 0.9]
lib_delta_vals = [0.6, 0.7, 0.8, 0.9]

def main():
  simulations = []
  for (sl_q, sl_beta, sl_delta) in itertools.product(sl_q_vals, sl_beta_vals, sl_delta_vals):
    simulation = {
      'countryName': 'Sierra Leone',
      'title': 'sl_q=%.0f,beta=%.4f,delta=%.2f' % (sl_q, sl_beta, sl_delta),
      'q': sl_q,
      'beta': sl_beta,
      'delta': sl_delta,
      'countyGraphType': 'small world',
      # ?? maybe should move population values to macro_graph/sl_labels.csv?
      'countiesToPopulation': sl_countyToPopulation # global var defined above: dict from countryName => population
    }
    simulations.append(simulation)

  for (guin_q, guin_beta, guin_delta) in itertools.product(guin_q_vals, guin_beta_vals, guin_delta_vals):
    simulation = {
      'countryName': 'Guinea',
      'title': 'guin_q=%.0f,beta=%.4f,delta=%.2f' % (guin_q, guin_beta, guin_delta),
      'q': guin_q,
      'beta': guin_beta,
      'delta': guin_delta,
      'countyGraphType': 'small world',
      'countiesToPopulation': guin_countyToPopulation
    }
    simulations.append(simulation)

  for (lib_q, lib_beta, lib_delta) in itertools.product(lib_q_vals, lib_beta_vals, lib_delta_vals):
    simulation = {
      'countryName': 'Liberia',
      'title': 'lib_q=%.0f,beta=%.4f,delta=%.2f' % (lib_q, lib_beta, lib_delta),
      'q': lib_q,
      'beta': lib_beta,
      'delta': lib_delta,
      'countyGraphType': 'small world',
      'countiesToPopulation': lib_countyToPopulation
    }
    simulations.append(simulation)

  with open('simulationFile.json', 'wb') as fp:
    json.dump(simulations, fp)

if __name__ == '__main__':
  main()
