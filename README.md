# CAC (Computer Aided Composition)

## Introduction

A coding environment to try out algorithmic composition ideas.

A common pattern for algorithmic composition is to call a random number generator at every step and compute the next state (either choose from a set of options or tweak current state randomly).
Here an alternatie approach is considered

* Take following requirements
  * an initial state
  * a function that produces potential next states
  * a function that filters out states that do not fit into constraints
* Do a BFS to produce a graph of all potential compositional paths
* Then composer studies this graph/landscape/space
  * to understand some implications of the algorithm
  * tweaks the next state function or filter to narrow down the space
* A composition is a traversal path on the graph of state transitions

## Example

Graph of a simple voice leading algorithm: "only move one note in a triplet chord one step"

![simple voice leading graph](https://www.dropbox.com/s/dnlaw0s7now7rbp/simple_voice_leading_graph.png?dl=1)

Simple path: start from the root node and choose middle successor as next state.

Play an orchestra texture using string and brass instruments, playing the same pattern over the chord progression of produced path: [simple chord progression](https://www.dropbox.com/s/21mip4why8prsww/exploration%2003%20-%20graph%20traversal%201.mp3?dl=0)
