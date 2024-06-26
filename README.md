# NHANES Interface

A Python interface to NHANES dataset

Please cite as
```
@misc{Ciezak-NHANES-2024,
    author      = {Andrew Ciezak},
    title       = {NHANES Interface},
    series      = {},
    year        = {2024},
    pages       = {},
    numpages    = {},
    url         = {},
    doi         = {},
    isbn        = {},
    publisher   = {},
    address     = {},
}
```

## What is NHANES?

NHANES is the [National Health and Nutrition Examination Survey](https://www.cdc.gov/nchs/nhanes/index.htm), which is run by the US Centers for Disease Control. Every year, the study examines a representative sample of individuals from across the United States, using a broad range of surveys, physiological measurements, and laboratory tests.

## Structure

The `data` dir contains the downloads of the NHANES datasets
The `out\data` dir contains the preprocessed data used as input for the regression models [download.py](src\download.py)
The `src` dir contains the top level functions
- [download.py](src\download.py) for download of the NHANES data and docs
- [filters.py](src\filters.py) for restricting consistent filtering and reduction of the datasets
- [indicies.py](src\indicies.py) for defining the NHANES index for each variable of concern
- [preproc.py](src\preproc.py) for the process of data reduction for the Woolcot paper and our own
- [stats.py](src\stats.py) for consistent data aggregation, manipulation and weighting operations
- [globals.py](src\globals.py) for defining common data
- [main.py](src\main.py) for entry to the application

## Output
The `out\data` dir produces the following key files
- `train_ours.csv` and `test_ours.csv` contains the raw data from NHANES with original indices after joining the datasets appropriately
- `train_ours_min.csv` and `test_ours_min.csv` contains the pre-processed NHANES data with limited and renamed indices as defined in the paper
- `train_paper.csv` and `test_paper.csv` contains the data in reconstructing [Woolcot's results](https://github.com/impvau/Woolcot-2018)

# Execution

## Exact reproduction

A reproduction container with all required packages etc. with VS Code line-by-line debuging availble here:
```
docker pull impvsol.azurecr.io/240626-nhanes
```

## Execution in VS Code
After downloading the appropriate repos and versions, Trigger F5 in VS Code to run `.vscode/launch.json` configuration in debug mode

## For the masochist

Run `python src/main.py` after configing everything manually

# Further Documetation

For use of VS Code, debugging, reproduction, containers, registries etc. see [procedures](https://github.com/impvau/proc).
