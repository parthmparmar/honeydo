
$(".delete-user-access").on("click", function () {
  user_id = $(this).data("user_id");
  list_id = $(this).data("list_id");
  $.ajax({
    url:"/api/access/?list_id="+list_id+"&user_id="+user_id,
    method: "DELETE",
  }).done(function (resp) {
    console.log(resp)
    if (resp == "Self Deleted"){
      location.href = "/lists";
    }
    else{
      location.reload();
    }
  });
});

$(".edit-list").on("click", function () {
  $(".edit-list-input").removeClass("d-none");
  $(".list-title").addClass("d-none");
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
  task_id = $(this).data("task_id");
    $.ajax({
      url:"/api/task/"+task_id+"/update_state/in_list",
      method: "PUT"
    }).done(function (resp) {
      if (resp == "task updated"){
        location.reload();
      }
    });
});


$(".toggle_task_on_summary").on("click", function() {
  task_id = $(this).data("task_id");
    $.ajax({
      url:"/api/task/"+task_id+"/update_state/in_summary",
      method: "PUT"
    }).done(function (resp) {
      if (resp == "task updated"){
        location.reload();
      }
    });
});




$(".show_task_description").on("click", function(){
  task_description = $(this).data("task_description");



  console.log(task_description)
  task_id = $(this).data("task_id");
  $('#task-description-modal').modal('show')
  if (task_description == 'None')  {
    $('textarea[name="task_description"]').val("");
  }
  else{
    $('textarea[name="task_description"]').val(task_description);
  }

  $("#submit-task-description").on("click", function() {
    task_description = $("#task_description").val().trim()
    $.ajax({
      url:"/api/task/"+task_id+"/update_description",
      method: "PUT",
      data: {task_description: task_description}
    }).done(function (resp) {
      if (resp == "task updated"){
        location.reload();
      }
    });
  });
});




$(".task_edit").on("click", function() {
  task_id = $(this).data("task_id");
  current_task_name = $(this).data('task_name');
  current_points = $(this).data('points');
  current_date = $(this).data('due_date');

  $('#task-edit-modal').modal('show')

  $('input[name="task_name"]').val(current_task_name);
  $('input[name="points"]').val(current_points);
  $('input[name="due_date"]').val(current_date);


  $("#submit-edited-task").on("click", function() {
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


$(".claim_task").on("click", function() {
  console.log("click");
  task_id = $(this).closest(".button-div").data("task_id");
  list_id = $(this).closest(".button-div").data("list_id");
  $.ajax({
    url:"/api/" + list_id + "/task/" + task_id + "/claim",
    method: "PUT",
  }).done(function (resp) {
    location.reload();
  });
});

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})
