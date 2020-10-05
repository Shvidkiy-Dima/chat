import React from 'react'
import {InputHook} from '../../../utils/hooks'
import Context from '../../../utils/context'

export default function SendMessage({dialog}){
    let input = InputHook('', null, dialog.max_length_message)
    let {request} = React.useContext(Context)

    function SendMessage(){
             request({method: 'post', url: '/dialog/' + dialog.id + '/message/', data: {
                   dialog: dialog.id,
                   text: input.value}},
               (res)=>{
                   input.clear()
               })

    }
    return (
            <div class="white">
            <div class="form-group basic-textarea">
              <textarea class="form-control pl-2 my-0" style={{"font-size": '13px'}} rows="2" placeholder="Type your message here..." onChange={input.el.onChange}>{input.value}</textarea>
            </div>
                      <button onClick={SendMessage} type="button" class="btn btn-sm float-right">Send</button>
          </div>

    )
}