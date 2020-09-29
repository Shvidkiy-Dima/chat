import React from 'react'
import {InputHook} from '../utils/hooks'
import axios from 'axios'

export default function Login({authorize}){
    let name_input = InputHook('')
    let pass_input = InputHook('')

    function DoLogin(event){
      event.preventDefault()
      axios.post(`/auth/jwt/create/`,
        {username: name_input.value, password: pass_input.value}).then(
      (res) => {
        sessionStorage.setItem('access', res.data.access)
        sessionStorage.setItem('refresh', res.data.refresh)
        authorize(true)
      },(err)=>{
        console.log(err)
      });

    }


    return (
<div className="col-md-6">
        <form onSubmit={DoLogin}>
                <h3>Sign In</h3>
                <div className="form-group">
                    <label>Username</label>
                    <input  placeholder="Enter username"
                    type="text"
                    className="form-control"
                    name="username"
                    {...name_input.el}/>
                </div>

                <div className="form-group">
                    <label>Password</label>
                    <input type="password"
                    className="form-control"
                    placeholder="Enter password"
                    name="password"
                    {...pass_input.el}/>
                </div>
                <button type="submit" className="btn btn-primary btn-block">Submit</button>
            </form>
          Registration
      </div>
    )
}