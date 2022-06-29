from .main import *

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
        
    if 'instance_num' in dataframe.columns:
        dataframe.rename(columns={'instance_num':'note_id'},inplace=True)
        
    dataframe['title'] = ("note_id : "+ dataframe['note_id'].astype(str))
    
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
    
    if 'eds.isin_spanparagraph' in list_pipe:
        dataframe['isin_spanparagraph'] = dataframe['ent'].apply(lambda x : x._.isin_spanparagraph)

    if save_path == None:
        pass
    elif save_path.endswith("csv"):
        dataframe.drop(["doc",], axis=1,).to_csv(save_path)
    else:
        raise Exception("Format de fichier incorrect : doit être .pickle ou .csv")

    print(dataframe.shape)
    return dataframe

def perf_regex (df_temp : pd.DataFrame) -> pd.DataFrame :
    
    label = df_temp["label_name"].iloc[0]
    a = df_temp.added_by_user == True
    gg = df_temp.gold_good_match_value == True
    gm = df_temp.good_match == True
    sp = df_temp.gold_isin_spanparagraph_value == True
    gsp = df_temp.isin_spanparagraph == True
    
    l_VP = []
    l_FN = []
    l_FP = []
    l_TOT = []
    
    if label in ['pnn_sg_bool','pnn_sg_val','gb_sg_bool','gb_sg_val']:
        VP = (
            df_temp['gold_label_value']
            .loc[(~a) & gm & gg & (~sp) & (~gsp)]
            .count()
        )
        FN = (
            df_temp['gold_label_value']
            .loc[a & (~sp) & (~gsp)]
            .count()
        )
        FP = (
            df_temp['gold_label_value']
            .loc[(~a) & gm & (~gg) & (~sp) & (~gsp)]
            .count()
        )
        TOT = (
            df_temp['gold_label_value']
            .loc[(~sp) & (~gsp)]
            .count()
        )
    
    elif label in ['gb_lcr','gly_lcr_bool','gly_lcr_val','gr_lcr','pnn_lcr','prot_lcr_val','prot_lcr_bool']:
        VP = (
            df_temp['gold_label_value']
            .loc[(~a) & gm & gg & sp & gsp]
            .count()
        )
        FN = (
            df_temp['gold_label_value']
            .loc[a & sp & gsp]
            .count()
        )
        FP = (
            df_temp['gold_label_value']
            .loc[(~a) & gm & (~gg) & sp & gsp]
            .count()
        )
        TOT = (
            df_temp['gold_label_value']
            .loc[sp & gsp]
            .count()
        )
    
    else:
        VP = (
            df_temp['gold_label_value']
            .loc[(~a) & gm & gg]
            .count()
        )
        FN = (
            df_temp['gold_label_value']
            .loc[a]
            .count()
        )
        FP = (
            df_temp['gold_label_value']
            .loc[(~a) & gm & (~gg)]
            .count()
        )
        TOT = (
            df_temp['gold_label_value']
            .count()
        )

    l_TOT.append(TOT)
    l_VP.append(VP)
    l_FP.append(FP)
    l_FN.append(FN)
    
    return pd.DataFrame({'Nb Vrai Positif':l_VP,
                         'Nb Faux Positif':l_FP,
                         'Nb Faux Négatif':l_FN,
                         'Nb Total':l_TOT})


def calc_diag_perf(x):
    
    Pr = round(x[0]/(x[0]+x[1]),2)
    Re = round(x[0]/(x[0]+x[2]),2)
    f1 = round(2*((Pr*Re)/(Pr+Re)),2)
    
    return [Re,Pr,f1,x[3]]


def bms_diagperf(
    df_postlabelling: pd.DataFrame, 
    directory_tosave: str = None, 
    nb_test: str = '0'
) -> List[pd.DataFrame.pivot_table]:
    """
    bms_diagperf est une fonction permettant de connaitre les performances 
    des regex après relecture.
    
    Paramètres:
    -----------
    df_postlabelling: pandas.DataFrame résultat 
    """

    df_f = df_postlabelling.groupby('label_name').apply(perf_regex)
    df_f = df_f.droplevel(1)
    
    df_t = df_f.apply(calc_diag_perf, axis=1, raw=True)
    df_t.columns = ['Recall','Precision','F1-score','Nb Total']

    res = [df_f,df_t]
    
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
            df_f.to_pickle(file_name_1)
            df_t.to_pickle(file_name_2)
            return res
        else :
            print('Data not save')
            return res
    else:
        print("Saving succeeded")
        df_f.to_pickle(file_name_1)
        df_t.to_pickle(file_name_2)
        return res