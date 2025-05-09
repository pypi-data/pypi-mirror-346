from abc import ABCMeta, abstractmethod
from typing import Generic, Generator, Iterable

from matchescu.typing._data import TRecord, DataSource, RecordSampler
from matchescu.typing._references import EntityReference, EntityReferenceIdFactory
from matchescu.references._record import EntityReference as RefImpl


class EntityReferenceExtraction(Generic[TRecord], metaclass=ABCMeta):
    def __init__(
        self,
        ds: DataSource[TRecord],
        id_factory: EntityReferenceIdFactory,
        record_sampler: RecordSampler,
    ):
        self.__ds = ds
        self.__id_factory = id_factory
        self.__record_sampler = record_sampler

    @abstractmethod
    def _merge_records(self, records: Iterable[TRecord]) -> TRecord:
        pass

    def __process_traits(
        self, input_records: Iterable[TRecord]
    ) -> Generator[TRecord, None, None]:
        for trait in self.__ds.traits:
            result = trait(input_records)
            result.source = self.source_name
            yield result

    def __extract_entity_reference(
        self, input_records: Iterable[TRecord]
    ) -> EntityReference:
        identifier = self.__id_factory(input_records)
        trait_records = self.__process_traits(input_records)
        merged_record = self._merge_records(trait_records)
        return RefImpl(identifier, merged_record)

    @property
    def source_name(self):
        return self.__ds.name

    def __call__(self) -> Iterable[EntityReference]:
        return map(self.__extract_entity_reference, self.__record_sampler(self.__ds))
