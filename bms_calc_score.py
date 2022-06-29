from .main import *

def clean_pnn_lcr(x):
    if type(x)==str:
        if x=='FP':
            return None
        else:
            temp = str(re.search(r'\d+',x)[0])
            if len(temp)==1:
                return float('0.0'+temp)
            else:
                return float('0.'+temp)
    elif type(x)==float:
        return x
    else :
        return None
    
def clean_bio(x):
    if type(x)==str:
        if (x =='FP') or (x ==''):
            return None
        else: return float(str(re.search(r'\d+',x)[0]))
    elif type(x)==float:
        return x
    else:
        return None
    
def pnn_lcr_count(x):
    if x[0] < 1000:
        return x[0]
    elif (x[0]>=1000) and (x[1]!=None):
        return x[0]*x[1]
    else: return None

def calc_ex_direct(x):
    if x[1] == 1:
        return 1
    elif (x[0]==1) and (x[1]!=1):
        return 1
    elif (x[1]==0) or (x[0]==0):
        return 0
    else: 
        return None
    

def clean_prot_lcr(x):
    if type(x)==str:
        if x !='FP':
            temp = re.sub(r'[^\d\.]','',x)
            temp = re.search(r'\d+\.\d*',temp)[0]
            return float(temp)
        else: return None
    elif type(x)==float:
        return x
    else: return None

def clean_FP(x):
    if x =='FP':
        return None
    else :
        return x

def calc_convulsion (x):
    if x==1:
        return x
    else :
        return 0
    
def calc_prot (x):
    if x >= 0.8:
        return 1
    elif x < 0.8:
        return 0
    else: return None

def calc_pnn_lcr(x):
    if x >= 1000:
        return 1
    elif x < 1000:
        return 0
    else: return None

def calc_pnn_sg(x):
    if (x[0] < 10000):
        return 0
    elif (x[1] < 10000):
        return 0
    elif x[1] >= 10000:
        return 1
    else: return None 

def binairisation(x):
    if x[0]==True:
        return 0
    elif x[1]==True:
        return 1
    else: return None

def bms_score_calc(df_nlp: pd.DataFrame) -> pd.DataFrame:
    """
    """
    dataframe = df_nlp.copy()

    list_bms_score = [
        "convulsion_value",
        "gb_lcr_value",
        "pnn_lcr_value",
        "gb_sg_val_value",
        "pnn_sg_val_value",
        "prot_lcr_val_value",
        "direct_lcr_value",
        "ex_direct_lcr_value",
    ]

    list_temp = []
    for i in list_bms_score:
        if i in dataframe.columns:
            list_temp.append(i)

    for i in list_temp:
        if i == "convulsion_value":
            dataframe[i] = dataframe[i].apply(clean_FP)
            dataframe["bms_conv"] = dataframe[i].apply(calc_convulsion)

        elif (i == "direct_lcr_value") & ('ex_direct_lcr_value' in list_temp):
            dataframe[i] = dataframe[i].apply(clean_FP)
            dataframe["bms_direct_lcr"] = (
                dataframe[["direct_lcr_value",'ex_direct_lcr_value']]
                .apply(calc_ex_direct,axis=1)
            )

        elif i == "prot_lcr_val_value":
            dataframe[i] = dataframe[i].apply(clean_prot_lcr)
            dataframe["bms_prot"] = dataframe[i].apply(calc_prot)

        elif (i == "pnn_lcr_value") & ("gb_lcr_value" in list_temp):
            dataframe[i] = dataframe[i].apply(clean_pnn_lcr)
            dataframe["gb_lcr_value"] = dataframe["gb_lcr_value"].apply(clean_bio)
            dataframe["pnn_lcr_count"] = dataframe[["gb_lcr_value",i]].apply(pnn_lcr_count,axis=1)
            dataframe['bms_pnn_lcr'] = dataframe['pnn_lcr_count'].apply(calc_pnn_lcr)

        elif (i == "pnn_sg_val_value") & ("gb_sg_val_value" in list_temp):
            dataframe[i] = dataframe[i].apply(clean_bio)
            dataframe['gb_sg_val_value'] = dataframe['gb_sg_val_value'].apply(clean_bio) 
            dataframe['bms_pnn_sg'] = (
                dataframe[['gb_sg_val_value','pnn_sg_val_value']]
                .apply(calc_pnn_sg,axis = 1)
            )

    list_bms = ['bms_conv','bms_direct_lcr',
                'bms_prot','bms_pnn_lcr',
                'bms_pnn_sg']
            
    list_temp2 = []
    for j in list_bms:
        if j in dataframe.columns:
            list_temp2.append(j)

    dataframe["score_bms"] = (
        dataframe[list_temp2].sum(axis=1,skipna=False)
    )
    dataframe["score_bms_bis"] = (
        dataframe[list_temp2].sum(axis=1,skipna=True)
    )
    dataframe["nb_NaN_bms"] = (
        dataframe.loc[:, list_temp2]
        .isnull()
        .sum(axis=1, skipna=False)
    )
    dataframe['bms_all_0'] = np.logical_and.reduce(dataframe[list_temp2]==0,axis=1)
    dataframe['bms_any_1'] = np.logical_or.reduce(dataframe[list_temp2]==1,axis=1)
    dataframe['score_bms_bin'] = (
        dataframe[['bms_all_0','bms_any_1']]
        .apply(binairisation,axis = 1)
    )

    return dataframe


def merge_na_bms(df_bms: pd.DataFrame, 
                 df_bio_i2b2: pd.DataFrame,) -> pd.DataFrame:
    """
    """

    list_bms_score = [
        "gb_lcr",
        "pnn_lcr",
        "gb_sg",
        "pnn_sg",
        "prot_lcr",
        "direct_lcr",
    ]
    dataframe = df_bms.copy()
    list_colonnes_interet = []
    for i in list_bms_score:
        colname_df = [x for x in df_bio_i2b2.columns if re.match(str(i), str(x))]
        colname_bms = [x for x in dataframe.columns if re.match(str(i), str(x))]

        if (len(colname_df) > 0) & (len(colname_bms) > 0):
            list_colonnes_interet.append(i)

    for l in list_colonnes_interet:
        colname_bms = [x for x in dataframe.columns if re.match(str(l), str(x))][0]
        colname_df = [x for x in df_bio_i2b2.columns if re.match(str(l), str(x))][0]

        na_cond = dataframe[colname_bms].isna()
        pat_cond_bms = dataframe.patient_num_13.isin(df_bio_i2b2.patient_num_13.unique())
        encount_cond_bms = dataframe.encounter_num.isin(df_bio_i2b2.encounter_num.unique())

        list_index = [
            x for x in dataframe.loc[(na_cond) & (pat_cond_bms) & (encount_cond_bms)].index
        ]
        list_pat = [x for x in dataframe["patient_num_13"].loc[(na_cond)]]
        list_encount = [x for x in dataframe["encounter_num"].loc[(na_cond)]]

        pat_cond = df_bio_i2b2.patient_num_13.isin(list_pat)
        encount_cond = df_bio_i2b2.encounter_num.isin(list_encount)

        i = 0
        list_value = [
            x for x in df_bio_i2b2.loc[(pat_cond) & (encount_cond), colname_df]
        ]

        for ind in list_index:
            if l in ["pnn_sg", "gb_sg"]:
                dataframe.loc[ind, colname_bms] = list_value[i] * (10 ** 3)

            else:
                dataframe.loc[ind, colname_bms] = list_value[i]
            i += 1

    dataframe = bms_score_calc(dataframe)

    return dataframe


def bms_contingeance(
    df_goldstandard: pd.DataFrame, 
    df_newtest: pd.DataFrame, 
    save_path: str = None,
    nbof_backup: str = '0',
) -> pd.crosstab:
    """
    """

    list_bms2 = [
        "bms_conv",
        "bms_direct_lcr",
        "bms_prot",
        "bms_pnn_lcr",
        "bms_pnn_sg",
        "score_bms",
        "score_bms_bis",
        "score_bms_bin",
        "score_bms_bis_bin",
    ]

    list_colname = []
    for l in list_bms2:
        if (l in df_goldstandard.columns) & (l in df_newtest.columns):
            list_colname.append(l)

    res_f = []
    for l in list_colname:
        globals()[f"res_{l}"] = pd.crosstab(
            columns = df_goldstandard[l],
            index = df_newtest[l],
            colnames=[f"goldstd_{l}"],
            rownames=[f"test_{l}"],
            dropna=False,
            margins=True,
        )
        path_save = str(save_path + f"_res_{l}_{nbof_backup}.pickle")
        globals()[f"res_{l}"].to_pickle(path_save)

        df_temp = pd.crosstab(
            columns = df_goldstandard[l],
            index = df_newtest[l],
            colnames=[f"goldstd_{l}"],
            rownames=[f"test_{l}"],
            dropna=False,
            margins=False,
        )

        VN = 0
        VP = 0
        FN = 0
        FP = 0
        for x in df_temp.columns:
            for y in df_temp.index:
                if (x == y) & (x != 0):
                    VP += df_temp.loc[y, x]
                elif (y == 0) & (x != 0):
                    FN += df_temp.loc[y, x]
                elif (x == 0) & (y != 0):
                    FP += df_temp.loc[y, x]
                elif (x == 0) & (y == 0):
                    VN = df_temp.loc[0, 0]

        TOT = VP + VN + FP + FN

        if VP == 0:
            precision = 0
            recall = 0
            f1_score = 0
            if VN == 0:
                accurancy = 0
            else:
                accurancy = round(((VN) / TOT), 2)
        else:
            accurancy = round(((VP + VN) / TOT), 2)
            precision = round((VP / (VP + FP)), 2)
            recall = round((VP / (VP + FN)), 2)
            f1_score = round(
                ((VP)/(VP+(0.5*(FN+FP))))
                , 2
            )

        res = {
            "label": l,
            "accurancy": accurancy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
        }
        res_f.append(res)

    df_perf = pd.DataFrame(res_f)
    
    file_name = f'{save_path}_final_res_{nbof_backup}.pickle'
    
    if save_path == None:
        print("Data not save")
    elif os.path.exists(file_name) :
        print("Data already exist, do you want to erase previous results?")
        print('Input "y" to erase or any other to not save')
        x = input()
        if x == "y":
            print("Saving succeeded")
            df_perf.to_pickle(file_name)
        else :
            print('Data not save')
    else:
        print("Saving succeeded")
        df_perf.to_pickle(file_name)
        
    return df_perf
