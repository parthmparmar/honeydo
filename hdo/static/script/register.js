console.log("Test")
function password_validation(password) {
  if (password.match(/[a-z]/g) && password.match(/[A-Z]/g) && password.match(/[0-9]/g) && password.match( /[^a-zA-Z\d]/g) && password.length >= 8){
      return true;
  }
  else {
      $(".alert").text("Error: New password does not meet requirements. Must be: 8 characters long, include one uppercase, one lowercase, one number and one special character");
      $(".alert").removeClass("d-none");
      return false;
  };
};

function password_compare(password, re_password) {
  if (password == re_password) {
    return true;
  }
  else{
    $(".alert").text("Error: Passwords don't match, please try again.");
    $(".alert").removeClass("d-none");
    return false;
  };
};


$("#register").submit(function(){
  var password = $("#password").val().trim();
  var re_password = $("#re-password").val().trim();
  if (password_validation(password) && password_compare(password, re_password)) {
    return true;
  }
  else {
    return false;
  };
  });

$(".navbar").addClass("d-none");
