$(function () {
    $('a#relay_state').bind('click', function () {
        $.getJSON($SCRIPT_ROOT + '/relay_state', {}, function (data) {
            $("#state").text(data.state);
        });
        return false;
    });
});

