import React from 'react'
import {InputHook} from '../../utils/hooks'
import axios from 'axios'

export default function LoginForm({authorize, setUseLoginForm, login_prompt}){

    let name_input = InputHook('')
    let pass_input = InputHook('')
    let [error, setError] = React.useState('')


   function DoLogin(event){
      event.preventDefault()
      setError('')
      axios.post('/auth/jwt/create/',
        {username: name_input.value, password: pass_input.value}).then(
      (res) => {
        sessionStorage.setItem('access', res.data.access)
        sessionStorage.setItem('refresh', res.data.refresh)
        authorize(true)
      },(err)=>{
             setError(err.response ? err.response.data.detail : err.message)


      });

    }


    return (

        <form onSubmit={DoLogin}>
                <h3>{login_prompt}</h3>
                <div className="form-group">
                    <input  placeholder="Enter username"
                    type="text"
                    className="form-control"
                    required={true}
                    name="username"
                    {...name_input.el}/>
                </div>

                <div className="form-group">
                    <input type="password"
                    className="form-control"
                    placeholder="Enter password"
                    required={true}
                    name="password"
                    {...pass_input.el}/>
                </div>
                <button type="submit" className="btn btn-sm btn-primary btn-block text-uppercase">Sing in</button>
                 <button class="btn btn-sm" onClick={()=>setUseLoginForm(false)}>Registration</button>

        {error ?
          <small id="passwordHelp" class="text-danger">
                {error}
          </small>
        :
        <p/>
        }
            </form>




    )



}