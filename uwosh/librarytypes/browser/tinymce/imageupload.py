from zope.interface import implements
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

from uwosh.librarytypes.interfaces.interfaces import IThemeSpecific

import simplejson
import time
import traceback
import os
import logging
logger = logging.getLogger("Plone")

class ImageUpload(BrowserView):
    """ 
    TinyMCE toolbar addon.  Adds image upload links.  Controls logic for image
    upload.  
    """
    implements(IThemeSpecific)
    template = ViewPageTemplateFile('imageupload.pt')
    
    STATUS_NORMAL = 0
    STATUS_CREATED = 1
    STATUS_FAIL = 2
    STATUS_MORE = 3

    def __call__(self):

        
        if not self._enforce_security():
            return ""
        
        self.last_upload_url = ''
        self.last_upload_name = 'Sorry, no image description'
        self.request['upload_status'] = self.STATUS_NORMAL
        self._new_upload = self.request.form.get('upload','default')
        self._file = self.request.form.get('iufile','')
        self._basic_info = self.request.form.get('check_conflict','')
        self._reuseable = self.request.form.get('multipleusage','')
        self.search = self.request.form.get('search','false')
        
        
        
        if self._new_upload  == 'default':
            return self.template()
        elif self._new_upload  == 'quickcheck':
            return self._quick_check()
        elif self._new_upload  == 'new':
            self._upload_image()
            self.request['upload_status'] = self.STATUS_CREATED
            return self.template()
            
    
    def get_all_images(self,location=''):
        """ Not used, might be in future... """
        results = []
        if location == 'misc':
            path = self.getImageDirectory().virtual_url_path()
        else:
            path = self.getMiscImageDirectory().virtual_url_path()
        return self._get_images_info_on_path(path)
    
    
    def _get_images_info_on_path(self,path):
        """ Not used, might be in future... """
        results = []
        brains = getToolByName(self.context,'portal_catalog').searchResults(portal_type='Image',path={'query':path,'depth':2})
        for brain in brains:
            results.append(brain)
        return results
            
    def _upload_image(self):
        if self._check_file_restrictions():
            obj = self.ifactory()
            
            # allow for resolveuid/
            if self._check_resolveuid_enabled():
                self.last_upload_url = 'resolveuid/' + obj.UID()
                self.last_upload_name = obj.Title()
            else:
                self.last_upload_url = self.getRelativeLinkToImgDir(obj)
                self.last_upload_name = obj.Title()
            
            if obj != None:
                obj.setImage(self._file.read())
                obj.reindexObject()
            else:
                self.request['upload_status'] = self.STATUS_FAIL
                
    def _check_resolveuid_enabled(self):
        return getToolByName(self.context,'portal_tinymce').link_using_uids
                
            
    def ifactory(self):
        """ Determines which factory to call """
        if self._reuseable != '':
            return self._factory()
        else:
            return self._misc_factory()
    
    def _factory(self):
        """ 
        Creates Image places it in the main directory, 
        if directory isn't there it will make it
        """
        id = self._file.filename
        title = self._file.filename
        try:
            return getattr(self.getImageDirectory(),id)
        except Exception:
            pass # already exists, get it
        try:
            id = self.getImageDirectory().invokeFactory(id=id, title=title, type_name='Image')
            return getattr(self.getImageDirectory(),id)
        except Exception:
            return None
        
    def _misc_factory(self):
        """ 
        Creates Image places it in the misc directory, 
        if directory isn't there it will make it
        """
        id = self._file.filename
        title = self._file.filename
        try:
            return getattr(self.getMiscImageDirectory(),id)
        except Exception:
            pass # already exists, get it
        try:
            id = self.getMiscImageDirectory().invokeFactory(id=id, title=title, type_name='Image')
            return getattr(self.getMiscImageDirectory(),id)
        except Exception:
            return None
        
        
    def _quick_check(self):
        """ Checks if image already exists """
        checkid = os.path.basename(self._basic_info)
        brains = getToolByName(self.context,'portal_catalog').searchResults(id=checkid, portal_type='Image',limit=1)
        number = len(brains)
        response = {'url':'None','name':'None'}
        if number > 0:
            if self._check_resolveuid_enabled():
                obj = brains[0].getObject()
                response['url'] = 'resolveuid/' + obj.UID()
                response['name'] = brains[0].Title
            else:
                response['url'] = brains[0].getURL()
                response['name'] = brains[0].Title
        self.request.response.setHeader('Content-Type', 'application/json')
        return simplejson.dumps(response)
        
    def _enforce_security(self):
        """ Double check, make sure this user has permissions """
        return self.context.portal_membership.checkPermission('Modify portal content', self.context)
    
    def _check_file_restrictions(self):
        """ Double check, make sure this image is safe """
        mime = ['image/png','image/jpg','image/jpeg','image/gif']
        if self._file.headers['Content-Type'] in mime:
            return True
        else:
            self.request['upload_status'] = self.STATUS_FAIL
            return False
            


    def getRelativeLinkToImgDir(self,image):
        """ Determines Relative Path from Image to Image Directory """
        image_url = image.absolute_url().split(self.portal().getId() + '/').pop()
        allowed_types = ['Folder','Plone Site']
        depth = ""
        
        obj = self.context
        if self.context.Type() not in allowed_types:
            obj = self.context.aq_parent
        
        for i in range(0,500):
            """ representing infinite loop, at least this ends """
            if obj.Type() == 'Plone Site': break
            depth += "../"
            obj = obj.aq_parent
        
        return depth + image_url

    
    def getImageDirectory(self):
        """ Gets Image Directory based off of properties """
        try:
            name = self._get_image_directory_name()
            return getattr(self.portal(),name.lower())
        except:
            name = self._get_image_directory_name()
            self._make_img_dir(self.portal(),name,name)
            return getattr(self.portal(),name.lower())
    
    def getMiscImageDirectory(self):
        """ Gets Image Directory based off of properties """
        imagesFolder = self.getImageDirectory()
        try:
            name = self._get_image_misc_directory_name()
            return getattr(imagesFolder,name.lower())
        except:
            name = self._get_image_misc_directory_name()
            self._make_img_dir(imagesFolder,name,name)
            return getattr(imagesFolder,name.lower())
        
    def _get_image_directory_name(self):
        return getToolByName(self.context,'portal_properties').site_properties.getProperty('image_directory_name')

    def _get_image_misc_directory_name(self):
        return getToolByName(self.context,'portal_properties').site_properties.getProperty('image_misc_directory_name')

    def _make_img_dir(self,context,id,title):
        _createObjectByType("Folder", context, id=id.lower(), title=title)
        obj = getattr(context,id)
        obj.reindexObject()

    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()
    
    def getImageDirectoryUrl(self):
        return self.getImageDirectory().absolute_url()
    
    def getImageMiscDirectoryUrl(self):
        return self.getMiscImageDirectory().absolute_url()
    
    def getBaseURL(self):
        return getToolByName(self.context, 'portal_url').getPortalObject().absolute_url()
