# -*- coding: utf-8 -*-
        date_entree = [r'(?<=entre\(e\)\sle:\s)[\d\/]{8,10}', 
                       r"(?<=date\sd\Wentr[ée]e\sau\sSAU:\s)[\d\/]{8,10}",
                       r'(?<=date\s:\s)[\d\/]{8,10}'
                      ],

        date_naissance = [r'(?<=ne[\(e\)]{3}\sle\s:\s)[\d\/]{8,10}',
                          r'(?<=date\sde\snaissance\s:\s)[\d\/]{8,10}',
                          r'(?<=naiss\s\W\s)[\d\/]{8,10}'
                         ],

        sex = [r'(?<=sexe\s\W\s)[F|M]'],

        glasgow = [r'(?<=glasgow\s\W\s)\d{1,2}'],

        temp = [r'\b(?<=temp\W{3})\d{2}.?\d?(?=\W*?[cC])',
                r'\b(?<=temp\s\(°C\)\s:\s)\d{2}.?\d?',
               ],

        pa = [r'(?<=[Pp][aA]\s\w{4}\s[g|G|D|d]\W{3})\s?\d{2,3}\s?\/\s?\d{2,3}',
              r'\b(?<=[tT]a[g|d].{15})(\d+)'
             ],

        pouls = [r'\b(?<=[F][C]\W{3})\d{2,3}(?=\/mi?n)',
                 r'\b(?<=[F][C].{12})(\d+)'
                ],

        freq_resp = [r'\b(?<=[Ff][rR]\W{3})\d{2}(?=\s?\/mi?n)',
                     r'\b(?<=[Ff][rR].{12})(\d{2})'
                    ],

        sao2_sat = [r'\b(?<=[Ss][a|p][oO]2\W{3})\d{2,3}(?=\s*?%)',
                    r'\b(?<=[Ss][a|A|P|p][oO]2\W{4})\d{2,3}(?!\s*?%)'
                   ],

        dextro = [r'\b(?<=dextro\W{3})\d+\.?\d?(?=\W*?mmol\W[Ll])',
                  # r'\b(?<=mmol par [Ll]\W{3})\d+.?\d?'
                 ],

        pl =[r'\b[pP][lL][\s|:|\n]', 
             r'\b[pP][Ll][\s|\W]', 
             r'\bponct\w*\W+lomb\w*',
             r'[lL][cC][rR]'
            ],

        raid_nuque = [r'\brai?de\w*\W*?(de)?\W*?nuq\w*',
                      r'\brai?de\w*', 
                      r'\bbrudz?\w+', 
                      r'\bker\w+'
                     ],
        
        cervicalgie = [r'\bc\w*alg\w*'
                      ],

        cephalee =[r'\bcep\w*[éeè]\w*', 
                   r'\bcephal\w*'
                  ] ,

        purpura = [r'\bpurp\w*'
                  ],

        convulsion = [r'\bconvu\w*', 
                      r'\bepilep\w*', 
                      r'\bcri\w*\s?ton\w*\W?clon\w*', 
                      r'\bpost\W?cri\w*',
                      r'\bcri\w*\s?comi\w*'
                     ],

        fievre = [r'\bfiev\w*', 
                  r'\b\w*therm\w*', 
                  r'\bfriss\w*',
                  r'\bfeb\w*'
                 ],
    
        sdmeninge = [r'\bmeninge+', 
                     r'\bs\w*?d\w*?\s?me\w*[n|g|n]{2,}\w*e+'
                    ],

        meningite = [r'\bm\w*git\w*',
                     r'meningo.?enceph\w*',
                    ],
    
        #LCR_match = [r'\b[pP][lL][\w|\s|\.|,|é|è|\/|:|%]+(^\v*)',
        #             r'\b[lL][cC][rR][\w|\s|\.|,|é|è|\/|:|%]+(^\v*)',
        #             r'\b[lL][cC][rR](.*\n)*',
        #             r'\b[pP][lL](.*\n)*'
        #            ],
        
        gb_lcr = [r'\b\d{1,5}\s?(?=\selements?)',
                  r'(?<=element)s?[\s|:]{1,4}\d{1,5}',
                  r'(?<=leucocyte)s?[\s|:]{1,4}\d{1,5}',
                  r'(?<=leu)[\s|:]{1,4}\d{1,5}',
                  r'(?<=leuco)s?[\s|:]{1,4}\d{1,5}'
                 ],
        
        gr_lcr = [r'\b\d{1,5}\s?(?=hemati)',
                  r'(?<=hematie)[\s|:]{1,4}\d{1,5}'
                 ],
        
        direct_lcr = [r'\bgermes?\W+\w*\W+direct',
                      r'\bbact[ée]ries?\W*?\w*\W*?(visibles?|direct)',
                      r'\b[cC]ultures?',
                      r'\bexamens?\W+directs?'
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
                       r'\b\w*?(?<=[gG]lycor)\w*?\W*\w*?\W*\d+[\.|\,]\d+',]
        
        pnn_sg = [],
    
