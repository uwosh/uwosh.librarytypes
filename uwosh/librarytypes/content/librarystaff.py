#from zope import schema 
from zope.component import getAdapter
#from zope.app.container.constraints import contains
#from zope.app.container.constraints import containers
from zope.interface import implements, directlyProvides, Interface
from AccessControl import ClassSecurityInfo

#from plone.app.blob.field import ImageField
from Products.ATContentTypes.content import base, folder, schemata
from Products.Archetypes import atapi
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import View

from uwosh.librarytypes import librarytypesMessageFactory as _
from uwosh.librarytypes.config import PROJECTNAME
from uwosh.librarytypes.util import render_tal_expressions
from uwosh.librarytypes.util import catalogSuperBrain
from uwosh.librarytypes.interfaces.superbrain import ISuperBrain

class ILibraryStaff(Interface):
    """ Interface """
    

"""
This is a basic Content type, one field for Class Type Referencing.
"""
LibraryStaffSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((                                                        

    atapi.StringField('department',
        required=True,
        searchable=False,
        default="",
        validators = (),
        widget = atapi.StringWidget(
            description = "The Library Division this staff member works in.  e.g. 'Public Services'",
            label = _(u'Library Division', default=u'Library Division'),
        )
    ),

    atapi.StringField('position',
        required=True,
        searchable=False,
        default="",
        validators = (),
        widget = atapi.StringWidget(
            description = "Staff member title.  e.g. 'History Specialist and Reference Librarian' ",
            label = _(u'Title/Responsibility', default=u'Title/Responsibility'),
        )
    ),          

    atapi.StringField('email',
        required=True,
        searchable=False,
        default="",
        validators = ('isEmail'),
        widget = atapi.StringWidget(
            description = 'The staff members email address',
            label = _(u'Email', default=u'Email'),
        )
    ),                     
                                   
    atapi.StringField('phoneOffice',
        required=False,
        searchable=False,
        default="",
        validators = ('isUSPhoneNumber'),
        widget = atapi.StringWidget(
            description = 'Office Phone Number, please add extension.',
            label = _(u'Office Phone', default=u'Office Phone'),
        )
    ),                                  
                                           
    atapi.StringField('phoneDesk',
        required=False,
        searchable=False,
        default="",
        validators = ('isUSPhoneNumber'),
        widget = atapi.StringWidget(
            description = 'Desk Phone Number, please add extension.',
            label = _(u'Desk Phone', default=u'Desk Phone'),
        )
    ),                                                                         

    atapi.StringField('fax',
        required=False,
        searchable=False,
        default="",
        validators = (),
        widget = atapi.StringWidget(
            description = 'Fax machine number.',
            label = _(u'Fax Number', default=u'Fax Number'),
        )
    ),   

    atapi.StringField('officeRoom',
        required=False,
        searchable=False,
        default="",
        validators = (),
        widget = atapi.StringWidget(
            description = 'Office room number.',
            label = _(u'Office Room Number', default=u'Office Room Number'),
        )
    ),                                                                    

    atapi.TextField('education',
        required=False,
        searchable=False,
        default="",
        validators = (),
        allowable_content_types=('text/html',),
        default_output_type='text/html',
        widget = atapi.RichWidget(
            allow_file_upload=False,
            description = 'Staff member educational information.',
            label = _(u'Education Information', default=u'Education Information'),
        )
    ),
                                                                         
    atapi.TextField('background',
        required=False,
        searchable=False,
        default="",
        validators = (),
        allowable_content_types=('text/html',),
        default_output_type='text/html',
        widget = atapi.RichWidget(
            allow_file_upload=False,
            description = 'Staff member background information.',
            label = _(u'Professional Background Information', default=u'Professional Background Information'),
        )
    ),
          
    atapi.TextField('involvement',
        required=False,
        searchable=False,
        default="",
        validators = (),
        allowable_content_types=('text/html',),
        default_output_type='text/html',
        widget = atapi.RichWidget(
            allow_file_upload=False,
            description = 'Professional involvement within the community or university.',
            label = _(u'University and Community Involvement', default=u'University and Community Involvement'),
        )
    ),


 atapi.TextField('stopmessage',
        required=False,
        searchable=False,
        default="",
        widget = atapi.LabelWidget(
            description = 'Information below is for the Technology Department only.',
            label = _(u'Do not fill out anything below.', default=u'Do not fill out anything below.'),
        )
    ),      
                                             
                                             
    atapi.TextField('chatWidget',
        required=False,
        searchable=False,
        default="",
        validators = (),
        allowable_content_types=('text/html',),
        default_output_type='text/html',
        widget = atapi.TextAreaWidget(
            description = 'Insert Chat Code Snippet to contact this member.  It can be a one-on-one chat or a department chat, ' + 
                          'there are no restrictions.  <br /> \n ' +
                          'Tip:  tal:condition="context/getIsDeptChatWidget"  tal:condition="not: context/getIsDeptChatWidget" <br /> \n ' +
                          'Visible ONLY for Portlet? Add this class "library_staff_port" <br /> \n ' + 
                          'Visible ONLY for Staff Page? Add this class "library_staff_page" '
                          ,
            label = _(u'Ignore this area', default=u'Ignore this area'),
        )
    ),      
                                                                         
                                                                          
    atapi.BooleanField('isDeptChatWidget',
        required=False,
        searchable=False,
        default=True,
        validators = (),
        widget = atapi.BooleanWidget(
            description = 'If the chat widget is for the deparment check this box, if this is a one-on-one chat widget place uncheck.',
            label = _(u'Is this a Department Chat Widget?', default=u'Is this a Department Chat Widget?'),
        )
    ),                                                                

    atapi.BooleanField('isTop',
        required=False,
        searchable=False,
        default=False,
        validators = (),
        widget = atapi.BooleanWidget(
            description = 'This will force this profile to the top of the staff directories.',
            label = _(u'Is this person the Director?', default=u'Is this person the Director?'),
        )
    ),      
                                                                       
    atapi.ImageField('imageReference',
        required=False,
        searchable=False,
        default="",
        validators = (),
        allowable_content_types=('image/gif','image/jpeg','image/png'),
        widget = atapi.ImageWidget(
            description = 'Allowed image types: gif|jpeg|png',
            label = _(u'Image of Staff Member', default=u'Image of Staff Member'),
        )
    ),
                                                                                                                                     
                                                                                                                                        
))

LibraryStaffSchema['title'].storage = atapi.AnnotationStorage()
LibraryStaffSchema['description'].storage = atapi.AnnotationStorage()
LibraryStaffSchema['position'].storage = atapi.AnnotationStorage()
LibraryStaffSchema['department'].storage = atapi.AnnotationStorage()
LibraryStaffSchema['email'].storage = atapi.AnnotationStorage()
LibraryStaffSchema['phoneOffice'].storage = atapi.AnnotationStorage()
LibraryStaffSchema['phoneDesk'].storage = atapi.AnnotationStorage()
LibraryStaffSchema['fax'].storage = atapi.AnnotationStorage()
LibraryStaffSchema['officeRoom'].storage = atapi.AnnotationStorage()
LibraryStaffSchema['education'].storage = atapi.AnnotationStorage()
LibraryStaffSchema['background'].storage = atapi.AnnotationStorage()
LibraryStaffSchema['involvement'].storage = atapi.AnnotationStorage()

LibraryStaffSchema['stopmessage'].storage = atapi.AnnotationStorage()
LibraryStaffSchema['chatWidget'].storage = atapi.AnnotationStorage()
LibraryStaffSchema['isDeptChatWidget'].storage = atapi.AnnotationStorage()
LibraryStaffSchema['isTop'].storage = atapi.AnnotationStorage()
LibraryStaffSchema['imageReference'].storage = atapi.AnnotationStorage()

LibraryStaffSchema['title'].widget.label = "Name of Staff member"
LibraryStaffSchema['title'].widget.description = "Example: John Smith or John M. Smith"
LibraryStaffSchema['description'].required = False


LibraryStaffSchema['description'].widget.visible = {'view': 'hidden', 'edit': 'hidden' }
LibraryStaffSchema['location'].widget.visible = {'view': 'hidden', 'edit': 'hidden' }
LibraryStaffSchema['language'].widget.visible = {'view': 'hidden', 'edit': 'hidden' }
LibraryStaffSchema['creators'].widget.visible = {'view': 'hidden', 'edit': 'hidden' }
LibraryStaffSchema['contributors'].widget.visible = {'view': 'hidden', 'edit': 'hidden' }
LibraryStaffSchema['rights'].widget.visible = {'view': 'hidden', 'edit': 'hidden' }
LibraryStaffSchema['allowDiscussion'].widget.visible = {'view': 'hidden', 'edit': 'hidden' }


schemata.finalizeATCTSchema(LibraryStaffSchema, moveDiscussion=False)

class LibraryStaff(base.ATCTContent):
    
    implements(ILibraryStaff,ISuperBrain)

    meta_type = "LibraryStaff"
    schema = LibraryStaffSchema
    security = ClassSecurityInfo()

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    def fetch(self):
        args =[self.getPosition,self.getEmail,self.getPhoneOffice,self.getPhoneDesk,   
               self.getFax,self.getOfficeRoom,self.hasImage,self.getIsTop,self.getDepartment]
        return catalogSuperBrain(args)
    
    security.declarePublic('hasImage')
    def hasImage(self):
        img = self.getField('imageReference').get(self)
        if not img or img == '':
            return False
        return True
    
    security.declarePublic('getChatWidgetTalEnabled')
    def getChatWidgetTalEnabled(self):
        if self.getChatWidget() == "":
            return ""
        return render_tal_expressions(self,id='__Library_Staff_Chat__',html=self.getChatWidget())
    
atapi.registerType(LibraryStaff, PROJECTNAME)