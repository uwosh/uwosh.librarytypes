jq(document).ready(function(){
	
	
	setupLibraryStaffExpanders();
	
});


function setupLibraryStaffExpanders() {
	var isHovering = false;
	
	jq('.library_staff_clickable').click(function(){
		id = '#'+jq(this).attr('data-id');
		jq(id).slideDown('fast');
	});
	
    jq('.library_staff_clickable').hover(
        function(){ 
            isHovering = true;  
        },
        function(){ 
            isHovering = false;
        }
    );
	
    jq('body').click(function() {
        if (!isHovering) {
			jq('.library_staff_hidden').slideUp(150);
		}
    });
	
}
