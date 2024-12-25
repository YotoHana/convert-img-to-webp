package main

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func main() {
	a := app.New()
	w := a.NewWindow("Конвертер WEBP")
	w.Resize(fyne.NewSize(400, 400))

	slider := widget.NewSlider(1, 100)
	progress := widget.NewProgressBar()
	progress.Max = 100
	progress.Min = 1

	go func() {
		for {
			progress.SetValue(slider.Value)
		}
	}()

	mainContainer := container.NewVBox(slider, progress)
	
	w.SetContent(mainContainer)
	w.ShowAndRun()
}