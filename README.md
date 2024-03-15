# Secret Assignment

This project generates bunch of delivery stops and pickup stops in 2D plane.
It selects the as many stops as it can possibly fit based on a capacity constraints
and then it creates a route based on the nearest neighbor. After it checks which
pickup stop is the closest to the route and fits it into the route

## Usage:
 - `run-assignment` - Runs the assignment. I am creative that way
 - `--n-deliveries` - Generates the specified number of delivery stops
 - `--n-pickups` - generates the specified number of pickup stops

 Example
 ```
--n-deliveries=1000 --n-pickups=100 run-assignment
 ```
Runs the assignment and generates 1000 delivery and 100 pickup stops

## Development

1. Clone or fork the repository.
2. Go into the project directory:
```cd secret-assignment```
3. Create a virtualenv:
```pyenv virtualenv 3.11.6 venv```
4. Activate environment
```pyenv activate venv```
6. Upgrade pip
``` pip install --upgrade pip```
5. Install the project in editable mode:
```pip install -e .```


### Pre-commit hook

Install [pre-commit](https://github.com/pre-commit/pre-commit-hooks) hook inside the repository:

```shell
pre-commit install
```

Please use:

- [Type hints](https://docs.python.org/3/library/typing.html#type-aliases)
- [Google style docstring](http://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#docstring-sections)
- [Black](https://github.com/ambv/black/)
