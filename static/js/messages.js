let location = window.location
let wsStart = 'ws.//'

if(loc.protocol === 'http'){
    wsStart = 'ws://'
}

let endpoint = wsStart + loc.host + loc.pathname

var socket = new WebSocket(endpoint)

socket.onopen = async function(e :Event){
    console.log('open', e)
}
socket.onmessage = async function(e :MessageEvent){
    console.log('message', e)
}
socket.onerror = async function(e :ErrorEvent){
    console.log('error', e)
}
socket.onclose = async function(e :CloseEvent){
    console.log('close', e)
}
