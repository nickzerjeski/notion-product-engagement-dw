# Data Warehouse Project Overview

This is a case study of which concerns with the design and implementation of a Data Warehouse for Product Engagement Analysis in Notion. The goal is to detect important analytical business questions, based on that design a conceptual design for a data warehouse that is capable to hold information which can be used to answer those questions. From that conceptual design, a logical design needs to be extracted, that defines the required tables, their attributes and their types. Finally, this design can be implemented and populated with meaningful data on which than queries for the analytical questions can be run. The goal is to show how the typical business analytics process works. 

## Deliverables
- The report can be found already compiled in `tex/main.pdf`.
- All scripts to create, populate and query the data can be found in the `scripts` folder. Additionally, the raw results of those queries can be found in the `results` folder.

## Report
To build the report, run `cd tex && pdflatex main.tex`. Note that you need to build the pdf twice in order to have the references rendered correctly.

## Dashboard
Install the requirements with `pip install -r requirements.txt`. To start the dashboard, run `python dashboard/app.py`

## Notes
The script for creating the schema and for populating the Data Warehouse were designed with the help of ChatGPT. Especially the populate script, since it was really hard to generate meaningful data. One example would be that users only have events after their account was created, or that they have activity within the first seven days. Furthermore, if queries got errors or needed to be refined, I also consulted ChatGPT. Especially the third and fifth key analytical question as well as the second additional query turned out to be way harder to implement as a query than I expected. Finally, for the dashboard I also used ChatGPT as help since I wasn't familiar with the *plotly dash* library but I wanted to do it with this library nevertheless.
