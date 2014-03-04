/***
 Equal Heights function.
 ***/

(function ($) {
    $.fn.equalHeights = function (browserWidth, additionalHeight) {
        // Calculating width of the scrollbar for Firefox
        var scrollbar = 0;
        if (typeof document.body.style.MozBoxShadow === 'string') {
            scrollbar = window.innerWidth - $('body').width();
        }
        // Getting number of blocks for height correction.
        var blocks = $(this).children().length;
        // Setting block heights to auto.
        $(this).children().css('min-height', 'auto');
        // Initializing variables.
        var currentBlock = 1;
        var equalHeight = 0;
        // Finding the highest block in the selection.
        while (currentBlock <= blocks) {
            var currentHeight = $(this).children(':nth-child(' + currentBlock.toString() + ')').height();
            if (equalHeight <= currentHeight) {
                equalHeight = currentHeight;
            }
            currentBlock = currentBlock + 1;
        }
        // Equalizing heights of columns.
        if ($('body').width() > browserWidth - scrollbar) {
            $(this).children().css('min-height', equalHeight + additionalHeight);
        } else {
            $(this).children().css('min-height', 'auto');
        }
    };
})($);

/* global document */
$(document).ready(function () {
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    var csrftoken = $.cookie('csrftoken');

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var $sf = $('#sf-menu');
    /***
     1. Main menu $ plugin.
     ***/

    $sf.superfish();

    /***
     2. Mobile Menu $ plugin.
     ***/

    $sf.mobileMenu({
        switchWidth: 767,
        prependTo: '.main-menu',
        combine: false
    });

    /***
     7. Adding <input> placeholders (for IE 8-9).
     ***/

    $('.text-input-grey, .text-input-black').placeholder();

    $('#advanced-search-button').click(function (event) {
        /* Preventing default link action */
        event.preventDefault();
        var $hidemapbutton = $('#hide-map-button');
        if ($hidemapbutton.hasClass('map-collapsed')) {
            $('#map').animate({ height: '400px' });
            $hidemapbutton.text('Hide Map').removeClass('map-collapsed').addClass('map-expanded');
        }
        $('#advanced-search').slideToggle('fast');
        if ($(this).text() === 'Close') {
            $(this).text('Search');
            $(this).removeClass('expanded');
        } else {
            $(this).text('Close');
            $(this).addClass('expanded');
        }

        $('#search-keyword').focus();
    });

    $('#hide-map-button').click(function (event) {
        event.preventDefault();
        if ($(this).hasClass('map-expanded')) {
            var $advanced = $('#advanced-search-button');
            if ($advanced.hasClass('expanded')) {
                $('#advanced-search').slideToggle('fast');
                $advanced.removeClass('expanded');
                $advanced.text('Search');

            }
            $('#map').animate({ height: '107px' });
            $(this).text('Show Map').removeClass('map-expanded').addClass('map-collapsed');

            $.cookie('map_collapsed', 'true_' + new Date().getTime(), {path: '/'});
        } else {
            $('#map').animate({ height: '400px' });
            $(this).text('Hide Map').removeClass('map-collapsed').addClass('map-expanded');
            $.removeCookie('map_collapsed', { path: '/' });
        }
    });

    var map_cookie = $.cookie('map_collapsed');
    if (map_cookie && map_cookie.split('_')[0] == 'true') {
        $('#hide-map-button').trigger('click');
    }

});

/* global window */
$(window).load(function () {

    /***
     12. Setting equal heights for required containers and elements on page load.
     ***/

    $('.zone-content .equalize').equalHeights(767, 0);

    /***
     12. Adding Twitter feed to the website footer.
     ***/

    $("#twitter-feed").tweet({
        username: "envato",
        template: "{avatar}{text}",
        count: 2,
        avatar_size: 24,
        loading_text: "Loading tweets..."
    });

    /***
     13. Adding Flickr feed to the website footer.
     ***/

    $("#flickr-feed").jflickrfeed({
        limit: 12,
        qstrings: {
            id: '52617155@N08'
        },
        itemTemplate: '<li>' +
            '<a href="{{image_b}}"><img src="{{image_s}}" alt="{{title}}" /></a>' +
            '</li>'
    });

});

$(window).resize(function () {

    /***
     15. Setting equal heights for required containers and elements on page resize.
     ***/

    $('.zone-content .equalize').equalHeights(767, 0);

});