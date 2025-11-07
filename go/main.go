package main

import (
	"encoding/json"
	"fmt"
	"time"
)

// Order is an object in the public API.
// Its created_at is documented to always be in RFC3339 format with "Z" notation.
type Order struct {
	CreatedAt time.Time `json:"created_at"`
}

func bad(unixTimestamp int64) {
	b, _ := json.MarshalIndent(Order{
		CreatedAt: time.Unix(unixTimestamp, 0),
	}, "", "  ")
	fmt.Printf("bad: %v\n", string(b))
}

func good(unixTimestamp int64) {
	b, _ := json.MarshalIndent(Order{
		CreatedAt: time.Unix(unixTimestamp, 0).UTC(),
	}, "", "  ")
	fmt.Printf("good: %v\n", string(b))
}

func main() {
	var t int64 = 1762066868
	bad(t)
	good(t)
}
