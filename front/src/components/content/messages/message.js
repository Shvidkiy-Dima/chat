import React from 'react'
import { Media } from 'react-bootstrap'

export default function Message({msg}){

        return (

       <li class="d-flex justify-content-left mt-2 bg-white">
              <img src={msg.author.image} alt="avatar"   class="avatar rounded-circle mr-2 ml-lg-3 ml-0 z-depth-1"/>
              <div class="chat-body white p-3 ml-2 z-depth-1">
                <div class="header">
                  <strong class="primary-font">{msg.author.username}</strong>
                  <small class="pull-right text-muted"><i class="far fa-clock"></i> 12 mins ago</small>
                </div>
                <hr class="w-100"/>
                <p class="mb-0">
                  {msg.text}
                </p>
              </div>
            </li>



    )

}