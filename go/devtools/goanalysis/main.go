package main

import (
	"golang.org/x/tools/go/analysis/multichecker"

	"demo/devtools/goanalysis/pkg/timeunixutc"
)

func main() {
	multichecker.Main(
		timeunixutc.Analyzer,
		// More analyzers...
	)
}
