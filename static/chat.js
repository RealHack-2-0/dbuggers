
$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);
    
    chatsock.onmessage = function(message) {
        var data = JSON.parse(message.data);
        var chat = $("#chat")
        var ele = $('<tr></tr>')
	
       if(localStorage['myID'] == data.handle){
       notification_added("The question : "+ data.message + " has been answered");
	}
	displayMessage(data.handle);
        chat.append(ele)
    };

    $("#sub1").click(function(event) {
	$('form#chatform').submit();
        var message = {
            handle: $('#handle').val(),
            message: $('#message').val(),
        }
        chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();
        return false;
	
    });
});