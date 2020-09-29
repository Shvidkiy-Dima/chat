import React from 'react'
import {InputHook} from '../../../utils/hooks'
import Context from '../../../utils/context'

export default function SendMessage({dialog_id}){
    let input = InputHook('')
    let {request} = React.useContext(Context)

    function SendMessage(){
             request({method: 'post', url: '/dialog/' + dialog_id + '/message/', data: {
                   dialog: dialog_id,
                   text: input.value}},
               (res)=>{
               console.log(res)
               })

    }
    return (
            <div class="white">
            <div class="form-group basic-textarea">
              <textarea class="form-control pl-2 my-0" rows="2" placeholder="Type your message here..." onChange={input.el.onChange}>{input.el.value}</textarea>
            </div>
                      <button onClick={SendMessage} type="button" class="btn btn-sm float-right">Send</button>
          </div>

    )
}