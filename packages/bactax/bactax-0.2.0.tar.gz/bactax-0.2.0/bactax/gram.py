from typing import Optional, overload, Literal
from enum import Enum

from . import tax


_GRAM_POSITIVE_PHYLA = [
    "Actinobacteria",
    "Chloroflexi",
    "Firmicutes",
    "Tenericutes",
    "Actinomycetota",
    "Chloroflexota",
    "Bacillota",
    "Mycoplasmatota",
]

_GRAM_NEGATIVE_CLASS_EXCEPTIONS = ["Negativicutes"]


class Gram(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"


@overload
def gram_stain(
    *,
    name: Optional[str] = None,
    ncbi_id: Optional[int] = None,
    species: Optional[str] = None,
    genus: Optional[str] = None,
    family: Optional[str] = None,
    order: Optional[str] = None,
    class_: Optional[str] = None,
    phylum: Optional[str] = None,
    kingdom: Optional[str] = None
) -> Optional[Literal[Gram.NEGATIVE, Gram.POSITIVE]]:
    """
    Determine whether a bacteria is gram negative or positive.

    Gets taxonomic information from the input information using
    `bactax.get_taxonomy` and then determines the gram stain
    based on the assigned phylum/class. The method was taken
    from the [AMR R package](https://msberends.github.io/AMR/)
    where any bacteria in one of the following phyla are
    considered gram positive:

    - Actinomycetota (previously called Actinobacteria)
    - Chloroflexota (previously called Chloroflexi)
    - Bacillota (previously called Firmicutes) ... except the Negativicutes class!
    - Mycoplasmatota (previously called Tenericutes)

    Since the gram stain is based on phylum/class information,
    at least class (or more granular) must be provided as input to
    avoid `None` being returned.

    Returns
    -------
    Gram.NEGATIVE | Gram.POSITIVE | None
        Returns either `Gram.NEGATIVE` or `Gram.POSITIVE` if the
        phylum/class can be determined. If the phylum/class are not
        found, then it returns `None` (because the gram stain cannot
        be determined).
    """


def gram_stain(**kwargs) -> Optional[Literal[Gram.NEGATIVE, Gram.POSITIVE]]:
    taxonomy = tax.get_taxonomy(**kwargs)

    if taxonomy.phylum is None or (
        taxonomy.phylum == "Bacillota" and taxonomy.class_ is None
    ):
        return None

    is_gram_positive = (
        taxonomy.phylum in _GRAM_POSITIVE_PHYLA
        and taxonomy.class_ not in _GRAM_NEGATIVE_CLASS_EXCEPTIONS
    )
    return Gram.POSITIVE if is_gram_positive else Gram.NEGATIVE


@overload
def is_gram_positive(
    *,
    name: Optional[str] = None,
    ncbi_id: Optional[int] = None,
    species: Optional[str] = None,
    genus: Optional[str] = None,
    family: Optional[str] = None,
    order: Optional[str] = None,
    class_: Optional[str] = None,
    phylum: Optional[str] = None,
    kingdom: Optional[str] = None
) -> bool:
    """
    Determine if a bacteria is gram positive.

    Uses `bactax.gram_stain` to determine the gram stain based
    on the input information.

    Returns
    -------
    bool
        `True` if the bacteria is gram positive and `False`
        otherwise. Note that if the gram stain is `None` (because
        not enough information was given to accurately determine
        the gram stain) then `False` is returned.
    """


def is_gram_positive(**kwargs) -> bool:
    return gram_stain(**kwargs) == Gram.POSITIVE


@overload
def is_gram_negative(
    *,
    name: Optional[str] = None,
    ncbi_id: Optional[int] = None,
    species: Optional[str] = None,
    genus: Optional[str] = None,
    family: Optional[str] = None,
    order: Optional[str] = None,
    class_: Optional[str] = None,
    phylum: Optional[str] = None,
    kingdom: Optional[str] = None
) -> bool:
    """
    Determine if a bacteria is gram negative.

    Uses `bactax.gram_stain` to determine the gram stain based
    on the input information.

    Returns
    -------
    bool
        `True` if the bacteria is gram negative and `False`
        otherwise. Note that if the gram stain is `None` (because
        not enough information was given to accurately determine
        the gram stain) then `False` is returned.
    """


def is_gram_negative(**kwargs) -> bool:
    return gram_stain(**kwargs) == Gram.NEGATIVE
