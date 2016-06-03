// "use strict"; to capture undeclared variables
"use strict";

// Adding global variables
var taskCheckedName;

// Submits comp task notification to SlackChannel

var SLACK_URL= "https://hooks.slack.com/services/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";

var newSlackMessage = "This task has been completed: \n";

$(".table tr").click(function() {
    if($("#checkbox").is(":checked")) {
        $.post(
            SLACK_URL,
            JSON.stringify({text: newSlackMessage + taskCheckedName,
                            "attachments": [
                            {
                                "color": "#36a64f",
                                "author_name": "Tiya Belay",
                                "title": "email",
                                "text": taskCheckedName
                            }]
                        })
        );
        alert("Thanks. Notified your slack team!");
    };
});

// Adding task completion checkbox to db

function taskCompleted(response) {
    var taskName = response.task_name;
    taskCheckedName = taskName;
}

$(".table tr").click(function() {
    var taskname = $(this).find(".taskname")[0].id;
    var taskComp = new Date();

    if($(this).find(".checkbox")[0].checked) {
        $.get("/add-completed-tasks", {'comp': 'True', 'task': taskname, 'task_comp_date': taskComp}, taskCompleted);
    } else {
        $.get("/add-completed-tasks", {'comp': 'False', 'task': taskname});
    }
});
