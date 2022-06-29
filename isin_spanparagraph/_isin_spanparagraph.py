from typing import List, Optional, Any, Dict

from spacy.tokens import Doc, Span, Token
from spacy.language import Language

from edsnlp.pipelines.core.matcher import GenericMatcher
from edsnlp.utils.filter import get_spans

from . import patterns

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

        

        super().__init__(
            nlp=nlp,
            attr=attr,
            regex=regex,
            terms=None,
            ignore_excluded=ignore_excluded,
        )

        self.list_labels = list_labels
        self.set_extensions()

    def set_extensions(self, self.list_labels) -> None:
        if not Token.has_extension("end_paragraph"):
            Token.set_extension("end_paragraph", default=None)

        if not Span.has_extension("end_paragraph"):
            Span.set_extension("end_paragraph", default=None)

        if not Doc.has_extension("list_labeltoparagraph"):
            Doc.set_extension("list_labeltoparagraph", default=[])

        if not Span.has_extension("in_spanparagraph_of"):
            Span.set_extension("in_spanparagraph_of", default=[])

        for label in self.list_labels:
            if not Span.has_extension(f"{label}_endparagraph"):
                Span.set_extension(f"{label}_endparagraph", default=None)

            if not Span.has_extension(f"entsin_{label}_paragraph"):
                Span.set_extension(f"entsin_{label}_paragraph", default=[])

            if not Span.has_extension(f"isin_{label}_paragraph"):
                Span.set_extension(f"isin_{label}_paragraph", default=False)

    def spanparagrapher(self, ent: Span, list_end_paragrapher: List[Span],) -> None:
        """
        Annotate entities using end_paragraph matches to create span_paragraphs

        Parameters
        ----------
        ent : Span
            Entity to annotate
        list_end_paragraph : List[Span]
            List of end_paragraph cues
        """

        cues = [m.start for m in list_end_paragrapher if m.start >= ent.start]

        if cues != []:
            ent._.set(f"{ent.label_}_endparagraph", min(cues))
        else:
            ent._.set(f"{ent.label_}_endparagraph", ent.end)

    def ent_isin_spanparagraph(
        self, ent_totest: Span, list_ent_ref: List[Span],
    ) -> None:
        """
        Annotate entities using span_paragraphs to know if is in span_paragraph or not.
        
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
                & (ent_totest.end <= m._.get(f"{m.label_}_endparagraph"))
            )
        ]
        label = list_ent[0].label_
        isin_paragraph = ent_totest._.get(f"isin_{label}_paragraph") or bool(list_ent)

        ent_totest._.set(f"isin_{label}_paragraph", isin_paragraph)

        ent_totest._.in_spanparagraph_of.append(list_ent)

    def ents_inspanparagraph(self, span: Span, doc: Doc) -> None:
        """
        Stock the information of which ent is in span_paragraph.

        Parameters
        ----------
        span: Span
            Entitie to start spanparagraph
        doc: Doc
            To enumerate all the entities in each spanparagraph

        """
        list_temp = []
        for key, list_ents in doc.spans.items():
            if key != span.label_:
                list_temp.append(
                    [
                        ent
                        for ent in list_ents
                        if (
                            (ent.start > span.start)
                            & (ent.end <= span._.get(f"{span.label_}_endparagraph"))
                        )
                    ]
                )
        span._.set(f"entsin_{span.label_}_paragraph", list_temp)

    def __call__(self, doc: Doc) -> Doc:
        matches = self.process(doc)

        list_end_paragrapher = get_spans(matches, "end_paragrapher")

        doc.spans["list_end_paragrapher"] = list_end_paragrapher

        if set(self.list_labels) & set(doc.spans):
            doc._.list_labeltoparagraph = self.list_labels
            list_span_labels = []
            for key, list_spans in doc.spans.items():
                if key in self.list_labels:
                    for span in list_spans:
                        list_span_labels.append(list_spans)
                        self.spanparagrapher(span, list_end_paragrapher)
                        self.ents_inspanparagraph(span, doc)

                elif key != "list_end_paragrapher":
                    for span in list_spans:
                        self.ent_isin_spanparagraph(
                            ent_totest=span, list_ent_ref=list_span_labels
                        )

        return doc

