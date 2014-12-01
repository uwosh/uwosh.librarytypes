from zope.interface import implements
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from uwosh.librarytypes.interfaces.interfaces import IThemeSpecific

import logging
logger = logging.getLogger("Plone")

class CatalogLink(BrowserView):
    """ 
    TinyMCE toolbar addon.  Adds voyager bibid links.  Also controls the 
    redirection logic.
    """
    implements(IThemeSpecific)
    template = ViewPageTemplateFile('cataloglink.pt')

    def __call__(self):
        server_info = self.request.form.get('query','').strip().lower()
        creation = self.request.form.get('create','').strip().lower()
        bibid = self.request.form.get('bibid','').strip()
        # -- add any other parameters here, filter by query (server_info) type --
        
        if server_info == 'voyager':
            self.catalog_redirection(bibid,self.handleVoyagerRedirection)
        elif creation == 'new':
            return self.template()
        else:
            logger.warning("Attempt to access /getItem? with wrong parameters")
            return 'Sorry, attempted to access /getItem? with wrong parameters, please contact site administration.'
        
    def catalog_redirection(self,id,func):
        try:
            foo = int(id)
            if id == '':
                raise
        except Exception as e:
            logger.error(str(e))
            return "Must have bibid and bibid must be a integer."
        func(id)
        
    def handleVoyagerRedirection(self,bibid):
        url = getToolByName(self.context,'portal_properties').external_resources.getProperty('voyager_holdings_info')
        url += '?bibId=' + bibid
        self.request.response.redirect(url)
        
    def getBaseURL(self):
        return getToolByName(self.context, 'portal_url').getPortalObject().absolute_url()
