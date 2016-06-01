// "use strict"; to capture undeclared variables
"use strict";

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