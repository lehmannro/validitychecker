/* Author: 

*/

$(document).ready(function() {
    $('form').submit(function(){
        //$('.mask').show();
    });

    $("#popular").tagcloud({type:"list",sizemin:18, sizemax:38, colormin:"1e90ff",colormax:"00008b"}).find("li");

    $('input[type=search]').textboxFocusOnStart({text:$('input[type=search]').attr('placeholder')});
});























