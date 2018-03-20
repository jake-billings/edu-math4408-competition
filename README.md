# edu-math4408-competition

Work-in-progress

Dr. Gethner announced that we will work in teams to create algorithms to determine graph thickness. This is where we should store our work. 

http://cse.ucdenver.edu/~gethner/GraphTheory/GraphTheory2018.html

## Strategy
Our strategy is to develop small algorithms that check for graph characterizations then perform efficient calculations to dermine thickness. For instance, if a graph is planar, its thickness is one. If a graph is complete, its thickness is given by a formula. If a graph is provided that fits no known optimization, a naive brute-force search is used to determine its thickness.

## Unit Testing

Unit testing is handled using functions prefixed with `test_` in the same file as the function they test. A function called `test()` calls each `test_` function. Each `test_` function uses basic python assert and print statements. Each file calls `test()` before running additional code if `__name__ == '__main__'`.
