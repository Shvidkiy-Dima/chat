import React from 'react'
import { Media } from 'react-bootstrap'

export default function Dialog({dialog, set_current_dialog}){


    function OpenDialog(){
        set_current_dialog(dialog.id)
    }

    return (

       <li class="p-2" onClick={OpenDialog}>
              <a href="#" class="d-flex justify-content-between" >
              <div class='d-flex'>
                <img src={dialog.another_user.image} alt="avatar" style={{'max-height': '50px'}} class="avatar rounded-circle d-flex align-self-center mr-2 z-depth-1"/>
                <div class="text-small float-left">
                  <strong>{dialog.another_user.username}</strong>
                  <p class="last-message text-muted">{dialog.last_message.text}</p>
                </div>
                </div>
                <div class="chat-footer">
                  <p class="text-smaller text-muted ml-3">5 min ago</p>
                  { dialog.unviewed_messages ?
                    <span class="badge badge-danger float-right">{ dialog.unviewed_messages }</span>
                    :
                    <p/>
                  }

                  <span class="text-muted float-right"><i class="fas fa-mail-reply" aria-hidden="true"></i></span>
                </div>
              </a>
            </li>

    )
}