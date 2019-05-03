
$('.dropdown-trigger').dropdown();


$(".alert-user").delay(3000).fadeOut(400, function() {
    $(this).alert('close');
});




$(document).ready(function() {

    $('.sidenav').sidenav();

    $('.modal').modal();

    $('#closeModal').click(function(){
        $('.modal').closeModal();
    });



    $('.tooltipped').tooltip();

    $('.blockMining').on('click', function(){
        $.ajax({
                    type : 'POST',
                    url : '/mine_block'
        })
        .done(function(data) {

            if (data.transactions.length >= 2){
                var transaction1 = data.transactions[0]['sender'] + ' sends ' + data.transactions[0]['amount'] + ' coins to ' + data.transactions[0]['receiver'];
                var transaction2 = data.transactions[1]['sender'] + ' sends ' + data.transactions[1]['amount'] + ' coins to ' + data.transactions[1]['receiver'];
            }

            else if (data.transactions.length == 1) {
                var transaction1 = data.transactions[0]['sender'] + ' sends ' + data.transactions[0]['amount'] + ' coins to ' + data.transactions[0]['receiver'];
                var transaction2 = "" ;

            }


            else {
                var transaction1 = "";
                var transaction2 = "";
            }

            $('#blockIndex').text("Block #" + data.index);
            $('#proofOfWork').text(data.proof);
            $('#HashNumber').text(data.previous_hash);
            $('#blockDate').text(data.timestamp_date);
            $('#blockTime').text(data.timestamp_time);
            $('#transaction1').text(transaction1);
            $('#transaction2').text(transaction2);

            $('#minedBlock').fadeOut(300).fadeIn(300);
            $("#rowBlockchain").prepend('<div class="col-md-4">' +
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

    $('.validationCheck').on('click', function(){
        $.ajax({
                    type : 'POST',
                    url : '/validation_check'
        })
        .done(function(data) {
            if (data.error) {
                $('#messageError').text(data.message + '. Current length: ' + data.length).show().fadeOut(3000);
                $('#messageAlert').hide();
            }
            else {
                $('#messageAlert').text(data.message + '. Current length: ' + data.length).show().fadeOut(3000);
                $('#messageError').hide();
            }
        });

    });

    $('#formTransaction').on('submit', function(event){
        $.ajax({
                data : {
				sender : $('#sender').val(),
				receiver : $('#receiver').val(),
				amount : $('#amount').val()
                },
                type : 'POST',
                url : '/add_transaction'

        })

        .done(function(data){
            $('#messageAlert').text(data.message).show().fadeOut(3000);
            $('#messageError').hide();
        });
        $('.modal').modal();
        $('body').css({
            overflow: 'visible'
        });
        event.preventDefault();
    });


    $('#formConverter').on('submit', function(event){
        $.ajax({
                data : {
				bits : $('#bits').val(),
                },
                type : 'POST',
                url : '/converter'

        })
         .done(function(data){
            $('#targetValue').text(data.target);
         });
        event.preventDefault();
    });
});






