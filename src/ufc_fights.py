import pandas as pd
import numpy as np

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

    data['B_PCT_STRIKES'] = round((data.B_avg_TOTAL_STR_landed / (data.B_avg_TOTAL_STR_att)) * 100)
    data['R_PCT_STRIKES'] = round((data.R_avg_TOTAL_STR_landed / (data.R_avg_TOTAL_STR_att)) * 100)

    data['B_PCT_HEAD'] = round((data.B_avg_HEAD_landed / (data.B_avg_HEAD_att)) * 100)
    data['R_PCT_HEAD'] = round((data.R_avg_HEAD_landed / (data.R_avg_HEAD_att)) * 100)

    data['B_PCT_BODY'] = round((data.B_avg_BODY_landed / (data.B_avg_BODY_att)) * 100)
    data['R_PCT_BODY'] = round((data.R_avg_BODY_landed / (data.R_avg_BODY_att)) * 100)

    data['B_PCT_LEG'] = round((data.B_avg_LEG_landed / (data.B_avg_LEG_att)) * 100)
    data['R_PCT_LEG'] = round((data.R_avg_LEG_landed / (data.R_avg_LEG_att)) * 100)

    data['B_PCT_DISTANCE'] = round((data.B_avg_DISTANCE_landed / (data.B_avg_DISTANCE_att)) * 100)
    data['R_PCT_DISTANCE'] = round((data.R_avg_DISTANCE_landed / (data.R_avg_DISTANCE_att)) * 100)

    data['B_PCT_CLINCH'] = round((data.B_avg_CLINCH_landed / (data.B_avg_CLINCH_att)) * 100)
    data['R_PCT_CLINCH'] = round((data.R_avg_CLINCH_landed / (data.R_avg_CLINCH_att)) * 100)

    data['B_PCT_GROUND'] = round((data.B_avg_GROUND_landed / (data.B_avg_GROUND_att)) * 100)
    data['R_PCT_GROUND'] = round((data.R_avg_GROUND_landed / (data.R_avg_GROUND_att)) * 100)

    col_todrop = col1.append(col2).append(col3)

    data.drop(col_todrop, axis=1, inplace=True)

    data.date = pd.to_datetime(data.date)

# Valores numéricos por su mediana y valores categóricos por su mode
def set_nan_columns(data):
    
    for c in data.columns:
        
        if data[c].isnull().sum()>0 and not np.dtype(data[c]) is np.dtype(np.object):
            
            data[c] = data[c].fillna(data[c].median())
            
    for c in data.columns:
        
        if data[c].isnull().sum()>0 and np.dtype(data[c]) is np.dtype(np.object):
            
            data[c] = data[c].fillna(data[c].mode().values[0])

    data.rename(columns={'B_avg_CTRL_time(seconds)':'B_avg_CTRL_time', 'R_avg_CTRL_time(seconds)':'R_avg_CTRL_time',
                         'B_total_time_fought(seconds)':'B_total_time_fought',
                         'R_total_time_fought(seconds)':'R_total_time_fought'}, inplace=True)

    data.insert(0, 'fight_id', [i for i in range(len(data))])

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