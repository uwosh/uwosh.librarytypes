//tinyMCEPopup.requireLangPack();

var CatalogLinkDialog = {
	init : function() {
		document.forms[0].btitle.value = tinyMCEPopup.editor.selection.getContent({format : 'text'}) ;
	},
	
	insert : function() {
		abs = document.forms[0].link.value;
		url = abs + "/getItem?bibid=" + document.forms[0].bibid.value + "&query=" + document.forms[0].server.value;
		myframe = '<a class="voyager-link" href="'+url+'">'+document.forms[0].btitle.value+'</a>';
		tinyMCEPopup.editor.execCommand('mceInsertContent', false, myframe);
		tinyMCEPopup.close();
	}
	
};

tinyMCEPopup.onInit.add(CatalogLinkDialog.init, CatalogLinkDialog);