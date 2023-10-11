function OpenAccount(pk) {
    $('#modal-account').empty();
    $.ajax({
        url: '/accounts/get_open_account/',
        async: true,
        dataType: 'json',
        type: 'GET',
        data: {'pk': pk},
        success: function (data) {
            $('#modal-account').html(data.grid).modal('show');
        },
        error: function (response) {
            toastr.error('Ocurrio un problema')
        }
    });
};

function CloseAccount(pk) {
    $('#modal-account').empty();
    $.ajax({
        url: '/accounts/get_close_account/',
        async: true,
        dataType: 'json',
        type: 'GET',
        data: {'pk': pk},
        success: function (data) {
            if (data.success) {
                $('#modal-account').html(data.grid).modal('show');
            } else {
                toastr.error(data.message);
            }
        },
        error: function (response) {
            toastr.error('Ocurrio un problema');
        }
    });
};