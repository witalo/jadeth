$(function () {
    //Initialize Select2 Elements
    $('.select2').select2()
    //Initialize Select2 Elements
    $('.select2bs4').select2({
        theme: 'bootstrap4'
    })
    $('#brand').trigger('change')
})
$(document).on('change keyup', '#brand', function () {
    let brand = $(this).val()
    if (brand !== "" && brand !== "0" && brand !== 0 && brand !== null) {
        SelectBrand(brand, $('#model').empty())
    }
});

function SelectBrand(brand, object) {
    $.ajax({
        url: '/products/get_model_by_brand/',
        dataType: 'json',
        type: 'GET',
        data: {'brand': brand},
        success: function (r) {
            if (r.success) {
                let model = JSON.parse(r['model']);
                model.forEach(element =>
                    object.append(
                        '<option value="' + element['pk'] + '">' + element['fields']['name'] + '</option>')
                )
            }
        },
        fail: function (r) {
            toastr.error(r, 'Error en la petición');
        }
    });
}

$('#FormPawnsCreate').submit(function (event) {
    event.preventDefault();
    let data = new FormData($('#FormPawnsCreate').get(0));
    // if (validate()) {
    $.ajax({
        url: $(this).attr('action'),
        type: $(this).attr('method'),
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        headers: {"X-CSRFToken": '{{ csrf_token }}'},
        success: function (r) {
            if (r.success) {
                var content = '<i class="fas fa-thumbs-up"></i> ¡' + r.message + '!';
                toastr.success(content);
                $('#btn-modal-close').trigger('click')
                AddRowDetail(0, 0, r.product.id, r.product.name, r.product.measure, 0, 'UND', 1, 0, 0)
            } else {
                toastr.error(r, r.message);
            }
        },
        error: function (r) {
            toastr.error(r, 'Ocurrio un problema al registrar');
        }
    });
    // }
});