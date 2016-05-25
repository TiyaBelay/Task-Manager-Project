"use strict";

// function taskStartDateTime() {
//     document.getElementById('submit').value = Date();
// }

var SLACK_URL= "https://hooks.slack.com/services/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";


var newSlackMessage = 

    "This task has been created: \n";

// var completedSlackMessage = 
// payload={
//     "text": "This task has been completed",
//     "title": task,
//     "time": "It took " x times "to complete this task"
// };

$("#submit").click(function() {
    var taskName = document.getElementById("taskName").value;
    // console.log("function called");
    if($("#slackchannel").is(":checked")) {
        // console.log("went through");
        $.post(
            SLACK_URL,
            JSON.stringify({text: newSlackMessage + taskName}),
            function() {
                alert ("Thanks. Notified your slack team!");
            }
        );
    } else {
        return None;
    }
});

$("#submit").click(function() {
    var today = new Date();
    alert("this was submitted on " + today)
})