console.log("nav loaded");
$(".task_summary").on("click", function() {
  $(".active").removeClass("active");
  $(".task_summary").addClass("active");
});

$(".dashboard").on("click", function() {
  $(".active").removeClass("active");
  $(".dashboard").addClass("active");
});
