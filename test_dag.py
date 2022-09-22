import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to
from src.dag import CustomFn

class TestSimple():

    def test_should_transform_data(self):
        with TestPipeline() as p:
            input = p | beam.Create([b'{ "name": "seila1", "value": "seila2" }'])

            output = input | beam.ParDo(CustomFn())

            assert_that(output, equal_to([{ "name": "seila1", "value": "seila2", "changed": True }]))

    def test_should_simple(self):
        assert 1 == 1
        
        