# -*- coding: utf-8 -*-
dict_grp = dict(end_paragrapher = [r'\n \n ']
)

dict_adm_sau = dict(
    date_entree = [r'(?<=entre\(e\)\sle:\s)[\d\/]{8,10}', 
                   r"(?<=date\sd\Wentr[ée]e\sau\sSAU:\s)[\d\/]{8,10}",
                   r'(?<=date\s:\s)[\d\/]{8,10}',
                  ],
    date_naissance = [r'(?<=ne\(e\)\sle\s:)\s?[\d\/]{8,10}',
                      r'(?<=date\sde\snaissance\s:\s)[\d\/]{8,10}',
                      r'(?<=naiss\s\W\s)[\d\/]{8,10}',
                     ],
    sex = [r'(?<=sexe\s\W)\s?[f|m]'],
)

dict_constvital_sau = dict(
    glasgow = [r'(?<=glasgow\s\W\s)\d{1,2}',
               r'(?<=glasgow\s)\d{1,2}',
               r'(?<=gcs\s\W\s)\d{1,2}',
               r'(?<=gcs\s)\d{1,2}'],
    temp = [r'\b(?<=temp\W{3})\d{2}.?\d?(?=\W*?[cC])?',
            r'\b(?<=temp\s\(°C\)\s:\s)\d{2}.?\d?',
           ],
    pas = [r'(?<=\b[Pp][aA]\s\w{4}\s[g|G|D|d]\W{3})\s?\d{2,3}(?=\s?\/\s?\d{2,3})',
          r'(?<=\b[tT]a[g|d].{15})(\d+)',
          r'(?<=\b[pP][Aa]\s:\s)\s?\d{2,3}(?=\s?\/\s?\d{2,3})',
          r'(?<=\bta\s\(\w{6}\)\s:\s)\d{2,3}(?=\s?\/\s?\d{2,3})',
         ],
    pad = [r'(?<=\b[Pp][aA]\s\w{4}\s[g|G|D|d]\W{3})\s?\d{2,3}\s?\/\s?\d{2,3}',
          r'(?<=\b[tT]a[g|d].{15})(\d+)\s?\/\s?\d{2,3}',
          r'(?<=\b[pP][Aa]\s:\s)\s?\d{2,3}\s?\/\s?\d{2,3}',
          r'(?<=\bta\s\(\w{6}\)\s:\s)\d{2,3}\s?\/\s?\d{2,3}',
         ],
    pouls = [r'\b(?<=[fF][cC]\W{3})\d{2,3}(?=\/mi?n)?',
             r'\b(?<=[fF][Cc].{12})(\d+)',
            ],
    freq_resp = [r'\b(?<=[Ff][rR]\W{3})\d{2}(?=\s?\/mi?n)?',
                 r'\b(?<=[Ff][rR].{12})(\d{2})',
                ],
    sao2_sat = [r'\b(?<=[Ss][a|p][oO]2\W{3})\d{2,3}(?=\s*?%)',
                r'\b(?<=[Ss][a|A|P|p][oO]2\W{4})\d{2,3}(?!\s*?%)',
               ],
    dextro = [r'\b(?<=dextro\W{3})\d+\.?\d{0,2}?(?=\W*?mmol\W[Ll])?',
              r'\b(?<=\(mmol par [Ll]\)\W{3})\d+.?\d{0,2}?',
              r'\b(?<=glycemie capillaire\s:\s)\s?\d+\.?\d{0,2}[\w|\/]+',
             ],
    eva = [r'\b(?<=eva : )\s?\d{1,2}']
)

dict_mening_sau = dict(
    pl =[r'\bpl[\s|:|\n]', 
         r'\bpl[\s|\W]', 
         r'\bponct\w*\W+lomb\w*',
         r'lcr',
        ],
    raid_nuque = [r'\brai?de\w*\W*?(de)?\W*?nuq\w*',
                  r'\brai?de\w*', 
                  r'\bbrudz?\w+', 
                  r'\bker\w+',
                 ],
    cervicalgie = [r'\bc\w*alg\w*',
                  ],
    cephalee =[r'\bcep\w*[éeè]\w*', 
               r'\bcephal\w*',
              ] ,
    purpura = [r'\bpurp\w*',
              ] ,
    convulsion = [r'\bconvu\w*', 
                  r'\bepilep\w*', 
                  r'\bcri\w*\s?ton\w*\W?clon\w*', 
                  r'\bpost\W?cri\w*',
                  r'\bcri\w*\s?comi\w*',
                 ],
    fievre = [r'\bfiev\w*', 
              r'\b\w*therm\w*', 
              r'\bfriss\w*',
              r'\bfeb\w*',
             ],
    sdmeninge = [r'\bmeninge+', 
                 r'\bs\w*?d\w*?\s?me\w*[n|g|n]{2,}\w*e+',
                ],
)

dict_meningite= dict(
    meningite = [
        r'\bm\w*git\w*',
        r'meningo.?enceph\w*',
    ],
)
        
dict_pl_sau = dict(
    gb_lcr = [r'\b\d{1,5} ?(?= ?elements?)',
              r'(?<=\belement)s?[\s|:]{1,4}\d{1,5}\s',
              r'(?<=\bleucocyte)s?[\s|:]{1,4}\d{1,5}\s',
              r'(?<=\bleu)[\s|:]{1,4}\d{1,5}\s',
              r'(?<=\bleuco)s?[\s|:]{1,4}\d{1,5}\s',
              r'\b\d+(?=\sel\w*)',
              r'(?<=\bgb)\W?\s?\d+\W',
              r'\b\d+(?=\s?leuc?\w*)',
              r'\b\d+(?=\s?gb\s)',
             ],
    pnn_lcr = [r'(?<=\bpnn\W)\s?\d+ *%',
               r'\d+ *%(?=\s?\Wpnn)',
               r'(?<=\bpolynucleaire neutrophile)\s+\d+ *%',
               r'\d+ *%(?=\s*polynucleaire neutrophile)'
        
    ],
    gr_lcr = [r'\b\d{1,5}\s?(?=hem\w*)',
              r'(?<=hematie)s?[\s|:]{1,4}\d{1,5}\W',
              r'\b\d+(?=\sgr\s)',
              r'\b(?<=hem\s)\d+\W',
              r'\b(?<=gr\s)\d+\W',
             ],
    direct_lcr = [r'\bgermes?\W+?\w*\W*?(visibles?|direct)',
                  r'\bbact[ée]ries?\W*?\w*\W*?(visibles?|direct)',
                  r'\bexamens?\W+directs?',
                  r'\bed\s',
                  r'direct\snormal',
                  r'\bgermes?',
                  r'\bdirect',
                 ],
    prot_lcr_bool = [r'\b[pP]rot\w*rachi[s|e]?\W*?[nN]\w*',
                     r'\b\w*[pP]rot\w*rachi[s|e]?',
                        ],
    prot_lcr_val = [r'(?<=[pP]rot)\w*?\W*\d+[\.|\,]\d+',
                    r'\b\w*?(?<=[Pp]rot)\w*?\W*\w*?\W*\d+[\.|\,]\d+',
                   ],
    gly_lcr_bool = [r'\b[gG]ly\w*rachi[s|e]?\W*?[nN]\w*',
                    r'\b\w*[gG]l\w*rachi[s|e]?',
                   ],
    gly_lcr_val = [r'(?<=[gG]luc)\w*?\W*\d+[\.|\,]\d+',
                   r'(?<=[gG]lycorachie)\w*?\W*\d+[\.|\,]\d+',
                   r'\b\w*?(?<=[gG]lycor)\w*?\W*\w*?\W*\d+[\.|\,]\d+',
                   r'\b(?<=gly\s)\d+\.\d',
                  ],
)

dict_sg_sau = dict(
    pnn_sg_bool = [r'\bpnn',
                   r'\bpolynucleaire neutrophile',
                  ],
    pnn_sg_val = [r'(?<=\bpnn\W)\s?\d+ ?\d*',
                  r'\d+ ?\d+(?=\s?\Wpnn)',
                  r'(?<=\bpolynucleaire neutrophile)\s+\d+ ?\d*',
                  r'\d+ ?\d*(?=\s*polynucleaire neutrophile)'
                 ],
    nfs = [r'nfs'],
    gb_sg_bool = [r'gb'],
    gb_sg_val = [r'(?<=gb\s)\s?\d+ ?\d*',
                r'\d+ ?\d*(?=\s*?gb)',
                r'(?<=\bleucocyte)s?[\s|:]{1,4}\d{1,5} ?\d*\s',
                r'(?<=\bleu)[\s|:]{1,4}\d{1,5} ?\d*\s',
                r'(?<=\bleuco)s?[\s|:]{1,4}\d{1,5} ?\d*\s',
                r'\b\d+ ?\d*(?=\sel\w*)',]
)

dict_bms_score = dict(
    convulsion = [r'\bconvu\w*', 
                  r'\bepilep\w*', 
                  r'\bcri\w*\s?ton\w*\W?clon\w*', 
                  r'\bpost\W?cri\w*',
                  r'\bcri\w*\s?comi\w*',
                 ],
    prot_lcr_bool = [r'\b[pP]rot\w*rachi[s|e]?\W*?[nN]\w*',
                     r'\b\w*[pP]rot\w*rachi[s|e]?',
                        ],
    prot_lcr_val = [r'(?<=[pP]rot)\w*?\W*\d+[\.|\,]\d+',
                    r'\b\w*?(?<=[Pp]rot)\w*?\W*\w*?\W*\d+[\.|\,]\d+',
                   ],
    gb_lcr = [r'\b\d{1,5} ?(?= ?elements?)',
              r'(?<=\belement)s?[\s|:]{1,4}\d{1,5}\s',
              r'(?<=\bleucocyte)s?[\s|:]{1,4}\d{1,5}\s',
              r'(?<=\bleu)[\s|:]{1,4}\d{1,5}\s',
              r'(?<=\bleuco)s?[\s|:]{1,4}\d{1,5}\s',
              r'\b\d+(?=\sel\w*)',
              r'(?<=\bgb)\W?\s?\d+\W',
              r'\b\d+(?=\s?leuc?\w*)',
              r'\b\d+(?=\s?gb\s)',
             ],
    direct_lcr = [r'\bgermes?\W+?\w*\W*?(visibles?|direct)',
                  r'\bbact[ée]ries?\W*?\w*\W*?(visibles?|direct)',
                  r'\bexamens?\W+directs?',
                  r'\bed\s',
                  r'direct\snormal',
                  r'\bgermes?',
                  r'\bdirect',
                 ],
    pnn_sg_bool = [r'\bpnn',
                   r'\bpolynucleaire neutrophile',
                  ],
    pnn_sg_val = [r'(?<=\bpnn\W)\d+',
                  r'\d+(?=\Wpnn)',
                 ],
)


dict_bms = {**dict_adm_sau, **dict_constvital_sau,
    **dict_mening_sau, **dict_meningite,
    **dict_pl_sau, **dict_sg_sau,
}


list_dict_adm_sau = []
for key,value in dict_adm_sau.items():
    list_dict_adm_sau.append(key)
    
list_dict_constvital_sau = []
for key,value in dict_constvital_sau.items():
    list_dict_constvital_sau.append(key)

list_dict_mening_sau = []
for key,value in dict_mening_sau.items():
    list_dict_mening_sau.append(key)
    
list_dict_meningite = []
for key,value in dict_meningite.items():
    list_dict_meningite.append(key)
    
list_dict_pl_sau = []
for key,value in dict_pl_sau.items():
    list_dict_pl_sau.append(key)
    
list_dict_sg_sau = []
for key,value in dict_sg_sau.items():
    list_dict_sg_sau.append(key)
    
list_keysdict_bms = [list_dict_adm_sau, list_dict_constvital_sau,
    list_dict_mening_sau, list_dict_meningite,
    list_dict_pl_sau, list_dict_sg_sau
]