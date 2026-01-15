THESIS\_SIM — Streamlit academic app (thesis\_sim)

=================================================
🔗 Live app: https://thesis-sim.streamlit.app


Overview

--------

THESIS\_SIM is an academic, non-commercial Streamlit web app developed as part of an original doctoral research project.

It presents results from building simulations focused on thermal comfort and cooling energy impacts in highly glazed

office buildings in tropical climates.



Author

------

Dr. Arq. Alexandre Oliveira



Repository structure (recommended)

----------------------------------

thesis\_sim/

&nbsp; app/

&nbsp;   thesis.py

&nbsp; assets/

&nbsp;   img/

&nbsp;     (all .png/.jpg images used by the app)

&nbsp; requirements.txt

&nbsp; LICENSE  (MIT)



How to run locally

------------------

1\) Create and activate a virtual environment (recommended):

&nbsp;  python -m venv .venv

&nbsp;  .venv\\Scripts\\activate   (Windows PowerShell)



2\) Install dependencies:

&nbsp;  pip install -r requirements.txt



3\) Run the Streamlit app:

&nbsp;  streamlit run app/thesis.py



Notes about paths (important for cloud deploy)

----------------------------------------------

This app loads images using relative paths resolved from the location of app/thesis.py:

\- ROOT\_DIR = parent folder of /app

\- ASSETS\_DIR = ROOT\_DIR / assets / img



So keep the images inside: assets/img



Deploy (Streamlit Community Cloud)

----------------------------------

1\) Push this repository to GitHub as a PUBLIC repo named: thesis\_sim

2\) In Streamlit Community Cloud:

&nbsp;  - Select the repo thesis\_sim

&nbsp;  - Set main file path: app/thesis.py

&nbsp;  - Deploy



License

-------

MIT License (recommended for academic tools and open source code).

If you publish the paper, consider adding the citation reference below.



Citation (suggested)

--------------------

Oliveira, A. (2026). THESIS\_SIM — Thermal causes and energy impacts of occupants adaptive responses in glass curtain-wall office buildings in the tropics. Doctoral thesis (PPGAU/UFRN - Brazil). (Paper link / DOI to be added.)

## Citation (Streamlit tool)
Oliveira, A. (2026). THESIS_SIM — Streamlit web app for thermal comfort and energy analysis.
Available at: https://thesis-sim.streamlit.app


Acknowledgement

---------------

Results from building simulations conducted as part of a doctoral thesis at the Graduate Program in Architecture and

Urbanism (PPGAU/UFRN - Brazil), under the supervision of Senior Lecturer PhD Aldomar Pedrini (Aug/2024).



