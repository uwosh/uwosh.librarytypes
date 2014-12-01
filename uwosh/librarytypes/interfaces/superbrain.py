from zope.interface import Interface

class ISuperBrain(Interface):

    def fetch(self,args):
        """
        @param args: list of functions
        
        Example: args = [self.getThis,self.getThat,self.getWhat] 
        
        Note: This is not the function call() but the function variable.
        """
        raise Exception('fetch() Method must be Implemented')
