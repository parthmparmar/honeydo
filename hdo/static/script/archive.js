

$(".unarchive").on("click", function() {
  console.log("archive")
  task_id = $(this).data("task_id");
  $.ajax({
    url: "/api/unarchive/"+task_id,
    method: "PUT",
    data: {task_id: task_id}
  }).done(function (resp){
    location.reload();
  });
});
