$(document).ready(function () {
    $('#document').keypress(function (e) {
        if (e.keyCode === 13) {
            e.preventDefault()
            $(this).trigger("enterKey");
            let dni = $(this).val();
            ConsultClient(dni)
        }
    })
})

function ConsultClient(dni) {
    $.ajax({
        url: "/clients/get_client_by_document/",
        type: "get",
        datatype: "json",
        data: {'document': dni},
        success: function (r) {
            $('#first_name').val(r.names)
            $('#last_name').val(r.surnames)
            $('#address').val(r.address)
        },
        error: function (jqXHR, textStatus, errorThrown) {
            toastr.error(jqXHR.responseJSON.error, "Error")
        }
    })
}
