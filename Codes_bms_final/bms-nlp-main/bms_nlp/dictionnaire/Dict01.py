date_entree = [r'[Ee]ntr[ée]\(e\)\s?le:\s?([\d\/]{8,10})', 
               r"[dD]ate\s?d\Wentr[ée]e\s?au\s?SAU:\s([\d\/]{8,10})",
               r'[dD]ate\s?:\s([\d\/]{8,10})']

date_naissance = [r'[nN][ée][\(e\)]\s?le\s?:\s?[\d\/]{8,10}',
                  r'Date\s?de\s?naissance\s?:\s?([\d\/]{8,10})',
                  r'[Nn]aiss\s?\W\s?[\d\/]{8,10}']

sex = [r'[Ss]exe\s?\W?\s?([F|M])']

PL =[r'[pP][lL][\s|:|\n]', r'\s[pP][Ll][\s|\W]', r'ponction\w?',
     r'lomb\w*',r'ponctions? lombaires?']

raid_nuque = [r'ra.?d\w*', r'brud\w+', r'ker\w+',r'nuq\w*']

cephalee =[r'c[eéè]]p\w*[éeè]\w*', ] 

purpura = [r'purp\w*']

convulsion = [r'conv\w*', 
              r'[eéEÉ]pilep\w*', 
              r'cri\w*\s?ton\w*\W?clon\w*', 
              r'post\W?cri\w*'] 

fievre = [r'^fi[eéè]\w*v\w*', 
          r'\w*th?erm\w*', 
          r'^[fF]riss\w*']

meningite = [r'm.*git\w*']

glasgow = [r'[gG]lasgow\s?\W?\s?(\d{1,2})']

temp = [r'[tT]emp\W{0,3}(\d{2}.\d)\W{2}[cC]']

PA = [r'[Pp][aA]\s?\w*\W+?\w?\W+(\d{2,3})\/(\d{2,3})']

pouls = [r'[fF][cC]\W+?(\d{2,3})']

freq_resp = [r'[fF][rR]\W+?(\d{2,3})']

sao2_sat = [r'[Ss][a|p][oO]2\W+?(\d{2,3})\s?%']

sao2_debit = [r'[fF][cC]\W+?(\d{2,3})']

dextro = [r'\w*\s?:\s?(\d+.\d)?\W?mmol\W[Ll]']

LCR_match = [r'\w*\W?[LlCcRr]{3}\s?[a-z]*?(\d*\W\d*)',
             r'\b[pP][lL][\w|\s|\.|,|é|è|\/|:|%]+(^\h\v)',
             r'\b[lL][cC][rR][\w|\s|\.|,|é|è|\/|:|%]+(^\h\v)']