/* Author: 

*/

$(document).ready(function() {

    $(".home .popular").tagcloud({type:"list", sizemin:16, sizemax:30, colormin:"aaa", colormax:"888"}).find("li");
    
    var search_input = $('.home form input[type=search]');
    search_input.textboxFocusOnStart({text: search_input.attr('placeholder')});
});























