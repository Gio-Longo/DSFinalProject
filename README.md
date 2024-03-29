# A Demand System Approach to Asset Pricing Verification

## Replication of Table D1

---

## Project Summary

*A Demand System Approach to Asset Pricing* by Ralph S.J. Koijen and Motohiro Yogo discusses the restrictions of the law of one price in asset pricing and further evaluates the sensitivity of investors given price changes with limited arbitrage in the stock market. In this project, we replicated Table D1 - A summary of 13F institutions by type - which provides financial statistics for banks, insurance companies, investment advisors, mutual funds, and pension funds starting from 1980 until 2017.

##  Challenges and Successes

Overall, it would be unfair to claim the replication process was entirely smooth; we faced some challenges. The initial challenge arose during the data retrieval. Even though we eventually pulled the 13F data and the mutual fund mapping from Wharton Research Data Services (WRDS), the size of the 13F data (~1.5GB) slowed our progress. Additionally, we encountered difficulty in obtaining the names of pension funds, resorting to manual extraction from a PDF file. A further challenge emerged from the absence of mutual fund mapping data from mid-2018 onwards, though this did not hinder the replication of Table D1; however, it proved troublesome for replicating Table D1 with more recent data (2018-2024). Apart from these impediments, close collaboration across team members and the instructions provided made this final project a great learning experience.

## Task List

### Daniel

- Created script to generate D1 Table statistics from cleaned dataset
- Created script to pull all necessary data from WRDS

### Dylan

- Set up `dodo.py` to automate pulling of data and generation of PDF report
- Created unit tests

### Gio

- Created LaTeX template for D1 Tables
- Created script to generate additional statistics and visuals from cleaned dataset

### Nick

- Created script to clean dataset as specified in the paper; contributed to dodo.py, unit tests
- Created script to compile all tables, text, and visuals into the singular `.tex` report

### Sarp

- Wrote write-up for the final report
- Created notebook walk-through of code and report generation process
