import axios from 'axios';

function Request(config, callback, errback){
  let access_token = sessionStorage.getItem('access')
  let refresh_token = sessionStorage.getItem('refresh')
  if (!access_token || !refresh_token) {
      errback()
  }
  else {
      config.headers = {...config.headers || {}, Authorization: 'JWT ' + access_token}
      console.log(config.headers)
      axios(config).then(callback,
        (err)=>{
          console.log(err)
        if (err.response.status === 401){
          axios.post('/auth/jwt/refresh', {refresh: refresh_token}).then(
            (res)=>{
              sessionStorage.setItem('access', res.data.access)
              config.headers = {Authorization: 'JWT ' + res.data.access}
              axios(config).then(callback)
            },(err)=>{
                errback()
            })
          }
      })
  }
}

export default Request;