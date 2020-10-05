import React from 'react'
import { Navbar } from 'react-bootstrap'
import Menu from './menu'

export default function ChatNavbar({user, logout, current_dialog}){


  return (
        <Navbar light bg="dark" className="py-1">
            <Menu user={user} logout={logout}/>
          <div class='container justify-content-md-center'>
            <div class="row">
                <div class="col">
                    <ul class="navbar-nav">
                        <li class="nav-item active">
                    <a class="nav-link text-white" href="#">{current_dialog ? current_dialog.another_user.username: ''}<span class="sr-only"></span></a>
                        </li>
                    </ul>
                </div>
            </div>
      </div>
        </Navbar>

  )

};