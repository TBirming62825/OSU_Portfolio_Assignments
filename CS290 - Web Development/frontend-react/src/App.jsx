import './App.css';
import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Link } from 'react-router-dom';
import RetrievePage from './pages/RetrievePage';
import CreatePage from './pages/CreatePage';
import UpdatePage from './pages/UpdatePage';

function App() {

  const [exerciseToEdit, setExerciseToEdit] = useState();

  return (
    <div className="app">
        <header>
          <h1>Workout Tracker</h1>
          <p>Log your workouts and track your progress!</p>
        </header>
        <Router>
          <nav>
            <Link to="/">Home</Link>
            <Link to="/create-page">Log your workout</Link>
          </nav>
          <main>
            <Routes>
              <Route path="/" element={<RetrievePage setExerciseToEdit={setExerciseToEdit}/>}></Route>
              <Route path="/create-page" element={<CreatePage/>}></Route>
              <Route path="/update-page" element={<UpdatePage exerciseToEdit={exerciseToEdit}/>}></Route>
            </Routes>
          </main>
        </Router>
        <footer>
          <p>&copy; 2025 Timothy Birmingham</p>
        </footer>
    </div>
  );
}

export default App;