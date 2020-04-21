# Plan for Modeling and Analysis in Complex Networks

## The different steps of our project

Our project can be separated into three steps: Create, validate and infect:

### Create

#### Probability graph

We are going to generate different models for user behaviour by creating different probability graphs.

- Every node u as a probability of the user exiting
- Every edge (u, v) has a probability that the user will go from node u to node v.
- The sum of the probabilities on outgoing edges plus the probability of exiting is 1

#### User model

Input:

- Probability graph
- Entry point

Output:

- A list of visited pages in the same format as the traffic we have collected

### Validate

1. Run user model on probability graph to create virtual traffic
2. Create virtual traffic graph
3. Compare virtual traffic graph to actual traffic graph
4. Assign a validation score to the probability graph

### Infect

- For each node n in probability graph:
    - Run user model k times with n as starting node
    - Give n a ranking based on the total added traffic to the network
- Rank nodes according to influence

## Results we want to present:

This will give us the following results to present:

- Probability graphs
    - Different models for creating the probability graph
    - Validity of different models
    - What it tells us about actual users
- Influence of nodes
    - How more views to one page impacts views for the entire website
    - How we can use this to promote traffic on the website

## How we are going to get there:

We need to divide the work and that means we need to modularize the pipeline, so everybody can work separately. Therefore:

1. I am going to set up a modularized pipeline by creating a simplified version of each step in a way that different components can be changed without influencing the larger pipeline.
2. Once we have the pipeline, we can divide tasks and all focus on improving one part of the pipeline