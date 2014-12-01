/**
 * Simple Video Embed
 * @author David Hieptas
 */


(function() {
    tinymce.create('tinymce.plugins.VideoEmbedPlugin', {
        init : function(ed, url) {
            // Register commands
		
			baseUrl = function() {
				id = ['portal_factory','edit','base_edit','atct_edit'];
				for (i in id) 
					if (window.location.href.indexOf("/" + id[i]) > 0) 
						return window.location.href.split(id[i])[0];
				return window.location.href + '/';
			}
		
            ed.addCommand('mceVideoEmbed', function() {
                
                ed.windowManager.open({
                    file : baseUrl() + 'videoEmbed',
                    width : 700 + parseInt(ed.getLang('VideoEmbed.delta_width', 0)),
                    height : 375 + parseInt(ed.getLang('VideoEmbed.delta_height', 0)),
                    inline : 1
                }, {
                    plugin_url : url, // Plugin absolute URL
					some_custom_arg : 'custom arg' // Custom argument
                });
            });

            // Register buttons
            ed.addButton('VideoEmbed', {
                title : 'Video Embed',
                cmd : 'mceVideoEmbed',
                image : baseUrl() + '++resource++uwosh.librarytypes.images/embed.png'
            });
            
            // Add a node change handler, selects the button in the UI when a image is selected
			ed.onNodeChange.add(function(ed, cm, n) {
				cm.setActive('VideoEmbed', n.nodeName == 'IMG');
			});
			
			// Change the context menu (note: this took a long time to figure out)
			ed.onInit.add(function(ed, e) {
				try{
					ed.plugins.contextmenu.onContextMenu.add(function(ed, e, n) {
						if ( (n.nodeName == 'OBJECT') || (n.nodeName == 'IFRAME') ||
						   (n.nodeName == 'IMG' && n.className.indexOf('mceItemFlash') != -1 )) {
							e.removeAll();
							e.add({
								title: 'Edit Embed Video',
								icon: 'media',
								cmd: 'mceVideoEmbed'
							});
						}
					});
					
				}
				catch(e) { console.log(e); }
			});
			
        },
		
         /**
		 * Creates control instances based in the incomming name. This method is normally not
		 * needed since the addButton method of the tinymce.Editor class is a more easy way of adding buttons
		 * but you sometimes need to create more complex controls like listboxes, split buttons etc then this
		 * method can be used to create those.
		 *
		 * @param {String} n Name of the control to create.
		 * @param {tinymce.ControlManager} cm Control manager to use inorder to create new control.
		 * @return {tinymce.ui.Control} New control instance or null if no control was created.
		 */
		 
		 createControl : function(n, cm) {
			return null;
		},
		
		/**
		 * Returns information about the plugin as a name/value array.
		 * The current keys are longname, author, authorurl, infourl and version.
		 *
		 * @return {Object} Name/value array containing information about the plugin.
		 */

        getInfo : function() {
            return {
                longname : 'Video Embed Button, embeds videos into MCE editor window',
                author : 'David Hietpas',
                authorurl : 'http://www.uwosh.edu/library',
                infourl : 'http://plone.org/products/tinymce',
                version : "0.0.1"
            };
        }
    });

    // Register plugin
    tinymce.PluginManager.add('VideoEmbed', tinymce.plugins.VideoEmbedPlugin);
})();


