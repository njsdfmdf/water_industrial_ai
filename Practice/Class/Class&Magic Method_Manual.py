from typing import Any


class AIModelWrapper:
    def __init__(self, model_name, version = "v1.0"):
        self.name = model_name
        self.version = version
        self.model_load = True

    def __call__(self, input_data):
        print([x for x in input_data])

object_1 = AIModelWrapper("WaterQualityPredictor")
object_1([1, 2, 3])