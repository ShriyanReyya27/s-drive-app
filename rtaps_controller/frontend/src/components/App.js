import React, { Component } from "react";
import { render } from "react-dom";
import ReactDOM from "react-dom/client";
import HomePage from "./HomePage";
import CreateProfile from "./CreateProfile";
import RoadSafetyAnalyzer from "./RoadSafetyAnalyzer";
import RoadSafetyMap from "./RoadSafetyMap";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/rtaps/home" element={<HomePage />}>
        </Route>
        <Route path="/rtaps/createProfile" element={<CreateProfile />}></Route>
        <Route
          path="/rtaps/roadSafetyAnalyzer/:userName"
          element={<RoadSafetyAnalyzer />}
        ></Route>
        <Route path="/rtaps/roadSafetyMap" element={<RoadSafetyMap />}></Route>
        <Route path="/rtaps/roadSafetyMap/:userName" element={<RoadSafetyMap />}></Route>
      </Routes>
    </Router>
  );
}

export default App;


