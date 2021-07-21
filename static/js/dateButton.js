

$('button#dateButton').click(() => {
    var start = $('input[name="start"]').val()
    var end = $('input[name="end"]').val()

    $.get("http://localhost:5000/"+ "startdate="+start )



});