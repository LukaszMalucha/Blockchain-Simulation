
$('.dropdown-trigger').dropdown();


$(".alert").delay(3000).fadeOut(200, function() {
    $(this).alert('close');
});




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

            if (data.transactions.length >= 1){
                var transaction1 = data.transactions[0]['sender'] + ' sends ' + data.transactions[0]['amount'] + ' coins to ' + data.transactions[0]['receiver'];
                var transaction2 = data.transactions[1]['sender'] + ' sends ' + data.transactions[1]['amount'] + ' coins to ' + data.transactions[1]['receiver'];
            }
            else {
                var transaction1 = ""
                var transaction2 = ""
            }

            console.log(transaction1);
            console.log(transaction2);
            $('#blockIndex').text("Block #" + data.index);
            $('#proofOfWork').text(data.proof);
            $('#HashNumber').text(data.previous_hash);
            $('#blockDate').text(data.timestamp_date);
            $('#blockTime').text(data.timestamp_time);
            $('#transactions').append( '<div class="row plain-element row-transactions">' +
                                                '<p class="transaction">'  + transaction1 + '</p>' +
                                               '<p class="transaction">'  + transaction2 + '</p>');


            $('#minedBlock').fadeOut(300).fadeIn(300);
            $("#rowBlockchain").append('<div class="col-md-4">' +
                                        '<div class="card card-block">' +
                                        '<div class="card-content">' +
                                            '<span class="card-title">' + "Block #" + data.index + '</span>'
                                            + '<br>' +
                                            '<p>' + '<b>Proof of Work: </b><span id="proofOfWork">' + data.proof  + '</span></p>' +
                                            '<p>' + '<b>Mined at: </b> <span id="blockDate"> ' + data.timestamp_date  + '</span></p>' +
                                            '<p>' + '<b>Time: </b><span id="blockTime">' + data.timestamp_time  + '</span></p>' +
                                            '<p><b>Previous Hash:</b></p>' +
                                            '<p class="hash_number">' + data.previous_hash + '</p>' +
                                            '<p><b>Transactions:</b></p>' +
                                            '<div class="row plain-element row-transactions">' +
                                                '<p class="transaction">'  + transaction1 + '</p>' +
                                               '<p class="transaction">'  + transaction2 + '</p>'
                                        + '</div>'
                                        + '</div>'
                                        + '</div>');
            });
    });
});






