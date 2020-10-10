import React from 'react'
import LoginForm from './login_form'
import RegForm from './reg_form'
import Loader from '../loader'
import { GithubLoginButton } from "react-social-login-buttons";
import axios from 'axios'

export default function Auth({authorize, is_auth}){
    let [use_login_form, setUseLoginForm] = React.useState(true)
    let [login_prompt, setLoginPrompt] = React.useState('Login')
    let [q_code, setq_Code] = React.useState(null)
    let Component = use_login_form ? LoginForm : RegForm


   function LoginGithub(){
        let client_id = 'acc314e8f22481966b39'
        window.location = 'https://github.com/login/oauth/authorize/?client_id=' + client_id

   }

    function CheckLoginGit(){
           let urlParams = new URLSearchParams(window.location.search).get('code')
           if (!urlParams || is_auth){
                return
           }
           setq_Code(urlParams)
           window.history.pushState({}, document.title, "/" + '' );
           axios.post('http://localhost:8000/login/social/jwt-pair/github/',{'code': urlParams}).then(
           (res)=>{
                sessionStorage.setItem('access', res.data.token)
                sessionStorage.setItem('refresh', res.data.refresh)
                authorize(true)
                setq_Code(null)
           }
           )

    }




    React.useEffect(CheckLoginGit, [is_auth])

    return (
          <div class="container-fluid bg-light">
            <div class="row">
              <div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
                <div class="card card-signin my-5">
                    <div class="card-body">

        {q_code ?
            <Loader/>
        :
        <>
        <Component login_prompt={login_prompt}
                    setLoginPrompt={setLoginPrompt}
                    authorize={authorize}
                    setUseLoginForm={setUseLoginForm}/>
        <GithubLoginButton onClick={LoginGithub}/>
        </>
        }
        </div>
        </div>
            </div>
            </div>
            </div>
    )
}