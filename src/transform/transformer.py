from __future__ import annotations
import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cp_request.attribute import Attribute
    from cp_request.measurement import Control, Measurement, Sample
    from cp_request.named_entity import NamedEntity
    from cp_request.treatment import Treatment
    from cp_request.unit import Unit
    from cp_request.value import Value
    from cp_request.version import Version
    from cp_request.experimental_request import ExperimentalRequest

    from cp_request.design.design_block import DesignBlock
    from cp_request.design.block_reference import BlockReference
    from cp_request.design.generate_block import GenerateBlock
    from cp_request.design.product_block import ProductBlock
    from cp_request.design.replicate_block import ReplicateBlock
    from cp_request.design.sum_block import SumBlock
    from cp_request.design.subject_reference import SubjectReference
    from cp_request.design.treatment_reference import (
        TreatmentReference,
        TreatmentValueReference
    )


class RequestTransformer(abc.ABC):
    """
    Abstract transformer for structured request classes.
    Includes stubbed methods for each class, with each returning a deep copy.

    To create a transformer, inherit from this class, define an initializer, and
    each appropriate visit method.
    """

    @abc.abstractmethod
    def __init__(self, symbol_table):
        self.__symbol_table = symbol_table

    def transform_design_block(self, block: DesignBlock):
        return DesignBlock(
            label=block.label,
            definition=block.transform(self)
        )

    def transform_product_block(self, block: ProductBlock):
        block_list = list()
        for block in block.block_list:
            block_list.append(block.transform(self))
        return ProductBlock(block_list=block_list)

    def transform_block_reference(self, reference: BlockReference):
        if reference.block_label in self.__symbol_table:
            block = self.__symbol_table[reference.block_label]
            # TODO: check type of object?
        else:
            block = reference.block.transform(self)
            self.__symbol_table[reference.block_label] = block
        return BlockReference(block=block)

    def transform_sum_block(self, block: SumBlock):
        block_list = list()
        for block in block.block_list:
            block_list.append(block.transform(self))
        return SumBlock(block_list=block_list)

    def transform_subject_reference(self, reference: SubjectReference):
        if reference.entity.name in self.__symbol_table:
            entity = self.__symbol_table[reference.entity.name]
            # TODO: check type of object?
        else:
            entity = reference.entity.transform(self)
            self.__symbol_table[reference.entity.name] = entity
        return SubjectReference(entity=entity)

    def transform_treatment_reference(self, reference: TreatmentReference):
        if reference.treatment_name in self.__symbol_table:
            treatment = self.__symbol_table[reference.treatment_name]
            # TODO: check type of object?
        else:
            treatment = reference.treatment.transform(self)
            self.__symbol_table[reference.treatment_name] = treatment
        return TreatmentReference(treatment=treatment)

    def transform_treatment_value_reference(
            self,
            reference: TreatmentValueReference):
        if reference.treatment_name in self.__symbol_table:
            treatment = self.__symbol_table[reference.treatment_name]
            # TODO: check type of object?
        else:
            treatment = reference.treatment.transform(self)
            self.__symbol_table[reference.treatment_name] = treatment
        return TreatmentValueReference(
            treatment=treatment,
            value=reference.value
        )

    def transform_replicate_block(self, block: ReplicateBlock):
        return ReplicateBlock(
            count=block.count,
            block=block.block.transform(self)
        )

    def transform_generate_block(self, block: GenerateBlock):
        value_list = list()
        for value in block.values:
            value_list.append(value.transform(self))

        return GenerateBlock(
            treatment=block.treatment.transform(self),
            attribute_name=block.attribute_name,
            values=value_list
        )

    def transform_attribute(self, attribute: Attribute):
        return

    def transform_version(self, version: Version):
        return

    def transform_treatment(self, treatment: Treatment):
        return

    def transform_sample(self, sample: Sample):
        return

    def transform_control(self, control: Control):
        return

    def transform_measurement(self, measurement: Measurement):
        return

    def transform_unit(self, unit: Unit):
        return

    def transform_value(self, value: Value):
        return

    def transform_named_entity(self, entity: NamedEntity):
        return

    def transform_experiment(self, experiment: ExperimentalRequest):
        return
