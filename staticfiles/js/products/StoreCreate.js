$('#FormStoreCreate').submit(function (event) {
    event.preventDefault();
    let data = new FormData($('#FormStoreCreate').get(0));
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
                let ruta = "modal_store_update"
                let tr = $('#product-list').find("tr.row-product[pk=" + r.store.product + "]")
                let html = '<span class="badge badge-warning span-stock">Stock: ' + parseFloat(r.store.quantity).toFixed(2) + '</span><br><span class="badge badge-warning span-price">Precio: ' + parseFloat(r.store.price).toFixed(2) + '</span><br>' +
                    '<button type="button" class="btn btn-warning btn-sm btn-store mt-1" onclick="showModalView(\'' + ruta + '\', ' + r.store.id + ')">' +
                    '<i class="fas fa-pencil-alt"></i>Edit' +
                    '</button>';
                tr.find('td.item-store').html(html)
            } else {
                toastr.error(r, r.message);
            }
        },
        error: function (response) {
            toastr.error(response);
        }
    });
});