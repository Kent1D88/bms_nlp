from .main import *
from bms_nlp.bms_nlp_pipe import *
from bms_nlp.bms_agregate import *
from bms_nlp.bms_calc_score import *
from bms_nlp.bms_cleandf import *

regex = dict_bms

config_norm = dict(lowercase = True,
              accents = True,
              pollution = False,
              quotes = False)

config_matcher = dict(regex=regex,
                      attr='NORM',
                      ignore_excluded = False)

config_isinspanparagraph = dict(list_labels=['pl'],
                                attr = 'NORM',
                                ignore_excluded = False,
                               )

list_pipe = ['eds.normalizer',
             'eds.sentences',
             'eds.matcher',
             'eds.negation',
             'eds.hypothesis',
             'eds.isin_spanparagraph'
            ]

list_togroupby = ['patient_num_13','encounter_num','note_id','label_name']

list_labels = [
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

list_reorg = ['convulsion_value','bms_conv',
              'gb_lcr_value','pnn_lcr_value','bms_pnn_lcr',
              'gb_sg_val_value','pnn_sg_val_value','bms_pnn_sg',
              'prot_lcr_val_value','bms_prot',
              'ex_direct_lcr_value','direct_lcr_value','bms_direct_lcr',
              'score_bms','score_bms_bis','score_bms_bin',
              'nb_NaN_bms']

def algo_bms(dataframe : pd.DataFrame,
             df_goldstd : pd.DataFrame,
             df_i2b2 : pd.DataFrame,
             save_path : str,
            )-> pd.DataFrame:
    """
    """
    
    # Introduire sécurités:
    # dataframe contient ['observation_blob','note_text','note_id',
    # 'patinet_num_13','encounter_num']
    
    df_pipe = get_bmspipe(
        dataframe = dataframe,
        config_norm = config_norm,
        config_matcher = config_matcher,
        config_isinspanparagraph = config_isinspanparagraph,
        list_pipe = list_pipe,
        save_path = None
    )
    
    df_pipe = df_pipe[['note_id','patient_num_13',
              'encounter_num',
              'offset_begin','offset_end', 'label_name', 'label_value',
              'negation', 'hypothesis', 'isin_spanparagraph',
              'ent', 'key', 'text_around','title']]
    
    df_temp = bms_aggregate(df_pipe,
                           list_togroupby = list_togroupby,
                           list_labels = list_labels)
    
    list_col=[col for col in df_temp.columns if re.search('_value',col)]
    
    df_temp = df_temp[list_col]
    
    df_temp1 = bms_score_calc(df_temp)
    df_temp1 = df_temp1[list_reorg]
    df_temp1.reset_index(inplace=True)
    df_temp2 = merge_na_bms(df_bms = df_temp1,
                            df_bio_i2b2 = df_i2b2
                           )
    
    list_bms_com = list(set(df_temp1.columns) &
                        set(df_temp2.columns) &
                        set(df_goldstd.columns)
                       )
    
    df_temp1 = (
        df_temp1[list_bms_com]
        .sort_values(by=['patient_num_13','encounter_num'],
                     ignore_index=True
                    )
    )
    df_temp2 = (
        df_temp2[list_bms_com]
        .sort_values(by=['patient_num_13', 'encounter_num'],
                    ignore_index=True
                    )
    )
    df_goldstd = (
        df_goldstd[list_bms_com]
        .sort_values(by=['patient_num_13','encounter_num'],
                   ignore_index=True)
    )
    
    path_save_1 = save_path+'_without_i2b2'
    path_save_2 = save_path+'_with_i2b2'
    
    df_f1 = bms_contingeance(
        df_goldstandard = df_goldstd,
        df_newtest = df_temp1,
        save_path = path_save_1,
        nbof_backup = ''
    )
    
    df_f2 = bms_contingeance(
        df_goldstandard = df_goldstd,
        df_newtest = df_temp2,
        save_path = path_save_2,
        nbof_backup = ''
    )
    
    return (df_f1, df_f2)