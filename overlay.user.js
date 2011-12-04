// ==UserScript==
// @name            Google Scholar Credibility Overlay
// @namespace       http://rhok.org/
// @description     reputation annotation for scientific search results
// @include         http://scholar.google.tld/scholar*
// @include         http://scholar.google.com/scholar*
// @include         http://scholar.google.de/scholar*
// @run-at          document-end
// ==/UserScript==

SERVICE = "http://localhost:8000/"

function getScore(author, title, callback) {
    GM_xmlhttpRequest({
        method: "POST",
        url: SERVICE + "score",
        data: "author=" + escape(author) + "&title=" + escape(title),
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "Accept": "text/plain"
        },
        onload: callback
    });
}

var p = document.getElementById("scife_hdr").getElementsByTagName("a")[1].parentElement;
p.appendChild(document.createElement("br"));
var navlink = document.createElement("a");
navlink.setAttribute("href", SERVICE + "search?q=" +
    escape(document.getElementsByName("q")[0].value.replace(" ", "+")));
navlink.appendChild(document.createTextNode("Climate Goggles"));
p.appendChild(navlink);

var nodes = document.getElementsByClassName("gs_r");
var completed = 0;

function finish() {
    for (var i = 0; i < nodes.length; i++) {
        for (var j = 0; j < nodes.length-1; j++) {
            cur = nodes[j]; next = nodes[j+1];
            if (cur.getAttribute("score") < next.getAttribute("score")) {
                next.parentElement.removeChild(next);
                cur.parentElement.insertBefore(next, cur);
            }
        }
    }
}

for (var i = 0; i < nodes.length; i++) {
    (function(){
    var article = nodes[i];
    var meta = article.getElementsByClassName("gs_a")[0];
    var desc = meta.textContent;
    var author = desc.substring(0, desc.indexOf("…"));
    var title = article.getElementsByTagName("h3")[0].textContent;
    getScore(author, title, function(response) {
        completed += 1;
        var score = parseInt(response.responseText);
        article.setAttribute("score", score);
        if (nodes.length == completed) {
            finish();
        }
        meta.appendChild(
            document.createTextNode(" - Credibility: " + score + "% "));
    });
    })();
}
