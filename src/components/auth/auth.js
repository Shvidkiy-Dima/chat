import React from 'react'
import LoginForm from './login_form'
import RegForm from './reg_form'


export default function Auth({authorize}){
    let [use_login_form, setUseLoginForm] = React.useState(true)

    let Component = use_login_form ? LoginForm : RegForm

    return (
          <div class="container-fluid bg-light">
            <div class="row">
              <div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
                <div class="card card-signin my-5">
                    <div class="card-body">


        <Component authorize={authorize} setUseLoginForm={setUseLoginForm}/>
        </div>
        </div>
            </div>
            </div>
            </div>
    )
}