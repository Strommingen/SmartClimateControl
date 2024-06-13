from machine import Pin

class Window:
    _isOpen: bool
    _togglePin: Pin
    
    def __init__(self, togglePin) -> None:
        self._togglePin = togglePin
        
# return true if humidity inside is below 40% and is more outside
# or if humidity inside is above 50% and is less inside
    def humidShouldOpen(self,humOut, humIn) -> bool:
        if (humOut > humIn) and (humIn < 0.4):
            return True
        elif (humOut < humIn) and (humIn > 0.5):
            return True
        else:
            return False
#https://lauryheating.com/ideal-home-humidity/
    
# return true if temperature inside is higher than outside and temp outside
# is not below 14 C
    def tempShouldOpen(self, tempOut, tempIn) -> bool:
        if (tempIn > tempOut) and (tempOut >= 15):
            return True
        else:
            return False
        
    def IsOpen(self) -> bool:
        if self._togglePin.value() == True:
            _isopen = True
            return _isopen
        else:
            _isopen = False
            return _isopen
        