from .main import *

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
        "pnn_lcr"
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
                    .replace(r"[a-zA-Zéè\/ :=\‰]*", "", regex=True)
                )
                dataframe.loc[m & n, "value"] = (
                    dataframe.loc[m & n, "value"]
                    .astype(str)
                    .replace(r"\,", ".", regex=True)
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
    return [value, text_t]


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
    return [value, text_t]


def fun_lcr_divers(dataframe: pd.DataFrame, m, m_bar):
    if not dataframe.loc[m].empty:
        value = dataframe.loc[m, "label_value"].value_counts(sort=True).index[0]
        text_t = (
            dataframe.loc[dataframe["label_value"] == value,'text_around']
            .value_counts(sort=True)
            .index[0]
        )
    elif not dataframe.loc[m_bar].empty:
        value = "FP"
        text_t = dataframe.loc[m_bar, "text_around"].value_counts(sort=True).index[0]
    else:
        value = None
        text_t = None
    return [value, text_t]


def fun_lcr_value(dataframe: pd.DataFrame, f, f_bar, m, m_bar):
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
    return [value, text_t]


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
    return [value, text_t]


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
    return [value, text_t]


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
    return [value, text_t]


def fun_param(dataframe: pd.DataFrame):
    if not dataframe.empty:
        value = dataframe["label_value"].iloc[0]
        text_t = dataframe["text_around"].iloc[0]
    else:
        value = np.nan
        text_t = np.nan
    return [value, text_t]


def repartition_function_agg(dataframe: pd.DataFrame):

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

    if label in ["direct_lcr",'ex_direct_lcr'] :
        res = fun_lcr_bool_neg(dataframe, m=m, m_bar=m_bar, n=n, n_bar=n_bar)
        
    elif label in ["gly_lcr_bool", "prot_lcr_bool"]:
        res = fun_lcr_bool(dataframe, m=m, m_bar=m_bar)
        
    elif label in ["gb_lcr", "gr_lcr"]:
        res = fun_lcr_value(dataframe, f=f, m=m,m_bar=m_bar, f_bar=f_bar)
        
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
        res = [0,0]
    else:
        res = [np.nan,np.nan]

    nb_occur.append(nb_occur_temp)
    value.append(res[0])
    text.append(res[1])

    return pd.DataFrame({"nb_occur": nb_occur, "value": value, "text": text,})


def bms_aggregate(
    DATAFRAME: pd.DataFrame, 
    list_togroupby: List[Any] = ["note_id", "label_name"],
    list_labels: List[Any] = [
        "pas",
        "pad",
        "dextro",
        "gly_lcr_val",
        "prot_lcr_val",
        "gr_lcr",
        "gb_lcr",
        "gb_sg_val",
        "pnn_sg_val",
]
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

    dataframe = DATAFRAME.groupby(list_togroupby)
    
    dataframe = dataframe.apply(repartition_function_agg)

    dataframe.reset_index(inplace=True)
    
    df_temp = bms_cleanaggregate(dataframe = dataframe, list_labels=list_labels)

    df_f = df_temp.pivot(
        index=["patient_num_13","encounter_num","note_id"],
        columns="label_name",
        values=["nb_occur", "value", "text"]
    )
    df_f.columns = [f"{t[1]}_{t[0]}" for t in df_f.columns]
    df_f.sort_index(axis=1, ascending=True, inplace=True)

    return df_f

