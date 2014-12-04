class MicroGraph:
  '''
  Base class for all the county-level graph representations.
  This class should never be instantiated.
  '''

  NOT_IMPLEMENTED_MESSAGE = 'Each subclass must implement this!'

  '''
  The infect method is called when an infection has spread from another county
  to this county. This county must then infect a node according to the protocol.
  '''
  def infect(self):
    raise NotImplementedError(self.NOT_IMPLEMENTED_MESSAGE)

  '''
  Returns the number of currently infected nodes in this county.
  '''
  def getNumInfected(self):
    raise NotImplementedError(self.NOT_IMPLEMENTED_MESSAGE)

  '''
  Advance the infection cascades by one timestep.
  '''
  def advanceDay(self):
    raise NotImplementedError(self.NOT_IMPLEMENTED_MESSAGE)

  def getType(self):
    raise NotImplementedError(self.NOT_IMPLEMENTED_MESSAGE)