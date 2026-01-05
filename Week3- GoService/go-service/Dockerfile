# ------------------BUILD ----------------------------------
FROM golang:1.23-alpine AS builder

WORKDIR /app

RUN apk add --no-cache git

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o server .

# -----------------------RUN TIME ----------------------------

FROM alpine:3.20
WORKDIR /app

RUN adduser -D -H appuser
USER appuser

COPY --from=builder /app/server /app/server

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:8080/healthz || exit 1

CMD ["/app/server"]