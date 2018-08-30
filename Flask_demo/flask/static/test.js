var socket = io.connect(location.protocol + "//" + document.domain + ":" + location.port);
function cli(){
    socket.emit('msg',{'param':'value'});
    socket.on('res',function(data){
        alert(data)
    });
}