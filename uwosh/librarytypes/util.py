from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate
from Acquisition import aq_base

def render_tal_expressions(context,id='default',html=None,content_type='text/html'):
    """
    @attention: Context must be in a public state for this to render!  Even if the
                user has permission to view, it will not allow them. 
    
    @param context: object context
    @param id: string name of this html snippet, doesn't really matter
    @param html: html with TAL
    @param content_type: type of content, 'text/plain'|'text/html'|etc...  
    """
    pt = ZopePageTemplate(id=id,text=html,content_type=content_type)
    pt = aq_base(pt).__of__(context) # set context of template
    return pt()
    
def catalogSuperBrain(args):
    """ Experimental """
    items = []
    for func in args:
        items.append(tuple([func.__name__,func()]))
    t = tuple(items)
    if len(str(t)) > 300:
        print "Warning: Superbrain is larger than 300 characters. Size is " + str(len(str(t))) + " characters."
    return t

def brain_surgery(brains):
    """ Experimental """
    i = 0
    try:
        for brain in brains:
            try:
                sb = SuperBrain()
                for f in brain.fetch:
                    sb.set(f[0],f[1])
                brains[i].fetch = sb
            except Exception as e:
                 pass # ignore brains without brain.fetch column
            i += 1
    except Exception as e:
        print "Error in brain_surgery: " + str(e)
    return brains


class SuperBrain(object):
    """ Experimental """
    def set(self,name,value):
        setattr(self,name,value)
        
    def get(self,name):
        return getattr(self,name)