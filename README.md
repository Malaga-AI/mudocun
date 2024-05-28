# Mudocun: A synthetic dataset for multimodal understanding of scientific documents

Mudocun is an evaluation dataset to check understanding of scientific documents. In particular, it focuses on charts and formulas, while referring to context provided in the surrounding text, to stress the model capabilities to reason around multiple modalities provided in the document.

The format of the question is of multiple choice over a particular image, chart or formula.

All questions are created by Gemini 1.5 pro.

## Configure

If you want to run request against Gemini, you'll need to set up your environment and GCP account first. Note that this is only needed if you'd like to contribute new results.

You can proceed as follows (a virtual environment is recommended):
```bash
pip install -r requirements.txt
gcloud auth application-default login
gcloud auth application-default set-quota-project <PROJECT_NAME>
```
where `<PROJECT_NAME>` is the project defined in Vertex AI.

Additionally, create an environment file with the following variables:
```bash
PROJECT=<PROJECT_NAME>  # As defined in Vertex AI, e.g. mudocun
REGION=<GCP_REGION>   # According to your location, e.g. europe-west9
```