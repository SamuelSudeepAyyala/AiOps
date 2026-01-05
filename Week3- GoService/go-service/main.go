package main

import ( 
	"encoding/json" 
	"log" 
	"net/http"
	"time"
)

type PingResponse struct{
	Message string `json:"message"`
	Time string `json:"time"`
}

func healthHandler (w http.ResponseWriter, r *http.Request){
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(map[string]string{
		"Status":"ok",
	})
}

func PingHandler (w http.ResponseWriter, r *http.Request){
	response := PingResponse{
		Message: "Recived Ping",
		Time: time.Now().Format(time.RFC3339),
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(response)
}

func main(){
	mux := http.NewServeMux()
	mux.HandleFunc("/healthz", healthHandler)
	mux.HandleFunc("/ping", PingHandler)

	addr := ":8080"
	log.Println("Starting Server on the address", addr)

	err := http.ListenAndServe(addr, mux)
	if err!= nil{
		log.Fatal(err)
	}
}