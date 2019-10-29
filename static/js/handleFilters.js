$(document).ready(function() {
    var fieldsModal = document.getElementById('fieldsModal');
    var source1Modal = document.getElementById('source1Modal');
    var source2Modal = document.getElementById('source2Modal');

    var fieldsBtn = document.getElementById("fieldsBtn");
    var source1Btn = document.getElementById("source1Btn");
    var source2Btn = document.getElementById("source2Btn");

    var fieldsSpan = document.getElementsByClassName("close")[0];
    var source1Span = document.getElementsByClassName("close")[1];
    var source2Span = document.getElementsByClassName("close")[2];



    fieldsBtn.onclick = function() {
      fieldsModal.style.display = "block";
    }

    source1Btn.onclick = function() {
      source1Modal.style.display = "block";
    }

    source2Btn.onclick = function() {
      source2Modal.style.display = "block";
    }

    fieldsSpan.onclick = function() {
      fieldsModal.style.display = "none";
    }

    source1Span.onclick = function() {
      source1Modal.style.display = "none";
    }

    source2Span.onclick = function() {
      source2Modal.style.display = "none";
    }

    window.onclick = function(event) {
      if (event.target == fieldsModal) {
        fieldsModal.style.display = "none";
      } else if (event.target == source1Modal) {
        source1Modal.style.display = "none";
      } else if (event.target == source2Modal) {
        source2Modal.style.display = "none";
      } 
    }
});

function reset(setAllActive, resetOnly) {
    const defaultFilters = ["title1", "title1_date", "title2", "title2_date", 
        "normal_display", "source1", "source2", "sources_display"];

    $(".field-btn").each(function() {
        const isChecked = $(this).prop("checked");
        const index = defaultFilters.indexOf($(this).prop("id"));

        if ((setAllActive && !isChecked) || (!setAllActive && isChecked && !resetOnly) ||
                (resetOnly && (isChecked && index === -1 && !setAllActive) || 
                (!isChecked && index !== -1))) {
            $(this).trigger("click");
        }
    });
}

function toggleAlert(){
    $(".alert").toggleClass('in out'); 
    return false; // Keep close.bs.alert event from removing from DOM
}

//reset(false, true);

/////////////////////////////////////////////////////////////
/** Reset, Select All/Deselect, and Submit button handlers */
/////////////////////////////////////////////////////////////

$("#btn_reset").click(function() {
    reset(false, true);
    toggleAlert();
});

$("#btn_selectall").click(function() {
    const text = $(this).prop("value");
    let selectall = true;

    if (text === "Select all") {
        $(this).prop("value", "Deselect all");
    }
    else {
        $(this).prop("value", "Select all");
        selectall = false;
    }

    reset(selectall, false);
});

$("#btn_selectall_source1").click(function() {
    const text = $(this).prop("value");
    let selectall = true;

    if (text === "Select all") {
        $(this).prop("value", "Deselect all");
    }
    else {
        $(this).prop("value", "Select all");
        selectall = false;
    }

    reset(selectall, false);
});

$("#btn_selectall_source2").click(function() {
    const text = $(this).prop("value");
    let selectall = true;

    if (text === "Select all") {
        $(this).prop("value", "Deselect all");
    }
    else {
        $(this).prop("value", "Select all");
        selectall = false;
    }

    reset(selectall, false);
});

$(".field-btn").change(function() {
    const activeButtons = $(".field-btn:checked").length;

    if(activeButtons) { 
        $("#btn_submit1").prop("disabled", false);
        $("#btn_submit1_source1").prop("disabled", false);
        $("#btn_submit1_source2").prop("disabled", false);        
    }
    else {
        $("#btn_submit1").prop("disabled", true);
        $("#btn_submit1_source1").prop("disabled", false);
        $("#btn_submit1_source2").prop("disabled", false);
    }
});

function submitForms() {
    document.getElementById("source1_form").submit();
    document.getElementById("source2_form").submit();
    document.getElementById("sliders_form").submit();
}