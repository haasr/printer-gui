function printFiles(csrfToken) {
    $.ajax({
        url: '/print_files/',
        type: 'POST',
        data: { 'csrfmiddlewaretoken': csrfToken },
        success: function() {
            console.log('POST succeeded.')
            alert('Files are printing...')
        },
        error: function() {
            console.log('POST failed.')
            alert('Your request could not be submitted.')
        }
    })
    window.setTimeout(function(){
        location.reload();
    }, 5000);
}
