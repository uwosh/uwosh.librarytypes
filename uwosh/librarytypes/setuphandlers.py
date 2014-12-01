from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Acquisition import aq_parent,aq_inner
from xml.dom import minidom
from DateTime import DateTime
import os.path

# Custom Installer, setups up GroupFinder Contents
def install_setup(context):

    # ONLY INSTALL FOR THIS PRODUCT (This "If" statement is needed)
    if context.readDataFile('uwosh.librarytypes_various.txt') is None:
        return

    portal = context.getSite()
    
    migrateScript(portal,context)
    

def migrateScript(portal,context):

    brains = getToolByName(portal, 'portal_catalog').searchResults(portal_type='LibraryLinks')
    if len(brains) != 0:
        print "MIGRATION SCRIPT"
        print "Start: TOTAL uwosh.librarylinks objects:"  + str(len(brains))
        
        for brain in brains:
            try:
                old = brain.getObject()
                old_id = old.getId()
                tmpId = old_id + "-200"
                old.setId(tmpId)
                
                parent = old.aq_inner.aq_parent
                
                new  = create(parent,type='LibraryLink',id=old_id,title=old.Title(),description=old.Description())
                
                new.setProxyRequired( old.getProxyRequired() )
                new.setRemoteUrl( old.getRemoteUrl() )
                try:
                    new.content_status_modify(workflow_action=brain.review_state)
                except Exception as ex:
                    print "WARNING: Could not change review state " + str(old_id)
                
                parent.manage_delObjects([tmpId])
                print "SUCCESS Migrated: " + str(old_id)
                parent.reindexObject()
            except Exception as e:
                print "FAILURE: " + str(e)
        
        brains = getToolByName(portal, 'portal_catalog').searchResults(portal_type='LibraryLinks')
        print "End: TOTAL uwosh.librarylinks objects:"  + str(len(brains))
        
        brains = getToolByName(portal, 'portal_catalog').searchResults(portal_type='LibraryLink')
        print "End: TOTAL uwosh.librarytype link objects:"  + str(len(brains))
    
    
def create(portal,type=None,id=None,title=None,description=None):
        _createObjectByType(type, portal, id=id, title=title,
                            description=description)
        obj = portal.get(id, None)
        obj.reindexObject()
        return obj
          