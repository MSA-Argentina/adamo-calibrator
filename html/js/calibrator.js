get_url = get_url_function("calibrator");

var nclicks = 0;
var pointers = [[100, 100], [200, 200]];

function initiate(){
    var screen_resolution = [screen.width, screen.height];
    send('initiate', screen_resolution);
}

function click(e){
    var click_pos = get_click_position(e);
    send('click', click_pos);
}

function move_pointer(x, y){
    var img_pointer = $("#img_pointer")
    img_pointer.css('display', 'inline');
    img_pointer.css('left', x - (parseInt(img_pointer.css('width')) / 2));
    img_pointer.css('top', y - (parseInt(img_pointer.css('height')) / 2));
}

function get_click_position(e) {
    var img_pointer = $("#img_pointer")
    var xPosition = e.clientX;
    var yPosition = e.clientY;
    return [xPosition, yPosition]
}

$(document).ready(function(){
    var screen_resolution = [screen.width, screen.height];
    send('initiate', screen_resolution);
    //Mostrar pantalla de inicio
    //$(document).click(click);
    $(document).click(function(e) {
        var click_pos = get_click_position(e);
        send('click', click_pos);
    });
});

