//tinyMCEPopup.requireLangPack();

var ImageUploadDialog = {
	init : function() {
		//document.forms[0].btitle.value = tinyMCEPopup.editor.selection.getContent({format : 'text'}) ;
	},
	
	insert : function() {
		var img = document.forms[0].imageUrl.value;
		var imgname = document.forms[0].imageName.value;
		var html_to_insert = '<img src="' + img + '" alt="' + imgname + '" />';
		tinyMCEPopup.editor.execCommand('mceInsertContent', false, html_to_insert);
		tinyMCEPopup.close();
	},
	
	insertImage : function(img,alt) {
		var html_to_insert = '<img src="' + img + '" alt="' + alt + '" />';
		tinyMCEPopup.editor.execCommand('mceInsertContent', false, html_to_insert);
		tinyMCEPopup.close();
	},
	
	quick : function() {
		var img = document.forms[0].iufile.value;
		var url_target = document.forms[0].url_target.value;
		
		var warn = function(msg) {
			return '<span style="font-weight:bold; color: red;">X</span> ' + msg;
		}
		var originalTarget = function(msg,url) {
			return '<a class="a_bold" target="_blank" href="'+url+'/view">'+msg+'</a> ';
		}
		var originalImage = function(msg,url,alt) {
			return '<a class="showPointer a_bold" onclick="ImageUploadDialog.insertImage(\''+url+'\',\''+alt+'\');">'+msg+'</a>';
		}
		
		var warning = warn(' Image Already Exists, this will replace the original. <br/>');
		var warning_ext = warn(' Only the file extensions .png | .gif | .jpg are allowed.');
		
		url_target = url_target + "?upload=quickcheck&check_conflict=" + img;
		tinymce.util.XHR.send({
                    url : url_target,
                    type : 'GET',
                    success : function(data) {
						var obj = tinymce.util.JSON.parse(data);
						if (!(img.indexOf('.png') > -1 || img.indexOf('.gif') > -1 || img.indexOf('.jpg') > -1 || img.indexOf('.jpeg') > -1)) {
							jQuery('#filechecker').html(warning_ext);
							jQuery('#insert').attr('disabled','disabled');
							jQuery('#insert').addClass('disabled');
						}
						else if (obj.url != "None") {
							jQuery('#filechecker').html(warning + originalImage(" USE ORIGINAL IMAGE", obj.url, obj.name) + " or " + originalTarget(" VIEW ORIGINAL IMAGE", obj.url) );
							jQuery('#insert').bind('click', function() { 
								if(!confirm('Are you sure? Your image will replace the original one.')){ return false; } });
							jQuery('#insert').removeClass('disabled');
							jQuery('#insert').removeAttr('disabled');
						}
						else {
							jQuery('#filechecker').html('');
							jQuery('#insert').removeAttr('disabled');
							jQuery('#insert').unbind('click');
							jQuery('#insert').removeClass('disabled');
						}
                	}
                });
	},
	
	changeSize : function() {
		// Finally figure this out var reference = tinyMCEPopup.getWin(); jQuery('.plonepopup',reference.document)
		var reference = tinyMCEPopup.getWin();
		reference.tinymce.EditorManager.activeEditor.windowManager.params['mce_height'] = 550;
	}
	
};

tinyMCEPopup.onInit.add(ImageUploadDialog.init, ImageUploadDialog);