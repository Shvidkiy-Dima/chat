class WebSocketConnection {
    constructor(){
        this.ws = null
        this.connected = false
        this.dispatch = {}
    }

    connect(path){
    if (!this.connected) {
        let url = ((window.location.protocol === "https:") ? "wss://" : "ws://") + window.location.host + path
        this.ws = new WebSocket(url)
        this.ws.onopen = ()=> {
            this.connected = true
            console.log('OPEN')

        }
        this.ws.onmessage = (response)=> {
          response = JSON.parse(response.data)
          let method = this.dispatch[response['type']]
          method(response['data'])
        }
        this.ws.onclose = ()=> {
        console.log('Close!')
        this.connected = false
        }
        }
    }

    close(){
        if (this.ws){
            this.ws.close()
        }

    }

    event_subscribe(){
        let token = 'JWT ' + sessionStorage.getItem('access')
        if (!token){
            return
        }
        let user_data = JSON.stringify({event: 'subscribe', data: {jwt: token}})
        this.send(user_data)
    }

    send(data){
        let count = 0
            function waitForSocketConnection(socket){
                count++
                if (count < 100000) {
                    setTimeout(
                        function () {
                            if (socket.readyState === 1) {
                                console.log("Connection is made")
                                socket.send(data)
                            }
                            else {
                                console.log("wait for connection..." + count)
                                waitForSocketConnection(socket);
                            }

                    }, 10);
            }
          }
      waitForSocketConnection(this.ws)
  }

}

export default WebSocketConnection
