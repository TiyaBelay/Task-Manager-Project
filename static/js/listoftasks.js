// "use strict"; to capture undeclared variables
"use strict";

// Adding task completion checkbox to db
$(".table tr").click(function() {
    var True = True;
    var False = False;
    var taskname = this.getElementsByClassName("taskname")[0].id;
    var taskComp = new Date();

    if($("#checkbox").is(":checked")) {
        $.get("/task-list", {'comp': 'True', 'task': taskname});
    } else {
        $.get("/task-list", {'comp': 'False', 'task': taskname});
    }
});
