from typing import Any, Iterable, Self

from banal import ensure_list
from followthemoney.types import registry
from followthemoney.util import join_text
from ftmq import Query
from ftmq.model import Entity
from ftmq.types import CE, SE
from pydantic import BaseModel, ConfigDict, Field

from ftmq_search.exceptions import IntegrityError
from ftmq_search.settings import Settings

settings = Settings()

ALLTHETHINGS = Query().where(schema="Thing", schema_include_descendants=True)


class EntityDocument(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., examples=["NK-A7z...."])
    caption: str = Field(..., examples=["Jane Doe"])
    schema_: str = Field(..., examples=["LegalEntity"], alias="schema")
    datasets: list[str] = Field([], examples=[["us_ofac_sdn"]])
    countries: list[str] = Field([], examples=[["de"]])
    names: list[str]
    text: str = ""

    @classmethod
    def from_proxy(cls, proxy: CE | SE) -> Self:
        if proxy.id is None:
            raise IntegrityError("Entity has no ID!")
        names = proxy.get_type_values(registry.name)
        text = join_text(*[v for values in proxy.properties.values() for v in values])
        text = text or ""

        return cls(
            id=proxy.id,
            datasets=list(proxy.datasets),
            schema=proxy.schema.name,
            countries=proxy.countries,
            caption=proxy.caption,
            names=names,
            text=text,
        )


class EntitySearchResult(BaseModel):
    id: str = Field(..., examples=["NK-A7z...."])
    entity: Entity
    score: float = 1

    def __init__(self, /, **data: Any) -> None:
        if "entity" not in data:
            data["entity"] = self.make_entity(**data)
        super().__init__(**data)

    def to_proxy(self) -> CE:
        return self.entity.to_proxy()

    @staticmethod
    def make_entity(
        id: str,
        schema: str,
        datasets: Iterable[str],
        caption: str,
        names: Iterable[str],
        countries: Iterable[str] | None = None,
        **kwargs: Any,
    ) -> Entity:
        return Entity(
            id=id,
            schema=schema,
            datasets=list(datasets),
            caption=caption,
            properties={"name": list(names), "country": ensure_list(countries)},
            referents=[],
        )


class AutocompleteResult(BaseModel):
    id: str
    name: str
