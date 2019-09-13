package main

import (
    "time"
    "log"
    "net/http"
    "github.com/go-chi/chi"
    "github.com/go-chi/chi/middleware"

)


func Routes() *chi.Mux {

    router := chi.NewRouter()

    router.Use(

        middleware.Logger,
        middleware.DefaultCompress,
        middleware.RedirectSlashes,
        middleware.Recoverer,
        middleware.Timeout(60 * time.Second),
    )

    router.Get("/", func(responsewriter http.ResponseWriter, request *http.Request) {
        responsewriter.Write([]byte("Paraweather /"))
    })

    router.Mount("/weather", WeatherRoutes())

    return router
}



// our main function
func main() {
    TestingStationList()
    router := Routes()
    log.Fatal(http.ListenAndServe(":8000", router))
}


