from typing import List, Optional, Any, Dict

from spacy.tokens import Doc, Span, Token
from spacy.language import Language

from edsnlp.pipelines.core.matcher import GenericMatcher
from edsnlp.utils.filter import get_spans

from .patterns import regex


class Isin_spanparagraph(GenericMatcher):
    
    """isin_spanparagraph est une fonction acceptant en entrée 
    un fichier Spacy Doc et une liste de nom de label. 
    
    La fonction a attribuer de nouveaux attributs au différent matchs:
    Pour les matchs de list_labels:
    - l'attribut self_paragraph contiendra les coordonnées d'un span 
            commencant par l'ent du label et finissant par une succession 
            de 2 changements de lignes
    - l'attribut ents_paragraph contenant la liste des matches contenu dans le paragraphe
    Pour l'ensemble des ent:
    - l'attribut isin_paragraph, 
    """

    def __init__(
        self,
        nlp: Language,
        attr: str,
        regex: Dict[str, List[Any]],
        list_labels: Optional[List[str]],
        ignore_excluded: bool,
    ):

        self.list_labels = list_labels

        super().__init__(
            nlp = nlp,
            attr = attr,
            regex = regex,
            terms = None,
            ignore_excluded = ignore_excluded,
        )
        
        self.set_extensions()

    @staticmethod
    def set_extensions() -> None:
        
        if not Token.has_extension("end_paragraph"):
            Token.set_extension("end_paragraph", default=None)

        if not Span.has_extension("end_paragraph"):
            Span.set_extension("end_paragraph", default=None)
        
        if not Span.has_extension('self_endparagraph'):
            Span.set_extension('self_endparagraph',default=None)

        if not Span.has_extension('ents_inspanparagraph'):
            Span.set_extension('ents_inspanparagraph',default=[])
            
        if not Span.has_extension('isin_spanparagraph_'):
            Span.set_extension('isin_spanparagraph_',
                              getter= lambda span:'NEG' if span._.negation else "AFF")
        
        if not Span.has_extension('isin_spanparagraph'):
            Span.set_extension('isin_spanparagraph',default=False)
            
        if not Span.has_extension('in_spanparagraph_of'):
            Span.set_extension('in_spanparagraph_of',default=[])


    def spanparagrapher(
        self,
        ent: Span,
        list_end_paragrapher: List[Span],
    ) -> None :
        """
        Annotate entities using end_paragraph matches

        Parameters
        ----------
        ent : Span
            Entity to annotate
        list_end_paragraph : List[Span]
            List of end_paragraph cues
        """
        
        cues = [m.start for m in list_end_paragrapher if m.start >= ent.start]
        
        if cues != []:
            ent._.self_endparagraph = min(cues)
        else: ent._.self_endparagraph = ent.end
        
        
    def ent_isin_spanparagraph(
        self,
        ent_totest: Span,
        list_ent_ref: List[Span],
    ) -> None :
        """
        Annotate entities using span_paragraph
        
        Parameters
        ----------
        ent: Span
            Entity to annotate
        list_ent_ref : List[Span]
            List of span with paragraph to test if ent is in.
        """
        list_ent = [
            m
            for m in list_ent_ref
            if (
                (ent_totest.start > m.start)
                & (ent_totest.end <= m._.self_endparagraph)
            )
        ]
        
        isin_paragraph = ent_totest._.isin_spanparagraph or bool(list_ent)
        
        ent_totest._.isin_spanparagraph = isin_paragraph
        
        ent_totest._.in_spanparagraph_of = list_ent
        
    def ents_inspanparagraph(
        self,
        span: Span,
        doc: Doc) -> None :
        
        for key, list_ents in doc.spans.items():
            if key != span.label_:
                span._.ents_inspanparagraph += [ent for ent in list_ents if (
                    (ent.start > span.start) & 
                    (ent.end <= span._.self_endparagraph))]

    def __call__(self, doc : Doc)-> Doc:
        matches = self.process(doc)

        list_end_paragrapher = get_spans(matches, "end_paragrapher")

        doc.spans['list_end_paragrapher'] = list_end_paragrapher
        
        if (set(self.list_labels) & set(doc.spans)):
            list_span_labels = []
            for label in self.list_labels:
                for span_toparagraph in doc.spans[label]:
                    self.spanparagrapher(
                        ent=span_toparagraph,
                        list_end_paragrapher=list_end_paragrapher)
                    list_span_labels.append(span_toparagraph)

            doc.spans['list_span_selfparagraph'] = list_span_labels

            for label, list_spans in doc.spans.items():
                if label in self.list_labels:
                    for span in list_spans:
                        self.ents_inspanparagraph(span, doc)
                
                elif ((label != 'list_end_paragrapher') or (
                    label != 'list_span_selfparagraph')
                     ):
                    for span in list_spans:
                        self.ent_isin_spanparagraph(
                            ent_totest = span,
                            list_ent_ref = list_span_labels
                        )
                        
                
        return doc
            