console.log("Loaded");

$(".delete_list").on("click", function() {
  list_id = $(this).data("list_id");
  console.log(list_id);
  $('#yes-no-modal').modal('show')

  $("#yes-btn").on("click", function() {
    $.ajax({
      url:"/api/list/"+list_id,
      method: "DELETE"
    }).done(function (resp) {
      if (resp == "list deleted"){
        location.reload();
      }
    });
  });

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
      method: "POST"
    }).done(function (resp) {
      if (resp == "task updated"){
        location.reload();
      // $("#task_info"+task_id).load(location.href + "#task_info"+task_id); MAKE THIS TOGGLE THE TEXT INSTEAD
      }
    });
});



$(".points-edit").on("click", function() {
  if($('#points-display').hasClass('d-none')) {
    $('#points-display').removeClass('d-none')
  }
  else{
    $('#points-display').addClass('d-none')
  }

  if($('#points-form').hasClass('d-none')) {
    $('#points-form').removeClass('d-none')
  }
  else{
    $('#points-form').addClass('d-none')
  }
})

$('input')[0].form.new_point_value.value
