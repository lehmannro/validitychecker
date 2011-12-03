/* Author: 

*/

$(document).ready(function() {
    $('form').submit(function(){
        //$('.mask').show();
    });

    $("#popular").tagcloud({type:"list",sizemin:16, sizemax:30, colormin:"aaa",colormax:"888"}).find("li");
});























