// "use strict"; to capture undeclared variables
"use strict";

var SLACK_URL= "https://hooks.slack.com/services/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";

var newSlackMessage = "This task has been created: \n";

$("#submit").click(function() {
    var taskName = document.getElementById("taskName").value;
    if($("#slackchannel").is(":checked")) {
        $.post(
            SLACK_URL,
            JSON.stringify({text: newSlackMessage + taskName})
        );
        alert("Thanks. Notified your slack team!");
    };
});

