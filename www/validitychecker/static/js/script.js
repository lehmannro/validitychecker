/* Author: 

*/

$(document).ready(function() {
    $('form').submit(function(){
        //$('.mask').show();
    });

    $("#popular").tagcloud({type:"list",sizemin:16, sizemax:35, colormin:"1e90ff",colormax:"00008b"}).find("li");
});























