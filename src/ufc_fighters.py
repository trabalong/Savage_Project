import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
import warnings
warnings.filterwarnings('ignore')

# Scrapea peleadores oficiales de la UFC
def load_ufc():

    driver=webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.ufcespanol.com/athletes/all')

    lista = []
    nombre, categoria, record = [], [], []

    # Checkea si existe un xpath
    def check_xpath(xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except:
            return False
        return True

    # Capturo a todos los luchadores por categorías de peso
    for i in range(2,14):

        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="block-mainpagecontent"]/div/div/div[2]/div/div/div/div[2]/a').click()
        time.sleep(5)
        driver.execute_script("arguments[0].scrollIntoView();",driver.find_element_by_xpath('//*[@id="block-mainpagecontent"]/div/aside/div[2]/div[2]/div/div[3]/div[2]/ul/li[14]'))

        try:
            driver.find_element_by_xpath(f'//*[@id="block-mainpagecontent"]/div/aside/div[2]/div[2]/div/div[2]/div[2]/ul/li[{i}]').click()
        except:
            time.sleep(5)
            driver.find_element_by_xpath(f'//*[@id="block-mainpagecontent"]/div/aside/div[2]/div[2]/div/div[2]/div[2]/ul/li[{i}]').click()

        time.sleep(5)
        
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except:
            time.sleep(5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        while (check_xpath('//*[@id="block-mainpagecontent"]/div/div/div[2]/div/div/ul/li/a')):

            try:
                driver.find_element_by_xpath('//*[@id="block-mainpagecontent"]/div/div/div[2]/div/div/ul/li/a').click()
            except:
                time.sleep(5)

        x = driver.find_elements_by_class_name('l-flex__item')

        for i in x:

            lista.append(i.text)

        driver.execute_script("arguments[0].scrollIntoView();",driver.find_element_by_xpath('//*[@id="edit-gender--wrapper"]/div'))
        driver.find_element_by_xpath('//*[@id="views-exposed-form-all-athletes-page"]/div/div[1]/div/div/span[3]').click()
        driver.find_element_by_xpath('//*[@id="views-exposed-form-all-athletes-page"]/div/div[1]/div/ul/li[1]/div/a').click()

    # Capturar solo el nombre, categoría y record de cada luchador
    for i in lista:

        if ('\nSEGUIR' in i) or ('\nPERFIL DE ATLETA' in i):
            i = i.replace('\nSEGUIR', '').replace('\nPERFIL DE ATLETA', '')

        i = i.split('\n')

        if len(i) > 3:

            if len(i) == 4:

                nombre.append(i[:-1][0])
                categoria.append(i[:-1][1])
                record.append(i[:-1][2])

            else:

                nombre.append(i[1:-2][0])
                categoria.append(i[1:-2][1])
                record.append(i[1:-2][2])

    # Paso todos los datos a csv
    a = pd.DataFrame(nombre, columns = ['Nombres'])
    b = pd.DataFrame(categoria, columns = ['Categoría'])
    c = pd.DataFrame(record, columns = ['Record'])
    x = pd.concat([a,b,c], axis = 1)
    x.to_csv(r'..data\ufc_fighters_official.csv')

# Nombres en mayúsculas
def set_fighter_upper(fighter):

    fighter.fighter_name = fighter.fighter_name.str.upper()

# Filtro data de luchadores por luchadores oficiales, modifico columnas y hago fillna
def clean_fighters(fighter,ufc_fighters):

    col_order = ['fighter_id','Name','DOB','Wins','Losses','Draws','Categoría','Height_cm','Weight_kg','Reach_cm','Stance',
             'SLpM','Str_Acc','SApM','Str_Def','TD_Avg','TD_Acc','TD_Def','Sub_Avg']

    x = fighter.set_index('fighter_name').join(ufc_fighters[['Nombres', 'Categoría', 'Record']].set_index('Nombres'),
                                               rsuffix='_dcha', how='inner')

    x['Name'] = x.index
    x['Weight'] = x.Weight.str[:3].astype(dtype=float) * 0.45
    x['Reach'] = round(x.Reach.replace(to_replace='\W', value='', regex=True).astype(dtype=float) * 2.54, 2)
    x['Height'] = x.Height.str[:1].astype(dtype=float) * 30.48 + x.Height.str[2:-1].astype(dtype=float) * 2.54
    x['DOB'] = pd.to_datetime(x['DOB'])
    x.Str_Acc = (x.Str_Acc.replace(to_replace='\W', value='', regex=True).astype(dtype=float))/100
    x.Str_Def = (x.Str_Def.replace(to_replace='\W', value='', regex=True).astype(dtype=float))/100
    x.TD_Def = (x.TD_Def.replace(to_replace='\W', value='', regex=True).astype(dtype=float))/100
    x.TD_Acc = (x.TD_Acc.replace(to_replace='\W', value='', regex=True).astype(dtype=float))/100

    x['Record'] = x.Record.str.split('-')
    x['Wins'] = x.Record.str[0]
    x['Losses'] = x.Record.str[1]
    x['Draws'] = x.Record.str[2].str[0]

    x.reset_index(drop=True, inplace=True)

    x.rename(columns={'Weight': 'Weight_kg', 'Reach': 'Reach_cm', 'Height': 'Height_cm'}, inplace=True)

    x.drop_duplicates('Name', inplace=True)

    x.reset_index(drop=True, inplace=True)

    #x[['Height_cm', 'Weight_kg', 'Reach_cm']] = x[['Height_cm', 'Weight_kg', 'Reach_cm']].fillna(0)
    x.Height_cm = x.Height_cm.fillna(x.Height_cm.mean())
    x.Weight_kg = x.Weight_kg.fillna(x.Weight_kg.mean())
    x.Reach_cm = x.Reach_cm.fillna(x.Reach_cm.mean())

    #x['Stance'] = x['Stance'].fillna('Unknown')
    x.Stance = x.Stance.fillna(x.Stance.mode())

    x['DOB'] = x['DOB'].fillna(0)

    x.insert(0, 'fighter_id', [i for i in range(len(x))])

    x = x[col_order]

    return x

load_ufc()