import React, {useState, useEffect} from 'react'
import { Row, Col } from 'react-bootstrap'
import axios from 'axios'
import Book from '../Components/Book'

function Home() {
    const [books,setBooks] = useState([])

    useEffect(() =>{
        async function fetchBooks(){

            const {data} = await axios.get('/api/books')
            setBooks(data)

             
    }
       fetchBooks()
    }, []
)

  return (
    <div><h1>Books</h1>
        <Row>
            {books.map(book=>(
                <Col key={book.id} sm ={12} md ={6} lg={4}>
                <Book book={book} />
                </Col>
            ))}
        </Row>
    </div>
  )
}

export default Home