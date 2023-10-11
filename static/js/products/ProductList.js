// $(function () {
//     //Initialize Select2 Elements
//     $('.select2').select2()
//     //Initialize Select2 Elements
//     $('.select2bs4').select2({
//         theme: 'bootstrap4'
//     })
// })
function showModalView(route, n) {
    $.ajax({
        url: '/products/' + route + '/',
        dataType: 'json',
        type: 'GET',
        data: {'pk': n},
        success: function (response) {
            if (response.success) {
                $('#modal-product').empty().html(response.form).modal('show');
            }
        },
        fail: function (response) {
            toastr.error('Error en la petición');
        }
    });
};