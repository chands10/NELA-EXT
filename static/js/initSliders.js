$(".js-range-slider").ionRangeSlider({
    skin: "square",
    hide_from_to: true,
    hide_min_max: true,
    grid_num: -1
});

$("#btn_reset_fields").click(function() {
    resetSliders();
    toggleAlert(); //in handleFilters.js
});

function resetSliders() {
	sliders = $(".js-range-slider");
     jQuery(sliders).each(function(index,slider){
         slider_instance = jQuery(slider).data("ionRangeSlider");
         slider_instance.update({
	        from: slider_instance.result.min,
	        to: slider_instance.result.max
	    });
     });
}