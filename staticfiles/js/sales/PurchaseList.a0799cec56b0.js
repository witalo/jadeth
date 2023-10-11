$(document).ready(function () {
    new Autocomplete('#autocomplete-product', {
        search: input => {
            const url = `/products/search_product/?search=${encodeURI(input.toUpperCase())}`

            return new Promise(resolve => {
                if (input.length < 3) {
                    $('#search-code').val('')
                    return resolve([])
                }
                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        resolve(data.product)
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
                    ${'<i class="spinner-grow"></i>'} ${result.name}
                 </div>
                 <div class="text-white-50 h6">
                    MEDIDA: ${result.measure} <br>
                    COLOR : ${result.color} <br>
                    <b class="text-white"> STOCK : ${result.store.quantity} </b><br>
                    PRECIO: S/. ${result.store.price} 
                  </div>
                </li>
                `
        },
        getResultValue: result => result.name,
        onSubmit: result => {
            if (result) {
                AddRowDetail(0, 0, result.pk, result.name, result.measure, result.store.quantity, 'UND', 1, result.store.price, 0)
            }
        }
    })
})

async function AddRowDetail(i, pk, id, name, measure, stock, unit, quantity, price, old) {
    let amount = parseFloat(quantity * price).toFixed(2)
    $('tbody#order_detail').append(
        '<tr class="p-0" product="' + id + '" pk="' + pk + '" i="' + i + '" old="' + old + '">' +
        '<td class="align-middle item-number p-1 text-center">' + '<span class="bs-stepper-circle bg-primary">' + i + '</span>' + '</td>' +
        '<td class="align-middle item-quantity p-1">' + '<input type="number" step="1" min="1" max="' + stock + '" placeholder="0.00" class="form-control value-quantity" value="' + quantity + '"/>' + '</td>' +
        '<td class="align-middle item-description p-1 text-justify">' + name + '</td>' +
        '<td class="align-middle item-unit p-1 text-center">' + unit +
        '<td class="align-middle item-price p-1 text-right">' + '<input type="number" step="0.01" placeholder="0.00" class="form-control text-right value-price" value="' + parseFloat(price).toFixed(2) + '"/>' + '</td>' +
        '<td class="align-middle item-amount p-1 text-right">' + amount + '</td>' +
        '<td class="align-middle item-delete p-1 text-center">' +
        '    <button type="button" class="btn btn-danger rounded">' + '<i class="fa fa-trash-alt">' + '</i>' + '</button>' +
        '</td>' +
        '</tr>'
    );
    CountRow()
    TotalDetail()
    $('#search-product').val('')
}

function CountRow() {
    let index = 1;
    $('tbody#order_detail tr').each(function () {
        $(this).find('td.item-number span').text(index)
        $(this).attr('i', index);
        let pk = $(this).attr('pk');
        let product = $(this).attr('product');
        $(this).find('td.item-delete button').attr('onclick', 'DeleteRowDetail(' + index + ', ' + pk + ', ' + product + ')')
        index++;
    });
};

function TotalDetail() {
    let total = 0;
    $('tbody#order_detail tr td.item-amount').each(function () {
        if ($(this).text()) {
            total = total + parseFloat($(this).text());
        } else {
            total = total + parseFloat("0.00");
        }
    });
    $('#total').val(total.toFixed(2))
    $('#amount').val(total.toFixed(2));
};

function DeleteRowDetail(i, pk, product) {
    let rows = $('tbody#order_detail').find("tr[i=" + i + "][pk=" + pk + "][product=" + product + "]")
    if (parseInt(pk) > 0) {
        let order = $('#id-order').val()
        if (order != '' && parseInt(pk) > 0) {
            let r = confirm("¿Esta seguro de eliminar el detalle?")
            if (r == true) {
                $.ajax({
                    url: '/sales/delete_order_detail/',
                    async: true,
                    dataType: 'json',
                    type: 'GET',
                    data: {'pk': pk, 'o': 'E'},
                    success: function (response) {
                        if (response.success) {
                            rows.remove();
                            CountRow();
                            TotalDetail();
                            toastr.success(response.message)
                        } else {
                            toastr.error(response.message)
                        }
                    },
                });
            }
        } else {
            toastr.error('Necesita buscar una orden')
        }
    } else {
        rows.remove();
        CountRow();
        TotalDetail();
    }
}

$('#document').keypress(function (e) {
    if (e.keyCode === 13) {
        e.preventDefault()
        $(this).trigger("enterKey");
        let document = $('#document').val();
        if ((document.length !== 8)) {
            toastr.warning('El DNI debe contener 8 digitos');
            return false;
        }
        $('#id-loading').css('display', '')
        $.ajax({
            url: '/providers/get_provider/',
            dataType: 'json',
            type: 'GET',
            data: {'document': document},
            success: function (response) {
                if (response.pk) {
                    toastr.success(response.message);
                    $("#provider").val(response.pk);
                    $("#names").val(response.names);
                    $("#phone").val(response.phone);
                    $("#address").val(response.address);
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

$(document).on('change keyup', 'tbody#order_detail tr td.item-quantity input.value-quantity', function () {
    Calculate($(this))
});
$(document).on('change keyup', 'tbody#order_detail tr td.item-price input.value-price', function () {
    Calculate($(this))
});

function Calculate(n) {
    let tr = n.parent('td').parent('tr')
    let p = tr.find('td.item-price input.value-price').val()
    let q = tr.find('td.item-quantity input.value-quantity').val()
    if (isNaN(p) || p === '') {
        p = parseFloat("0.00").toFixed(2)
    }
    if (isNaN(q) || q === '') {
        q = parseFloat("0.00").toFixed(2)
    }
    let td_amount = tr.find('td.item-amount')
    td_amount.text(parseFloat(q * p).toFixed(2))
    TotalDetail()
}

function CreatePurchase() {
    let order = $('#order').val()
    if (isNaN(order) || order === "") {
        order = 0
    }
    console.log(order)
    let provider = $('#provider').val()
    if (isNaN(provider) || provider === "") {
        provider = 0
        toastr.warning('Porfavor ingrese un proveedor')
        return false
    }
    let date = $('#date_current').val()
    if (date === "") {
        toastr.warning('Ingrese la fecha de la compra')
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
    let payment = $('#account').attr("pk")
    let code = $('#code').val()
    let Order = {
        "Detail": [],
        "order": order,
        "provider": provider,
        "date": date,
        "payment": payment,
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
     if (hasRowDetails() === false) {
        toastr.info('Ingrese un producto almenos', 'Mensaje');
        return false;
    }
    if (!status) {
        return false
    } else {
        SendPurchase(Order)
    }
}

function SendPurchase(object) {
    console.log(object)
    let r = confirm('¿ESTA SEGURO DE PROCESAR CON LA COMPRA?');
    if (r === true) {
        $.ajax({
            url: '/sales/purchase_save/',
            dataType: 'json',
            type: 'POST',
            data: {'order': JSON.stringify(object)},
            success: function (response) {
                if (response.success) {
                    toastr.success(response.message)
                    CleanPurchase()
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

function CleanPurchase() {
    $('#provider').val('')
    $('#document').val('')
    $('#names').val('')
    $('#phone').val('')
    $('#address').val('')
    $("tbody#order_detail").empty()
    $("#total").val('0.00')
    $("#order").val('')
    $("#order-search").val('')
    $("#account").attr('pk', '');
    $("#account").val("");
    $("#amount").val("");
    $("#code").val("");
}

$('#order-search').keypress(function (e) {
    if (e.keyCode === 13) {
        e.preventDefault()
        $(this).trigger("enterKey");
        let order = $('#order-search').val();
        if (order !== '') {
            CleanPurchase()
            $('#id-loading').css('display', '')
            $.ajax({
                url: '/sales/get_order/',
                dataType: 'json',
                type: 'GET',
                data: {'order': order, 'type': 'C'},
                success: async function (response) {
                    if (response.pk) {
                        $("#order").val(response.pk);
                        $("#provider").val(response.person);
                        $("#document").val(response.document);
                        $("#names").val(response.names);
                        $("#phone").val(response.phone);
                        $("#address").val(response.address);
                        $("#date_current").val(response.current);
                        $("#account").attr('pk', response.payment);
                        $("#account").val(response.account);
                        $("#amount").val(response.amount);
                        $("#code").val(response.code);
                        AddDetail(response['detail'])
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
    }
});

async function AddDetail(Detail) {
    console.log(Detail)
    for (let i = 0; i < Detail.length; i++) {
        await AddRowDetail(i + 1, Detail[i].pk, Detail[i].id, Detail[i].product, Detail[i].measure, Detail[i].stock.quantity, 'UND', Detail[i].quantity, Detail[i].price, Detail[i].quantity)
    }
}

$('#address').keypress(function (e) {
    if (e.keyCode === 13) {
        e.preventDefault()
        $(this).trigger("enterKey");
        ProviderSave($(this))
    }
});
$('#phone').keypress(function (e) {
    if (e.keyCode === 13) {
        e.preventDefault()
        $(this).trigger("enterKey");
        ProviderSave($(this))
    }
});

function ProviderSave(n) {
    let pk = $('#provider').val();
    if (pk !== '' && pk !== '0') {
        let address = $('#address').val();
        if ((n.val().length <= 5)) {
            toastr.warning('Ingrese 5 caractares almenos');
            return false;
        }
        let phone = $('#phone').val();
        $('#id-loading').css('display', '')
        $.ajax({
            url: '/providers/provider_save/',
            dataType: 'json',
            type: 'POST',
            data: {'pk': pk, 'address': address, 'phone': phone},
            success: function (response) {
                if (response.pk) {
                    toastr.success(response.message);
                    $("#provider").val(response.pk);
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
}

$(document).on('change keyup', '#account', function () {
    SumDetailSales()
    $.ajax({
        url: '/accounts/validate_account/',
        dataType: 'json',
        type: 'GET',
        data: {'pk': $(this).val()},
        success: function (response) {
            if (response.success) {
                toastr.success(response.message);
            } else {
                toastr.error(response.message)
                $("#account").val("")
            }
        },
        fail: function (response) {
            toastr.error('Ocurrio un problema en el proceso')
            $(this).val("")
        }
    });
})

function SumDetailSales() {
    let total = parseFloat('0.00')
    $('tbody#order_detail tr').each(function () {
        let amount = parseFloat($(this).find('td.item-amount').text());
        total = total + amount
        $('#amount').val(total.toFixed(2));
    });
}
function hasRowDetails() {
    var r = false;
    if ($("tbody#order_detail tr").length > 0) {
        r = true;
    }
    return r;
}