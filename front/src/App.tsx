import { BrowserRouter as Router, Link, Route, Routes } from "react-router-dom";
import "./App.css";

import Home from "./components/home";

function App() {
  return (
    <Router basename="/AquaMind">
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </Router>
  );
}

export default App;
