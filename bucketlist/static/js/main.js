$(document).ready(function(){
    var goBack = function(event){
        event.preventDefault();
        return window.history.back();
    }

    var validate = function(event){
        event.preventDefault();
        var length = $('#id_name').val().length;
        if(length < 1) { 
            if(document.URL.indexOf('items') == -1)
                alert('Please kindly specify a name for your bucketlist');
            else
                alert('Please kindly specify a name for your bucketlist item');
        } else {
            $(this).closest('form').submit();
        }
    }

    var markAsDone = function(event){
        $(this).closest('form').submit();
    }

    $('.btn-cancel').on('click', goBack);
    
    $('#id_submit_btn').on('click', validate);

    $('#id_done_check').on('click', markAsDone);

});