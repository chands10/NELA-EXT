$(".js-range-slider").ionRangeSlider({
    skin: "square",
    hide_from_to: true,
    hide_min_max: true,
    grid_num: -1
});

//DEAD CODE
$("#btn_reset_fields").click(function() {
    resetSliders();
    toggleAlert(); //in handleFilters.js
});

//DEAD CODE
function resetSliders() {
	sliders = $(".js-range-slider");
     jQuery(sliders).each(function(index,slider){
         slider_instance = jQuery(slider).data("ionRangeSlider");
         slider_instance.update({
	        from: slider_instance.result.min,
	        to: slider_instance.result.max
	    });
     });

     //taken from https://stackoverflow.com/questions/1531093/how-do-i-get-the-current-date-in-javascript
     var today = new Date();
     var dd = String(today.getDate()).padStart(2, '0');
     var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0
     var yyyy = today.getFullYear();

     today = mm + '/' + dd + '/' + yyyy;

     document.getElementById("daterange").value = "01/01/2010 - " + today;
}