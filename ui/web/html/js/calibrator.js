get_url = get_url_function("calibrator");

function initiate(){
    var screen_resolution = [screen.width, screen.height];
    send('initiate', screen_resolution);
}

function click(e){
    $("#error").css('display', 'none');
    var click_pos = get_click_position(e);
    send('click', click_pos);
}

function move_pointer(xy){
    var img_pointer = $("#img_pointer");
    img_pointer.css('display', 'inline');
    img_pointer.css('left', xy[0] - (parseInt(img_pointer.css('width')) / 2));
    img_pointer.css('top', xy[1] - (parseInt(img_pointer.css('height')) / 2));
}

function get_click_position(e) {
    var img_pointer = $("#img_pointer")
    var xPosition = e.clientX;
    var yPosition = e.clientY;
    return [xPosition, yPosition]
}

function ready() {
    $("#img_pointer").css('display', 'inline');
    send('ready');
}

function misclick(data){
    $("#error-msg").text("Misclick Detected on " + data);
    $("#error").css('display', 'inline');
}

function doubleclick(data){
    $("#error-msg").text("Doubleclick Detected on " + data);
    $("#error").css('display', 'inline');
}

$(document).ready(function(){
    //Sending a screen resolution to backend
    var screen_resolution = [screen.width, screen.height];
    send('initiate', screen_resolution);

    //Adding click event
    $(document).click(function(e) {
        var click_pos = get_click_position(e);
        send('click', click_pos);
    });
});

