import React, { useState } from 'react'
import { Navbar, Container, Nav, Button, Dropdown, Offcanvas } from 'react-bootstrap';
import { Menu, X, Home, Users, Settings, BarChart, FileText, Calendar, ChevronDown, User } from 'lucide-react';
function Dashboard() {
  const [isSidebarOpen, setSidebarOpen] = useState(true);


  const menuItems = [
    { icon: Home, text: 'Home' },
    { icon: Users, text: 'Users' },
    { icon: BarChart, text: 'Analytics' },
    { icon: FileText, text: 'Reports' },
    { icon: Calendar, text: 'Schedule' },
    { icon: Settings, text: 'Settings' }
  ];
  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f8f9fa' }}>
      {/* Navbar */}
      <Navbar bg="white" fixed="top" className="shadow-sm">
        <Container fluid>
          <div className="d-flex align-items-center">
            <Button 
              variant="light"
              onClick={() => setSidebarOpen(!isSidebarOpen)}
              className="me-3"
            >
              {isSidebarOpen ? <X size={24} /> : <Menu size={24} />}
            </Button>
            <Navbar.Brand className="fs-4 fw-semibold">Dashboard</Navbar.Brand>
          </div>
          
          {/* Profile Dropdown */}
          <Dropdown align="end">
            <Dropdown.Toggle as={Button} variant="light" className="d-flex align-items-center">
              <div className="d-flex align-items-center justify-content-center bg-secondary rounded-circle me-2" 
                   style={{ width: '32px', height: '32px' }}>
                <User size={20} />
              </div>
              <span className="me-2">John Doe</span>
              <ChevronDown size={16} />
            </Dropdown.Toggle>

            <Dropdown.Menu>
              <Dropdown.Item href="#">Profile</Dropdown.Item>
              <Dropdown.Item href="#">Settings</Dropdown.Item>
              <Dropdown.Item href="#">Logout</Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>
        </Container>
      </Navbar>

      {/* Sidebar */}
      <Offcanvas 
        show={isSidebarOpen} 
        onHide={() => setSidebarOpen(false)}
        backdrop={false}
        scroll={true}
        placement="start"
        style={{ marginTop: '56px', width: '250px' }}
      >
        <Offcanvas.Body className="p-0">
          <Nav className="flex-column">
            {menuItems.map((item, index) => (
              <Nav.Link 
                key={index}
                href="#"
                className="d-flex align-items-center p-3 text-dark"
              >
                <item.icon size={20} />
                <span className="ms-3">{item.text}</span>
              </Nav.Link>
            ))}
          </Nav>
        </Offcanvas.Body>
      </Offcanvas>

      {/* Main Content */}
      <main style={{ 
        marginLeft: isSidebarOpen ? '250px' : '0',
        marginTop: '56px',
        transition: 'margin-left 0.3s'
      }}>
        <Container fluid className="p-4">
          <h1 className="fs-3 fw-semibold mb-4">Welcome Back!</h1>
          <p className="text-muted">This is where your dashboard content will go.</p>
        </Container>
      </main>
    </div>
  )
}

export default Dashboard