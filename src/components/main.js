import React from 'react'
import ContentContainer from './content/content_container'
import ChatNavbar from './navbar/navbar'

export default function Main({user, logout}){

    return (
    <div>
          <div class="card bg-light chat-room">
          <ChatNavbar logout={logout} user={user}/>
            <ContentContainer/>
          </div>
          </div>
    )

}