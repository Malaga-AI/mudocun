import pathlib

ROOT_DIR = str(pathlib.Path(__file__).parent)

local_documents = [
    {
        "title": "Towards Autotuning by Alternating Communication Methods",
        "uri": f"{ROOT_DIR}/docs/autotuning_cscs.pdf",
    }
]

online_documents = [
    {"title": "Mixtral of Experts", "uri": "https://arxiv.org/pdf/2401.04088"},
    {
        "title": "Principles of bursty mRNA expression and irreversibility in single cells and extrinsically varying populations",
        "uri": "https://arxiv.org/pdf/2405.12897",
    },
]
