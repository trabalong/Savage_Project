# Winner Prediction in UFC Title Fights

<img src="https://soaldar.com/wp-content/uploads/2020/05/ultimate-fighting-championship-ufc-logo.png" alt="drawing" width="600"/>

## Intro

In this project, I apply a ETL method for all UFC fighters and all the fights between 1994 and 2021. With all the data cleaned and transformated, I use Random Forest model to make predictions of a fight between two fighters to select. In this case, I predicted the winner in Glover Teixeira vs Jiri Prochazka (fight1), Valentina Schevchenko vs Taila Santos (fight2) and Alexander Volkanovski vs Max Holloway (fight3), all of them are title fights in June 2022. I finally maked a Tableau visualization of specific fight1 measurements and a comparison between my predictions in fight1, fight2 and fight3, and betting shops predictions.

## Data

- `data.csv` dataset got from Kaggle with all the fights of company between 1994 and 2021. Each sample has information about the fight, the fighters, their features and the measurements that were obtained in the fight.
- `raw_fighter_details.csv` dataset got from Kaggle with all the fighters that participate in the fights. Each sample is a fighter, his features and the average of all measurements that he/she got in all the fights.
- `ufc_fighters_official.csv` dataset got from scraping method on official UFC website with all the fighters on UFC catalog, their weight-class and their record.
- `ufc_fighters_styles.csv` dataset got from scraping method on official UFC website with all the fighters on UFC catalaog and their style of fight.

## Functions

- `load_ufc_fighters()` scraping all the fighters on UFC catalog by weight-class and upload a csv with the information.
- `load_ufc_fighters_styles()` scraping all the fighters on UFC catalog by fight's style and upload a csv with the information.
- `set_fighter_upper(fighter)` makes names upper for a better joining.
- `clean_fighters(fighter, ufc_fighters)` joins all the information between fighters dataset from Kaggle and fighters dataset from scraping. It also transforms and cleans some columns.
- `set_names_upper(data)` makes names upper for a better strings work.
- `set_name_winner(data)` changes Winner column values (Blue or Red) by the name of the winner.
- `fix_columns(data)` transforms and cleans columns.
- `set_nan_columns(data)` fills nan and renames columns.

## Notebook Main

1. ETL of UFC fighters.
2. ETL of UFC fights.
3. Load Database to MySQL for work Tableau.
4. Transforms data for learning and predicting.
5. In comment, another ways for prediction (Logistic Regression, Random Forest and H2O).

<img src="https://github.com/trabalong/Savage_Project/blob/main/img/GTvsJP_measurements.png" alt="drawing" width="800"/>

## Resources

https://www.kaggle.com/datasets/rajeevw/ufcdata
https://www.ufcespanol.com/
