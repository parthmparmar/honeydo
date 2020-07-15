
$(".delete-user-access").on("click", function () {
  user_id = $(this).data("user_id");
  list_id = $(this).data("list_id");
  $.ajax({
    url:"/api/access/?list_id="+list_id+"&user_id="+user_id,
    method: "DELETE",
  }).done(function (resp) {
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
  new_name = $("#new_name").val().trim();
  if (new_name) {
    newListName($(this), new_name);
    $(".edit-list-input").addClass("d-none");
    $(".list-title").removeClass("d-none");
    $.ajax({
      url: "/api/list/"+list_id,
      method: "PUT",
      data: {new_name: new_name}
    }).done(function (resp){
      // location.reload();
    });
  };
});

$(".edit-list-description").on("click", function () {
  $(".edit-list-description-input").removeClass("d-none");
  $(".list-description").addClass("d-none");
});

$("#update-list-description").on("click", function (){
  list_id = $(this).data("list_id");
  new_list_description = $("#new_list_description").val().trim();
  if (new_list_description) {
    updateListDescription($(this), new_list_description);
    $(".edit-list-description-input").addClass("d-none");
    $(".list-description").removeClass("d-none");
    $.ajax({
      url: "/api/list/description/"+list_id,
      method: "PUT",
      data: {new_list_description: new_list_description}
    }).done(function (resp){
      // location.reload();
    });
  };
});

$(document).on("click", ".delete_task", function(){
  list_id = $(this).data("list_id");
  task_id = $(this).data("task_id");
  element = $(this)
  $('#yes-no-modal').modal('show')

  $("#yes-btn").on("click", function() {
    $.ajax({
      url:"/api/"+list_id+"/task/"+task_id+"/delete",
      method: "DELETE"
    }).done(function (resp) {
      if (resp == "task deleted"){
        // location.reload();
        deleteTask(element);

      }
    });
  });
});


$(document).on("click", ".toggle_task", function(){
  toggleTask($(this));
  task_id = $(this).data("task_id");
    $.ajax({
      url:"/api/task/"+task_id+"/update_state/in_list",
      method: "PUT"
    }).done(function (resp) {
      if (resp == "task updated"){
        // location.reload();
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


$(document).on("click", ".show_task_description", function(){
  task_description = $(this).data("task_description");
  element = $(this);
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
        // location.reload();
        taskDescription(element, task_description);
      }
    });
  });
});




// $(".task_edit").on("click", function() {
$(document).on("click", ".task_edit", function() {
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
    element = $("#" + task_id + ".task-div")
    obj = {
      task_name: task_name,
      points: points,
      due_date: due_date,
    }
    updateTaskItem(element, obj);
    $.ajax({
      url:"/api/task/"+task_id+"/update",
      method: "PUT",
      data: {task_name: task_name, points: points, due_date: due_date}
    }).done(function (resp) {
      if (resp == "task updated"){
        // location.reload();
      }
    });
  });
});


$(document).on("click", ".claim_task", function() {
  task_id = $(this).closest(".button-div").data("task_id");
  list_id = $(this).closest(".button-div").data("list_id");
  var element = $(this)
  $.ajax({
    url:"/api/" + list_id + "/task/" + task_id + "/claim",
    method: "PUT",
  }).done(function (resp) {
    if (resp == "not allowed"){
      location.reload();
    }
    else {
      claimTask(element, resp);
    };
  });
});

// Toggle DOM task items to completed or not
function toggleTask(element){
  $(element).addClass("d-none");
  $(element).siblings().removeClass("d-none");
  if($(element).closest(".task-div").hasClass("open-task")){
    $(element).closest(".task-div").removeClass("open-task").addClass("completed-task");
    $(element).parent().next(".task-name").addClass("completed");
  }
  else{
    $(element).closest(".task-div").addClass("open-task").removeClass("completed-task");
    $(element).parent().next(".task-name").removeClass("completed");
  };
};

function claimTask(element, name){

  $(element).toggleClass("claimed");
  $(element).closest(".task-div").toggleClass("me");
  $(element).closest(".task-div").find(".task-name").attr("data-original-title", name);
};

function taskDescription(element, desc){
  $(element).data("task_description", desc);
  if (desc){
    $(element).children("i").addClass("contains-note");
  }
  else {
    $(element).children("i").removeClass("contains-note");
  };
};

function deleteTask(element){
  $(element).closest(".task-div").remove();
};

function newListName(element, name){
  $(element).closest("#new_name").val(name);
  $(element).closest(".edit-list-input").siblings(".list-title").children("#list-name").text(name);
};

function updateListDescription(element, desc){
  $(element).closest("#new_list_description").val(desc);
  $(element).closest(".edit-list-description-input").siblings(".list-description").children("i").text(desc);
};

function updateTaskItem(element, obj){
  $(element).find(".task-name").text(obj.task_name);
  $(element).find(".badge-pill").text(obj.points);
  $(element).find(".badge-pill").removeClass("d-none");
  $(element).find(".due-date-value").text(obj.due_date);
};


$("#new-task-submit").on("click", function(){
  list_id = $(this).data("list_id")
  console.log($("#task-name").val())
  if($("#task_name").val()){
    data = $(".add-task").serializeArray();
    $.ajax({
      url:"/api/task/add/" + list_id,
      method: "POST",
      data: data
    }).done(function (resp) {
        newTask(resp);
        $(".add-task").trigger("reset");
    });
  };
});
function newTask(obj){
  if($(".task-div").length < 1){
    location.reload();
    // console.log("reload");
  }
  else{
    current_task = $(".task-div")[0];
    task = $(current_task).clone(true);
    $(task).attr("id", obj.task_id);

    if (obj.status == 0){
      $(task).addClass("open-task");
      $(task).find("done").addClass("d-none");
      $(task).find("not-done").removeClass("d-none");
      $(task).find("task-name").removeClass("completed");
    }
    else if (obj.status == 1){
      $(task).addClass("completed-task")
      $(task).find("done").removeClass("d-none");
      $(task).find("not-done").addClass("d-none");
      $(task).find("task-name").addClass("completed");
    };
    $(task).find(".task-name").text(obj.task_name);
    $(task).find(".task-name").tooltip('update')
    $(task).find(".due-date-value").text(dateStringOnly(obj.due_date));

    if (obj.points > 0){
      $(task).find(".badge-pill").text(obj.points);
    }
    else {
      $(task).find(".badge-pill").text(obj.points);
      $(task).find(".badge-pill").addClass("d-none");
    };

    $(task).find(".button-div").attr("data-task_id", obj.task_id);
    $(task).find(".button-div").attr("data-list_id", obj.list_id);

    if (obj.assigned_user_id) {
      $(task).find(".claim_task").addClass("claimed");
      $(task).find(".task-name").attr("data-original-title", obj.assigned_user_name);
    }
    else {
      $(task).find(".claim_task").removeClass("claimed");
      $(task).find(".task-name").attr("data-original-title", "");
    };

    $(task).find(".show_task_description").attr("data-task_description", obj.task_description);
    $(task).find(".show_task_description").attr("data-task_id", obj.task_id);

    if (obj.task_description){
      $(task).find(".fa-sticky-note").removeClass("contains-note");
    }
    else {
      $(task).find(".fa-sticky-note").removeClass("contains-note");
    }

    $(task).find(".task_edit").attr("data-task_id", obj.task_id);
    $(task).find(".task_edit").attr("data-task_name", obj.task_name);
    $(task).find(".task_edit").attr("data-due_date", dateStringOnly(obj.due_date));
    $(task).find(".task_edit").attr("data-points", obj.points);

    $(task).find(".delete_task").attr("data-task_id", obj.task_id);
    $(task).find(".delete_task").attr("data-list_id", obj.list_id);

    $(".task-view").append($(task));
  };
};

function dateStringOnly(dateObj){
  if (dateObj){
    var date_item = new Date(Date.parse(dateObj));
    date_only = date_item.toISOString();
    return date_only.split("T")[0];
  }
  else{
    return ""
  }
};

// turn on tooltip option
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
});
