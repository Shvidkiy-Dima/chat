import React from 'react'
import ContentContainer from './content/content_container'

export default function Main({user, logout}){

    return (
    <div>
          <div class="card bg-light chat-room">
            <ContentContainer user={user} logout={logout}/>
          </div>
          </div>
    )

}