function diecutter_url( path ) {
    if( path === undefined ) {
        path = $('#diecutter_resource').val();
        if( path !== '' && path[0] != '/') {
            path = '/' + path;
            $('#diecutter_resource').val(path);
        }
        path = $('#diecutter_prefix').html() + path;
    }
    service = $('#diecutter_service').val();
    url = service + path;
    return url;
}

/* POST to diecutter resource. */
function post_diecutter( values ) {
    url = diecutter_url();
    data_form = $('<form method="POST">');
    data_form.attr('action', url);
    for (key in values) {
        data_form.append('<input type="hidden" name="cookiecutter.'+key+'" value="'+ values[key] +'"/>');
    }
    $('body').append(data_form);
    console.log(data_form);
    data_form.submit();
}


(function ( $ ) {
    var diecutter_form = null;
    var data_form_prefix = 'cookiecutter_';
    var data_form = null;

    /* Return URL for resource.
     *
     * Path is built with the following values:
     *
     * - value of the input with id="diecutter_service"
     * - value of the span with id="diecutter_prefix"
     * - value of the input with id="diecutter_resource"
     *
     */
    /* Set client form's "action" attribute to event's subject value. */
    function update_form_action( event ) {
        url = diecutter_url();
        data_form.attr('action', url);
    }

    /* GET to diecutter service root. */
    function get_diecutter_service_status( event ) {
        // Disable button.
        $( '#diecutter_service_test' ).attr('disabled', 'disabled');
        // Display processing message in place of status.
        $( '#diecutter_service_status' ).siblings('.loading').show();
        // AJAX call.
        url = diecutter_url( '/' );
        $.ajax( url, {
            type: 'GET',
            dataType: 'json',
            crossDomain: true,
            processData: false,
            error: function ( jqXHR, textStatus, errorThrown ) {
                $( '#diecutter_service_status' )
                    .removeClass( 'badge-success' )
                    .addClass( 'badge-important' );
                $( '#diecutter_service_status > i' )
                    .removeClass( 'icon-question-sign' )
                    .removeClass( 'icon-ok-circle' )
                    .addClass( 'icon-warning-sign' );
            },
            success: function ( data, textStatus, jqXHR ) {
                $( '#diecutter_service_status' )
                    .removeClass( 'badge-important' )
                    .addClass( 'badge-success' );
                $( '#diecutter_service_status > i' )
                    .removeClass( 'icon-question-sign' )
                    .removeClass( 'icon-warning-sign' )
                    .addClass( 'icon-ok-circle' );
            },
            complete: function ( jqXHR, textStatus ) {
                $( '#diecutter_service_status' ).siblings('.loading').hide();
                $( '#diecutter_service_test' ).removeAttr('disabled');
            }
        });
        return false;
    }

    /* GET diecutter resource. */
    function get_diecutter_resource( event ) {
        $( '#get_resource_form' ).attr( 'action', diecutter_url() );
        $( '#get_resource_form' ).submit();
        return false;
    }

    $(document).ready(function() {
        diecutter_form = $('#diecutter_form');
        data_form = $('#' + data_form_prefix + 'form');

        update_form_action();
        get_diecutter_service_status();

        // Event listeners.
        $( '#diecutter_service' )
            .on( 'change', get_diecutter_service_status );
        $( '#diecutter_service_test' )
            .on( 'click', get_diecutter_service_status );
        $( '#diecutter_resource_get' )
            .on( 'click', get_diecutter_resource );
        $( '#diecutter_service' ).on( 'change', update_form_action );
        $( '#diecutter_resource' ).on( 'change', update_form_action );
    });
})( jQuery );
