import {useState, useEffect} from 'react'
import Header from './Header'
import URL from './URL'
import { TablePagination } from 'react-pagination-table';
import './App.css';

const App = () => {
  
  //Setting up states for storing the urls fetched from database and the query url passed in input form
  const [urls, setUrls] = useState([])
  const [queryres, setQueryres] = useState(false)
  
  //Use Effect hook to run at the creation of webpage to retrieve all URLs
  useEffect(()=>{
    const fetchURLs = async () => {
      const response = await fetch(`${process.env.REACT_APP_ENDPOINT}`+ '/TABLE')
      const data = await response.text()
      setUrls(JSON.parse(data))
    }
    fetchURLs()
  }, [])
  
  //handler function for queries in input form
  
  const queryURL = (URL) =>{
      const fetchURLs = async () => {
      const response = await fetch(`${process.env.REACT_APP_ENDPOINT}`+ '/TABLE?='+ URL.URL)
      const data = await response.text()
      const req_res = JSON.parse(data)
      if ('Item' in req_res && req_res.Item.URL === URL.URL)
      {
        setQueryres(true)
      }
      else if(!('Item' in req_res) || req_res.Item.URL !== URL.URL)
      {
        setQueryres(false)
      }
      else
      {
        setQueryres(false)
      }

    }

    fetchURLs()
  }

  return (
    <div className="App">
      <Header title='SkipQ Front End Web App for Accessing URLs stored in Database'/>
      <URL onAdd={queryURL}/>
      {queryres ? <h3>Queried URL exists in database</h3> : <h3>Queried URL does not exist in database</h3> }
      <TablePagination
        title="URLs fetched from DynamoDB Table using Backend API"
        subtitle =''
        headers={ ["URL" , "URL Name"] }
        data={ urls }
        columns="URL.Name"
        perPageItemCount={ 3 }
        partialPageCount={ 2 }
        totalCount={ 5 }
        arrayOption={ [[' ', 'all', ',']] }
        nextPageText="Next"
        prePageText="Prev"
      />
    </div>
  );
}

export default App;
