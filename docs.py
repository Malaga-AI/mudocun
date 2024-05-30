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
    {
        "title": "Cancer statistics, 2024",
        "uri": "https://onlinelibrary.wiley.com/doi/pdfdirect/10.3322/caac.21820",
    },
    {
        "title": "Nodular/Keloidal Scleroderma with No Systemic Involvement—A Case Report and a Review of the Literature",
        "uri": "https://www.mdpi.com/2077-0383/13/9/2662/pdf?version=1714557569",
    },
    {
        "title": "Operations Research, Mathematics, Computer Science and Statistics: The Relationships",
        "uri": "https://talenta.usu.ac.id/JoCAI/article/download/653/2722",
    },
    {
        "title": "Biotechnology, Physics, Computer Science",
        "uri": "https://www.nature.com/articles/35108009.pdf",
    },
    {
        "title": "The 6th International Conference on Computer Science and Computational Mathematics (ICCSCM 2017)",
        "uri": "https://iopscience.iop.org/article/10.1088/1742-6596/892/1/011001/pdf",
    },
    {
        "title": "Show issue Year 03/2024 Volume 16 Issue 1 Objectives of Public Finance Law and Axiological Analysis of Law – the Guiding Principles and a Proposal for a Research Approach",
        "uri": "https://journals.kozminski.edu.pl/system/files/Zawadzka-Pak_EN.pdf",
    },
    {
        "title": "The Economics of Tropical Deforestation",
        "uri": "http://eprints.lse.ac.uk/120074/1/Burgess_economics_of_tropical_deforestation_published.pdf",
    },
    {
        "title": "The Economics of Health and Health Care",
        "uri": "http://www3.ub.tu-berlin.de/ihv/001703614.pdf",
    },
    {
        "title": "The Economics of Climate Change",
        "uri": "https://www.aeaweb.org/articles/pdf/doi/10.1257/aer.98.2.1",
    },
    {
        "title": "The worldwide leaf economics spectrum",
        "uri": "http://conservancy.umn.edu/bitstream/11299/176900/1/Wright%20et%20al%202004.pdf",
    },
    {
        "title": "Climate Change 2021 – The Physical Science Basis",
        "uri": "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/84D59430721AC15204CEAFA4F3902A42/stamped-9781009157889pre1_i-ii.pdf/frontmatter.pdf",
    },
    {
        "title": "The Use of Cronbach’s Alpha When Developing and Reporting Research Instruments in Science Education",
        "uri": "https://link.springer.com/content/pdf/10.1007%2Fs11165-016-9602-2.pdf",
    },
    {
        "title": "Reproducible, interactive, scalable and extensible microbiome data science using QIIME 2",
        "uri": "https://europepmc.org/articles/pmc7015180?pdf=render",
    },
    {
        "title": "Analysing the relationships between students and mathematics: a tale of two paradigms",
        "uri": "https://research-repository.griffith.edu.au/bitstream/10072/342065/1/JorgensenPUB4489.pdf",
    },
    {
        "title": "Analysing the relationships between students and mathematics: a tale of two paradigms",
        "uri": "https://research-repository.griffith.edu.au/bitstream/10072/342065/1/JorgensenPUB4489.pdf",
    },
    {
        "title": "Beyond Bits and Bytes: The Role of Electronics, Computer Networking, and Applied Mathematics in Shaping Commerce",
        "uri": "https://journal.hmjournals.com/index.php/JECNAM/article/download/3346/2753",
    },
    {
        "title": "A Study of the Mathematics of Deep Learning",
        "uri": "https://research.manchester.ac.uk/files/207099406/2104.14033v1.pdf",
    },
    {
        "title": "Teaching Mathematics in Tomorrow’s Society: A Case for an Oncoming Counter Paradigm",
        "uri": "https://link.springer.com/content/pdf/10.1007%2F978-3-319-12688-3_13.pdf",
    },
    {
        "title": "Quantum Computing and Machine Learning for Cybersecurity: Distributed Denial of Service (DDoS) Attack Detection on Smart Micro-Grid",
        "uri": "https://www.mdpi.com/1996-1073/16/8/3572/pdf?version=1682040064",
    },
    {
        "title": "The Impact of Quantum Computing on Cybersecurity",
        "uri": "https://doi.org/10.47363/jmca/2023(2)140",
    },
    {
        "title": "Development of Cybersecurity Technology and Algorithm Based on Quantum Computing",
        "uri": "https://www.mdpi.com/2076-3417/11/19/9085/pdf?version=1632912665",
    },
    {
        "title": "Case Study-Based Approach of Quantum Machine Learning in Cybersecurity: Quantum Support Vector Machine for Malware Classification and Protection",
        "uri": "https://arxiv.org/pdf/2306.00284",
    },
    {
        "title": "Quantum computing and its potential impact on U.S. cybersecurity: A review: Scrutinizing the challenges and opportunities presented by quantum technologies in safeguarding digital assets",
        "uri": "https://gjeta.com/sites/default/files/GJETA-2024-0026.pdf",
    },
    {
        "title": "Cyber diplomacy: defining the opportunities for cybersecurity and risks from Artificial Intelligence, IoT, Blockchains, and Quantum Computing",
        "uri": "https://www.tandfonline.com/doi/pdf/10.1080/23742917.2024.2312671?needAccess=true",
    },
    {
        "title": "Technological diversity of quantum computing providers: a comparative study and a proposal for API Gateway integration",
        "uri": "https://link.springer.com/content/pdf/10.1007/s11219-023-09633-5.pdf",
    },
    {
        "title": "Minimizing incident response time in real-world scenarios using quantum computing",
        "uri": "https://link.springer.com/content/pdf/10.1007/s11219-023-09632-6.pdf",
    },
    {
        "title": "AI-based quantum-safe cybersecurity automation and orchestration for edge intelligence in future networks",
        "uri": "https://papers.academic-conferences.org/index.php/eccws/article/download/1211/1221",
    },
    {
        "title": "A Review of Quantum Cybersecurity: Threats, Risks and Opportunities",
        "uri": "https://arxiv.org/pdf/2207.03534",
    },
    {
        "title": "Prospective of colon cancer treatments and scope for combinatorial approach to enhanced cancer cell apoptosis.",
        "uri": "https://europepmc.org/articles/pmc3561496?pdf=render",
    },
    {
        "title": "Dendrimer-Mediated Delivery of Anticancer Drugs for Colon Cancer Treatment",
        "uri": "https://www.mdpi.com/1999-4923/15/3/801/pdf?version=1677650739",
    },
    {
        "title": "Effective drug combinations in breast, colon and pancreatic cancer cells",
        "uri": "https://www.nature.com/articles/s41586-022-04437-2.pdf",
    },
    {
        "title": "Overtreatment of young adults with colon cancer: more intense treatments with unmatched survival gains.",
        "uri": "https://jamanetwork.com/journals/jamasurgery/articlepdf/2207939/soi140121.pdf",
    },
    {
        "title": "Aerobic Exercise and Pharmacological Treatments Counteract Cachexia by Modulating Autophagy in Colon Cancer",
        "uri": "https://www.nature.com/articles/srep26991.pdf",
    },
    {
        "title": "Colon cancer treatment: a review of preclinical and clinical studies on the use of natural products",
        "uri": "https://www.mdpi.com/1420-3049/25/20/4732/pdf"
    },
    {
        "title": "A2M-LEUK: attention-augmented algorithm for blood cancer detection in children",
        "uri": "https://link.springer.com/content/pdf/10.1007/s00521-023-08678-8.pdf"
    },
    {
        "title": "Clonal hematopoiesis and blood-cancer risk inferred from blood DNA sequence.",
        "uri": "https://www.nejm.org/doi/pdf/10.1056/NEJMoa1409405?articleTools=true"
    },
    {
        "title": "Recognition of Blood Cancer Using Different Classification Techniques",
        "uri": "https://iteecs.com/index.php/iteecs/article/download/4/72"
    },
    {
        "title": "Automatic Detection of White Blood Cancer From Bone Marrow Microscopic Images Using Convolutional Neural Networks",
        "uri": "https://ieeexplore.ieee.org/ielx7/6287639/8948470/09149873.pdf"
    },
    {
        "title": "Targeting Protein Kinases in Blood Cancer: Focusing on CK1α and CK2",
        "uri": "https://www.mdpi.com/1422-0067/22/7/3716/pdf?version=1617939782"
    },
    {
        "title": "Ethnic and border differences on blood cancer presentation and outcomes: A Texas population-based study",
        "uri": "https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/cncr.33347"
    },
    {
        "title": "Detection and manipulation of methylation in blood cancer DNA using terahertz radiation",
        "uri": "https://www.nature.com/articles/s41598-019-42855-x.pdf"
    }
     
]
