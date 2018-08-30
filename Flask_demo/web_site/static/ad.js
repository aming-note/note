var socket = io.connect(location.protocol + "//" + document.domain + ":" + location.port);
function cli(key) {
    socket.emit('button',key);
    socket.on('msg',function (data) {
        window.location.href=data
    });
}