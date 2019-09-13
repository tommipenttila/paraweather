import { RETRIEVE_WEATHER_STATIONS  } from "../actiontypes";

const initialState = {

  };
  
  function rootReducer(state = initialState, action) {

    if (action.type === RETRIEVE_WEATHER_STATIONS) {

        return Object.assign({}, state, {weather: "Rainy thingy"});
    }

    return state;
  };
  
  export default rootReducer;