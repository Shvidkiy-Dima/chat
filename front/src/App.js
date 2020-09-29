import React from 'react'
import Auth from './components/auth'
import WebSocketConnection from './utils/ws'

function App() {

  let ws = new WebSocketConnection()
  console.log('APP')

  return (
           <Auth ws={ws}/>
    )
}

export default App;
