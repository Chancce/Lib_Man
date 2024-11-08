import React from 'react'
import {Card} from 'react-bootstrap'
import { Link } from 'react-router-dom'

function Book({ book}) {
  return (
    <Card className="my-3 p-3 rounded">
    <Link to={`/book/${book.title}`}>
    </Link>
    <Card.Body>
      <Link 
        to={`/book/${book.title}`} 
        className="text-decoration-none"
      >
        <Card.Title as="div">
          <strong>{book.title}</strong>
        </Card.Title>
      </Link>
      
      <Card.Text as="div" className="my-3">
        <div className="text-muted">{book.author}</div>
      </Card.Text>
      
      <Card.Text as="div">
        <div className={`badge ${
          book.status === 'available' 
            ? 'bg-success' 
            : book.status === 'checked-out' 
            ? 'bg-warning'
            : 'bg-danger'
        }`}>
          {book.status}
        </div>
      </Card.Text>
      
      <Card.Text as="div" className="mt-2">
        <small className="text-muted">
          {book.available_count} of {book.stock_count} available
        </small>
      </Card.Text>
    </Card.Body>
  </Card>
  )
}

export default Book