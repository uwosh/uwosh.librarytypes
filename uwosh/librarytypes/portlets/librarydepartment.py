from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope import schema
from zope.formlib import form

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from uwosh.librarytypes import librarytypesMessageFactory as _
from uwosh.librarytypes.util import render_tal_expressions
from operator import itemgetter


class ILibraryDepartmentPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    #link_category = schema.TextLine(title=_(u"Students Link"),description=_(u"Please provide a xHTML anchor link."), required=True)
    #link_subcategories = schema.Text(title=_(u"Sub-Category Links"),description=_(u"List of xHTML anchor links."), required=False)


    header_title = schema.TextLine(title=_(u"Portlet Header"),description=_(u"Portlet Header"), required=False)
    persons_name = schema.TextLine(title=_(u"Staff Members Name"),description=_(u"Generally used if department portlet points to one staff member as a primary contact"), required=False)
    #persons_staff_link = schema.TextLine(title=_(u"Staff Members Profile URL"),description=_(u"Generally used if department portlet points to one staff member as a primary contact"), required=False)
    
    dept_phone = schema.TextLine(title=_(u"Phone Number"),description=_(u"Phone Number to contact department"), required=False)
    dept_fax = schema.TextLine(title=_(u"Fax Number"),description=_(u"Fax Number for department"), required=False)
    dept_email = schema.TextLine(title=_(u"Email"),description=_(u"Department Email"), required=False)
    dept_chat = schema.Text(title=_(u"Chat Widget"),description=_(u"Place xHTML code for chat widget. Note: TAL and METAL are allowed"), required=False)
    show_chat = schema.Bool(title=u"Display Chat?", required=False, default=True)
    show_only_here = schema.TextLine(title=_(u"Endswith Display Filter"),description=_(u"e.g. 'uwosh.edu/library' will only show on this url"), required=False, default=u'')
    force_to_global_chat = schema.Bool(title=u"Use Ask A Librarian Widget? (Note: Only Endswith Display Filter and Chat Widget are available with this on.)", required=False, default=False)
    
class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ILibraryDepartmentPortlet)

    persons_name = ""
    
    def __init__(self,**kwargs):
        self.header_title = kwargs.get('header_title','Header')
        self.persons_name = kwargs.get('persons_name','')
        self.dept_phone = kwargs.get('dept_phone','')
        self.dept_fax = kwargs.get('dept_fax','')
        self.dept_email = kwargs.get('dept_email','')
        self.dept_chat = kwargs.get('dept_chat','')
        self.show_chat = kwargs.get('show_chat',False)
        self.show_only_here = kwargs.get('show_only_here','')
        self.force_to_global_chat = kwargs.get('force_to_global_chat',False)
        
    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u"Department Contact Portlet")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('librarydepartment.pt')
    
    def update(self):
        pass
    
    def _is_restrict_view(self):
        if self.data.show_only_here != None:
            return not self._is_restriction_met()
        return False
    
    def _is_restriction_met(self):
        if self.data.show_only_here != None:
            current = self.context.absolute_url()
            pattern = self.data.show_only_here.strip()
            if len(pattern) > 2:
                if current.endswith(pattern):
                    return True
        return False
    
    def is_ask_a_dept_widget(self):
        return (not self.data.force_to_global_chat and not self._is_restrict_view())
    
    def is_ask_a_librarian_widget(self):
        return (self.data.force_to_global_chat and not self._is_restrict_view())
            
    def show_name(self):
        return self._check(self.data.persons_name)
    
    def show_phone(self):
        return self._check(self.data.dept_phone)
    
    def show_fax(self):
        return self._check(self.data.dept_fax)

    def show_email(self):
        return self._check(self.data.dept_email)

    def _check(self,string):
        if string == None:
            return False
        elif string.strip() == '':
            return False
        return True
        
    def getChatWidget(self):
        """ returns None if empty """
        return render_tal_expressions(self,id='__Library_Staff_Portlet__',html=self.data.dept_chat)
    
    def safeTextLength(self,text):
        if len(text) > 22:
            return False
        return True


    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def portalAbsolute(self):
        return self.portal().absolute_url()
    
    
    
    
#    @property
#    def render(self):
#         return ViewPageTemplateFile('libraryUserCustomizationPortlet.pt')
#    
#    def render(self):
#        return ViewPageTemplateFile('libraryUserCustomizationPortlet.pt')

# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ILibraryDepartmentPortlet)

    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment


# NOTE: IF this portlet does not have any configurable parameters, you can
# remove this class definition and delete the editview attribute from the
# <plone:portlet /> registration in configure.zcml

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(ILibraryDepartmentPortlet)
