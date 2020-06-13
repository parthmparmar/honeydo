

$(".delete_list").on("click", function() {
  list_id = $(this).data("list_id"); //comes from data tag on button element
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
