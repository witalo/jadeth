$(function () {
    //Initialize Select2 Elements
    $('.select2').select2()
    //Initialize Select2 Elements
    $('.select2bs4').select2({
        theme: 'bootstrap4'
    })
    // $('#FormProductCreate').validate({
    //     rules: {
    //         name: {
    //             required: true,
    //             minlength: 3
    //         },
    //         measures: {
    //             required: true,
    //             minlength: 1
    //         },
    //         description: {
    //             required: false
    //         },
    //         brand: {
    //             required: true
    //         },
    //         model: {
    //             required: true
    //         },
    //         color: {
    //             required: true
    //         },
    //     },
    //     messages: {
    //         name: {
    //             required: "Por favor, ingresa el nombre del producto",
    //             minlength: "El nombre de producto debe tener al menos 3 caracteres"
    //         },
    //         measures: {
    //             required: "Por favor, ingresa la medida",
    //             minlength: "la medida debe tener almenos 3 caracteres"
    //         },
    //         brand: {
    //             required: "Por favor, seleccione la marca del producto"
    //         },
    //         model: {
    //             required: "Por favor, seleccione el modelo del producto"
    //         },
    //         color: {
    //             required: "Por favor, seleccione almenos un color del producto"
    //         }
    //     },
    //     errorElement: 'span',
    //     errorPlacement: function (error, element) {
    //         error.addClass('invalid-feedback');
    //         element.closest('.form-group').append(error);
    //     },
    //     highlight: function (element, errorClass, validClass) {
    //         $(element).addClass('is-invalid');
    //     },
    //     unhighlight: function (element, errorClass, validClass) {
    //         $(element).removeClass('is-invalid');
    //     }
    // });
    //Date picker
    // $('#date-init').datetimepicker({
    //     format: 'DD/MM/YYYY'
    // });
    // $('#date-end').datetimepicker({
    //     format: 'DD/MM/YYYY'
    // });
    $('#brand').trigger('change')
})
$(document).on('change keyup', '#brand', function () {
    let brand = $(this).val()
    if (brand !== "" && brand !== "0" && brand !== 0 && brand !== null){
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
            toastr.error('Error en la petición');
        }
    });
}

$('#FormProductCreate').submit(function (event) {
    event.preventDefault();
    let data = new FormData($('#FormProductCreate').get(0));
    // if (validate()) {
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
                toastr.error(response, response.message);
            }
        },
        error: function (response) {
            toastr.error('Ocurrio un problema al registrar');
        }
    });
    // }
});
