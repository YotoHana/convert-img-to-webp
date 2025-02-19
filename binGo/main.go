package main

import (
	"bytes"
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"

	"github.com/chai2010/webp"
	"github.com/disintegration/imaging"
)

var wg sync.WaitGroup
var maxWorkers int

func main() {
	timeStart := time.Now()

	quality := flag.Int("q", 80, "quality of convertation image")
	perf := flag.Int("p", 1, "level of performance (0 - low, 1 - medium, 2 - high, 3 - max)")
	tmp := flag.Bool("tmp", false, "saving on temp dir")
	flag.Parse()
	imgs := flag.Args()
	fmt.Printf("Images paths: %v\n",imgs)
	fmt.Printf("Level of quality: %v\n",*quality)
	fmt.Printf("Level of performance: %v\n", *perf)

	if *perf == 0 {
		maxWorkers = 2
	} else if *perf == 1 {
		maxWorkers = 4
	} else if *perf == 2 {
		maxWorkers = 6
	} else {
		maxWorkers = 10
	}

	workers := make(chan struct{}, maxWorkers)


	for i, v := range imgs {
		wg.Add(1)
		go func(id int, imgPath string) {
			defer wg.Done()
			workers <- struct{}{}
			worker(imgPath, *quality, *tmp)
			fmt.Fprintf(os.Stdout, "PROGRESS: %v", id)
			<- workers
		}(i, v)
	}

	wg.Wait()
	fmt.Fprintf(os.Stdout, "Convertation complete!")
	timeEnd := time.Now()
	timeDuration := timeEnd.Sub(timeStart)
	fmt.Println("Время выполнения: ", timeDuration)
	os.Exit(0)
}

func worker(filePath string, quality int, tmp bool) {
	var buf bytes.Buffer
	outputPath := setOutput(filePath, tmp)
	file, err := os.Open(filePath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error with opening file: %v", err)
		os.Exit(1)
	}
	defer file.Close()

	img, err := imaging.Decode(file)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error with decoding image: %v", err)
		os.Exit(1)
	}
	
	err = webp.Encode(&buf, img, &webp.Options{Quality: float32(quality)})
	if err != nil {
		fmt.Fprintf(os.Stderr, "error with encoding to webp: %v", err)
		os.Exit(1)
	}

	err = os.WriteFile(outputPath, buf.Bytes(), 0666)
	if err != nil {
		fmt.Fprintf(os.Stderr, "error with creating file: %v", err)
		os.Exit(1)
	}
}

func setOutput (filePath string, tmp bool) string {
	var result string
	file := filepath.Base(filePath)
	ext := filepath.Ext(filePath)
	fileName := strings.TrimSuffix(file, ext)
	if !tmp {
		result = "./output/" + fileName + ".webp"
		return result
	}
	result = "./tmp/" + fileName + ".webp"
	return result
}