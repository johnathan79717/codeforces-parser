package main

import (
	"bufio"
	"fmt"
	"os"
)

var DEBUG = "N"

func debug(args ...interface{}) {
	if DEBUG != "N" {
		fmt.Fprint(os.Stderr, "DEBUG: ")
		fmt.Fprintln(os.Stderr, args...)
	}
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Scan()
	// code goes here

}
