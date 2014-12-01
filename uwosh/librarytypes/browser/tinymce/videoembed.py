from zope.interface import implements
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

import simplejson
import time
import traceback
import os
import logging
logger = logging.getLogger("Plone")

class VideoEmbed(BrowserView):
    """ 
    TinyMCE toolbar addon.  Adds image upload links.  Controls logic for image
    upload.  
    """
    template = ViewPageTemplateFile('videoembed.pt')
    

    def __call__(self):
        if not self._enforce_security():
            return ""
        
        return self.template()
        
        
    def _enforce_security(self):
        """ Double check, make sure this user has permissions """
        return self.context.portal_membership.checkPermission('Modify portal content', self.context)
    
    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()