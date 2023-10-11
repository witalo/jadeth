$(function () {
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
        PermissionAll()
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

function PermissionAll() {
    let user = $('#user').val();
    let Detail = {
        "row": [],
        "user": user
    };
    $("tbody#permission_list tr").each(function () {
        let input = $(this).find('td.item-check div input')
        let pk = input.val();
        let state = 0;
        if (input.is(':checked')) {
            state = 1;
        }
        let row = {
            "pk": pk,
            "state": state
        };
        Detail.row.push(row);
    })
    $.ajax({
        url: '/users/create_permission/',
        dataType: 'json',
        type: 'POST',
        data: {'detail': JSON.stringify(Detail)},
        success: function (response) {
            if (response.success) {
                toastr.success(response.message)
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

$("tbody#permission_list tr td.item-check div input").on("click", function () {
    let user = $('#user').val();
    let pk = $(this).val();
    let state = 0;
    if ($(this).is(':checked')) {
        state = 1;
    }
    SavePermission(pk, user, state)
});

function SavePermission(pk, user, state) {
    $.ajax({
        url: '/users/save_permission/',
        async: true,
        dataType: 'json',
        type: 'POST',
        data: {'state': state, 'pk': pk, 'user': user},
        success: function (response, textStatus, xhr) {
            if (xhr.status === 200) {
                toastr.success(response['message'], response['group']);
            } else {
                toastr.error(response['message'])
            }
        },
        fail: function (response) {
            console.log(response);
        }
    });
}