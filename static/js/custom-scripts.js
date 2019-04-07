
$('.dropdown-trigger').dropdown();

//
//$(".alert").delay(3000).fadeOut(200, function() {
//    $(this).alert('close');
//});
//



$(document).ready(function() {
    $('.sidenav').sidenav();

     $('.modal').modal();

    $('.tooltipped').tooltip();

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
            $('#minedBlock').fadeOut(300).fadeIn(300);
            $("#rowBlockchain").append('<div class="col-md-3">' +
                                        '<div class="card card-block">' +
                                        '<div class="card-content white-text">' +
                                            '<span class="card-title">' + "Block #" + data.index + '</span>'
                                            + '<br>' +
                                            '<p>' + 'Proof of Work: ' + data.proof  + '</p>' +
                                            '<p>' + 'Mined at: ' + data.timestamp_date  + '</p>' +
                                            '<p>' + 'Time: ' + data.timestamp_time  + '</p>'
                                        + '</div>'
                                        + '<div class="row plain-element">'
                                        + '<div class="col-md-6 plain-element">' +
                                            '<a class="btn btn-blockchain tooltipped"' + 'data-position="bottom"' + 'data-tooltip="' + "asdasdas" + '">' + 'Previous Hash'  + '</a>'
                                        + '</div>'
                                        + '<div class="col-md-6 plain-element">' +
                                            '<a class="btn btn-blockchain" href="#">' + 'Transactions'  + '</a>'
                                        + '</div>'

                                        + '</div>'
                                        + '</div>'
                                        + '</div>'
                                        + '</div>');

        });
    });
});