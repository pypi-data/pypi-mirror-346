#The Encoded By Sajad


""" Nodes that represent tensorflow functions

"""

from SajodeSx.HardImportRegistry import addModuleDynamicHard

from .HardImportNodesGenerated import ExpressionTensorflowFunctionCallBase

addModuleDynamicHard(module_name="tensorflow")


class ExpressionTensorflowFunctionCall(ExpressionTensorflowFunctionCallBase):
    kind = "EXPRESSION_TENSORFLOW_FUNCTION_CALL"

    def replaceWithCompileTimeValue(self, trace_collection):
        # TODO: The node generation should allow for this to not be necessary
        trace_collection.onExceptionRaiseExit(BaseException)

        return self, None, None



