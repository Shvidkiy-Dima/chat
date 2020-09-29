import React from 'react'

function InputHook(defaultValue='', callback=null){
    let [value, setValue] = React.useState(defaultValue)

    function onChange(event){
        let current_value = event.target.value
        setValue(current_value)
        if (callback){
            callback(current_value)
        }
    }
    return {
            el: {
               onChange,
               value,
            },
            value,
            clear(){
                setValue('')
            }
    }
}

export {InputHook}

