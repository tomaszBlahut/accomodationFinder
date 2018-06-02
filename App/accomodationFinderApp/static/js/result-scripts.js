function handleCheckStatusResponse(response) {
    $(".statusContainer").each(function() {
        $(this).addClass('hidden');
    });

    if(response.status == 1 || response.status == 2) {        
        $("#processing").removeClass('hidden');
        setTimeout(checkStatus, settings.resultCheckInterval);
    } else if (response.status == 4) {
        $("#processing").removeClass('hidden');
    } else if (response.status == 3) {
        createHeatMap(response);
        $("#success").removeClass('hidden');
    }
}

function checkStatus() {
    $.ajax({
        url: settings.API_URL + 'result/' + currentId,
        type: 'GET',
        async: false,
        success: handleCheckStatusResponse
      });
}

$(document).ready(function() {
    checkStatus();
});