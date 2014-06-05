function misclick_dialog(data){
    $("#error_misclick").css('display', 'block');
}

function doubleclick_dialog(data){
    $("#error_doubleclick").css('display', 'block');
}

function time_dialog(){
    $("#error_time").css('display', 'block');
}

function end_dialog(){
    hide_all();
    $(".indicators").css('display', 'none');
    $(".success").css('display', 'block');
}

function hide_error_dialog(){
    $("#error_misclick").css('display', 'none');
    $("#error_doubleclick").css('display', 'none');
    $("#error_time").css('display', 'none');
}

function hide_all(){
    hide_error_dialog();
    hide_indicators();
    $("#calibration_msg").css('display', 'none');
}

function show_indicators(){
    $("#pointer").css('display', 'inline');
    $("#progress").css('display', 'inline');
}

function hide_indicators(){
    $("#pointer").css('display', 'none');
    $("#progress").css('display', 'none');
}

function show_calibration_msg(){
    $("#calibration_msg").css('display', 'inline');
}
