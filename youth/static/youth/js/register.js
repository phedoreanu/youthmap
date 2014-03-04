$(document).ready(function () {

    /*$('#login-link').click(function() {
     $('#login-form').toggle();
     $('#register-form').hide();
     });
     $('#register-link').click(function() {
     $('#register-form').toggle();
     $('#login-form').hide();
     });*/

    $("#sign-in-tab").click(function () {
        loadSignIn();  // function to display the sin in form
    });

    $("#register-tab").click(function () {
        loadRegister(); // function to display the register form
    });

    $("div.close").click(function () {
        disablePopup();  // function to close pop-up forms
    });

    $("#background-on-popup").click(function () {
        disablePopup();  // function to close pop-up forms
    });

    $(this).keyup(function (event) {
        if (event.which == 27) { // 27 is the code of the ESC key
            disablePopup();
        }
    });

    var status = 0;

    function loadSignIn() {
        if (status == 0) {
            $("#sign-in-form").fadeIn(300);
            $("#background-on-popup").css("opacity", "0.7").fadeIn(300);
            status = 1;
            $('#username').focus();
        }
    }

    function loadRegister() {
        if (status == 0) {
            $("#register-form").fadeIn(300);
            $("#background-on-popup").css("opacity", "0.7").fadeIn(300);
            status = 1;
            $('#first_name').focus();
        }
    }

    function loadAddExperience() {
        if (status == 0) {
            $("#register-form").fadeIn(300);
            $("#background-on-popup").css("opacity", "0.7").fadeIn(300);
            status = 1;
            $('#first_name').focus();
        }
    }

    function disablePopup() {
        if (status == 1) {
            $("#sign-in-form").fadeOut("normal");
            $("#register-form").fadeOut("normal");
            $("#background-on-popup").fadeOut("normal");
            status = 0;
        }
    }


    $("#checkbox .unchecked-state").click( // checkbox select event
        function (event) {
            $(this).parent().addClass("selected");
            $(this).parent().find("checkbox").attr("checked", "checked");
        }
    );

    $("#checkbox .checked-state").click( // checkbox deselect event
        function (event) {
            $(this).parent().removeClass("selected");
            $(this).parent().find("checkbox").removeAttr("checked");
        }
    );
});