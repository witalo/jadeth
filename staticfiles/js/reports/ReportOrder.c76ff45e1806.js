$(function () {
    //Initialize Select2 Elements
    $('.select2').select2()
    //Initialize Select2 Elements
    $('.select2bs4').select2({
        theme: 'bootstrap4'
    })
    //Enable check and uncheck all functionality
    $('.checkbox-toggle').click(function () {
        var clicks = $(this).data('clicks')
        if (clicks) {
            //Uncheck all checkboxes
            $('.mailbox-messages input[type=\'checkbox\']').prop('checked', false)
            $('.checkbox-toggle .far.fa-check-square').removeClass('fa-check-square').addClass('fa-square')
        } else {
            //Check all checkboxes
            $('.mailbox-messages input[type=\'checkbox\']').prop('checked', true)
            $('.checkbox-toggle .far.fa-square').removeClass('fa-square').addClass('fa-check-square')
        }
        $(this).data('clicks', !clicks)
    })

    //Handle starring for font awesome
    $('.mailbox-star').click(function (e) {
        e.preventDefault()
        //detect type
        var $this = $(this).find('a > i')
        var fa = $this.hasClass('fa')

        //Switch states
        if (fa) {
            $this.toggleClass('fa-star')
            $this.toggleClass('fa-star-o')
        }
    })
})

function SearchOrder() {
    let init = $('#init').val()
    let end = $('#end').val()
    let type = $('#type').val()
    if (type === '0') {
        toastr.info('Seleccione el tipo de orden')
        return false
    }
    if ((init && end) === '') {
        toastr.info('Seleccione las fechas correctamente')
        return false
    }
    $('#loader').css('display', '')
    $.ajax({
        url: '/sales/get_orders/',
        async: true,
        dataType: 'json',
        type: 'GET',
        data: {
            'type': type,
            'init': init,
            'end': end
        },
        success: function (response) {
            $('#loader').css('display', 'none')
            $('span.item-count').text("1-" + response.count + "/" + response.count)
            $('#order_list').empty().html(response['grid']);
        },
        fail: function (response) {
            $('#loader').css('display', 'none')
            toastr.error('Error de operación!');
        }
    });
}

$(document).ready(function () {
    $("#buscador").keyup(function () {
        _this = this;
        // Show only matching TR, hide rest of them
        $.each($("table#tabla tbody tr"), function () {
            if ($(this).text().toLowerCase().indexOf($(_this).val().toLowerCase()) === -1)
                $(this).hide();
            else
                $(this).show();
        });
    });
});
// document.addEventListener("DOMContentLoaded", function () {
//     const buscador = document.getElementById("buscador");
//     const tabla = document.getElementById("tabla");
//     const filas = tabla.getElementsByTagName("tr");
//
//     buscador.addEventListener("keyup", function () {
//         const valor = buscador.value.toLowerCase();
//
//         for (let i = 1; i < filas.length; i++) {
//             const fila = filas[i];
//             const textoFila = fila.textContent.toLowerCase();
//
//             if (textoFila.includes(valor)) {
//                 fila.style.display = "";
//             } else {
//                 fila.style.display = "none";
//             }
//         }
//     });
// });

