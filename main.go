package main

import (
	"io"
	"os"
	"fmt"
	"sync"
	"sync/atomic"
	"regexp"
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
	resp, err := http.Get(url)
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

func crawl(url string, wg *sync.WaitGroup, openThreads *int32, maxThreads int32) {
	defer wg.Done()
	wg.Add(1)
	atomic.AddInt32(openThreads, 1)
	fmt.Println("Crawling:", url)
	page := fetchPage(url)
	links := findHyperlinks(page)
	for _, link := range links {
		if openThreads != &maxThreads {
			go crawl(link, wg, openThreads, maxThreads)
		}
	}
}

func startCrawler(maxThreads int32) {
	var openThreads int32 = 0
	seeds := getSeeds()

	var wg sync.WaitGroup

	for _, domain := range seeds {
		go crawl("https://" + domain, &wg, &openThreads, maxThreads)
	}

	wg.Wait()
}

func main() {
	startCrawler(1000)
}
