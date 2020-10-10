import React from 'react'
import Main from './main'
import Auth from './auth/auth'
import Request from '../utils/request'
import Context from '../utils/context'


export default function Dispatch({ws}){
  let [user, setUser] = React.useState({})
  let [is_authorized, setAuthBool] = React.useState(null)


  function authorize(is_auth=null){
    setAuthBool(is_auth)
  }

  function request(config, callback){
      let errback = ()=> {
        authorize(false)
      }
      Request(config, callback, errback)
  }

  function FetchUser(){
  request({method: 'get', url: '/users/me',},
           (res)=>{
           setUser(res.data)
           authorize(true)
           })
  }

  function ConnectWS(){
        if (is_authorized){
           console.log(is_authorized)
           ws.connect('/ws/chat/')
           ws.event_subscribe()
        }
        else {
            ws.close()
        }
  }

  function logout(){
        sessionStorage.removeItem('access')
        sessionStorage.removeItem('refresh')
        authorize(false)
  }


  React.useEffect(ConnectWS, [is_authorized])
  // Set current user
  React.useEffect(FetchUser, [is_authorized])


    return (
          <Context.Provider value={{request, user, ws}}>
      <div>
      {is_authorized === null ?
            <div/>: (
            is_authorized ?

              <Main logout={logout} user={user}/>:
              <Auth authorize={authorize} is_auth={is_authorized} />
            )
       }
      </div>
            </Context.Provider>
    )


}