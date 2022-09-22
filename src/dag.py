import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import logging
import json

class MyOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls,parser):
        parser.add_value_provider_argument('--subscription_name', type=str, default='')
        parser.add_value_provider_argument('--table_spec', type=str, default='')

class CustomFn(beam.DoFn):

  def process(self, element):
    print(element)
    logging.info(element)
    data = json.loads(element.decode('utf-8'))
    print(data)
    logging.info(data)    
    data['changed'] = True
    print('chegou aqui print')
    logging.info('chegou aqui')
    return [data]

def main():
    optlist = PipelineOptions()

    logging.info('chegou aqui1')

    my_options = optlist.view_as(MyOptions)

    table_schema = { 'fields': [{ 'name': 'text', 'type': 'STRING' }, { 'name': 'value', 'type': 'STRING' }, { 'name': 'changed', 'type': 'BOOL' }] }

    p = beam.Pipeline(options=optlist)
    (p
    # | 'simple' >> beam.Create([ { 'text': 'seila', 'value': 'top' } ])
    # | 'process teste' >> beam.ParDo(CustomFn())
    | 'read pub/sub' >> beam.io.ReadFromPubSub(subscription=str(my_options.subscription_name))
    | 'process' >> beam.ParDo(CustomFn())
    | 'write big query'   >> beam.io.WriteToBigQuery(str(my_options.table_spec),
                                                     schema=table_schema,
                                                     write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                                                     create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED)
    )
    p.run()

if __name__ == '__main__':
    main()