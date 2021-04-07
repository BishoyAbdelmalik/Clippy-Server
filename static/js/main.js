function toggleEdit() {
    $("#edit-ports ").toggleClass("d-none ");
    $("#editing-port ").toggleClass("d-none ");
    websocketstate = $("#websocket-port")[0].disabled;
    flaskstate = $("#flask-port")[0].disabled;
    $("#websocket-port")[0].disabled = !websocketstate;
    $("#flask-port")[0].disabled = !flaskstate;
}
var websocketPort;
var flaskPort;
$(document).ready(function() {
    // Handler for .ready() called.
    websocketPort = $("#websocket-port")[0].value;
    flaskPort = $("#flask-port")[0].value;

    $("#edit-ports ").click(() => toggleEdit());
    $("#cancel ").click(() => {
        $("#websocket-port")[0].value = websocketPort;
        $("#flask-port")[0].value = flaskPort;
        toggleEdit();
    });
    $("#save").click(() => {
        toggleEdit();

    });
});