package main

import (
	"io"
	"os"
	"fmt"
	"time"
	"regexp"
	"sync"
	"net/http"
	"encoding/json"
)

func getSeeds() []string {
	seedsBytes, err := os.ReadFile("seeds.json")
	if err != nil {
		fmt.Println("Error reading seeds.json:", err)
		return nil
	}
	var seeds []string
	err = json.Unmarshal(seedsBytes, &seeds)
	if err != nil {
		fmt.Println("Error unmarshalling seeds.json:", err)
		return nil
	}
	return seeds
}

func fetchPage(url string) string {
	client := &http.Client{
		Timeout: 5 * time.Second,
	}
	resp, err := client.Get(url)
	if err != nil {
		fmt.Println("Error fetching page:", err)
		return ""
	}
	defer resp.Body.Close()
	bodyBytes, err := io.ReadAll(resp.Body)
	page := string(bodyBytes)
	return page
}

func findHyperlinks(page string) []string {
	re := regexp.MustCompile(`(<a[^>]+href="(https?://[^"]+)"[^>]*>)`)
	matches := re.FindAllStringSubmatch(page, -1)
	var links []string
	for _, match := range matches {
		links = append(links, match[2])
	}
	return links
}

func crawl(url string, wg *sync.WaitGroup) {
	defer wg.Done()
	fmt.Println("Crawling:", url)
	page := fetchPage(url)
	links := findHyperlinks(page)
	for _, link := range links {
		wg.Add(1)
		go crawl(link, wg)
	}
}

func startCrawler() {
	seeds := getSeeds()

	var wg sync.WaitGroup

	for _, domain := range seeds {
		wg.Add(1)
		go crawl("https://" + domain, &wg)
	}

	wg.Wait()
}

func main() {
	startCrawler()
}
