import React from 'react'
import { Navbar } from 'react-bootstrap'
import Menu from './menu'

export default function ChatNavbar({user, logout}){


  return (
        <Navbar light bg="dark" className="py-1">
            <Menu user={user} logout={logout}/>
        </Navbar>

  )

};