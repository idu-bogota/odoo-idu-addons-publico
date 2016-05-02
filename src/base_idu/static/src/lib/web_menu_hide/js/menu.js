$(document).ready(function () {
 
    $( ".toggle_leftmenu").click(function() {
            $( ".oe_leftbar").animate({
            width: 'toggle'
        });
            $( ".oe_leftbar").find('img').animate({
            width: 'toggle'
        });

    });
    
    $( "ul.nav li a" ).each(function(index) {
        $(this).on("click", function(){
            $( ".oe_leftbar").show();
            $( ".oe_leftbar").find('img').show();
        }); 
    });
});
