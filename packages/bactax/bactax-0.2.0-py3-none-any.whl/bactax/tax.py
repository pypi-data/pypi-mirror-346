from typing import Optional, overload
import gzip
import warnings

import polars as pl

from . import utils, errors


_TAXONOMY_ORDER = [
    "domain",
    "kingdom",
    "phylum",
    "class",
    "order",
    "family",
    "genus",
    "species",
    "tax_name",
    "tax_id",
]


class Taxonomy:
    """
    Represents a taxonomic classification from the NCBI
    taxonomy database.

    Attributes
    ----------
    name : str, optional
        The taxonomy name.
    ncbi_id : int, optional
        The NCBI ID of the taxonomy.
    species : str, optional
        The species of the taxonomy.
    genus : str, optional
        The genus of the taxonomy.
    family : str, optional
        The family of the taxonomy.
    order : str, optional
        The order of the taxonomy.
    class_ : str, optional
        The class of the taxonomy.
    phylum : str, optional
        The phylum of the taxonomy.
    kingdom : str, optional
        The kingdom of the taxonomy.
    domain : str, optional
        The domain of the taxonomy.
    """

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        ncbi_id: Optional[int] = None,
        species: Optional[str] = None,
        genus: Optional[str] = None,
        family: Optional[str] = None,
        order: Optional[str] = None,
        class_: Optional[str] = None,
        phylum: Optional[str] = None,
        kingdom: Optional[str] = None,
        domain: Optional[str] = None,
    ):
        self._name: Optional[str] = name
        self.ncbi_id: Optional[int] = ncbi_id
        self.species: Optional[str] = species
        self.genus: Optional[str] = genus
        self.family: Optional[str] = family
        self.order: Optional[str] = order
        self.class_: Optional[str] = class_
        self.phylum: Optional[str] = phylum
        self.kingdom: Optional[str] = kingdom
        self.domain: Optional[str] = domain

    def __repr__(self):
        args = {k: v for k, v in vars(self).items() if v is not None}
        name = args.pop("_name", None)

        kwargs = ", ".join([f"{k}={repr(v)}" for k, v in args.items()])

        return (
            f"Taxonomy({name}, {kwargs})" if name is not None else f"Taxonomy({kwargs})"
        )

    @property
    def name(self):
        """
        The name for the taxonomic classification if provided,
        otherwise the species name.
        """
        return self._name if self._name is not None else self.species_name

    @property
    def species_name(self):
        """
        The species for the taxonomic classification if provided,
        otherwise the genus + 'sp.'.
        """
        if self.species is not None:
            return self.species
        genus = self.genus if self.genus is not None else "[Unknown genus]"
        return f"{genus} sp."


@overload
def get_taxonomy(
    *,
    name: Optional[str] = None,
    ncbi_id: Optional[int] = None,
    species: Optional[str] = None,
    genus: Optional[str] = None,
    family: Optional[str] = None,
    order: Optional[str] = None,
    class_: Optional[str] = None,
    phylum: Optional[str] = None,
    kingdom: Optional[str] = None,
) -> Taxonomy:
    """
    Retrieve bacterial taxonomic information from the NCBI taxonomy
    database based on the provided input parameters.

    Only one of the potential input parameters needs to be provided
    (i.e., you don't need to specify both a species and a class).

    Parameters
    ----------
    name : str, optional
        The name of the organism.
    ncbi_id : int, optional
        The NCBI ID of the taxonomy.
    species : str, optional
        The species of the organism.
    genus : str, optional
        The genus of the organism.
    family : str, optional
        The family of the organism.
    order : str, optional
        The order of the organism.
    class_ : str, optional
        The class of the organism.
    phylum : str, optional
        The phylum of the organism.
    kingdom : str, optional
        The kingdom of the organism.

    Returns
    -------
    Taxonomy
        An instance of the Taxonomy class filled in with taxonomic
        information pulled from the NCBI taxonomy database.

    Raises
    ------
    NoTaxonomyDataError
        If no taxonomy data matches the provided input parameters.
    """


def get_taxonomy(**kwargs) -> Taxonomy:
    # Change names to what's in the NCBI data
    kwargs["class"] = kwargs.pop("class_", None)
    kwargs["tax_id"] = kwargs.pop("ncbi_id", None)
    kwargs["tax_name"] = kwargs.pop("name", None)

    # Load and filter the taxonomy data based on the input constraints
    filter_dict = {k: v for k, v in kwargs.items() if v is not None}
    predicates = [
        pl.col(k).str.to_lowercase() == str(v).lower() for k, v in filter_dict.items()
    ]
    data = _load_tax_data().filter(*predicates)

    if data.is_empty():
        raise errors.NoTaxonomyDataError(**filter_dict)

    # Figure out values for each of the taxonomy levels
    include = False
    taxonomy = {}
    for tax_level in reversed(_TAXONOMY_ORDER):
        if tax_level in filter_dict:
            include = True

        if include:
            all_values = (
                data.filter(pl.col(tax_level).is_not_null(), pl.col(tax_level) != "")
                .get_column(tax_level)
                .unique()
            )
            if len(all_values) > 1:
                warnings.warn(
                    f"More than one possible value found for '{tax_level}'. Using first value"
                )
                print(all_values)
            taxonomy[tax_level] = all_values.first()

    # Change names back to what the Taxonomy object expects
    taxonomy["name"] = taxonomy.pop("tax_name", None)
    taxonomy["ncbi_id"] = taxonomy.pop("tax_id", None)
    taxonomy["class_"] = taxonomy.pop("class", None)

    return Taxonomy(**taxonomy)


def _load_tax_data():
    """
    Loads the taxonomy data and returns it in a polars DataFrame.

    Raises
    ------
    TaxonomyFileNotFoundError
        If a downloaded NCBI taxonomy file is not found in the
        bactax package. A new file can be downloaded with
        the function `bactax.ncbi.update_tax_data()`.
    """
    tax_file = utils.get_taxonomy_data_filepath()

    if tax_file is None:
        raise errors.TaxonomyFileNotFoundError()

    with gzip.open(tax_file, "rb") as f:
        return pl.read_csv(f)
