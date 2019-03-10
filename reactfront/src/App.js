import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { WeatherStationsList } from "./WeatherStations";

class App extends Component {
  render() {
    return (
      <WeatherStationsList/>
    );
  }
}

export default App;
