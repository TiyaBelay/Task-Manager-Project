// "use strict"; to capture undeclared variables
"use strict";

$("#completed").click(function() {
    var True = True
    var False = False
    if($("#completed").is(":checked")) {
        $.post("/task-list", {'comp': True});
    } else {
        $.post("/task-list", {'comp': False});
    }
});