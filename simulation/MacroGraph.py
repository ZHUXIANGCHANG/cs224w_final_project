import json

class MacroGraph:
  def __init__(self, simulationInfo):
    self.simulationInfo = simulationInfo
    # TODO: Instantiate the graph

  def __str__(self):
    return json.dumps(self.simulationInfo, indent=4, separators=(',',' : '))