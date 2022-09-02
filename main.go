package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
)

func main() {
	log.SetFlags(0)

	key, ok := os.LookupEnv("KPAY_API_KEY")
	if !ok {
		log.Fatalln("KPAY_API_KEY is not defined")
	}

	resp, err := http.Get("https://api.kiezelpay.com/api/merchant/summary?key=" + key)
	if err != nil {
		log.Fatalln("Could not contact API")
	}

	var data struct {
		Income       float32 `json:"totalIncome"`
		Purchases    int     `json:"totalPurchases"`
		ActiveTrials int     `json:"totalActiveTrials"`
	}

	defer resp.Body.Close()
	if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
		log.Fatalln("Could not decode API response")
	}

	fmt.Printf("$%.2f[%d(%d)]\n", data.Income, data.Purchases, data.ActiveTrials)
}
