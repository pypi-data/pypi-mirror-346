jQuery(document).ready(function($) {
    $('.schedule-mask-widget').each(function(){
        input = $(this);
        input.mask('99:99');
    });
});
