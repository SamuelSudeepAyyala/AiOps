package main

import (
	"encoding/json"
	"io"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

type PingResponse struct {
	Message string `json:"message"`
	Time    string `json:"time"`
}

var (
	httpRequestsTotal = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Name: "http_requests_total",
			Help: "Total number of HTTP requests processed.",
		},
		[]string{"method", "path", "status"},
	)

	httpRequestsDurationSeconds = prometheus.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "http_request_duration_seconds",
			Help:    "HTTP request duration in seconds.",
			Buckets: prometheus.DefBuckets,
		},
		[]string{"method", "path"},
	)
)

func init() {
	prometheus.MustRegister(httpRequestsTotal)
	prometheus.MustRegister(httpRequestsDurationSeconds)
}

func writeJSON(w http.ResponseWriter, status int, payload any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(payload)
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
}

func PingHandler(w http.ResponseWriter, r *http.Request) {
	response := PingResponse{
		Message: "Recived Ping",
		Time:    time.Now().Format(time.RFC3339),
	}
	writeJSON(w, http.StatusOK, response)
}

func metricsAndLoggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {

		start := time.Now()

		lrw := &loggingResponseWriter{ResponseWriter: w, statusCode: http.StatusOK}
		next.ServeHTTP(lrw, r)

		duration := time.Since(start)
		path := r.URL.Path

		httpRequestsTotal.WithLabelValues(r.Method, path, http.StatusText(lrw.statusCode)).Inc()
		httpRequestsDurationSeconds.WithLabelValues(r.Method, path).Observe(duration.Seconds())

		log.Printf("method=%s path=%s status=%d duration_ms=%d", r.Method, r.URL.Path, lrw.statusCode, duration.Milliseconds())
	})
}

type loggingResponseWriter struct {
	http.ResponseWriter
	statusCode int
}

func (lrw *loggingResponseWriter) WriteHeader(code int) {
	lrw.statusCode = code
	lrw.ResponseWriter.WriteHeader(code)
}

func setupLogging() {
	logFile := os.Getenv("LOG_FILE")
	if logFile == "" {
		log.SetOutput(os.Stdout)
		return
	}

	_ = os.Mkdir("/shared-logs", 0755)

	f, err := os.OpenFile(logFile, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		log.Printf("failed to open log file: %v", err)
		log.SetOutput(os.Stdout)
		return
	}

	log.SetOutput(io.MultiWriter(os.Stdout, f))
}

func main() {
	setupLogging()

	mux := http.NewServeMux()
	mux.HandleFunc("/healthz", healthHandler)
	mux.HandleFunc("/ping", PingHandler)

	mux.Handle("/metrics", promhttp.Handler())

	addr := ":8080"
	log.Println("Starting Server on the address", addr)

	handler := metricsAndLoggingMiddleware(mux)

	srv := &http.Server{
		Addr:         addr,
		Handler:      handler,
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
		IdleTimeout:  30 * time.Second,
	}

	err := srv.ListenAndServe()
	if err != nil {
		log.Fatal(err)
	}
}
