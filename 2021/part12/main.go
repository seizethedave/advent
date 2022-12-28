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

	fmt.Println(countPaths1(edges, make(map[string]struct{}), "start"))
	fmt.Println(countPaths2(edges, make(map[string]struct{}), "", "start"))
}

func reentrant(node string) bool {
	c := node[0]
	return c >= 'A' && c <= 'Z'
}

func canDoubleVisit(node string) bool {
	return node != "start" && node != "end"
}

func countPaths1(edges edgeMap, visited map[string]struct{}, u string) int {
	if u == "end" {
		return 1
	}

	if !reentrant(u) {
		if _, ok := visited[u]; ok {
			return 0
		}
		visited[u] = struct{}{}  // visit
		defer delete(visited, u) // unvisit
	}

	subpaths := 0
	for _, v := range edges[u] {
		subpaths += countPaths1(edges, visited, v)
	}
	return subpaths
}

func countPaths2(edges edgeMap, visited map[string]struct{}, doubleVisit string, u string) int {
	if u == "end" {
		return 1
	}

	if !reentrant(u) {
		// doubleVisit allows a single node to be visited twice.
		if _, ok := visited[u]; ok {
			if canDoubleVisit(u) && doubleVisit == "" {
				doubleVisit = u
			} else {
				return 0
			}
		}
		visited[u] = struct{}{} // visit
		defer func() {          // unvisit
			// Unvisiting now acts on doubleVisit IF it's `u`,
			// otherwise it unvisits it in the visited map.
			if doubleVisit == u {
				doubleVisit = ""
			} else {
				delete(visited, u)
			}
		}()
	}

	subpaths := 0
	for _, v := range edges[u] {
		subpaths += countPaths2(edges, visited, doubleVisit, v)
	}
	return subpaths
}
