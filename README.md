## Banker's Algorithm 
Anastasia Riawan Soenjoto 

Simulates optimistic resource manager and banker's algorithm in Python3.

Purpose: To do resource allocation using both an optimistic resource manager and the banker’s algorithm of Dijkstra. The optimistic resource manager will satisfy request in a FIFO manner. 

The program takes the name of the file containing the input as a command line argument. The first line of the input file will be T, the number of tasks, and R, the number of resource types, followed by R additional values, the number of units present of each resource type. The next lines will represent the activities of the specific tasks. The possible activities are initiate, request, release, and terminate.

The initiate activity will be of the following format: 

  ` initiate   task-number delay resource-type initial-claim `
  
The request and release activity will be of the following format: 

`request    task-number delay resource-type number-requested `

 `release    task-number delay resource-type number-released `
 
 The terminate activity will be of the following format: 
 
 `terminate task-number delay unused unused`
 
 
 
