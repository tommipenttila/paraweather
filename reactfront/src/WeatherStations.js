import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { retrieveWeatherStations } from './redux/actions'
import { RETRIEVE_WEATHER_STATIONS } from './redux/actiontypes';


export class WeatherStationsList extends React.Component {

    constructor(props){
        super(props)
    }

    handleThing = () => {
        console.log("PREPROPS: ", this.props);
        //props.store.dispatch({ type: RETRIEVE_WEATHER_STATIONS })
        //this.props.retrieveWeatherStations();
        console.log("POST: ", this.props.weather);
    }   

    render() {

        return (
            <div>
            <div>WeatherStations listing</div>
            <button className="buttoning" onClick={this.handleThing}>
          Thingy
        </button>
        </div>
        )
    }

}

const mapStateToProps = state => state

function mapDispatchToProps(dispatch) {
    console.log("MAP DISPATCH")
    return {
        actions: bindActionCreators(retrieveWeatherStations, dispatch)
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(WeatherStationsList);