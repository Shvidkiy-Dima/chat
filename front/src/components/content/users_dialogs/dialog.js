import React from 'react'
import { Media } from 'react-bootstrap'
import Moment from 'react-moment';

export default function Dialog({dialog, set_current_dialog}){


    function OpenDialog(){
        set_current_dialog(dialog.id)
    }

    return (

       <li class="p-2" onClick={OpenDialog}>
              <a class="d-flex justify-content-between" >
              <div class='d-flex'>
                <img src={dialog.another_user.image} alt="avatar" style={{'height': '50px', 'width': '50px', 'border-radius': '50%'}} class="avatar rounded-circle d-flex align-self-center mr-2 z-depth-1"/>
                <div class="text-small float-left">
                  <strong>{dialog.another_user.username}</strong>
                  <p class="last-message text-muted">{dialog.last_message.text}</p>
                </div>
                </div>
                <div class="chat-footer">
                  <small class="text-muted ml-3 ">
                   <Moment fromNow >{dialog.last_message.created}</Moment>
                    |
                  </small>
                                   {dialog.another_user.is_online ?
                                    <small class="text-success">On</small>
                                    :
                                    <small class="text-dark">Off</small>
                                   }
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