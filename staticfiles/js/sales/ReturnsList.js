$(function () {
    //Enable check and uncheck all functionality
    $('.checkbox-toggle').click(function () {
        var clicks = $(this).data('clicks')
        if (clicks) {
            //Uncheck all checkboxes
            $('.mailbox-messages input[type=\'checkbox\']').prop('checked', false)
            $('.checkbox-toggle .far.fa-check-square').removeClass('fa-check-square').addClass('fa-square')
        } else {
            //Check all checkboxes
            $('.mailbox-messages input[type=\'checkbox\']').prop('checked', true)
            $('.checkbox-toggle .far.fa-square').removeClass('fa-square').addClass('fa-check-square')
        }
        $(this).data('clicks', !clicks)
    })

    //Handle starring for font awesome
    $('.mailbox-star').click(function (e) {
        e.preventDefault()
        //detect type
        var $this = $(this).find('a > i')
        var fa = $this.hasClass('fa')

        //Switch states
        if (fa) {
            $this.toggleClass('fa-star')
            $this.toggleClass('fa-star-o')
        }
    })
})

$('#search-dni').keypress(function (e) {
    if (e.keyCode === 13) {
        e.preventDefault()
        $(this).trigger("enterKey");
        let dni = $('#search-dni').val();
        if ((dni.length < 8)) {
            toastr.warning('El documento debe contener almenos 8 digitos');
            return false;
        }
        $('#id-loading').css('display', '')
        $.ajax({
            url: '/sales/get_pawns_by_provider/',
            dataType: 'json',
            type: 'GET',
            data: {'dni': dni},
            success: function (response) {
                if (response.success) {
                    toastr.success(response.message);
                    $('#return-list').empty().html(response['grid']);
                } else {
                    toastr.error(response.message)
                }
                $('#id-loading').css('display', 'none')
            },
            fail: function (response) {
                toastr.error('Ocurrio un problema en el proceso')
            }
        });
    }
});

function showModalReturn(n) {
    $.ajax({
        url: '/sales/modal_return_pawns/',
        dataType: 'json',
        type: 'GET',
        data: {'pk': n},
        success: function (response) {
            if (response.success) {
                $('#modal-returns').empty().html(response.form).modal('show');
            }
        },
        fail: function (response) {
            toastr.error('Error en la petición');
        }
    });
};