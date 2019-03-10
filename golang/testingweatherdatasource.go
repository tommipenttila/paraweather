package main

import (
    "bufio"
    "encoding/csv"
    "encoding/json"
    "fmt"
    "io"
    "log"
    "os"
    "strconv"
)


type WeatherStation struct {
    Stationname     string      `json:"stationname"`
    Stationid       string     `json:"stationid"`
    Location        *Location   `json:"location, omitempty"`
}

type Location struct {
    Latitude    float64   `json:"latitude"`
    Longitude   float64   `json:"longitude"`
}


func TestingStationList() []byte {

    csvFile, _ := os.Open("../python/weatherservice/weatherstations.csv")
    reader := csv.NewReader(bufio.NewReader(csvFile))
    var stations []WeatherStation

    for {
        line, error := reader.Read()
        if error == io.EOF {
            break
        } else if error != nil {
            log.Fatal(error)
        }

        lat, err := strconv.ParseFloat(line[2], 64)
        if err != nil {
            log.Fatal(err)
        }
        lon, err := strconv.ParseFloat(line[3], 64)
        if err != nil {
            log.Fatal(err)
        }

        stations = append(stations, WeatherStation {
            Stationname:    line[0],
            Stationid:      line[1],
            Location:       &Location {
                Latitude:   lat,
                Longitude:  lon,
            },
        })
    }

    stationsJson, _ := json.Marshal(stations)

    fmt.Println(string(stationsJson))

    return stationsJson
}