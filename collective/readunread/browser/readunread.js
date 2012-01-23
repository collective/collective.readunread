var $ = jQuery.noConflict();

$(document).ready(function(){
    $('.readunread_button').click(function(){
        var $form = $(this).closest('form');
        $.ajax({
            type: "POST",
            url: "mark_as",
            data: $form.serialize(),
            dataType: "json",
            success: function(result){
                if(result.status=='ok'){
                    var to_show = result.marked_as == 'read' ? 'unread' : 'read';
                    var to_hide = result.marked_as == 'read' ? 'read' : 'unread';
                    $form.find('.mark_as_'+to_show).css({'display':'inline'});
                    $form.find('.mark_as_'+to_hide).css({'display':'none'});
                    $form.find('input[name=mark_as]').val(to_show);
                }
            }
        });
        return false;
    });
});