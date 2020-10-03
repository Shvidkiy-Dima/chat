import React from 'react'
import Context from '../../../utils/context'
import { Media } from 'react-bootstrap'

export default function User({user, set_current_dialog}){
      let {request} = React.useContext(Context)

      function StartDialogWithUser(){
                request({method: 'post', url: '/dialog/start_dialog_with_user/', data: {user_id: user.id}},
                (res)=>{
                    set_current_dialog(res.data)
                })
    }


    return (

       <li class="p-2" onClick={StartDialogWithUser}>
              <a href="#" class="d-flex justify-content-left" >
                <img src={user.image} alt="avatar" style={{'max-height': '50px'}} class="avatar rounded-circle d-flex align-self-center mr-2 z-depth-1"/>
                <div class="text-small">
                  <strong>{user.username}</strong>
                </div>
                <div class="chat-footer">
                  <span class="text-muted float-right"><i class="fas fa-mail-reply" aria-hidden="true"></i></span>
                </div>
              </a>
            </li>
    )

}


