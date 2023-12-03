const loc = window.location;
const wsStart = loc.protocol === 'https:' ? 'wss://' : 'ws://';
const endpoint = wsStart + loc.host + '/ws/chat/';

const socket = new WebSocket(endpoint);
const inputMessage = $('#input-message');
const messageBody = $('.message-body');
const send_message_form = $('#send-message-form');

socket.onopen =  async function (event) {
    console.log('WebSocket connection opened:', event);
	send_message_form.on('submit', function(e){
		e.preventDefault()
		let message = inputMessage.val();
		let data = {
			'message': message
		}
		data = JSON.stringify(data)
		socket.send(data)
		$(this)[0].reset()
	})
};

socket.onmessage = async function (event) {
    console.log('WebSocket message received:', event);
    // Handle incoming messages as needed
};

socket.onerror = async function (event) {
    console.error('WebSocket error:', event);
};
 
socket.onclose = async function (event) {
    console.log('WebSocket connection closed:', event);
};


function newMessage(message) {
    if ($.trim(message) === '') {
        return false;
    }
    const messageElement = `
        <div class="d-flex mb-4 replied">
            <div class="msg_cotainer_send">
                ${message}
                <span class="msg_time_send">8:55 AM, Today</span>
            </div>
            <div class="img_cont_msg">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlbpevK2ziShTmJ6CfSY3Doh3v1_70SLMxYg&usqp=CAU" class="rounded-circle user_img_msg">
            </div>
        </div>
    `;

    messageBody.append($(messageElement))
    messageBody.animate({
        scrollTop: $(document).height()
    }, 100);
    inputMessage.val(null);
}
