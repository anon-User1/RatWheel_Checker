# Artifacts for RatWheel_Checker

This repository includes the artifacts of the paper: RatWheel Checker: Identifying Loop-Induced Hang among long-running tasks

The repository includes the following artifacts:

## `study_data`: 
* loop_compare.csv : The loop complexity comparision between real-world loop-induced hang bugs and benchmark loop code.
* long_running_cases_study.csv : 85 studied long running tasks of 7 software. 

## `code`: 
* /trace_and_analyze: The code of tracing LBR and system call and trace analysis.
* /selected_test: 25 selected tests of five software () that run as normal tasks.

## `result`: 
* overhead.csv: Experiment result of the overhead (For two level tracing) on normal tasks. 
* LHB_dataset.csv: The identifying results of 24 repoduced infinite loop hang bugs. And the developers fix stratagy to solve the bugs.
