package main

import (
	"fmt"
	"os"
)

var DEBUG = "N"
var DEBUG_BOOL = false

func debug(args ...interface{}) {
	if DEBUG_BOOL {
		fmt.Fprintln(os.Stderr, args...)
	}
}

func main() {
	if DEBUG != "N" {
		DEBUG_BOOL = true
	}

	var N int
	fmt.Scan(&N)

	debug(N)
}
