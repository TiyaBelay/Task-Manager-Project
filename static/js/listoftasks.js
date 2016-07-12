// "use strict"; to capture undeclared variables
"use strict";

// Submits comp task notification to SlackChannel
var SLACK_URL =
    "https://hooks.slack.com/services/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";
var newSlackMessage = "This task has been completed: \n";


// Global variable
var email;

// Adding task completion checkbox to db and sending to Slack 
function emailName(response) {
    var emailName = response.email_task;
    email = emailName;
}

$(".table tr").click(function() {
    var taskName = $(this).find(".taskname")[0].id;
    var taskComp = new Date();
    if ($(this).find(".checkbox")[0].checked) {
        $.get("/add-completed-tasks", {
            'comp': 'True',
            'task': taskName,
            'task_comp_date': taskComp
        }, emailName);
        $.post(SLACK_URL, JSON.stringify({
            text: newSlackMessage,
            "attachments": [{
                "color": "#36a64f",
                "author_name": "Tiya Belay",
                "author_icon": "https://avatars1.githubusercontent.com/u/18127030?v=3&s=460",
                // "title": "Email: " + email,
                "text": "Task: " + taskName,
                "fields": [{
                    "value": "Completed: " +
                        taskComp
                }]
            }]
        }));
    } else {
        $.get("/add-completed-tasks", {
            'comp': 'False',
            'task': taskName
        });
    }
});