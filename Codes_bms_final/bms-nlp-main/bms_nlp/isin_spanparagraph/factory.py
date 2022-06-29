from typing import Dict, List, Optional, Union
from spacy.language import Language
from bms_nlp.isin_spanparagraph import Isin_spanparagraph
from bms_nlp.isin_spanparagraph import patterns

DEFAULT_CONFIG = dict(
    list_labels=None,
    regex=patterns.regex,
    attr="NORM",
    ignore_excluded=False,
)

@Language.factory("eds.isin_spanparagraph", default_config=DEFAULT_CONFIG)
def create_component(
    nlp: Language,
    name: str,
    attr: str,
    regex: Optional[Dict[str, Union[str, List[str]]]],
    list_labels: Optional[List[str]],
    ignore_excluded: bool,
):
    
    if regex is None:
        regex = dict()

    return Isin_spanparagraph(
        nlp = nlp,
        attr = attr,
        list_labels = list_labels,
        ignore_excluded = ignore_excluded,
        regex = regex,
    )
