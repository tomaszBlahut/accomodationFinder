function chech_status() {


    setTimeout(show_my_table, 10000);

// function show_my_table() {
//     $ajax({url: "http://127.0.0.1:5000/search",
//     type:'html',
//     success: function (FindingResult.Status)
//         {
//             //how to get status?
//             if (FindingResult.Status == "Processing") {
//                 setInterval(show_my_table, 10000);
//             }
//             else if (FindingResult.Status == "Completed") {
//                 $('#search').html(FindingResult.Status).show();
//             }
//             else (FindingResult.Status == "Failed")
//             {
//                 alert("Something goes wrong...");
//             }
//         }
//     })
// }

    //for testing response
    var response = "Complete";

    function show_my_table() {
        $ajax({
            url: "http://127.0.0.1:5000/search",
            type: 'html',
            success: function (response) {
                $('#search').html(response).hide();
                //how to get status?
                if (response === "Processing" || response === "New") {
                    setTimeout(show_my_table, 10000);
                }
                else if (response === "Completed") {
                    $('#search').html(response).show();
                }
                else (response === "Failed")
                {
                    alert("Something goes wrong...");
                }
            }
        })
    }
}