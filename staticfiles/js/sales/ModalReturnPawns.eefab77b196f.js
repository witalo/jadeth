$(document).ready(function () {
    SumDetail()
})

function SumDetail() {
    let total = parseFloat('0.00')
    $('tbody#order_detail tr').each(function () {
        let amount = parseFloat($(this).find('td.item-amount').text());
        total = total + amount
        $('#amount').val(total.toFixed(2));
    });
}

$(document).on('change keyup', '#account', function () {
    SumDetail()
})

$(document).on('change keyup', 'tbody#order_detail tr td.item-price input.value-price', function () {
    let price = $(this).val()
    if (isNaN(price) || price == '') {
        price = parseFloat('0.00')
    } else {
        price = parseFloat($(this).val())
    }
    let row = $(this).parent('td.item-price').parent('tr')
    let quantity = parseFloat(row.find('td.item-quantity input.value-quantity').val())
    row.find('td.item-amount').text(parseFloat(quantity * price).toFixed(2))
    SumDetail()
});

function SaveReturn() {
    let order = $('#order').val()
    if (isNaN(order) || order === "") {
        toastr.in('No se logro identificar la orden')
        return false
    }
    let date = $('#date').val()
    if (date === "") {
        toastr.warning('Ingrese la fecha de la entrega')
        return false
    }
    let account = $('#account').val()
    if (account === "") {
        toastr.warning('Seleccione una caja o cuenta')
        return false
    }
    let amount = $('#amount').val()
    if (amount === "") {
        toastr.warning('Ingrese el monto a pagar')
        return false
    }
    let code = $('#code').val()
    let Order = {
        "Detail": [],
        "order": order,
        "date": date,
        "account": account,
        "amount": amount,
        "code": code
    };
    let status = true
    $("tbody#order_detail tr").each(function () {
        let row = $(this)
        let pk = row.attr('pk')
        let i = row.attr('i')
        let product = row.attr('product')
        if (product === '0' || product === '') {
            toastr.info('Producto desconocido en la fila ' + i.toString())
            status = false
            return status
        }
        let quantity = row.find('td.item-quantity input.value-quantity').val()
        if (parseFloat(quantity) === 0 || quantity === '') {
            toastr.info('Ingrese una cantidad en la fila ' + i.toString())
            status = false
            return status
        }
        let price = row.find('td.item-price input.value-price').val()
        if (parseFloat(price) === 0 || price === '') {
            toastr.info('Ingrese un precio en la fila ' + i.toString())
            status = false
            return status
        }
        let old = row.attr('old')
        if (old === "") {
            old = parseFloat('0.00').toFixed(2)
        }
        let Detail = {
            "detail": pk,
            "product": product,
            "quantity": parseFloat(quantity).toFixed(2),
            "old": parseFloat(old).toFixed(2),
            "price": parseFloat(price).toFixed(2)
        };
        Order.Detail.push(Detail);
    })
    if (!status) {
        return false
    } else {
        SendReturn(Order)
    }
}

function SendReturn(object) {
    console.log(object)
    let r = confirm('¿ESTA SEGURO DE PROCESAR EL PAGO Y LA DEVOLUCION?');
    if (r === true) {
        $.ajax({
            url: '/sales/return_save/',
            dataType: 'json',
            type: 'POST',
            data: {'order': JSON.stringify(object)},
            success: function (response) {
                if (response.success) {
                    toastr.success(response.message)
                    let td = '<i class="fas fa-star text-success"></i>' + response.status;
                    $('tbody#table_return_list tr').find('td.i-status').html(td)
                    $('#btn-modal-close').trigger('click')
                } else {
                    toastr.error(response.message)
                }
            },
            error: function (jqXhr, textStatus, xhr) {
                if (jqXhr.status === 500) {
                    toastr.error(jqXhr.responseJSON.error, '¡Error!');
                }
            }
        });
    }
}
