setInterval(show_my_table, 10000);

function show_my_table() {
    $ajax({url: "http://127.0.0.1:5000/search",
    type:'html',
    success: function (FindingResult.Status)
        {
            //how to get status?
            if (FindingResult.Status == "Processing") {
                setInterval(show_my_table, 10000);
            }
            else if (FindingResult.Status == "Completed") {
                $('#search').html(FindingResult.Status).show();
            }
            else (FindingResult.Status == "Failed")
            {
                alert("Something goes wrong...");
            }
        }
    })
}

