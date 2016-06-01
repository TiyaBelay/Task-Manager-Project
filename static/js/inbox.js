// "use strict"; to capture undeclared variables

"use strict";

// Signs user out

function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
      console.log('User signed out.');
    });
}

// Global msg id varibale being set to be used by other functions
var msgIdResult;

// Retrieves body of message when clicking on any row in the inbox

function getMessage(response){
    var msgBody = response.message;
    var msgId = response.msg_id;
    msgIdResult = msgId;
    $(".table").hide();
    document.getElementById("messageoutput").innerHTML = msgBody;
    document.getElementById("create-task").style.display = "block";
}

function getId(evt){
    var msgId = this.id;
    $.get("/handle-message", {'id': msgId}, getMessage);
}

$(".messagebody").click(getId);


// Submits task to SlackChannel using incoming webhooks when checkbox is checked

var SLACK_URL= "https://hooks.slack.com/services/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";

var newSlackMessage = "This task has been created: \n";

$("#submit").click(function() {
    var taskName = document.getElementById("taskname").value;
    if($("#slackchannel").is(":checked")) {
        $.post(
            SLACK_URL,
            JSON.stringify({text: newSlackMessage + taskName})
        );
        alert("Thanks. Notified your slack team!");
    };
});

// Adds task info to db

$("#submit").click(function() {
    var newTaskName = document.getElementById("taskname").value;
    var taskDueDate = document.getElementById("duedate").value;
    $.get("/add-tasks", {'msgid': msgIdResult, 'entertask': newTaskName, 'duedate': taskDueDate});
});