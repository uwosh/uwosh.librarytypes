#from zope import schema
from zope.interface import Interface
#from zope.app.container.constraints import contains
#from zope.app.container.constraints import containers

from zope.interface import implements, directlyProvides
from Products.Archetypes import atapi
from Products.ATContentTypes.content import link, base, schemata

from Products.Archetypes.atapi import TextField,StringField,TextAreaWidget,ImageField,ImageWidget,SelectionWidget

from uwosh.librarytypes.config import PROJECTNAME
from uwosh.librarytypes import librarytypesMessageFactory as _

from Products.CMFCore.utils import getToolByName

class ILibraryLink(Interface):
    """a form to request a query"""


# Keep as StringField/StringWidget, do not use TextArea, Textarea purges HTML code.
# Embbeded video's will have html purged during display if TextArea.
LibraryLinkSchema = link.ATLink.schema.copy() + atapi.Schema(( 
    TextField('videoEmbed',
        required=False,
        searchable=True,
        default = "",
        validators = (),
        widget = TextAreaWidget(
            description = 'Add a video from Youtube or other Video Sites. Use &lt;embed&gt;, &lt;iframe&gt; or &lt;video&gt tags for videos.',
            label = _(u'Video Addition', default=u'Video Addition'),
            )),
            
    StringField('proxyRequired',
        required=True,
        searchable=False,
        default="0",
        validators = (),
        vocabulary=[("0","No"),("1","Yes")],
        widget = SelectionWidget(
            format='select',
            description = 'Does this link need to go through a proxy server?',
            label = _(u'Proxy Connection?', default=u'Proxy Connection?'),
            )),
            
    ImageField('imageReference',
        required=False,
        searchable=False,
        default = "",
        validators = (),
        widget = ImageWidget(
            size=100,
            description = 'Image associated with Link.',
            label = _(u'Upload Image', default=u'Upload Image'),
            )),
))

LibraryLinkSchema['title'].storage = atapi.AnnotationStorage()
LibraryLinkSchema['description'].storage = atapi.AnnotationStorage()

LibraryLinkSchema['title'].widget.label = "Library Advanced Links"
LibraryLinkSchema['description'].widget.description = "Give a description of the Link."
LibraryLinkSchema['description'].required = False

LibraryLinkSchema['videoEmbed'].storage = atapi.AnnotationStorage()
LibraryLinkSchema['proxyRequired'].storage = atapi.AnnotationStorage()
LibraryLinkSchema['imageReference'].storage = atapi.AnnotationStorage()


#HIDE THESE
LibraryLinkSchema['location'].widget.visible = {'view': 'hidden', 'edit': 'hidden' }
LibraryLinkSchema['language'].widget.visible = {'view': 'hidden', 'edit': 'hidden' }
LibraryLinkSchema['creators'].widget.visible = {'view': 'hidden', 'edit': 'hidden' }
LibraryLinkSchema['contributors'].widget.visible = {'view': 'hidden', 'edit': 'hidden' }
LibraryLinkSchema['rights'].widget.visible = {'view': 'hidden', 'edit': 'hidden' }
LibraryLinkSchema['allowDiscussion'].widget.visible = {'view': 'hidden', 'edit': 'hidden' }



schemata.finalizeATCTSchema(LibraryLinkSchema, moveDiscussion=False)
LibraryLinkSchema.changeSchemataForField('relatedItems', 'default')


class LibraryLink(base.ATCTContent, link.ATLink):
    """Project Request Form"""
    implements(ILibraryLink)

    meta_type = "LibraryLink"
    schema = LibraryLinkSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    def getVideoEmbed(self):
        value = self.getField('videoEmbed').get(self)
        if value == None:
            return ""
        return value


    def hasVideoEmbed(self):
        value = self.getVideoEmbed()
        if value != None:
            if len(value) > 3:
                return True
        return False

    # Returns Proxy URL if set or empty string for not.
    def proxyWrapper(self):
        value = self.getField('proxyRequired').get(self)
        if int(value) > 0:
            props = getToolByName(self, 'portal_properties')
            return props.external_resources.getProperty('proxy_server_url')
        return ""
    
    
    def getImageReference(self):
        value = self.getField('imageReference').get(self)
        if value == None:
            return ""
        return value
    
    def hasImageReference(self):
        value = self.getField('imageReference').get(self)
        if value != None:
            if len(value) > 0:
                return True
        return False
    
    # Simple Catalog Record
    def libraryLinkReferences(self):
        catalog = []
        if self.hasVideoEmbed():
            catalog.append("has_video")
        if self.hasImageReference():
            catalog.append("has_image")
        return tuple(catalog)
    
    
atapi.registerType(LibraryLink, PROJECTNAME)
