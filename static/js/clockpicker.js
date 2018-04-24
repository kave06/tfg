$('.clockpicker-with-callbacks').clockpicker({
    donetext: 'Done',
    init: function () {
        console.log("colorpicker initiated");
    },
    beforeShow: function () {
        console.log("before show");
    },
    afterShow: function () {
        console.log("after show");
    },
    beforeHide: function () {
        console.log("before hide");
    },
    afterHide: function () {
        console.log("after hide");
    },
    beforeHourSelect: function () {
        console.log("before hour selected");
    },
    afterHourSelect: function () {
        console.log("after hour selected");
    },
    beforeDone: function () {
        console.log("before done");
    },
    afterDone: function () {
        console.log("after done");
    }
})
    .find('input').change(function () {
    console.log(this.value);
    $.getJSON($SCRIPT_ROOT2 + '/_add_numbers', {
        a: this.value
    })
    return false
});


// Manually toggle to the minutes view
$('#check-minutes').click(function (e) {
    // Have to stop propagation here
    e.stopPropagation();
    input.clockpicker('show')
        .clockpicker('toggleView', 'minutes');
});
if (/mobile/i.test(navigator.userAgent)) {
    $('input').prop('readOnly', true);
}

hljs.configure({tabReplace: '    '});
hljs.initHighlightingOnLoad();

