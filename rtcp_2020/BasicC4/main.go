package main

import (
	"fmt"
    "os"
	//"strings"
	"github.com/Avalanche-io/c4"
)

func stopOnError(err error) {
    if err != nil {
        fmt.Errorf("error %s\n", err)
        os.Exit(-1)
    }
}

func main() {
	inputname := "da_bomb.txt"
	// Generate a C4 ID for any contiguous block of data...
	// id := c4.Identify(strings.NewReader("alfa"))
	// fmt.Println(id)
	// output: c43zYcLni5LF9rR4Lg4B8h3Jp8SBwjcnyyeh4bc6gTPHndKuKdjUWx1kJPYhZxYt3zV6tQXpDs2shPsPYjgG81wZM1

    // // Generate a C4 ID for any number of non-contiguous blocks...
	// var ids c4.IDs
	// var inputs = []string{"alfa", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "india"}
	// for _, input := range inputs {
	// 	ids = append(ids, c4.Identify(strings.NewReader(input)))
	// }
	// fmt.Println(ids.ID())
	// // output: c435RzTWWsjWD1Fi7dxS3idJ7vFgPVR96oE95RfDDT5ue7hRSPENePDjPDJdnV46g7emDzWK8LzJUjGESMG5qzuXqq

    fin, err := os.Open(inputname)
    stopOnError(err)
    defer fin.Close()
    main_id := c4.Identify(fin)
	fmt.Println(main_id)
}
