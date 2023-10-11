$('#FormStoreUpdate').submit(function (event) {
    event.preventDefault();
    let data = new FormData($('#FormStoreUpdate').get(0));
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
                toastr.success(r.message);
                let tr = $('#product-list').find("tr.row-product[pk=" + r.store.product + "]")
                tr.find('td.item-store span.span-price').text('Precio: ' + parseFloat(r.store.price).toFixed(2))
            } else {
                toastr.error(r.message);
            }
        },
        error: function (r) {
            toastr.error('Ocurrio un problema al registrar');
        }
    });
    // }
});