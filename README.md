# Big Data ETL with Apache Spark

In this repo, we see
* how to create a Google Cloud Platform (GCP) Spark cluster with JupyterLab installed
* how to submit a PySpark Job to this cluster
* in `notebooks/jupyter`: Hands-On introduction to key concepts of Spark
  * `spark-intro`: Lessons learned after my first Spark application, building a recommender with cross join of customers and products involved

## Starting a GCP Dataproc Cluster with JupyterLab

Please make sure that your Google Cloud SDK  is >=243.0.0.

First, reate a bucket on Google Cloud Storage (GCS). For example: `gs://spark-intro`.
Be sure to add your bucket in the YAML key `configBucket` of your [cluster configuration YAML](./dataproc-jupyter-cluster.yaml). There, you can also see the `optionalComponents` Anaconda and Jupyter. 

Start a [Dataproc](https://cloud.google.com/dataproc/) cluster with Jupyter installed using

```bash
gcloud beta dataproc clusters import INSERT_CLUSTER_NAME \
    --source dataproc-jupyter-cluster.yaml \
    --region=europe-west1 \
    --project=YOUR_PROJECT
```
You can also choose other [regions](https://cloud.google.com/about/locations/?region=europe#region).

You need to upload the Jupyter notebook after the cluster initialization. Use

```bash
gsutil -m cp -r . gs://YOUR_BUCKET
```
Go to the **Web Interfaces** tab and open `JupyterLab`. The working dir is in your config bucket at `notebooks/jupyter`.

## Submitting PySpark Jobs to GCP

Please follow the instructions on the [GCloud SDK documentation](https://cloud.google.com/sdk/gcloud/reference/dataproc/jobs/submit/pyspark) to submit PySpark jobs via the SDK.

For example, to create the transaction data, you can do:

```
gcloud dataproc jobs submit pyspark datagen/create_transactions.py \
--cluster=YOUR_CLUSTER_NAME \
--region=YOUR_REGION
```

As said in the [Spark Docs](https://spark.apache.org/docs/latest/submitting-applications.html),
we can provide dependencies as `py`, `zip` or `egg` files. From my experience, it's very convenient to build an `egg` using `setup.py` and use this as the dependency.
