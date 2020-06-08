//change class of checkbox if opened in tasksummary page to enable UNDO feature
$(".checkbox").removeClass("toggle_task");
$(".checkbox").addClass("toggle_task_on_summary");

$(".active").removeClass("active");
$(".task_summary").addClass("active");
//$('.active').remove(); removes the entire HTML
