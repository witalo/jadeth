$(document).ready(function () {
    new Autocomplete('#autocomplete-provider', {
        search: input => {
            const url = `/providers/search_provider/?search=${encodeURI(input.toUpperCase())}`

            return new Promise(resolve => {
                if (input.length < 3) {
                    // $('#search-code').val('')
                    return resolve([])
                }
                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        resolve(data.p)
                    })
            })
        },
        renderResult: (result, props) => {
            let group = ''
            if (result.index % 3 === 0) {
                group = '<li class="group">Group</li>'
            }
            return `
                ${group}
                <li ${props} class="font-weight-bold">
                 <div class="text-white-50 h5">
                    ${'<i class="spinner-grow"></i>'} ${result.names}
                 </div>
                 <div class="text-white-50 h6">
                    NRO DOCUMENTO: ${result.document}
                  </div>
                </li>
                `
        },
        getResultValue: result => result.names,
        onSubmit: result => {
            if (result) {
                SearchProvider(result.document)

            }
        }
    })
})

function SearchProvider(dni) {
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

function DeleteItem(d) {
    if (parseInt(d) > 0) {
        let rows = $('tbody#order_detail').find("tr[pk=" + d + "]")
        rows.remove();
        SumDetail()
    }
}