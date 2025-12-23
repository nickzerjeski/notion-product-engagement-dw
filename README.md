# Data Warehouse Project Overview

This is a case study of which concerns with the design and implementation of a Data Warehouse for Product Engagement Analysis in Notion. The goal is to detect important analytical business questions, based on that design a conceptual design for a data warehouse that is capable to hold information which can be used to answer those questions. From that conceptual design, a logical design needs to be extracted, that defines the required tables, their attributes and their types. Finally, this design can be implemented and populated with meaningful data on which than queries for the analytical questions can be run. The goal is to show how the typical business analytics process works. 

## Project Goal
Design, implement, and query a PostgreSQL data warehouse (DW) using real or synthetic data (e.g., generatedata.com) for a chosen company/domain. Work solo or in teams of up to three.

## Workflow and Tasks
- **Task 1 — Domain Analysis and Description**: Pick a company/domain; describe the domain and data landscape; explain motivation; gather background docs; list business processes, business questions, and KPIs; decide grain; each member covers at least one process.
- **Task 2 — Conceptual Design**: For each fact, define at least four dimensions and one or more measures; note additivity; create Dimensional Fact Model (DFM) schemas (Indyco or equivalent) with facts, dimensions, hierarchies, measures, descriptive attributes, convergence/shared/multiple/optional arcs.
- **Task 3 — Logical Design**: Build star (or snowflake if better) schemas with PK/FK relationships, attributes, and estimated cardinalities; document modeling rationale (e.g., multiple arcs, recursive hierarchies); pick two key business questions per fact and write SQL to answer them; prepare small example tables, execute queries, and show results.
- **Task 4 — Physical Design & ETL**: Write SQL to create the DW schema (all fact and dimension tables); load data; document cleaning, transformations, assumptions, and simplifications.
- **Task 5 — Querying**: Provide SQL examples using ROLLUP, CUBE, and GROUPING SETS; include one ranking query (NTILE/RANK/DENSE_RANK), one WINDOW clause query, and one period-to-period comparison (e.g., current vs. prior year).
- **Task 6 — Data Analysis Tool**: Produce an interactive dashboard that visualizes the key results described in the tex report and uses all the data from the queries and their respective results which you can find in the results folder. Before you start, discuss, which programming language you want to use for that

## Deliverables
- ~15-page report for technical and non-technical readers.
- All scripts to create, populate, and query the DW.
- Optional presentation and live demo.

## Evaluation Criteria
- Correctness, complexity, completeness, and clarity of implementation, report, and demo.
- Soundness of DW design and dimensional modeling.
- Quality and clarity of justifications and arguments.
- Effectiveness of query design, motivation, correctness, and result visualization.

## Learning Objectives
- Analyze business domains; identify processes and KPIs for DW.
- Design conceptual, logical, and physical DW models.
- Design ETL processes for integration and cleaning.
- Formulate analytical SQL with advanced operators and window functions.
- Develop dashboards that communicate business insights effectively.
