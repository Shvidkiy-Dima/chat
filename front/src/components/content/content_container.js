import React from 'react'
import UsersDialogsContainer from './users_dialogs/users_dialogs_container'
import MessagesContainer from './messages/messages_container'
import Context from '../../utils/context'
import { Container, Col, Row } from 'react-bootstrap'

export default function ContentContainer(){
  let [current_dialog, setCurrentDialog] = React.useState(null)
  let [dialogs, setDialogs]  = React.useState({data: [], next: null})
  let [msgs, setMessages] = React.useState({data: [], next: null})
  let [users, setUsers] = React.useState({users: [], display_users: false})
  let {ws, request} = React.useContext(Context)

  function GetMessageFromWS(data){
    if (current_dialog == data.dialog){
      msgs.data.push(data)
      setMessages({data: msgs.data, next: msgs.next})
     }
      else {
        request({method: 'GET', url: '/dialog/' + data.dialog + '/'},
         (res)=>{
            let filtered_dialogs = dialogs.data.filter((dialog)=>{
                if (dialog.id !== res.data.id){
                    return true
                }
            })

            filtered_dialogs.push(res.data)
            setDialogs({data: filtered_dialogs, next: dialogs.next})

         })
      }

  }

  function UnviewedMessages(){
        let patch_dialogs = dialogs.data.map((dialog)=>{
                                if (dialog.id === current_dialog){
                                    dialog.unviewed_messages = 0
                                }
                                return dialog
                            })
        setDialogs({data: patch_dialogs, next: dialogs.next})
  }

  React.useEffect(()=>{ws.dispatch.message = GetMessageFromWS})
  React.useEffect(UnviewedMessages, [current_dialog])


  return (
          <div class="card-body pt-1">
             <div class="row px-lg-2 px-2">
                <UsersDialogsContainer set_current_dialog={setCurrentDialog}
                                  dialogs={dialogs}
                                  users={users}
                                  setUsers={setUsers}
                                  setDialogs={setDialogs} />

                <MessagesContainer current_dialog={current_dialog}
                                   msgs={msgs}
                                   setMessages={setMessages}/>
             </div>
          </div>
   )


}