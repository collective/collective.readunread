var $ = jQuery.noConflict();

$(document).ready(function(){
    $('.readunread_action').click(function(){
        var $container = $(this).closest('#readunread_actions');
        $.ajax({
            type: "POST",
            url: "change_read_unread_status?action=" + $(this).attr('id'),
            data: $container.serialize(),
            dataType: "json",
            success: function(result){
                if(result.ret=='ok'){
                    var to_show = result.status == 'read' ? 'unread' : 'read';
                    var to_hide = result.status == 'read' ? 'read' : 'unread';
                    $container.find('#mark_as_'+to_show).css({'display':'inline'});
                    $container.find('#mark_as_'+to_hide).css({'display':'none'});
                    $container.find('#readunread_status').text(result.status)
                }
            }
        });
        return false;
    });
});
