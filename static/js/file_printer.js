function printFiles(csrfToken) {
    $.ajax({
        url: '/print_files/',
        type: 'POST',
        data: { 'csrfmiddlewaretoken': csrfToken },
        success: function() {
            console.log('POST succeeded.');
            window.location.reload(); // Shows the jobs completed message
            
            window.setTimeout(function() {
                window.location.replace('/'); // Clears out the files listed on screen
            }, 5000);
        },
        error: function() {
            console.log('POST failed.');
            alert('The system encountered errors while processing your print jobs.');
            window.location.reload();
        }
    })
}
