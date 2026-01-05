package main

import ( 
	"encoding/json" 
	"log" 
	"net/http"
	"time"

	"github.com/prometheus/client_golang/prometheus/promhttp"
)

type PingResponse struct{
	Message string `json:"message"`
	Time string `json:"time"`
}

func writeJSON(w http.ResponseWriter, status int, payload any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(payload)
}

func healthHandler (w http.ResponseWriter, r *http.Request){
	writeJSON(w,http.StatusOK,map[string]string{"Status":"ok"})
}

func PingHandler (w http.ResponseWriter, r *http.Request){
	response := PingResponse{
		Message: "Recived Ping",
		Time: time.Now().Format(time.RFC3339),
	}
	writeJSON(w, http.StatusOK ,response)
}

func loggingMiddleware(next http.Handler) http.Handler{
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request){

		start := time.Now()

		lrw := &loggingResponseWriter{ResponseWriter: w, statusCode: http.StatusOK}
		next.ServeHTTP(lrw, r)

		duration := time.Since(start)
		log.Printf("method=%s path=%s status=%d duration_ms=%d",r.Method, r.URL.Path, lrw.statusCode, duration.Milliseconds())
	})
}

type loggingResponseWriter struct{
	http.ResponseWriter
	statusCode int
}

func (lrw *loggingResponseWriter) WriteHeader(code int) {
	lrw.statusCode = code
	lrw.ResponseWriter.WriteHeader(code)
}

func main(){
	mux := http.NewServeMux()
	mux.HandleFunc("/healthz", healthHandler)
	mux.HandleFunc("/ping", PingHandler)

	mux.Handle("/metrics", promhttp.Handler())

	addr := ":8080"
	log.Println("Starting Server on the address", addr)

	handler := loggingMiddleware(mux)
	
	srv := &http.Server{
		Addr:         addr,
		Handler:      handler,
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
		IdleTimeout:  30 * time.Second,
	}

	err := srv.ListenAndServe()
	if err!= nil{
		log.Fatal(err)
	}
}