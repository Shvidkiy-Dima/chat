import React from 'react'
import {InputHook} from '../../../utils/hooks'
import { Form } from 'react-bootstrap'
import Context from '../../../utils/context'

export default function UsersSearch({setUsers}){
    let {request} = React.useContext(Context)
    let [show_close, setShowClose] = React.useState(false)
    let input = InputHook('', Search)

    function Search(prefix){
        if (! prefix){
            return
        }
        request({method: 'get', url: '/users/', params: {username: prefix}},
                (res)=>{
                    setShowClose(true)
                    setUsers({display_users: true, data: res.data['results']})
                })
        }

    function CloseSearch(){
        setUsers({display_users: false, data: []})
        setShowClose(false)
        input.clear()
    }


    return (
        <Form inline>
              <input type="search" class="form-control" placeholder="Search"  {...input.el} />
              {show_close ?
              <button type="button" class="close ml-2" onClick={CloseSearch} >&times;</button> : <div/>
              }
        </Form>
    )

}