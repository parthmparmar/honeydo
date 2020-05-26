console.log("js loding")
$(".delete-user-access").on("click", function () {
  user_id = $(this).data("user_id");
  list_id = $(this).data("list_id");
  $.ajax({
    url:"/api/access/?list_id="+list_id+"&user_id="+user_id,
    method: "DELETE",
  }).done(function (resp) {
      location.reload();
  });
});

$(".edit-list").on("click", function () {
  $(".edit-list-input").removeClass("d-none");
});

$("#update-list-name").on("click", function (){
  list_id = $(this).data("list_id");
  new_name = $("#new_name").val().trim()
  if (new_name) {
    $.ajax({
      url: "/api/list/"+list_id,
      method: "PUT",
      data: {new_name: new_name}
    }).done(function (resp){
      location.reload();
    });
  };
});

$(".delete_task").on("click", function() {
  list_id = $(this).data("list_id");
  task_id = $(this).data("task_id");

  $('#yes-no-modal').modal('show')

  $("#yes-btn").on("click", function() {
    $.ajax({
      url:"/api/"+list_id+"/task/"+task_id+"/delete",
      method: "DELETE"
    }).done(function (resp) {
      if (resp == "task deleted"){
        location.reload();
      }
    });
  });
});


$(".toggle_task").on("click", function() {
  list_id = $(this).data("list_id");
  task_id = $(this).data("task_id");
    $.ajax({
      url:"/api/"+list_id+"/task/"+task_id+"/update_state",
      method: "PUT"
    }).done(function (resp) {
      if (resp == "task updated"){
        location.reload();
      // $("#task_info"+task_id).load(location.href + "#task_info"+task_id); MAKE THIS TOGGLE THE TEXT INSTEAD
      }
    });
});



$(".task_edit").on("click", function() {
  task_id = $(this).data("task_id");
  //var $current_task_name = decodeURIComponent($('.task_edit').data('task_name'))
  current_task_name = $(this).data('task_name');
  //strings are saved with "_" replacing spaces for now. This replaces the "_" with spaces before loading the value into the form
  current_task_name = current_task_name.replace(/_/g," ") 
  current_points = $(this).data('points');
  current_date = $(this).data('due_date');

  $('#task-edit-modal').modal('show')
  $('input[name="task_name"]').val(current_task_name);
  $('input[name="points"]').val(current_points);
  $('input[name="due_date"]').val(current_date);

  $("#submit-new-task").on("click", function() {
    task_name = $("#new_task_name").val().trim()
    points = $("#new_points").val().trim()
    due_date = $("#new_due_date").val().trim()
    $.ajax({
      url:"/api/task/"+task_id+"/update",
      method: "PUT",
      data: {task_name: task_name, points: points, due_date: due_date}
    }).done(function (resp) {
      if (resp == "task updated"){
        location.reload();
      }
    });
  });
});

//$('input')[0].form.new_point_value.value
