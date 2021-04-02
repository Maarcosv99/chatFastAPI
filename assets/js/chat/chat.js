var app = new Vue({
    el: '#chat',
    delimiters: ['${', '}'],
    data: {
        message: '',
        messages: [],
        username: 'Anonimo',
        socket: null
    },
    created: function() {
        this.getUsername();
        this.socket = new WebSocket('ws://' + window.location.host + '/ws');
        setInterval(() => this.socket.send(JSON.stringify({'event': 'echo'})), 500);

        this.socket.onmessage = ((ev) => {
            const response = JSON.parse(ev.data);
            this.newMessage(response);
        });
    },
    methods: {
        setUsername: function(username) {
            document.cookie = "username=" + username;
            this.username = username;
        },
        getUsername: function() {
            username = getCookie('username');
            if (username == '') {
                username = prompt('Qual o seu nome de usuário?');
                this.setUsername(username);
            } else {
                this.username = username;
            }
        },
        sendMessage: function() {
            var date = new Date();
            if (date.getHours() < 10){
                hora = '0' + date.getHours();
            } else {hora = date.getHours();}
            if (date.getMinutes() < 10) {
                minuto = '0' + date.getMinutes();
            } else {minuto = date.getMinutes();}
            

            var msg = {
                'message': this.message,
                'user': this.username,
                'time': hora + ':' + minuto
            }

            this.socket.send(JSON.stringify(msg));
            this.messages.push(msg);
            this.message = '';
        },
        newMessage: function(response) {
            console.log(response['message']);
            if (response['user'] != this.username) {
                this.messages.push({
                    'message': response['message'],
                    'user': response['user'],
                    'time': response['time']
                });
            }
        }
    }
})