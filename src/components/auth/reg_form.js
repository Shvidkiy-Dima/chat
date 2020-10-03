import React from 'react'
import {InputHook} from '../../utils/hooks'
import axios from 'axios'


export default function RegForm({setUseLoginForm}){

    let name_input = InputHook('')
    let pass_input = InputHook('')
    let [errors, setErrors] = React.useState({username: [], password: []})


      function Registration(e){
            e.preventDefault();
             axios.post(`/users/`, {username: name_input.value,
                                    password: pass_input.value})
             .then(res => {
                    setUseLoginForm(true)
                   },
                   err=>{
                        if (err.response){
                        let errors = {}
                        console.log(err.response.data)
                        errors.username = err.response.data.username || []
                        errors.password = err.response.data.password || []
                        setErrors(errors)
                        }

                   });

    }
    return (

        <form onSubmit={Registration}>
                <h3>Registration</h3>
                <div className="form-group">
                    <input  placeholder="Enter username"
                    type="text"
                    required={true}
                    className="form-control"
                    name="username"
                    {...name_input.el}/>

             {errors.username.map((err)=>{

                return  <small class="text-danger"> {err}</small>
             })}

                </div>

                <div className="form-group">
                    <input type="password"
                    required={true}
                    className="form-control"
                    placeholder="Enter password"
                    name="password"
                    {...pass_input.el}/>

             {errors.password.map((err)=>{

                return  <small class="text-danger"> {err}</small>
             })}

                </div>
                <button type="submit" className="btn btn-sm btn-primary btn-block text-uppercase">Registration</button>
                         <button class="btn btn-sm" onClick={()=>setUseLoginForm(true)}>Login</button>
            </form>


    )

}