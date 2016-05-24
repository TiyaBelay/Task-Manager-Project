"use strict";

// function taskStartDateTime() {
//     document.getElementById('submit').value = Date();
// }

var SLACK_URL= "https://hooks.slack.com/services/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";

var newSlackMessage = 
{
    "text": "This task has been created",
    "title": "task"
};

// var completedSlackMessage = 
// payload={
//     "text": "This task has been completed",
//     "title": task,
//     "time": "It took " x times "to complete this task"
// };

$("#submit").click(function() {
    // console.log("function called");
    if($("#slackchannel").is(":checked")) {
        // console.log("went through");
        $.post(
            SLACK_URL,
            JSON.stringify(newSlackMessage),
            function() {
                alert ("Thanks. Notified your slack team!");
            }
        );
    } else {
        return None;
    }
});

