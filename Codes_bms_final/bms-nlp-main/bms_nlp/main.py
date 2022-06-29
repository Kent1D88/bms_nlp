import sys
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path

import os
from os import path
import pandas as pd
import numpy as np
import spacy
from spacy.language import Language
from spacy.tokens import Doc, Span
import edsnlp
from edsnlp import components
import typing
from typing import Any, Dict, List
import pickle
import math

import re
from .dictionnaire.dicts_tabs import *
from .dictionnaire.Dict14 import *