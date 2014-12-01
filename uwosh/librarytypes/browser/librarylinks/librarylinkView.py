from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from uwosh.librarytypes.interfaces.interfaces import IThemeSpecific


class LibraryLinkView(BrowserView):
    implements(IThemeSpecific)
    template = ViewPageTemplateFile('librarylink_view.pt')

    def __call__(self):
        properties = getToolByName(self.context, 'portal_properties')
        membership = getToolByName(self.context, 'portal_membership')
        redirect_links = properties.site_properties.getProperty('redirect_links', False)
        can_edit = membership.checkPermission('Modify portal content', self.context)
        
        if redirect_links and not can_edit and not self.context.hasVideoEmbed():
            return self.request.RESPONSE.redirect(self.context.proxyWrapper() + self.context.getRemoteUrl())
        else:
            return self.template()        
    
    def render(self):
        return self.template()
    
    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()
