package main

import (
	"fmt"
	"math/rand"
	"strconv"
	"strings"
	"time"
)

type MachineAccessingNetwork struct {
	IP            string
	OS            string
	Browser       string
	DownloadSpeed string
	UploadSpeed   string
	ISP           string
}

func main() {
	n := 1 * 1000 * 1000
	withPointersTestData := generateTestData(n)
	withPointersStart := time.Now()
	for i := 0; i < n-1; i++ {
		a := withPointersTestData[i]
		b := withPointersTestData[i+1]
		swapWithPointers(&a, &b)
	}
	fmt.Printf("Time taken using pointers: %v\n", time.Since(withPointersStart))

	withoutPointersTestData := generateTestData(n)
	withoutPointersStart := time.Now()
	for i := 0; i < n-1; i++ {
		a := withoutPointersTestData[i]
		b := withoutPointersTestData[i+1]
		a, b = swapWithoutPointers(a, b)
	}
	fmt.Printf("Time taken without using pointers: %v\n", time.Since(withoutPointersStart))
}

func swapWithPointers(a, b *MachineAccessingNetwork) {
	temp := *a
	*a = *b
	*b = temp
}

func swapWithoutPointers(a, b MachineAccessingNetwork) (MachineAccessingNetwork, MachineAccessingNetwork) {
	return b, a
}

func generateTestData(n int) []MachineAccessingNetwork {
	testData := make([]MachineAccessingNetwork, n)

	for i := 0; i < n; i++ {
		testData[i] = generateRandomMachineAccessingNetwork()
	}

	return testData
}

func generateRandomMachineAccessingNetwork() MachineAccessingNetwork {
	IP := generateRandomIPv4Address()
	OS := generateRandomOS()
	Browser := generateRandomBrowser()
	DownloadSpeed := generateRandomSpeed()
	UploadSpeed := generateRandomSpeed()
	ISP := generateRandomISP()
	man := MachineAccessingNetwork{IP, OS, Browser, DownloadSpeed, UploadSpeed, ISP}
	return man
}

func generateRandomIPv4Address() string {
	parts := make([]string, 4)
	for i := range parts {
		parts[i] = strconv.Itoa(rand.Intn(256))
	}
	return strings.Join(parts, ".")
}

func generateRandomOS() string {
	options := []string{"Mac", "Linux", "Windows", "Temple"}
	return options[rand.Intn(4)]
}

func generateRandomBrowser() string {
	options := []string{"Chrome", "Firefox", "Safari", "Opera", "Vivaldi", "Brave", "Tor"}
	return options[rand.Intn(7)]
}

func generateRandomSpeed() string {
	return strconv.Itoa(rand.Intn(10)+1) + " Mbps"
}

func generateRandomISP() string {
	options := []string{"Singtel", "M1", "Starhub", "Circles"}
	return options[rand.Intn(4)]
}
