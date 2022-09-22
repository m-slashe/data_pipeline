## Generate template file for dataflow

`python src/dag.py --runner DataflowRunner --project sbx-186706-sustjadesb-89460529 --staging_location gs://templatesteste/staging --temp_location gs://templatesteste/temp --template_location gs://templatesteste/src/dag_template --subscription_name projects/sbx-186706-sustjadesb-89460529/subscriptions/test_subscription --table_spec sbx-186706-sustjadesb-89460529:test_dataset.table_test --streaming`

## Example data

`{ "name": "seila1", "value": "seila2" }`