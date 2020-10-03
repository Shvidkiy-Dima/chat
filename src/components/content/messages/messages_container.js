import React from 'react'
import Message from './message'
import SendMessage from './send_message'
import Context from '../../../utils/context'
import Loader from '../../loader'

export default function MessagesContainer({current_dialog, msgs, setMessages}){
  let [loader, setLoader] = React.useState(false)
  let {request} = React.useContext(Context)
  let freeze = false

  function _GetMessages(url, callback){
      request({method: 'get', url},
       (res)=>{
            if (callback) {
                callback(res)
                }
        })
    }

  function GetMessages(){
       if (current_dialog === null){
            return
       }
        setLoader(true)
       _GetMessages('/dialog/' + current_dialog.id + '/message/',
            (res)=>{
                setLoader(false)
                setMessages({data: res.data['results'].reverse(), next: res.data['next']})
                let block = document.getElementById("messages-container");
                block.scrollTop = block.scrollHeight;
       })
  }

  function CheckScroll(e){

    if (((e.target.scrollTop - (e.target.offsetHeight-100)) < 0) && msgs.next !== null && !freeze){
        freeze = true
        _GetMessages(msgs.next, (res)=>{

           let new_data = res.data['results'].reverse().filter((msg)=>
                                                                msgs.data.every(
                                                                (m)=>msg.id !== m.id))
           new_data = new_data.concat(msgs.data)
           setMessages({data: new_data, next: res.data['next']})
        })
    }

  }

  function Scroll(){
    if (msgs.data.length > 0){
                        let block = document.getElementById("messages-container");
                block.scrollTop = block.scrollHeight;
    }
  }

  React.useEffect(GetMessages, [current_dialog])
    React.useEffect(Scroll, [msgs])


  return (


      <div class="col-md-6 col-xl-8 pl-md-3 px-lg-auto px-0 border">
      { !loader ?
        <div class="chat-message">
          <ul class="list-unstyled chat-1 scrollbar-light-blue" onScroll={CheckScroll} id="messages-container">
              {msgs.data.map((msg, i)=>{
                return <Message msg={msg} key={i} />
              })}
        </ul>
            { current_dialog !== null ? <SendMessage dialog={current_dialog} />: <div/> }
       </div>
       :
        <Loader/>
       }
     </div>

  )


}