import React from 'react'
import { Dropdown } from 'react-bootstrap'
import Context from '../../../utils/context'
import axios from 'axios';


export default function Menu({user, logout}){
    let ImageInput = React.useRef(null);
    let ImageSrc = React.useRef(null);
    let {request} = React.useContext(Context)

    function ChangeImage(e){
        e.preventDefault();
        let image = e.target.files[0];
        let formData = new FormData();
        formData.append("image", image);
        request({method: 'PATCH', url: 'users/' + user.id + '/', data: formData,
                 headers: {'Content-Type': 'multipart/form-data'}
                 },
                (res)=>{
                    ImageSrc.current.src = res.data.image
                    }
                )
    }


    return (

<Dropdown>
   <input type='file' style={{display: 'none'}} ref={ImageInput} onChange={ChangeImage}/>
  <Dropdown.Toggle size="sm" variant="success" id="dropdown-basic">
    Menu
  </Dropdown.Toggle>

  <Dropdown.Menu>
    <Dropdown.Item>
           <a href="#" class="d-flex justify-content-between" >
              <div class='d-flex'>
                <img src={user.image} ref={ImageSrc} alt="avatar" style={{'max-height': '50px'}} class="avatar rounded-circle d-flex align-self-center mr-2 z-depth-1"/>
                <div class="text-small float-left">
                  <strong>{user.username}</strong>
                </div>
                </div>
              </a>
    </Dropdown.Item>
   <Dropdown.Item onClick={()=>ImageInput.current.click()}>
   Change Image
   </Dropdown.Item>
   <Dropdown.Item onClick={logout}>Logout</Dropdown.Item>
  </Dropdown.Menu>
</Dropdown>


    )

}

