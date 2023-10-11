$(document).ready(function () {

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
    if (brand !== "" && brand !== "0" && brand !== 0)
        SelectBrand(brand, $('#model').empty())
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
            toastr.error('Error en la petición');
        }
    });
}

$('#FormProductUpdate').submit(function (event) {
    event.preventDefault();
    let data = new FormData($('#FormProductUpdate').get(0));
    $.ajax({
        url: $(this).attr('action'),
        type: $(this).attr('method'),
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        headers: {"X-CSRFToken": '{{ csrf_token }}'},
        success: function (response) {
            if (response.success) {
                toastr.success(response.message);
                setTimeout(() => {
                    location.reload();
                }, 500);
            } else {
                toastr.error(response.message);
            }
        },
        error: function (response) {
            toastr.error('Ocurrio un problema al registrar');
        }
    });
});