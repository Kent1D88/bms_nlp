from .main import *

# df_redcap_clean = pd.read_pickle(
#     "/export/home/cse200091/QD/bms_nlp/data/_redcap_clean.pickle"
# )

# def merge_analyser(dataframe):

#     dimension = []
#     pat_uniq = []
#     concord_rc = []
#     diff_rc = []
#     encout_u = []

#     df_temp = dataframe.loc[~dataframe["datetime"].isna()]
#     dimension.append(len(df_temp.index))
#     pat_uniq.append(df_temp["patient_num_13"].nunique())
#     concord_rc.append(
#         df_redcap_clean["patient_num_13"].isin(df_temp["patient_num_13"]).count()
#     )
#     diff_rc.append(
#         df_redcap_clean["patient_num_13"].nunique()
#         - df_temp["patient_num_13"].nunique()
#     )
#     encout_u.append(df_temp["encounter_num"].nunique())

#     return pd.DataFrame(
#         {
#             "n_rows": dimension,
#             "pat_uniq": pat_uniq,
#             "concord_rc": concord_rc,
#             "perte_rc": diff_rc,
#             "encount_u": encout_u,
#         }
#     )

def bestlength_patnum(list1, list2):
    df_temp = pd.DataFrame(
        {
            "start_char": [],
            "end_char": [],
            "len_pat_num": [],
            "nb_pat_1": [],
            "nb_pat_2": [],
            "cor_1_in_2": [],
            "cor_2_in_1": [],
        }
    )
    for i in range(0, 21):
        for j in range(1, 21):
            list_temp1 = list(map(lambda x: x[i:j], list1))
            list_temp2 = list(map(lambda x: x[i:j], list2))
            df_temp.loc[len(df_temp.index)] = [
                i,
                j,
                j - i,
                len(list1),
                len(list2),
                len(set(list_temp1).intersection(set(list_temp2))),
                len(set(list_temp2).intersection(set(list_temp1))),
            ]
    return df_temp


def concat_df_i2b2_bio (dataframe : pd.DataFrame) -> pd.DataFrame:
    """
    La fonction sert à concatener les informations extrait 
    du fichier i2b2 en un nouveau dataframe contenant 1 colonne par name_exam 
    et une ligne par encounter_num
    """
    
    df = pd.DataFrame(index=dataframe.index)
    
    for i in dataframe.columns.get_level_values('name_exam'):
        temp = pd.concat(
            [x for k,x in dataframe.loc(axis=1)[:,i,:,:,:,:].items()],
            join = 'outer', axis=1)
        temp = temp.agg("mean",axis="columns")
        df['pat_num'] = dataframe['patient_num_13']
        df['encount_num'] = dataframe['encounter_num']
        df[f'{i}_i2b2'] = temp
        
    df.dropna(axis=1, how='all',inplace=True)
    
    return df


def diff_source(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    """
    
    dataframe.index

    source = []
    etape = []
    nb_pat_u = []
    nb_visit_u = []
    nb_rapport_u = []
    remarque = []
    index = []
    
    if len(dataframe.index)>1:
        for i in range(0,(len(dataframe.index)-1)):
            source.append(dataframe.source.iloc[i])
            index.append(dataframe.index[i])
            etape.append(dataframe.index[i+1])
            nb_pat_u.append(
                (
                    dataframe
                    .nb_pat_u
                    .iloc[i+1]
                ) - (
                    dataframe
                    .nb_pat_u
                    .iloc[i]
                )
            )
            nb_visit_u.append(
                (
                    dataframe
                    .nb_visit_u
                    .iloc[i+1]
                )- (
                    dataframe
                    .nb_visit_u
                    .iloc[i]
                )
            )
            nb_rapport_u.append(
                (
                    dataframe
                    .nb_rapport_u
                    .iloc[i+1]
                ) - (
                    dataframe
                    .nb_rapport_u
                    .iloc[i]
                )
            )
            remarque.append(dataframe.remarque.iloc[i+1])
    
        res = {
            'source': source,
            'index_dfsource_edge': index,
            'index_dfsource_subg': etape,
            'nb_pat_u': nb_pat_u,
            'nb_visit_u': nb_visit_u,
            'nb_rapport_u': nb_rapport_u,
            'remarque': remarque,
        }
    
        return  pd.DataFrame(res)