// "use strict"; to capture undeclared variables
"use strict";

// Adding task completion checkbox to db
$(".table tr").click(function() {
    var True = True;
    var False = False;
    var taskname = this.getElementsByClassName("taskname")[0].id;
    if($("#checkbox").is(":checked")) {
        $.get("/task-list", {'comp': True, 'task': taskname});
    } else {
        $.get("/task-list", {'comp': False, 'task': taskname});
    }
});

// Adding completion date to db
$("#checkbox").click(function() {
    if($(this).is(":checked")) {
        var taskComp = new Date();
        $.get("/task-list", {'compdate': taskComp});
    }
})