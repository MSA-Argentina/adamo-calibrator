get_url = get_url_function("calibrator");
// SVG stuff
var bg = null;
var ctx = null;
var imd = null;
var circ = Math.PI * 2;
var quart = Math.PI / 2;
var step = 1;
var interval = null;
var progress_speed = 10


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
	var indicators = $(".indicators");
	var img_pointer = $("#pointer");
	var progress = $("#progress");

	indicators.css('display', 'inline');

	img_pointer.css('left', xy[0] - (parseInt(img_pointer.css('width')) / 2));
	img_pointer.css('top', xy[1] - (parseInt(img_pointer.css('height')) / 2));

	progress.css('left', xy[0] - (parseInt(progress.css('width')) / 2));
	progress.css('top', xy[1] - (parseInt(progress.css('height')) / 2));
}

function get_click_position(e) {
	var xPosition = e.clientX;
	var yPosition = e.clientY;
	return [xPosition, yPosition]
}

function ready() {
  	$(".indicators").css('display', 'inline');
	send('ready');
}

function misclick(data){
	$("#error").text("Error: Misclick Detected on " + data);
	$("#error").css('display', 'inline');
}

function doubleclick(data){
	$("#error").text("Error: Doubleclick Detected on " + data);
	$("#error").css('display', 'inline');
}

function time_error(){
	$("#error").text("Error: Please maintain pressed the pointer more time.");
	$("#error").css('display', 'inline');
}

function end(){
	$("#error").css('display', 'none');
	$(".indicators").css('display', 'none');
	$(".success").css('display', 'block');
}

var draw = function(current) {
	ctx.putImageData(imd, 0, 0);
	ctx.beginPath();
	ctx.arc(50, 50, 30, -(quart), ((circ) * current) - quart, false);
	ctx.stroke();
}

function get_click_position(e) {
  var xPosition = e.clientX;
  var yPosition = e.clientY;
  return [xPosition, yPosition]
}

$(document).ready(function(){
	//Sending a screen resolution to backend
	var click_pos = null;
	var screen_resolution = [screen.width, screen.height];
	send('initiate', screen_resolution);

	bg = document.getElementById('progress');
	ctx = bg.getContext('2d');

	ctx.beginPath();
	ctx.strokeStyle = '#0080FF';
	ctx.lineCap = 'square';
	ctx.closePath();
	ctx.fill();
	ctx.lineWidth = 10.0;

	imd = ctx.getImageData(0, 0, 100, 100);

	$(document).mousedown(function(e){
		$("#error").css('display', 'none');
		click_pos = get_click_position(e);
	  	interval = setInterval(function(){
			draw(step / 100);
			step++;
			if (step > 100){
			  	window.clearInterval(interval);
			}
	  	}, progress_speed);
	});

	$(document).mouseup(function(){
	  	ctx.clearRect(0, 0, bg.width, bg.height);
	  	window.clearInterval(interval);
	  	if (step < 100){
			time_error()
	  	}
	  	else{
			send('click', click_pos);
	  	}
	  	step = 1;
	});
});

