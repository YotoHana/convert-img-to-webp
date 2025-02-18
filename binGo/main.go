package main

import (
	"bytes"
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"sync"

	"github.com/chai2010/webp"
	"github.com/disintegration/imaging"
)

var wg sync.WaitGroup

func main() {
	quality := flag.Int("q", 80, "quality of convertation image")
	tmp := flag.Bool("tmp", false, "saving on temp dir")
	flag.Parse()
	imgs := flag.Args()
	fmt.Println(imgs)
	fmt.Println(*quality)

	for _, v := range imgs {
		wg.Add(1)
		go func(imgPath string) {
			defer wg.Done()
			worker(imgPath, *quality, *tmp)
		}(v)
	}

	wg.Wait()
	fmt.Fprintf(os.Stdout, "Convertation complete!")
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
		result = "./conv/" + fileName + ".webp"
		return result
	}
	result = "./tmp/" + fileName + ".webp"
	return result
}