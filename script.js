// function clear_canvas() {
// 	document.getElementById("canvas").src += "";
// }

function changeTheme(theme) {
	// document.getElementById("stylebutton").class = "disabled";
	document.getElementById("theme").href = theme+".css";
}


comment = document.getElementById("swaphover");
open = document.getElementById("open_canvas");
if (location.hostname === "localhost" || location.hostname === "127.0.0.1") {
	comment.innerHTML = "Connected!"
	document.getElementById("open_canvas").style.display = "none";
} else if (location.hostname === "") {
	comment.innerHTML = "Not connected"
	document.getElementById("send_button").className = "disabled";
} else {
	alert("Idk");
}


// hidden = document.getElementById("hide");
// window.onscroll = function() {scrollFunction()};
// function scrollFunction() {
//   if (document.body.scrollTop > 10 || document.documentElement.scrollTop > 10) {
//     hidden.style.display = "none";
//   } else {
//     hidden.style.display = "block";
//   }
// }