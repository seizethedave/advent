package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type edgeMap map[string][]string

func main() {
	edges := make(edgeMap)
	connect := func(from, to string) {
		if s, ok := edges[from]; ok {
			edges[from] = append(s, to)
		} else {
			edges[from] = []string{to}
		}
	}

	for s := bufio.NewScanner(os.Stdin); s.Scan(); {
		nodes := strings.Split(s.Text(), "-")
		connect(nodes[0], nodes[1])
		connect(nodes[1], nodes[0])
	}

	visited := make(map[string]struct{})
	p := findPaths(edges, visited, "start")

	fmt.Println(p)
}

func reentrant(node string) bool {
	c := node[0]
	return c >= 'A' && c <= 'Z'
}

func findPaths(edges edgeMap, visited map[string]struct{}, u string) int {
	if !reentrant(u) {
		if _, ok := visited[u]; ok {
			return 0
		}
		visited[u] = struct{}{}
		defer delete(visited, u) // unvisit
	}

	if u == "end" {
		return 1
	}

	subpaths := 0
	for _, v := range edges[u] {
		subpaths += findPaths(edges, visited, v)
	}
	return subpaths
}
