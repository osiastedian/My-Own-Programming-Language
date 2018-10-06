var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    lineNumbers: true,
    styleActiveLine: true,
    matchBrackets: true,
    lineSeparator: '\n'
});
var inputEditor = CodeMirror.fromTextArea(document.getElementById("inputs"), {
    lineNumbers: true,
    styleActiveLine: true,
    matchBrackets: true
});
var outputEditor = CodeMirror.fromTextArea(document.getElementById("outputs"), {
    lineNumbers: true,
    styleActiveLine: true,
    matchBrackets: true
});
var input = document.getElementById("select");
function selectTheme() {
    var theme = input.options[input.selectedIndex].textContent;
    editor.setOption("theme", theme);
    inputEditor.setOption("theme", theme);
    outputEditor.setOption("theme", theme);
    location.hash = "#" + theme;
}
var choice = (location.hash && location.hash.slice(1)) ||
                (document.location.search &&
                decodeURIComponent(document.location.search.slice(1)));
if (choice) {
    input.value = choice;
    editor.setOption("theme", choice);
    inputEditor.setOption("theme", choice);
    outputEditor.setOption("theme", choice);
}
CodeMirror.on(window, "hashchange", function() {
    var theme = location.hash.slice(1);
    if (theme) { input.value = theme; selectTheme(); }
});
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$( "#runButton" ).click(function() {
    let params = {
        lines: editor.getValue().split('\n'),
        inputs: inputEditor.getValue().split('\n')
    };
    var csrftoken = getCookie('csrftoken');
    $.postJSON = function(url, data, success, args) {
    args = $.extend({
        url: url,
        type: 'POST',
        headers: {"X-CSRFToken": csrftoken},
        data: JSON.stringify(data),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: true,
        success: success
    }, args);
        return $.ajax(args);
    };
    $.postJSON("/api/execute/", params, function(data, status){
        outputEditor.setValue(data.logs.join('\n'))
    });
});