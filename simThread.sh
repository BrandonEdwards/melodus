#!/bin/bash
for i in {1..20000}; do
	for j in {1..10}; do
		./simulate.py $j &
	done
	wait
done 2>/dev/null

