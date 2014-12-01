from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.memoize import ram

from uwosh.librarytypes.interfaces.interfaces import IThemeSpecific
from uwosh.librarytypes.util import brain_surgery

from operator import itemgetter
from time import time

class ILibraryStaffFolderView(Interface):
    """ Marker for single column listing view """
class ILibraryStaffFolderColumnView(Interface):
    """ Marker for column listing view """
class ILibraryStaffDirectory(Interface):
    """ Marker for directory view """
    

class LibraryStaffBase(BrowserView):
    """ Base Class """
    implements(IThemeSpecific)


class StaffFolderView(LibraryStaffBase):

    director = None

    def showDisplayOptions(self):
        """ The plony way """
        if ILibraryStaffDirectory.providedBy(self.context):
            return True
        else:
            return False

    def directorySort(self,brains):
        """
        Directory view.
        Get only Library Staff and sort by Lastname.
        """
        results = []
        for brain in brains:
            if brain.portal_type == "LibraryStaff":
                if brain.fetch.getIsTop == True:
                    self.setDirector(brain)
                else:
                    results.append(brain)
                    
        results = self.firstToLast(results)
        results = sorted(results,key=itemgetter('Title'))  
        i = len(results)//2
        if len(results) % 2 == 0:
            return [results[:i],results[i:]]
        return [results[:i+1],results[i+1:]]
    
    def firstToLast(self,brains):
        """
        Rearranges persons name, so last name is first.
        Not the greatest approach, but eh.  Lastname, Firstname is
        only used in one occasion. 
        """
        for brain in brains:
            s = brain.Title.split(' ')
            f = s.pop() + ', '
            for l in s:
                f += l + " "
            brain.Title = f
        return brains
    
    def setDirector(self,brain):
        self.director = brain
    
    def getDirector(self):
        try:
            return self.director
        except Exception:
            return None
    
    def hasDirector(self):
        try:
            foo = self.director.id
            return True
        except Exception:
            return False
    
    
    def getChildernObjects(self):
        """ Standard starting point for recursive helper """
        return self.getChildernObjectsHelper()
    
    def getChildernObjectsHelper(self,context=None):
        """ Recursive function, finds all content below it and orders it by its known
        position in that folder.  Uses only catalog calls to avoid object wakeup, this results
        in more logic code...
        """
        if context == None:
            context = self.context
            
        keys = context.keys() # Folder Children Position
        ordered_children = []
        for key in keys:
            child = self.getChild(key)
            
            try:
                if child.portal_type == "Folder":
                    children = self.getChildernObjectsHelper(context=child.getObject())
                    ordered_children.append(child)
                    ordered_children.extend(children)
                else:
                    ordered_children.append(child)
            except:
                pass # ignore, it means obj is private.
                
        return ordered_children

    def getChild(self,id):
        """
        Finds one item in catalog with this id.
        @param id: object id
        """
        brains = brain_surgery(getToolByName(self.context,'portal_catalog').searchResults(path={'query':self.getStaffPath(),'depth':10},id=id))
        if len(brains) > 0:
            return brains[0]
        return ""
    
    def getStaffPath(self):
        return getToolByName(self.context,'portal_properties').base_paths.getProperty('base_staff_path')
    
    def render(self):
        return self.template()
    
    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()
    
    
    
    