# Data Schema

## Pulled Data
**Note**
- "\*" denotes derived data if exists. The data without "\*" is downloaded from databases.
- Can use "DataFrame.stack()" to stack the downloaded time-series data.

## 13F Data

|  **Name**  | **Type** |     **Key**     |                **Description**                |**Completed**|
|:----------:|:--------:|:---------------:|:---------------------------------------------:|:-----------:|
| fdate      | date     | Primary         | Quarter-end                                   |     [x]     |
| mgrno      | float    | Primary         | Manager number                                |     [x]     |
| mgrname    | str      |                 | Manager name                                  |     [x]     |
| typecode   | int      |                 | Manager type                                  |     [x]     |
| cusip      | str      |                 | Identification code of asset                  |     [x]     |
| shares     | float    |                 | Shares Held at End of Qtr (shares)            |     [x]     |
| prc        | float    |                 | Share Price                                   |     [x]     |
| shrout1    | float    |                 | Shares Outstanding in Millions                |     [x]     |
| stkcd      | str      |                 | Stock Class Code                              |     [x]     |
| exchcd     | str      |                 | Exchange Code                                 |     [x]     |


## Mutual Fund Mapping

|  **Name**  | **Type** |     **Key**     |               **Description**                 |**Completed**|
|:----------:|:--------:|:---------------:|:---------------------------------------------:|:-----------:|
| fdate       | date    | Primary         | Quarter-end                                   |     [x]     |
| mgrco       | str     | Primary         | Manager name                                  |     [x]     |


## Manual Data
**Note**
- This is the manual data mapped from the pdf file

## Pension Fund Mapping
|  **Name**  |
|:----------:|
| mgrco      |

