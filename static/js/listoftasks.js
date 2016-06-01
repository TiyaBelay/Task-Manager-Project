// "use strict"; to capture undeclared variables
"use strict";

// Adding task completion checkbox to db
$(".table tr").click(function() {
    var True = True;
    var False = False;
    var taskname = this.id;
    if($("#completed").is(":checked")) {
        $.get("/task-list", {'comp': True, 'task': taskname}), alert("Task completed!");
    } else {
        $.get("/task-list", {'comp': False, 'task': taskname}), alert("Incomplete task");
    }
});

// Adding completion date to db
$("#checkbox").click(function() {
    if($(this).is(":checked")) {
        var taskComp = new Date();
        $.get("/task-list", {'compdate': taskComp}, alert("added to DB"));
    }
})