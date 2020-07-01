
$(document).ready(function(){
  reload_options();
});

function appendNewList(list, toElement){
  $(toElement).empty()
  $(toElement).append(list)
}

function sortBy(list, by){
  list.sort(function(a,b){
    var dateA = Date.parse($(a).find(".due-date").children().first().text());
    var dateB = Date.parse($(b).find(".due-date").children().first().text());
    if (isNaN(dateA)){
      return 1;
    };
    if (isNaN(dateB)){
      return -1;
    };
    if (by == "asc"){
      return dateA - dateB;
    };
    if (by == "desc"){
      return dateB - dateA;
    };
  });
  return list
};

function searchBy(text){
  $(".task-div").each(function(){
    var taskName = $(this).find(".task-name").text().toLowerCase();
      if(!taskName.includes(text.toLowerCase())){
        $(this).addClass("d-none").removeClass("d-flex");
      }
      else {
        $(this).addClass("d-flex").removeClass("d-none");
      };
  });
};

$("#search-txt").on("keyup",function(){
  searchBy($(this).val());
});

$("#open-tasks").on("click", function () {
  $(".completed-task").removeClass("d-flex");
  $(".completed-task").addClass("d-none");
  $(".open-task").addClass("d-flex");
  $(".open-task").removeClass("d-none");
  window.sessionStorage.setItem("type", "open");
});

$("#closed-tasks").on("click", function () {
  $(".open-task").removeClass("d-flex");
  $(".open-task").addClass("d-none");
  $(".completed-task").addClass("d-flex");
  $(".completed-task").removeClass("d-none");
  window.sessionStorage.setItem("type", "closed");
});

$("#claimed-tasks").on("click", function () {
  $(".task-div").not(".me").removeClass("d-flex");
  $(".task-div").not(".me").addClass("d-none");
  window.sessionStorage.setItem("claimed", "true");
});

$(".reset-options").on("click", function () {
  reset_session_storage();
  location.reload();
});

$(".due-date-desc-trigger").on("click", function() {

  appendNewList(sortBy($(".task-div"), "desc"), ".task-view");
  window.sessionStorage.setItem("sort", "desc");
});

$(".due-date-asc-trigger").on("click", function() {
  appendNewList(sortBy($(".task-div"), "asc"), ".task-view");
  window.sessionStorage.setItem("sort", "asc");
});

function reload_options(){
  if (window.sessionStorage.getItem("sort") == "asc"){
    $(".due-date-asc-trigger").click();
  }
  else if (window.sessionStorage.getItem("sort") == "desc"){
    $(".due-date-desc-trigger").click();
  };

  if (window.sessionStorage.getItem("claimed") == "true"){
    $("#claimed-tasks").click();
  };

  if (window.sessionStorage.getItem("type") == "open"){
    $("#open-tasks").click();
  }
  else if (window.sessionStorage.getItem("type") == "closed"){
    $("#closed-tasks").click();
  };

};

function reset_session_storage(){
  window.sessionStorage.setItem("sort", "None");
  window.sessionStorage.setItem("claimed", "None");
  window.sessionStorage.setItem("type", "None");
}
