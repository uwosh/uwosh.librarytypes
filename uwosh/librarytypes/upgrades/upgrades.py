from Products.CMFCore.utils import getToolByName

default_profile = 'profile-uwosh.librarytypes:default'


def upgrade(upgrade_product,version): 
    """ Decorator for updating the QuickInstaller of a upgrade """
    def wrap_func(fn):
        def wrap_func_args(context,*args):
            p = getToolByName(context,'portal_quickinstaller').get(upgrade_product)
            setattr(p,'installedversion',version)
            return fn(context,*args)
        return wrap_func_args
    return wrap_func


@upgrade('uwosh.librarytypes','0.1.0b')
def upgrade_to_0_1_0b(context):
    print "Upgrading"
    
@upgrade('uwosh.librarytypes','0.1.2b')
def upgrade_to_0_1_2b(context):
    print "Upgrading"
    
@upgrade('uwosh.librarytypes','0.1.3b')
def upgrade_to_0_1_3b(context):
    print "Upgrading"
    
@upgrade('uwosh.librarytypes','0.1.4b')
def upgrade_to_0_1_4b(context):
    print "Upgrading"
    
@upgrade('uwosh.librarytypes','0.1.5')
def upgrade_to_0_1_5(context):
    print "Upgrading"
    
    
    
    
    
    
    
    