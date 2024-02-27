package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"net/http/cookiejar"
)

func main() {
	// client := &http.Client{}
	// jar := &myjar.Myjar{}
	// jar.Jar = make(map[string][]*http.Cookie)
	// client.Jar = jar

	jar, err := cookiejar.New(nil)
	if err != nil {
		log.Fatal(err)
	}

	client := &http.Client{
		Jar: jar,
	}

	req, err := http.NewRequest("GET", "https://mangalib.me/manga-list/", nil)
	if err != nil {
		log.Fatal(err)
	}
	// req.Header.Add("Host", "mangalib.me")
	// req.Header["User-Agent"] = []string{"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"}
	// req.Header["user-agent"] = []string{"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"}
	req.Header.Add("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0")
	fmt.Printf("%s", req.Header)
	//req.Header.Set("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0")
	// req.Header.Add("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
	// req.Header.Add("Accept-Language", "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3")
	// req.Header.Add("Accept-Encoding", "utf-8")
	// req.Header.Add("Connection", "keep-alive")
	// req.Header.Add("Content-Type", "text/html; charset=UTF-8")

	res, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	// res.Cookies()
	body, err := io.ReadAll(res.Body)
	header := res.Header
	res.Body.Close()
	if res.StatusCode > 299 {
		log.Fatalf("Response failed with status code: %d and\nbody: %s\n", res.StatusCode, body)
	}
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%s", body)
	fmt.Printf("%s", header)
}
