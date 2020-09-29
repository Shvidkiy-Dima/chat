import React from 'react'
import Context from '../../../utils/context'
import Dialog from './dialog'
import User from './user'
import UsersSearch from './users_search'
import { Col } from 'react-bootstrap'

export default function UsersDialogsContainer({set_current_dialog, dialogs, setDialogs, users, setUsers}){

  let {request} = React.useContext(Context)
  let freeze = false
  React.useEffect(GetDialogs, []);

  function GetDialogs(){
    request({method: 'get', url: '/dialog/'},
            (res)=>{
                setDialogs({data: res.data['results'], next: res.data.next})
            })
        }

    function CheckScroll(e){
        if ((e.target.scrollTop + e.target.offsetHeight === e.target.scrollHeight) && !freeze && dialogs.next){
            freeze = true
            request({method: 'GET', url: dialogs.next},
                    (res)=>{
                        let data = res.data['results'].filter(
                            (dialog)=>dialogs.data.every((d)=>d.id !== dialog.id)
                            )

                        let new_data = dialogs.data.concat(data)
                        setDialogs({data: new_data, next: res.data.next})

                        })

        }
    }
  return (
       <div class="col-md-6 col-xl-4 px-0 bg-white">
        <div class="white z-depth-1 px-2 pt-3 pb-0 members-panel-1 scrollbar-light-blue" onScroll={CheckScroll}>
          <ul class="list-unstyled friend-list">

              <UsersSearch setUsers={setUsers}/>
              {!users.display_users ?
                dialogs.data.map((dialog, i)=>{
                    return <Dialog dialog={dialog}
                                   key={i}
                                   set_current_dialog={set_current_dialog}
                                   />
                    })
                :
                users.data.map((user, i)=>{

                    return <User user={user} key={i} set_current_dialog={set_current_dialog} />

                     })

              }
            </ul>
          </div>
        </div>
  )

}