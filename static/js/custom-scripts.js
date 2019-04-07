
$('.dropdown-trigger').dropdown();

//
//$(".alert").delay(3000).fadeOut(200, function() {
//    $(this).alert('close');
//});
//



$(document).ready(function() {
    $('.sidenav').sidenav();

    $('.blockMining').on('click', function(){
        $.ajax({
                    type : 'POST',
                    url : '/mine_block'
        })
        .done(function(data) {
            $('#blockIndex').text("Block #" + data.index);
            $('#proofOfWork').text("Proof of Work: " + data.proof);
            $('#blockDate').text("Mined at: " + data.timestamp_date);
            $('#blockTime').text("Time: " + data.timestamp_time);
        });

        $('#minedBlock').fadeOut(300).fadeIn(300);

    });

});