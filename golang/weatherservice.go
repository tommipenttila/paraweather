package main

import (

    "net/http"
    "github.com/go-chi/chi"
)


func WeatherRoutes() *chi.Mux {

    router := chi.NewRouter()

    router.Get("/stations", GetWeatherStations)

    return router
}

func GetWeatherStations(writer http.ResponseWriter, request *http.Request) {

    // TODO: Inject datasource after db
    testingstationsdata := TestingStationList()
    writer.Header().Set("Content-Type", "application/json")
    writer.Write(testingstationsdata)
    
}

