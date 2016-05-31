// "use strict"; to capture undeclared variables
"use strict";

function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
      console.log('User signed out.');
    });
}

function getMessage(response){
    var msg_body = response.message;
    var msg_id = response.msg_id;
    $(".container").hide();
    document.getElementById("messageoutput").innerHTML = msg_body;
    document.getElementById("create-task").style.display = "block";
}

function getid(evt){
    var msg_id = this.id;
    $.get("/handle-message", {'id': msg_id}, getMessage);
}

$(".messagebody").click(getid);


