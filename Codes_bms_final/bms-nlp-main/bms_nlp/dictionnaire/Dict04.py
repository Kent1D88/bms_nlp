# -*- coding: utf-8 -*-
        date_entree = [r'[Ee]ntr[ée]\(e\)\s?le:\s?([\d\/]{8,10})', 
                       r"[dD]ate\s?d\Wentr[ée]e\s?au\s?SAU:\s([\d\/]{8,10})",
                       r'[dD]ate\s?:\s([\d\/]{8,10})'],

        date_naissance = [r'[nN][ée][\(e\)]{0,3}\s?le\s?:\s?[\d\/]{8,10}',
                          r'Date\s?de\s?naissance\s?:\s?([\d\/]{8,10})',
                          r'[Nn]aiss\s?\W\s?[\d\/]{8,10}'],

        sex = [r'[Ss]exe\s?\W?\s?([F|M])'],

        glasgow = [r'[gG]lasgow\s?\W?\s?(\d{1,2})'],

        temp = [r'\b[tT]emp\W{0,3}(\d{2}.?\d?)\W*?[cC]',
                r'\b[tT]emp\W*[\w|\s]*\W*(\d+\.?\d)'],

        PA = [r'\b[P][A]\s?\w*\W+?\w*?\W+(\d{2,3})\W?\/\W?(\d{2,3})',
              r'\b[tT]a[g|d]\W?\w*\W*\w*\s?\w*\W*(\d+)'],

        pouls = [r'\b[F][C]\W+?(\d{2,3})',
                 r'\b[F][C]\W*[\w|\s]*?\W*(\d+)'],

        freq_resp = [r'\b[F][R]\W+?(\d{2,3})',
                     r'\b[F][R]\W*[\w|\s]*\W*(\d+\.?\d?)'],

        sao2_sat = [r'[Ss][a|p][oO]2\W+?(\d{2,3})\s*?%',
                    r'\b[sS][aA][oO]2\W*(\d+\.?\d?)'],

        sao2_debit = [r'[F][C]\W+?(\d{2,3})'],

        dextro = [r'\b\w*\s?:\s?(\d+.?\d?)\W*?mmol\W[Ll]',
                  r'\b\w*\s?\(mmol par [Ll]\)\s?:\s?(\d+.?\d?)'],

        PL =[r'\b[pP][lL][\s|:|\n]', 
             r'\b[pP][Ll][\s|\W]', 
             r'\bponct\w*\W+lomb\w*',
             r'[lL][cC][rR]'],

        raid_nuque = [r'\brai?de\w*\W*?(de)?\W*?nuq\w*',
                      r'\brai?de\w*', 
                      r'\b[Bb]rudz?\w+', 
                      r'\b[kK]er\w+'],
        
        cervicalgie = [r'\b[cC]\w*alg\w*'],

        cephalee =[r'\b[cC][eéè]p\w*[éeè]\w*', 
                   r'\b[cC][eéè]phal\w*'] ,

        purpura = [r'\b[pP]urp\w*'],

        convulsion = [r'\b[cC]onvu\w*', 
                      r'\b[eéEÉ]pilep\w*', 
                      r'\b[cC]ri\w*\s?ton\w*\W?clon\w*', 
                      r'\b[pP]ost\W?[cC]ri\w*',
                      r'\b[cC]ri\w*\s?[cC]omi\w*'] ,

        fievre = [r'\b[fF]i[eéè]v\w*', 
                  r'\b\w*therm\w*', 
                  r'\b[fF]riss\w*',
                  r'\b[fF][eé]b\w*'],
    
        sdmeninge = [r'\bm[éeè]ning[éèes]+', 
                     r'\b[sS]\w*?[dD]\w*?\s?m[éeè]\w*[n|g|n]{2,}\w*[éèes]+'],

        meningite = [r'\b[mM]\w*git\w*',r'[mM]eningo.?enceph\w*'],
    
        #LCR_match = [r'\b[pP][lL][\w|\s|\.|,|é|è|\/|:|%]+(^\v*)',
        #             r'\b[lL][cC][rR][\w|\s|\.|,|é|è|\/|:|%]+(^\v*)',
        #             r'\b[lL][cC][rR](.*\n)*',
        #             r'\b[pP][lL](.*\n)*'],
        
        GB_LCR = [r'\b\d*?\W?(?= [eEéÉ]l[ée]ments?)',
                  r'(?<=[eEéÉ]l[ée]ment)s?\W*\d+',
                  r'(?<=[lL]eucocyte)s?\W*\d+',
                  r'(?<=[lL]eu)\w*\W*\d+'],
        
        GR_LCR = [r'\b\d+?\W?(?=[hH][eé]mati)',
                  r'(?<=[hH][ée]matie)s?\W*\d+'],
        
        Direct_LCR = [r'\bgermes?\W+\w*\W+direct',
                      r'\bbact[ée]ries?\W*?\w*?\W*?(visibles?|direct)'],
        
        Prot_LCR = [r'(?<=[pP]rot)\w*?\W*\d+[\.|\,]\d+',
                    r'\b[pP]rot\w*rachi[s|e]?\W*?[nN]\w*',
                    r'\b\w*[pP]rot\w*rachi[s|e]?'],
        
        Gly_LCR = [r'(?<=[gG]luc)\w*?\W*\d+[\.|\,]\d+',
                   r'(?<=[gG]lycorachie)\w*?\W*\d+[\.|\,]\d+',
                   r'\b[gG]ly\w*rachi[s|e]?\W*?[nN]\w*',
                   r'\b\w*[gG]l\w*rachi[s|e]?'],
        
        PNN_SG = [],
    
