from cp_request.design.block_definition import BlockDefinition
from transform import RequestTransformer
from typing import List


class SumBlock(BlockDefinition):
    """
    Represents a design block definition that is the sum of a sequence of
    blocks.
    """

    def __init__(self, *, block_list: List[BlockDefinition]):
        self.__block_list = block_list

    def __repr__(self):
        return "SumBlock(block_list={})".format(repr(self.__block_list))

    # TODO: defined str method
    def __str__(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, SumBlock):
            return False
        return self.__block_list == other.__block_list

    def apply(self, visitor):
        visitor.visit_sum_block(self)

    def transform(self, transformer: RequestTransformer):
        return transformer.transform_sum_block(self)

    @property
    def block_list(self):
        return self.__block_list
