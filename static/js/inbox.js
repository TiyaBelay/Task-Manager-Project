// "use strict"; to capture undeclared variables
"use strict";

// Signs user out
function signOut() {
        var auth2 = gapi.auth2.getAuthInstance();
        auth2.signOut().then(function() {
            console.log('User signed out.');
        });
    }

// Global msg id varibale being set to be used by other functions
var msgIdResult;
var msgSubjResult;

// Retrieves body of message when clicking on any row in the inbox
function getMessage(response) {
    var msgBody = response.message;
    var msgId = response.msg_id;
    var msgSubj = response.email_subject;
    msgIdResult = msgId;
    msgSubjResult = msgSubj;
    $(".table").hide();
    document.getElementById("messageoutput").innerHTML = msgBody;
    document.getElementById("create-task").style.display = "block";
}

function getId(evt) {
    var msgId = this.id;
    $.get("/handle-message", {
        'id': msgId
    }, getMessage);
}
$(".messagebody").click(getId);


// Submits task to SlackChannel using incoming webhooks when checkbox is checked

var SLACK_URL= "https://hooks.slack.com/services/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";

var newSlackMessage = "This task has been created: \n";




$("#submit").click(function(e) {
    var taskDueDate = document.getElementById("duedate").value;
    var taskName = document.getElementById("taskname").value;
    var addTask = function() {
                $.get("/add-tasks", {'msgid': msgIdResult, 'entertask': taskName, 'duedate': taskDueDate}, function() {
                    window.location="/task-list";
                });
            };    
    if($("#slackchannel").is(":checked")) {
        $.post(
            SLACK_URL,
            JSON.stringify({text: newSlackMessage,
                            "attachments": [
                            {
                                "color": "#36a64f",
                                "author_name": "Tiya Belay",
                                "author_icon": "https://avatars1.githubusercontent.com/u/18127030?v=3&s=460",
                                "title": "Email: " + msgSubjResult,
                                "text": "Task: " + taskName,
                            }]
                        })
        ).always(addTask)
        // alert("Thanks. Notified your slack team!");
    } else {
        addTask();
    }
    e.preventDefault();
});

// Adds task info to db
// $("#submit").click(function() {
//     var newTaskName = document.getElementById("taskname").value;
//     var taskDueDate = document.getElementById("duedate").value;
//     $.get("/add-tasks", {'msgid': msgIdResult, 'entertask': newTaskName, 'duedate': taskDueDate}, function() {
//         window.location="/task-list";
//     });
// });