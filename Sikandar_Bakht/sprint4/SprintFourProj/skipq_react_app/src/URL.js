import React from 'react'
import {useState} from 'react'

const URL = ({onAdd}) => {

    const [URL, setURL] = useState('')

    const onSubmit = (e) => {
        e.preventDefault()
    
        if (!URL) {
          alert('Please add a URL')
          return
        }
    
        onAdd({ URL })
    
        setURL('')
      }


    return (
       <form className='url-form' onSubmit={onSubmit}>
           <div className='form-control'>
                <label>URL </label>
                <input type='text' placeholder='Enter URL to search' 
                value = {URL} onChange={(e)=>setURL(e.target.value)}/>
           </div>
           <input type='submit' value='Query URL' className='btn btn-block' />
       </form>
    )
}

export default URL
