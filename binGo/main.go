package main

import (
	"bytes"
	"strings"
	"flag"
	"fmt"
	"os"
	"sync"
	"github.com/chai2010/webp"
	"github.com/disintegration/imaging"
)

var wg sync.WaitGroup
var buf bytes.Buffer

func main() {
	quality := flag.Int("q", 80, "quality of convertation image")
	tmp := flag.Bool("tmp", false, "saving on temp dir")
	flag.Parse()
	imgs := flag.Args()
	fmt.Println(imgs)
	fmt.Println(*quality)

	for _, v := range imgs {
		wg.Add(1)
		go worker(v, *quality, *tmp, &wg)
	}

	wg.Wait()
	fmt.Fprint(os.Stdout, "Convertation complete!")
	os.Exit(0)
}

func worker(filepath string, quality int, tmp bool, wg *sync.WaitGroup) {
	defer wg.Done()
	outputPath := setOutput(filepath, tmp)
	file, err := os.Open(filepath)
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

func setOutput (filepath string, tmp bool) string {
	var result string
	file := strings.Split(filepath, ".")
	file[1] = "webp"
	if !tmp {
		result = "conv/" + file[0] + "." + file[1]
		return result
	}
	result = "tmp/" + file[0] + "." + file[1]
	return result
}