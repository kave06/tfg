$(function () {
    $('a#calculate').bind('click', function () {
        $.getJSON($SCRIPT_ROOT + '/_add_numbers', {
            a: $('input[name="a"]').val(),
            b: $('input[name="b"]').val()
        }, function (data) {
            $("#result").text(data.result);
        });
        return false;
    });
});

$(function () {
    $('a#relay_state').bind('click', function () {
        $.getJSON($SCRIPT_ROOT + '/relay_state',
         function (data) {
            $("#result").text(data.result);
        });
        return false;
    });
});
