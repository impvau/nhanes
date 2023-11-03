# NHANES

A Python interface to NHANES dataset and replication of Woolcot's Relative Fat Mass [work in 2018](https://doi.org/10.1038/s41598-018-29362-1)

## Purpose

This work attempts to:
- Replicate Woolcot's work
- Detail errors and issues of replication in depth
- Provide software for downstream research
- Explicitly communicate the exact procedure for replication, including the specific indicies and calculations used 

The authors desired that our work be reproduced rather than offering their workng, and we were unable to reconcile discrepancies, but have offered our best understanding of the problems within the [ISSUES.md readme](ISSUES.md).

## What is NHANES?

NHANES is the [National Health and Nutrition Examination Survey](https://www.cdc.gov/nchs/nhanes/index.htm), which is run by the US Centers for Disease Control. Every year, the study examines a representative sample of individuals from across the United States, using a broad range of surveys, physiological measurements, and laboratory tests.

## Project Structure

The `data` dir contains the output of the NHANES datasets and documentation generated from the code within [download.py](src\download.py)
The `out\data` dir contains CSVs of the different versions of the NHANES datasets for standard input into regressors
The `out\rep` dir contains replicated output
The `src` dir contains the top level functions
- [download.py](src\download.py) for download of the NHANES data and docs
- [filters.py](src\filters.py) for restricting consistent filtering and reduction of the datasets
- [indicies.py](src\indicies.py) for defining the NHANES index for each variable of concern
- [preproc.py](src\preproc.py) for the process of data reduction for the Woolcot paper and our own
- [stats.py](src\stats.py) for consistent data aggregation, manipulation and weighting operations
- [main.py](src\main.py) for entry to the application

The `src\replicate\tbl` dir contains a file for the replication of each table within the primary paper for comparison with our data
The `src\replicate\fig` dir contains a file for the replication of each figure within the primary paper for comparison with our data
The `src\replicate\sup_tbl` dir contains a file for the replication of each figure within the supplimentary material for comparison with our data
The `src\replicate\sup_fig` dir contains a file for the replication of each figure within the supplimentary material for comparison with our data

`.devcontainer` and `.vscode` folders contain the VSC configuration files for dev-container operation and launching/debugging the application
