//tinyMCEPopup.requireLangPack();

var VideoEmbedDialog = {
	init : function() {
		var content = tinyMCEPopup.editor.selection.getContent();
		if (content != null || content != '')
			document.forms[0].embedCode.value = content;
	},
	
	insert : function() {
		var code = document.forms[0].embedCode.value;
		
		tinyMCEPopup.editor.execCommand('mceInsertContent', false, code);
		tinyMCEPopup.close();
	},
	
	
};

tinyMCEPopup.onInit.add(VideoEmbedDialog.init, VideoEmbedDialog);
