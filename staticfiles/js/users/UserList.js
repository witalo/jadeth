function ShowModalUserPermission(pk) {
    $.ajax({
        url: '/users/modal_user_permission/',
        dataType: 'json',
        type: 'GET',
        data: {'pk': pk},
        success: function (response) {
            if (response.success) {
                $('#modal-user-permission').empty().html(response.form).modal('show');
            }
        },
        fail: function (response) {
            toastr.error('Error en la petición');
        }
    });
};