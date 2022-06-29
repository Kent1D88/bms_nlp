import os
from os import path
import pandas as pd
import numpy as np
import spacy
from spacy.language import Language
from spacy.tokens import Doc, Span
import edsnlp
from edsnlp import components
import typing
from typing import Any, Dict, List
import pickle

import re
from dictionnaire.dicts_tabs import *
from dictionnaire.Dict11 import *

df_redcap_clean = pd.read_pickle(
    "/export/home/cse200091/QD/bms_nlp/data/_redcap_clean.pickle"
)



def get_entities(doc: Doc) -> List[Dict[str, Any]]:
    """Return a list of dict representation for the entities/span"""

    entities = []

    for key, listent in doc.spans.items():
        for ent in listent:
            d = dict(
                offset_begin=ent.start_char,
                offset_end=ent.end_char,
                label_name=ent.label_,
                label_value=ent.text,
                negation=ent._.negation,
                hypothesis=ent._.hypothesis,
                ent=ent,
                text_around=doc[ent.start - 10 : ent.end + 10].text,
                key="spans",
            )
            entities.append(d)

    return entities



def get_bmspipe(
    dataframe: pd.DataFrame,
    config_norm: Dict[str, List[Any]],
    config_matcher: Dict[str, List[Any]],
    config_isinspanparagraph: Dict[str, List[Any]],
    list_pipe: List[str] = [
        "eds.normalizer",
        "eds.sentences",
        "eds.matcher",
        "eds.negation",
        "eds.hypothesis",
    ],
    save_path: str = None,
):
    """get_bmspipe est une fonction réalisant l'ensemble des étapes 
    d'extraction des données d'une liste de documents inclus dans un dataframe. 
    La fonction renvoie le même dataframe explosé en une ligne par entité extraite 
    via nlp. La fonction peut sauvegarder le résultat dans un fichier pickle ou csv.
    
    Paramètre:
    ----------
    dataframe: pandas.dataframe contenant les documents 
        dans une colonne intitulé 'observation_blob' ou 'note_text'
    config_norm: Dictionnaire des paramêtres de la pipe 'eds.normalizer'
    config_matcher: Dictionnaire des paramêtres de la pipe 'eds.normalizer'
    config_isinspanparagraph: Dictionnaire des paramêtres de la pipe 
        'eds.isinspanparagraph'
    list_pipe: Liste des noms des pipes edsnlp
    save_path: string contenant l'adresse de sauvegarde 
        du fichier post-pipe et avant explosion par entité 
        (spacy ne permettant pas de sauvegarder les spans).
        Doit se finir en .pickle ou .csv
    """

    nlp = spacy.blank("fr")

    for term in list_pipe:
        if term == "eds.matcher":
            nlp.add_pipe(term, config=config_matcher)
        elif term == "eds.normalizer":
            nlp.add_pipe(term, config=config_norm)
        elif term == "eds.isin_spanparagraph":
            nlp.add_pipe(term, config=config_isinspanparagraph)
        else:
            nlp.add_pipe(term)

    if ("observation_blob" or "note_text") in dataframe.columns:
        if "observation_blob" in dataframe.columns:
            dataframe.rename(columns={"observation_blob": "note_text"}, inplace=True)
        dataframe["doc"] = list(nlp.pipe(dataframe.note_text))

    if save_path == None:
        pass
    elif save_path.endswith("pickle"):
        data = pickle.dumps(dataframe)
        data.to_pickle(save_path)

    dataframe["entities"] = dataframe["doc"].apply(get_entities)

    dataframe = dataframe.explode("entities")
    dataframe.reset_index(drop=True, inplace=True)

    df_temp1 = pd.DataFrame.from_records(dataframe["entities"])
    dataframe = dataframe.merge(df_temp1, left_index=True, right_index=True)

    dataframe.drop(
        ["entities",], axis=1, inplace=True,
    )

    dataframe.drop_duplicates(keep="first", ignore_index=True, inplace=True)
    
    if 'instance_num' in dataframe.columns:
        dataframe.rename(columns={'instance_num':'note_id'},inplace=True)
    dataframe['title']=('note_id : '+dataframe['note_id'].astype(str))
    dataframe['isin_spanparagraph'] = dataframe['ent'].apply(
        lambda x: x._.isin_spanparagraph
    )

    if save_path == None:
        pass
    elif save_path.endswith("csv"):
        dataframe.drop(["doc",], axis=1,).to_csv(save_path)
    else:
        raise Exception("Format de fichier incorrect : doit être .pickle ou .csv")

    print(dataframe.shape)
    return dataframe



def merge_analyser(dataframe):

    dimension = []
    pat_uniq = []
    concord_rc = []
    diff_rc = []
    encout_u = []

    df_temp = dataframe.loc[~dataframe["datetime"].isna()]
    dimension.append(len(df_temp.index))
    pat_uniq.append(df_temp["patient_num_13"].nunique())
    concord_rc.append(
        df_redcap_clean["patient_num_13"].isin(df_temp["patient_num_13"]).count()
    )
    diff_rc.append(
        df_redcap_clean["patient_num_13"].nunique()
        - df_temp["patient_num_13"].nunique()
    )
    encout_u.append(df_temp["encounter_num"].nunique())

    return pd.DataFrame(
        {
            "n_rows": dimension,
            "pat_uniq": pat_uniq,
            "concord_rc": concord_rc,
            "perte_rc": diff_rc,
            "encount_u": encout_u,
        }
    )



def clean_df(dataframe):
    for col in dataframe.columns:
        print("-" * 15, col, "-" * 15)
        print("Nombre de valeurs unique : ", dataframe[[col]].nunique()[0])
        if (dataframe[[col]].nunique()[0] == 0) | (dataframe[[col]].nunique()[0] == 1):
            dataframe.drop(columns=col, inplace=True)
    return dataframe


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



def bms_cleanaggregate(
    dataframe: pd.DataFrame,
    list_labels: List[str] = [
        "pas",
        "pad",
        "dextro",
        "gly_lcr_val",
        "prot_lcr_val",
        "gr_lcr",
        "gb_lcr",
        "gb_sg_val",
        "pnn_sg_val",
    ],
) -> pd.DataFrame:

    """
    """

    for label in dataframe.label_name.unique():
        if label in list_labels:
            m = dataframe["label_name"] == label
            n = dataframe["value"] != "FP"

            if label == "pas":
                dataframe.loc[m, "value"] = dataframe.loc[m, "value"].str.replace(
                    r"\/ ?\d+", "", regex=True
                )

            elif label == "pad":
                dataframe.loc[m, "value"] = (
                    dataframe.loc[m, "value"]
                    .astype(str)
                    .replace(r"\d+ ?\/ ?", "", regex=True)
                )

            elif (label == "gb_sg_val") or (label == "pnn_sg_val"):
                f = dataframe.value.str.contains(
                    r"\d{1,2}\.\d{0,3}\w?", regex=True, flags=re.IGNORECASE, na=False
                )
                f_bar = ~dataframe.value.str.contains(
                    r"\d{1,2}\.\d{0,3}\w?", regex=True, flags=re.IGNORECASE, na=False
                )

                if dataframe.loc[m & n & f, "value"].empty == False:
                    for d in dataframe.loc[m & n & f, "value"]:
                        k = dataframe["value"] == d
                        res = re.findall(r"\d{1,2}\.\d{0,3}", d)[0]
                        if len(re.sub(r"\.\d{0,3}", "", res)) == 1:
                            res = re.sub(r"\.", "", res)
                            while len(res) < 4:
                                res += "0"

                        elif len(re.sub(r"\.\d{0,3}", "", res)) == 2:
                            res = re.sub(r"\.", "", res)
                            while len(res) < 5:
                                res += "0"
                        dataframe.loc[m & n & f & k, "value"] = res

                if dataframe.loc[m & n & f_bar, "value"].empty == False:
                    for d in dataframe.loc[m & n & f_bar, "value"]:
                        k = dataframe["value"] == d
                        res = re.sub(r"\D", "", d)
                        if len(res) == 1:
                            while len(res) < 4:
                                res += "0"
                        elif len(res) == 2:
                            while len(res) < 5:
                                res += "0"
                        dataframe.loc[m & n & f_bar & k, "value"] = res

            else:
                dataframe.loc[m & n, "value"] = (
                    dataframe.loc[m & n, "value"]
                    .astype(str)
                    .replace(r"[a-zA-Zéè\/ :=]*", "", regex=True)
                )
                dataframe.loc[m & n, "value"] = (
                    dataframe.loc[m & n, "value"]
                    .astype(str)
                    .replace(r"\,", "\.", regex=True)
                )

    return dataframe


def fun_lcr_bool_neg(dataframe: pd.DataFrame, m, m_bar, n, n_bar):
    if not dataframe.loc[m & n].empty:
        value = 0
        text_t = dataframe.loc[m & n, "text_around"].value_counts(sort=True).index[0]
    elif not dataframe.loc[m & n_bar].empty:
        value = 1
        text_t = (
            dataframe.loc[m & n_bar, "text_around"].value_counts(sort=True).index[0]
        )
    elif not dataframe.loc[m_bar].empty :
        value = "FP"
        text_t = dataframe.loc[m_bar, "text_around"].value_counts(sort=True).index[0]
    else:
        value = np.nan
        text_t = np.nan
    return (value, text_t)


def fun_lcr_bool(dataframe: pd.DataFrame, m, m_bar):
    if not dataframe.empty:
        if not dataframe.loc[m].empty:
            value = 1
            text_t = dataframe.loc[m, "text_around"].value_counts(sort=True).index[0]
        elif not dataframe.loc[m_bar].empty:
            value = "FP"
            text_t = dataframe.loc[m_bar, "text_around"].value_counts(sort=True).index[0]
    else:
        value = np.nan
        text_t = np.nan
    return (value, text_t)


def fun_lcr_divers(dataframe: pd.DataFrame, m, m_bar):
    if not dataframe.loc[m].empty:
        value = dataframe.loc[m, "label_value"].value_counts(sort=True).index[0]
        text_t = (
            dataframe.loc[dataframe["label_value"] == value,"text_around"]
            .value_counts(sort=True)
            .index[0]
        )
    elif not dataframe.loc[m_bar].empty:
        value = "FP"
        text_t = dataframe.loc[m_bar, "text_around"].value_counts(sort=True).index[0]
    else:
        value = np.nan
        text_t = np.nan
    return (value, text_t)


def fun_lcr_value(dataframe: pd.DataFrame, f, m, m_bar, f_bar):
    if not dataframe.loc[m & f].empty:
        value = dataframe.loc[m & f, "label_value"].value_counts(sort=True).index[0]
        text_t = (
            dataframe.loc[dataframe["label_value"] == value, "text_around"]
            .value_counts(sort=True)
            .index[0]
        )
    elif (not dataframe.loc[m_bar & f].empty) or (not dataframe.loc[m & f_bar].empty):
        value = "FP"
        text_t = dataframe["text_around"].value_counts(sort=True).index[0]
    else:
        value = np.nan
        text_t = np.nan
    return (value, text_t)


def fun_sg_val(dataframe: pd.DataFrame, m_bar, m):
    c = ~dataframe.label_value.str.contains(
            r"\d+:\d+", regex=True, flags=re.IGNORECASE, na=False
        )
    c_bar = dataframe.label_value.str.contains(
            r"\d+:\d+", regex=True, flags=re.IGNORECASE, na=False
    )
    if not dataframe.loc[m_bar & c].empty :
        value = (
            dataframe
            .loc[m_bar & c, "label_value"]
            .str
            .replace(r"[a-zA-Z=\:]", "", regex=True)
            .value_counts(sort=True)
            .index[0]
        )
        text_t = (
            dataframe.loc[m_bar & c, "text_around"]
            .value_counts(sort=True)
            .index[0]
        )
    elif not dataframe.loc[(m)|(m_bar & c_bar)].empty:
        value = "FP"
        text_t = dataframe.loc[(m) | (m_bar & c_bar), "text_around"].value_counts(sort=True).index[0]
    else:
        value = np.nan
        text_t = np.nan
    return (value, text_t)


def fun_sg_bool(dataframe: pd.DataFrame, m, m_bar):
    if not dataframe.loc[m_bar].empty:
        value = 1
        text_t = dataframe.loc[m_bar, "text_around"].value_counts(sort=True).index[0]
    elif not dataframe.loc[m].empty:
        value = "FP"
        text_t = dataframe.loc[m, "text_around"].value_counts(sort=True).index[0]
    else:
        value = np.nan
        text_t = np.nan
    return (value, text_t)


def fun_bool_neg_majorite(dataframe: pd.DataFrame, n):
    if dataframe["negation"].value_counts(sort=True).index[0]:
        value = 0
        text_t = dataframe.loc[n, "text_around"].value_counts(sort=True).index[0]
    elif not dataframe["negation"].value_counts(sort=True).index[0]:
        value = 1
        text_t = (
            dataframe.loc[dataframe["negation"] == False, "text_around"]
            .value_counts(sort=True)
            .index[0]
        )
    else:
        value = np.nan
        text_t = np.nan
    return (value, text_t)


def fun_param(dataframe: pd.DataFrame):
    if not dataframe.empty:
        value = dataframe["label_value"].iloc[0]
        text_t = dataframe["text_around"].iloc[0]
    else:
        value = np.nan
        text_t = np.nan
    return (value, text_t)


def repartition_function(dataframe: pd.DataFrame):

    label = dataframe["label_name"].iloc[0]
    nb_occur = []
    value = []
    text = []

    # conditions
    m = dataframe.isin_spanparagraph
    m_bar = ~dataframe.isin_spanparagraph
    n = dataframe.negation
    n_bar = ~dataframe.negation
    f = ~dataframe.label_value.str.contains(
        r"\d+[\.\,]\d*", regex=True, flags=re.IGNORECASE, na=False
    )
    f_bar = dataframe.label_value.str.contains(
        r"\d+[\.\,]\d*", regex=True, flags=re.IGNORECASE, na=False
    )

    nb_occur_temp = dataframe.shape[0]

    if label == "direct_lcr":
        res = fun_lcr_bool_neg(dataframe, m=m, m_bar=m_bar, n=n, n_bar=n_bar)
    elif label in ["gly_lcr_bool", "prot_lcr_bool"]:
        res = fun_lcr_bool(dataframe, m=m, m_bar=m_bar)
    elif label in ["gb_lcr", "gr_lcr"]:
        res = fun_lcr_value(dataframe, f=f, m=m,m_bar=m_bar,f_bar=f_bar)
    elif label in ['prot_lcr_val','gly_lcr_val','pnn_lcr']:
        res = fun_lcr_divers(dataframe, m=m, m_bar=m_bar)

    elif label in ["pnn_sg_val", "gb_sg_val"]:
        res = fun_sg_val(dataframe, m=m, m_bar=m_bar)
    elif label in ['pnn_sg_bool','gb_sg_bool','nfs']:
        res = fun_sg_bool(dataframe, m=m, m_bar=m_bar)

    elif (label in list_dict_mening_sau) or (label in list_dict_meningite):
        res = fun_bool_neg_majorite(dataframe, n=n)

    elif (label in list_dict_adm_sau) or (label in list_dict_constvital_sau):
        res = fun_param(dataframe)
        
    elif label in ['end_paragrapher','atcd']:
        res = (0,0)
    else:
        res = [np.nan,np.nan]

    value_temp = res[0]
    text_temp = res[1]

    nb_occur.append(nb_occur_temp)
    value.append(value_temp)
    text.append(text_temp)

    return pd.DataFrame({"nb_occur": nb_occur, "value": value, "text": text})


def bms_aggregate2(
    DATAFRAME: pd.DataFrame,
    list_togroupby: List[Any] = ["note_id", "label_name"],
    list_labels: List[str] = ["pas","pad","dextro","gly_lcr_val","prot_lcr_val","gr_lcr","gb_lcr","gb_sg_val","pnn_sg_val",],
) -> pd.DataFrame:
    """Fonction servant à passer d'une dataframe contenant nxp lignes où n représente 
    le nombre d'entité par document et p le nombre de document, à un dataframe contenant p lignes. 
    L'aggrégation des données est basées sur des règles simples:
    - Sélection de la variable: 
        - Majoritaire: Valeur la plus représentée dans le document
        - Première occurance
        - Dominante: La condition satisfaite remporte la décision
    - Conditionnelle: Valeur prédominante suivant une condition donnée
        par exemple: 
            - négation = True/False 
            - isin_spanparagraph = True/False
            - format value = True/False
    
    Paramêtres:
    -----------
    - dataframe: pandas.DataFrame contenant les noms de colonne suivants:
        - label_value
        - negation
        - isin_spanparagraph
        - text_around
    - list_togroupby: Liste des nom de colonne nécessaire au pandas.DataFrame.groupby
    """

    dataframe = DATAFRAME.groupby(list_togroupby).apply(repartition_function)

    dataframe.reset_index(inplace=True)

    df_temp = bms_cleanaggregate(dataframe=dataframe, list_labels=list_labels)

    df_f = df_temp.pivot(
        index=["patient_num_13","encounter_num","note_id"], 
        columns="label_name", 
        values=["nb_occur", "value", "text"]
    )
    df_f.columns = [f"{t[1]}_{t[0]}" for t in df_f.columns]
    df_f.sort_index(axis=1, ascending=True, inplace=True)

    return df_f



def bms_diagperf(
    df_postlabelling: pd.DataFrame, directory_tosave: str = None, nb_test: int = 0
) -> List[pd.DataFrame.pivot_table]:
    """
    bms_diagperf est une fonction permettant de connaitre les performances 
    des regex après relecture.
    
    Paramètres:
    -----------
    df_postlabelling: pandas.DataFrame résultat 
    """

    res_f = []
    for label in df_postlabelling.label_name.unique():
        df_temp = (
            df_postlabelling
            .loc[df_postlabelling.label_name == label]
        )
        VP = (
            df_temp["gold_label_value"]
            .loc[(df_temp.added_by_user == False) & (df_temp.good_match == True)]
            .count()
        )
        FN = (
            df_temp["gold_label_value"]
            .loc[df_temp.added_by_user == True]
            .count()
        )
        FP = (
            df_temp["gold_label_value"]
            .loc[
                (df_temp.good_match == True) & 
                (df_temp.gold_good_match_value == False)
            ]
            .count()
        )
        TOT = df_temp["gold_label_value"].count()
        res = {
            "label": label,
            "true_positive": VP,
            "false_negative": FN,
            "false_positive": FP,
            "total": TOT,
            "precision": round((VP / (VP + FP)), 2),
            "recall": round((VP / (VP + FN)), 2),
            "f1_score": round(((2 * VP) / (2 * VP + FP + FN)), 2),
        }
        res_f.append(res)
    df_f = pd.DataFrame(res_f)
    
    table1 = (
        df_f[
        ["label", "false_negative", 
         "false_positive", "true_positive", 
         "total"]
    ].pivot_table(columns="label", sort=False))

    table2 = (
        df_f[["label", "total", "recall", "precision", "f1_score"]]
        .pivot_table(columns="label", sort=False)
    )
    res = [table1, table2]

    file_name_1 = f"{directory_tosave}/table1_{nb_test}.pickle"
    file_name_2 = f"{directory_tosave}/table2_{nb_test}.pickle"
    
    if directory_tosave == None:
        print("Data not save")
        return res
    elif (os.path.exists(file_name_1) or os.path.exists(file_name_2)):
        print("Data already exist, do you want to erase previous results?")
        print('Input "y" for yes or any other for no')
        x = input()
        if x == "y":
            print("Saving succeeded")
            table1.to_pickle(file_name_1)
            table2.to_pickle(file_name_2)
            return res
        else :
            print('Data not save')
            return res
    else:
        print("Saving succeeded")
        table1.to_pickle(file_name_1)
        table2.to_pickle(file_name_2)
        return res

    
def bms_score_calc (df_nlp :pd.DataFrame)-> pd.DataFrame:
    """
    """
    dataframe = df_nlp.copy()
    
    list_bms_score = [
        'convulsion_value',
        'gb_lcr_value',
        'pnn_lcr_value',
        'gb_sg_val_value',
        'pnn_sg_val_value',
        'prot_lcr_val_value',
        'direct_lcr_value',
    ]
    
    list_bms = [
        'bms_conv',
        'bms_direct_lcr',
        'bms_prot',
        "bms_pnn_lcr",
        "bms_pnn_sg"
    ]
    
    list_temp = []
    
    for i in list_bms_score:
        if i in dataframe.columns:
            list_temp.append(i)
    
    for i in list_temp:
        dataframe.loc[dataframe[i]=='FP',i] = (
            dataframe
            .loc[dataframe[i]=='FP',i]
            .astype(str)
            .replace('FP',np.nan)
        )
        dataframe.loc[:,i] = pd.to_numeric(dataframe[i],errors='coerce')
        na_cond = dataframe[i].isna()==False
        
        if i == "convulsion_value":
            dataframe['bms_conv'] = dataframe.loc[:,i]
            
        if i == "direct_lcr_value":
            dataframe['bms_direct_lcr'] = dataframe.loc[:,i]
        
        if i == "prot_lcr_val_value":
            seuil_prot = (dataframe[i]>=0.8)
            # conditions = [
            #     (seuil_prot),
            #     (seuil_prot==False) & (na_cond)
            # ]
            # choices = [1,0]
            # dataframe['bms_prot'] = np.select(conditions,choices, default=np.nan)
            
            dataframe['bms_prot']=np.nan
            if dataframe.loc[seuil_prot].empty==False:
                for d in dataframe.loc[seuil_prot].index:
                    dataframe.loc[d,'bms_prot'] = 1
            if dataframe.loc[na_cond & (seuil_prot==False)].empty==False:
                for d in dataframe.loc[na_cond & (seuil_prot==False)].index:
                    dataframe['bms_prot'].loc[d] = 0
            
        if i == "pnn_lcr_value":
            seuil_gb_lcr = dataframe['gb_lcr_value']<1000
            seuil_pnn_lcr = (
                dataframe.loc[
                    (seuil_gb_lcr == False) & (na_cond),'gb_lcr_value'
                ]*dataframe.loc[
                    (seuil_gb_lcr == False) & (na_cond), "pnn_lcr_value"]>= 1000)
            
#             conditions = [
#                 (seuil_gb_lcr),
#                 (seuil_gb_lcr== False) & (na_cond) & (seuil_pnn_lcr),
#                 (seuil_gb_lcr== False) & (na_cond) & (seuil_pnn_lcr==False)
#             ]
#             choices = [0,1,0]
#             dataframe['bms_pnn_lcr'] = np.select(conditions,choices,default=np.nan)
            
            dataframe['bms_pnn_lcr'] = np.nan
            dataframe['bms_pnn_lcr'].loc[seuil_gb_lcr] = 0
            if dataframe.loc[
                (na_cond) & 
                (seuil_gb_lcr==False)].empty==False:
                for d in dataframe.loc[
                    (na_cond) & 
                    (seuil_gb_lcr==False)].index:
                    if (dataframe.loc[d,'gb_lcr_value']*dataframe.loc[d,"pnn_lcr_value"]>=1000):
                        dataframe["bms_pnn_lcr"].loc[d] = 1
                    else: dataframe["bms_pnn_lcr"].loc[d] = 0
                    
        if i =="pnn_sg_val_value":
            seuil_gb_sg = dataframe['gb_sg_val_value']<=10000
            seuil_pnn_sg = dataframe[i]<10000
            na_cond_gb = (dataframe['gb_sg_val_value'].isna()==True)
            
            
#             conditions = [
#                 (seuil_gb_sg),
#                 (na_cond_gb) & (seuil_pnn_sg),
#                 (na_cond) & (seuil_pnn_sg==False) & (na_cond_gb),
#                 (na_cond) & (seuil_pnn_sg==False) & (seuil_gb_sg==False)
#             ]
            
#             choices = [0,0,1,1]
            
#             dataframe['bms_pnn_sg'] = np.select(conditions, choices, default=np.nan)
            
            dataframe['bms_pnn_sg'] = np.nan
            dataframe['bms_pnn_sg'].loc[seuil_gb_sg] = 0
            dataframe['bms_pnn_sg'].loc[na_cond_gb & seuil_pnn_sg] = 0
            
            if dataframe.loc[na_cond & (seuil_pnn_sg==False) & na_cond_gb].empty==False:
                for d in dataframe.loc[na_cond & (seuil_pnn_sg==False) & na_cond_gb].index:
                    dataframe['bms_pnn_sg'].loc[d] = 1
                    
            if dataframe.loc[na_cond & (seuil_gb_sg==False) & (seuil_pnn_sg==False)].empty==False:
                for d in dataframe.loc[na_cond & (seuil_gb_sg==False) & (seuil_pnn_sg==False)].index:
                    dataframe['bms_pnn_sg'].loc[d] = 1
        
    list_temp2 = []
    
    for i in list_bms:
        if i in dataframe.columns:
            list_temp2.append(i)
    
    dataframe['score_bms'] = dataframe.loc[:,list_temp2].sum(axis=1,skipna=False)
    dataframe['score_bms_bis'] = dataframe.loc[:,list_temp2].sum(axis=1,skipna=True)
    dataframe['nb_NaN_bms'] = dataframe.loc[:,list_temp2].isnull().sum(axis=1, skipna=False)
    
    # for col in list_temp2:
    #    for i in dataframe.loc[dataframe[col].isna()==True].index:
    #        dict_index.setdefault(i,[]).append(col)
    # for k,v in dict_index.items():
    #    dataframe.loc[k,'col_NaN']=v
                    
    return dataframe


def concat_df_i2b2_bio (dataframe : pd.DataFrame) -> pd.DataFrame:
    """
    La fonction sert à passer à concatener les informations extrait 
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


def merge_na_bms (
    df_bms: pd.DataFrame,
    df_bio_i2b2: pd.DataFrame,
) -> pd.DataFrame :
    """
    """
    
    df_temp = df_bms.copy()
    
    list_bms_score = [
        'gb_lcr',
        'pnn_lcr',
        'gb_sg',
        'pnn_sg',
        'prot_lcr',
        'direct_lcr',
    ]

    list_colonnes_interet=[]
    for i in list_bms_score:
        colname_df = [x for x in df_bio_i2b2.columns if re.match(str(i),str(x))]
        colname_bms = [x for x in df_temp.columns if re.match(str(i),str(x))]

        if (len(colname_df) > 0) & (len(colname_bms) > 0):
            list_colonnes_interet.append(i)
    
    for l in list_colonnes_interet:
        colname_bms = [x for x in df_temp.columns if re.match(str(l),str(x))][0]
        colname_df = [x for x in df_bio_i2b2.columns if re.match(str(l),str(x))][0]

        na_cond = df_temp[colname_bms].isna()
        pat_cond_bms = df_temp.pat_num.isin(df_bio_i2b2.pat_num.unique())
        encount_cond_bms = df_temp.encount_num.isin(df_bio_i2b2.encount_num.unique())
        
        list_index = [x for x in df_temp.loc[(na_cond) & (pat_cond_bms) & (encount_cond_bms)].index]
        list_pat = [x for x in df_temp['pat_num'].loc[(na_cond)]]
        list_encount = [x for x in df_temp['encount_num'].loc[(na_cond)]]
        
        pat_cond = df_bio_i2b2.pat_num.isin(list_pat)
        encount_cond = df_bio_i2b2.encount_num.isin(list_encount)

        i=0
        list_value = [x for x in df_bio_i2b2.loc[
            (pat_cond) &
            (encount_cond),
            colname_df
        ]]
        
        for ind in list_index:
            if l in ["pnn_sg","gb_sg"]:
                df_temp.loc[ind ,colname_bms] = list_value[i]*(10**3)
                                                    
            else :
                df_temp.loc[ind ,colname_bms] = list_value[i]
            i += 1
            
    dataframe = bms_score_calc(df_temp)
    
    return dataframe


def bms_contingeance (
    df_goldstandard : pd.DataFrame,
    df_newtest : pd.DataFrame,
    save_path : str,
) -> pd.crosstab :
    """
    """
    
    list_bms2 = [
    'bms_conv',
    'bms_direct_lcr',
    'bms_prot',
    "bms_pnn_lcr",
    "bms_pnn_sg",
    "score_bms",
    "score_bms_bis",
    "score_bms_bin",
    "score_bms_bis_bin"
    ]
    
    list_colname = []
    for l in list_bms2:
        if (l in df_goldstandard.columns) & (l in df_newtest.columns):
            list_colname.append(l)
    
    res_f = []
    for l in list_colname:
        globals()[f'res_{l}'] = (
            pd
            .crosstab(
                columns = df_goldstandard[l], 
                index = df_newtest[l],
                colnames = [f'goldstd_{l}'], 
                rownames = [f'test_{l}'],
                dropna = False,
                margins = True
            )
        )
        path_save = str(save_path+f'res_{l}.pickle')
        globals()[f'res_{l}'].to_pickle(path_save)
        
        df_temp = (
            pd
            .crosstab(
                columns = df_goldstandard[l], 
                index = df_newtest[l],
                colnames = [f'goldstd_{l}'], 
                rownames = [f'test_{l}'],
                dropna = False,
                margins = False
            )
        )
        
        VN = 0
        VP = 0
        FN = 0
        FP = 0
        for x in df_temp.columns:
            for y in df_temp.index:
                if (x == y) & (x != 0):
                    VP += df_temp.loc[y,x]
                elif (y == 0) & (x !=0):
                    FN += df_temp.loc[y,x]
                elif (x == 0) & (y != 0):
                    FP += df_temp.loc[y,x]
                elif (x==0) & (y == 0):
                    VN = df_temp.loc[0,0]
        
        TOT = VP + VN + FP + FN
        
        if VP == 0:
            precision = 0
            recall = 0
            f1_score = 0
            if VN == 0:
                accurancy = 0
            else:
                accurancy = round(((VP+VN)/TOT),2)
        else:
            accurancy = round(((VP+VN)/TOT),2)
            precision = round((VP / (VP + FP)), 2)
            recall = round((VP / (VP + FN)), 2)
            f1_score = round((2*((precision*recall)/(precision+recall))), 2)
        
        res = {"label": l,
               "accurancy": accurancy,
               "precision": precision,
               "recall": recall,
               "f1_score": f1_score,
               "na_gold": df_goldstandard[l].isna().sum(),
               "na_test": df_newtest[l].isna().sum(),
               "total_pat": df_goldstandard[l].shape[0]
        }
        res_f.append(res)
        
    df_perf = pd.DataFrame(res_f)
        
    return df_perf


