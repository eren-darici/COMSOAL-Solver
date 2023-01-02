
# COMSOAL Solver Implementation in Python

Made for Production Systems Analysis Lecture.






## Usage of solver

#### File format (must be an Excel file)

| is_elemani | is_suresi     | onculler                |
| :-------- | :------- | :------------------------- |
| `name of the job` | `time required for the job` | `premises of the job` |

#### Initializing the solver

```
COMSOAL(data_path, C)
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `data_path`      | `string` | **required**.  File path of Excel file that includes data in correct format|
| `C`      | `numeric` | **required**.  Cycle time for stations|


#### .solve()

Solves the problem and returns the assignments. Also logs relevant data for each iteration and writes assignments to a .json file.

#### .evaluate(assignments)

Takes assignments in the type of Python's dictionary. Evaluates the assignments in three metrics:
* Station Balance Delay
* Assembly Line Activity
* Smoothness Index

Also logs these metrics into a text file.

<br>
Eren Darıcı 2023.