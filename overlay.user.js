// ==UserScript==
// @name            Google Scholar Credibility Overlay
// @namespace       http://rhok.org/
// @description     reputation annotation for scientific search results
// @include         http://scholar.google.tld/scholar*
// @include         http://scholar.google.com/scholar*
// @include         http://scholar.google.de/scholar*
// @resource        service http://localhost:8000/score
// @run-at          document-end
// ==/UserScript==

function getScore(author, title, callback) {
    GM_xmlhttpRequest({
        method: "POST",
        url: GM_getResourceText("service"),
        data: "author=" + escape(author) + "&title=" + escape(title),
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "Accept": "text/plain"
        },
        onload: callback
    });
}

function finish() {
    // sort
}

var nodes = document.getElementsByClassName("gs_r");
var completed = 0;
for (i = 0; i < nodes.length; i++) {
    (function(){
    var article = nodes[i];
    var meta = article.getElementsByClassName("gs_a")[0];
    var desc = meta.textContent;
    var author = desc.substring(0, desc.indexOf("…"));
    var title = article.getElementsByTagName("h3")[0].textContent;
    getScore(author, title, function(response) {
        completed += 1;
        if (nodes.length == completed) {
            finish();
        }
        var score = parseInt(response.responseText);
        if (score < 20) {
            article.style.backgroundColor = "red";
        }
        meta.appendChild(
            document.createTextNode(" - Credibility: " + score + "% "));
    });
    })();
}
