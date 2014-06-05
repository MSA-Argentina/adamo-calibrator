function set_locale(data_locale){
    $('#title').text(data_locale.title);
    $('#init_msg').text(data_locale.init_msg);
    $('#calibration_msg').text(data_locale.calibration_msg);
    $('#error_misclick').text(data_locale.error_misclick);
    $('#error_doubleclick').text(data_locale.error_doubleclick);
    $('#error_time').text(data_locale.error_time);
    $('#finish_msg').text(data_locale.finish_msg);
}

function set_locale_manual(data_locale){
    $('#title').text("Adamo Calibrator");
    $('#init_msg').text("Presione la pantalla para continuar o espere para salir...");
    $('#calibration_msg').text("Presione el puntero o espere para salir...");
    $('#error_misclick').text("Click incorrecto detectado.");
    $('#error_doubleclick').text("Doble click detectado.");
    $('#error_time').text("Por favor mantenga presionado el puntero más tiempo.");
    $('#finish_msg').text("Su pantalla ha sido calibrada.");
}

function show_all(){
    $('#title').css('display', 'block');
    $('#init_msg').css('display', 'block');
    $('#calibration_msg').css('display', 'block');
    $('#error_misclick').css('display', 'block');
    $('#error_doubleclick').css('display', 'block');
    $('#error_time').css('display', 'block');
    $('#finish_msg').css('display', 'block');
}
