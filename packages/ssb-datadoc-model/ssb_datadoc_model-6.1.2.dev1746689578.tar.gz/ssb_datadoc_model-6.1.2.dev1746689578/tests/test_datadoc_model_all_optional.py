import pytest
from datadoc_model.model import (
    DatadocMetadata,
    MetadataContainer,
    PseudonymizationMetadata,
)
from pydantic import ValidationError


def test_instantiate_no_values_container():
    container = MetadataContainer()
    assert isinstance(container, MetadataContainer)


def test_instantiate_no_values_datadoc():
    datadoc = DatadocMetadata()
    assert isinstance(datadoc, DatadocMetadata)


def test_instantiate_no_values_pseudo():
    pseudo = PseudonymizationMetadata()
    assert isinstance(pseudo, PseudonymizationMetadata)


def test_unknown_field():
    with pytest.raises(ValidationError):
        DatadocMetadata(unknown_field="random_value")
