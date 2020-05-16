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
