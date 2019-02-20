package main

import (
    "encoding/json"
    "log"
    "net/http"
    "github.com/gorilla/mux"
)

// our main function
func main() {

    router := mux.NewRouter()
    router.HandleFunc("/commit", GetCommit).Methods("GET")
    log.Fatal(http.ListenAndServe(":8000", router))
}


func GetCommit(w http.ResponseWriter, r *http.Request) {

commits := map[string]int{
    "rsc": 3711,
    "r":   2138,
    "gri": 1908,
    "adg": 912,
}
    json.NewEncoder(w).Encode(commits)
}

