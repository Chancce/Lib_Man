import Header from './Components/Header'
import { Container } from 'react-bootstrap'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import LandingPage from './Pages/LandingPage';
import Dashboard from './Pages/Dashboard';
import Home from './Pages/Home';



function App() {
  return (
    
    <div >
       <Router className="App">
      <Header />
      <Container>
      <main className='py-3'>
      
      </main>
      <Routes>
      <Route path="/" element={<LandingPage />} exact />
      <Route path ="/home" element ={<Home />} />
      <Route path="/dashboard" element={<Dashboard />}  />

      </Routes>
      
      </Container>
      </Router>
      
      
      
    </div>
  );
}

export default App;
