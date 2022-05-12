import pandas as pd

# Ponemos nombres en mayúsculas
def set_names_upper(data):

    data.R_fighter = data.R_fighter.str.upper()

    data.B_fighter = data.B_fighter.str.upper()

# Cambiamos valores de columna Winner por el nombre del luchador
def set_name_winner(data):

    for k, v in enumerate(data.Winner):

        if data.Winner[k] == 'Red': data.Winner[k] = data.R_fighter[k]

        elif data.Winner[k] == 'Blue': data.Winner[k] = data.B_fighter[k]

        else: data.Winner[k] = 'DRAW'

# Borramos columnas innecesarias, creamos nuevas con porcentajes y cambiamos tipo de datos
def fix_columns(data):

    #col_posiblementeborrar = [Height|Weight|Reach|_age|_Stance|win_by|wins|losses|draw|total_time|total_rounds|
    #                           total_title|TD_att|TD_landed|]
    col1 = data.columns[
        data.columns.str.contains('avg_opp|GROUND|Referee')]

    col2 = data.columns[data.columns.str.contains('SIG_STR_att|SIG_STR_landed')]

    col3 = data.columns[
        data.columns.str.contains('longest|current|TOTAL_STR|HEAD|BODY|LEG|DISTANCE|CLINCH')]

    data['B_PCT_STRIKES'] = round((data.B_avg_TOTAL_STR_landed / (data.B_avg_TOTAL_STR_att + data.B_avg_TOTAL_STR_landed)) * 100)
    data['R_PCT_STRIKES'] = round((data.R_avg_TOTAL_STR_landed / (data.R_avg_TOTAL_STR_att + data.R_avg_TOTAL_STR_landed)) * 100)

    data['B_PCT_HEAD'] = round((data.B_avg_HEAD_landed / (data.B_avg_HEAD_att + data.B_avg_HEAD_landed)) * 100)
    data['R_PCT_HEAD'] = round((data.R_avg_HEAD_landed / (data.R_avg_HEAD_att + data.R_avg_HEAD_landed)) * 100)

    data['B_PCT_BODY'] = round((data.B_avg_BODY_landed / (data.B_avg_BODY_att + data.B_avg_BODY_landed)) * 100)
    data['R_PCT_BODY'] = round((data.R_avg_BODY_landed / (data.R_avg_BODY_att + data.R_avg_BODY_landed)) * 100)

    data['B_PCT_LEG'] = round((data.B_avg_LEG_landed / (data.B_avg_LEG_att + data.B_avg_LEG_landed)) * 100)
    data['R_PCT_LEG'] = round((data.R_avg_LEG_landed / (data.R_avg_LEG_att + data.R_avg_LEG_landed)) * 100)

    data['B_PCT_DISTANCE'] = round((data.B_avg_DISTANCE_landed / (data.B_avg_DISTANCE_att + data.B_avg_DISTANCE_landed)) * 100)
    data['R_PCT_DISTANCE'] = round((data.R_avg_DISTANCE_landed / (data.R_avg_DISTANCE_att + data.R_avg_DISTANCE_landed)) * 100)

    data['B_PCT_CLINCH'] = round((data.B_avg_CLINCH_landed / (data.B_avg_CLINCH_att + data.B_avg_CLINCH_landed)) * 100)
    data['R_PCT_CLINCH'] = round((data.R_avg_CLINCH_landed / (data.R_avg_CLINCH_att + data.R_avg_CLINCH_landed)) * 100)

    data['B_PCT_GROUND'] = round((data.B_avg_GROUND_landed / (data.B_avg_GROUND_att + data.B_avg_GROUND_landed)) * 100)
    data['R_PCT_GROUND'] = round((data.R_avg_GROUND_landed / (data.R_avg_GROUND_att + data.R_avg_GROUND_landed)) * 100)

    col_todrop = col1.append(col2).append(col3)

    data.drop(col_todrop, axis=1, inplace=True)

    data.date = pd.to_datetime(data.date)

# Referee será Unknown y los datos estadísticos de los combates serán 0
def set_nan_columns(data):

    data.Referee.fillna('Unknown', inplace = True)

    data[['B_avg_KD', 'B_avg_SIG_STR_pct',
           'B_avg_TD_pct', 'B_avg_SUB_ATT', 'B_avg_REV',
           'B_avg_CTRL_time(seconds)', 'R_avg_KD', 'R_avg_SIG_STR_pct',
           'R_avg_TD_pct', 'R_avg_SUB_ATT', 'R_avg_REV',
           'R_avg_CTRL_time(seconds)', 'B_PCT_STRIKES', 'R_PCT_STRIKES',
           'B_PCT_HEAD', 'R_PCT_HEAD', 'B_PCT_BODY', 'R_PCT_BODY', 'B_PCT_LEG',
           'R_PCT_LEG', 'B_PCT_DISTANCE', 'R_PCT_DISTANCE', 'B_PCT_CLINCH',
           'R_PCT_CLINCH', 'B_PCT_GROUND', 'R_PCT_GROUND']] =\
    data[['B_avg_KD', 'B_avg_SIG_STR_pct',
           'B_avg_TD_pct', 'B_avg_SUB_ATT', 'B_avg_REV',
           'B_avg_CTRL_time(seconds)', 'R_avg_KD', 'R_avg_SIG_STR_pct',
           'R_avg_TD_pct', 'R_avg_SUB_ATT', 'R_avg_REV',
           'R_avg_CTRL_time(seconds)', 'B_PCT_STRIKES', 'R_PCT_STRIKES',
           'B_PCT_HEAD', 'R_PCT_HEAD', 'B_PCT_BODY', 'R_PCT_BODY', 'B_PCT_LEG',
           'R_PCT_LEG', 'B_PCT_DISTANCE', 'R_PCT_DISTANCE', 'B_PCT_CLINCH',
           'R_PCT_CLINCH', 'B_PCT_GROUND', 'R_PCT_GROUND']].fillna(0)

    data.rename(columns={'B_avg_CTRL_time(seconds)': 'B_avg_CTRL_time', 'R_avg_CTRL_time(seconds)': 'R_avg_CTRL_time'},
                inplace=True)

    data.insert(0, 'event_id', [i for i in range(len(data))])

# Añadir id de los luchadores
def add_fighterid(data2,fighters2):

    data2.insert(2,'RFighter_id', fighters2.fighter_id)
    data2.insert(4,'BFighter_id', fighters2.fighter_id)

    x = data2.set_index('R_fighter').join(fighters2[['fighter_id','Name']].set_index('Name'),
                                                rsuffix='_dcha', how='left')

    x.insert(1, 'R_fighter', x.index)

    x.reset_index(drop=True, inplace=True)

    x['RFighter_id'] = x['fighter_id']

    x = x.set_index('B_fighter').join(fighters2[['fighter_id','Name']].set_index('Name'),
                                                rsuffix='_dcha', how='left')

    x.insert(3, 'B_fighter', x.index)

    x.reset_index(drop=True, inplace=True)

    x['BFighter_id'] = x['fighter_id_dcha']

    x = x.drop(['fighter_id','fighter_id_dcha'],axis=1)

    x.sort_values(by=['event_id'], ignore_index=True, inplace=True)

    x.RFighter_id.fillna(2208, inplace=True)
    x.BFighter_id.fillna(2208, inplace=True)
    x.RFighter_id = x.RFighter_id.astype(dtype=int)
    x.BFighter_id = x.BFighter_id.astype(dtype=int)

    return x