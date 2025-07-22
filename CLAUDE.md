# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a data analysis project focused on TCE-SP (Tribunal de Contas do Estado de São Paulo) approved candidates data. The project contains public examination results and candidate information.

## Data Structure

The repository contains:
- `lista_tce.csv`: Main dataset with candidate information including positions (CARGO), locations (LOCALIDADE), names, registration numbers, birth dates, scores, and demographic information (race and disability status)

Note: The DataWranglingMMLL folder is excluded from version control and analysis.

## Data Fields

Key columns in the dataset:
- CARGO: Position/role applied for (e.g., ACE-ADM)
- LOCALIDADE: Location (e.g., CAPITAL)
- NOME: Candidate name
- INSCRICAO: Registration number
- DATA NASC: Birth date
- CG/CE: Scores (knowledge areas)
- ACERTOS: Number of correct answers
- NOTA: Final grade
- NEGRO: Race declaration (SIM/NAO)
- PCD: Disability status (SIM/NAO)

## Working with This Data

- Data is in Portuguese and follows Brazilian public examination standards
- Contains sensitive personal information - handle with appropriate privacy considerations
- CSV uses semicolon (;) as delimiter
- Data includes affirmative action tracking (quota candidates)
- Focus on statistical analysis and reporting rather than individual candidate details


## Standard Workflow Instructions
1. Use TodoWrite tool to create and track tasks for complex implementations
2. Break down tasks into simple, manageable steps
3. The plan should have a list of todo items that you can check off as you complete them.
4. Before you begin working, check in with me and I will verify the plan.
5. Then, begin working on the todo items, marking them as complete as you go.
6. Focus on making minimal changes that impact as little code as possible
7. Please every step of the way just give me a high level explanation of what changes you made.
8. Run linting and type checking after changes
9. Test functionality before marking tasks complete
10. Prioritize simplicity and maintainability in all implementations. want to avoid making any massive or complex changes. Every change should impact as little code as possible. Everything is about simplicity.
11. Finally, add a review section to the `todo.md` file with a summary of the changes you made and any other relevant information.
