class MicroGraph:
  """
  TODO: DEFINE THE INTERFACE
  TODO: Have each method raise an error in here - they must be implemented by subclasses
  TODO: This class should never be instantiated
  """

  NOT_IMPLEMENTED_MESSAGE = 'Each subclass must implement this!'

  def getType(self):
    raise NotImplementedError(self.NOT_IMPLEMENTED_MESSAGE)