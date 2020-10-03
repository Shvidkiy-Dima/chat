import React from 'react'
import Dispatch from './components/dispatch'
import WebSocketConnection from './utils/ws'

function App() {

  let ws = new WebSocketConnection()
  console.log('APP')

  return (
           <Dispatch ws={ws}/>
    )
}

export default App;
