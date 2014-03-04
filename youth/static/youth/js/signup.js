$(document).ready(function () {
    var mousedownHappened = false;

    var newsletter = $("#newsletter");
    newsletter.focus(function () {
        $(this).animate({
            opacity: 1.0,
            width: '+=60px'
        }, 350, function () {
            // callback method empty
        });

        // display submit button
        $("#newsletter_submitbtn").fadeIn(350);
    });


    newsletter.blur(function () {
        if (mousedownHappened) {
            // reset mousedown and cancel fading effect
            mousedownHappened = false;
        } else {
            $("#newsletter").animate({
                opacity: 0.75,
                width: '-=60px'
            }, 500, function () {
                // callback method empty
            });
            // hide submit button
            $("#newsletter_submitbtn").fadeOut(400);
        }
    });


    var newslettersubmitbtn = $("#newsletter_submitbtn");
    newslettersubmitbtn.mousedown(function () {
        mousedownHappened = true;
    });

    newslettersubmitbtn.on("click", function (e) {
        e.preventDefault();
        var form = $('#newsletter_form');
        form.submit = function (e) {
            $.post(form.attr('action'), form.serialize(),function (response, status) {
                if (response.message == 'ok') {
                    $("#signup").fadeOut(280, function () {
                        // callback method to display new text
                        $(this).after('<p id="success">Thanks! We will keep in touch.</p>');
                    });
                } else {
                    $('#newsletter').val('').attr('placeholder', 'Enter a valid email');
                    newsletter.blur();
                }
            }).fail(function () {
                    newsletter.blur();

                });
        };
        form.submit();
    });
});