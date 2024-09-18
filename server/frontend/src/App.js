import React from "react";
import { Routes, Route } from "react-router-dom";
import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register";
import Dealers from "./components/Dealers/Dealers";  // Import the Dealers component
import Dealer from "./components/Dealers/Dealer";  // Import the Dealer component
import PostReview from "./components/Dealers/PostReview"

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} /> {/* Register route */}
      <Route path="/dealers" element={<Dealers />} />   {/* Dealers route */}
      <Route path="/dealer/:id" element={<Dealer />} /> {/* Dealer route */}
      <Route path="/postreview/:id" element={<PostReview/>} /> {/* Post review route */}
    </Routes>
  );
}

export default App;

