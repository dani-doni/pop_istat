import streamlit as st
import pandas as pd
import requests
import urllib3
import ssl

url_CL_ITTER107 = 'https://raw.githubusercontent.com/ondata/guida-api-istat/master/processing/DCIS_POPRES1/3_Dimension_CL_ITTER107.csv'
CL_ITTER107 = pd.read_csv(url_CL_ITTER107)
# take data of ITTER107 and read it as csv

with st.form("my_form"):
    chosen_ITTER107 = st.selectbox('Comune', options=list(CL_ITTER107['dimensionValueDescription']))
    id_ITTER107 = CL_ITTER107.loc[CL_ITTER107 ['dimensionValueDescription'] == chosen_ITTER107,'dimensionValueID'].iloc[0]
    submitted = st.form_submit_button("Submit")
#choose a ITTER107 from streamlit frontend and take the ID

FREQ = "A"
ETA = "TOTAL"
ITTER107 = id_ITTER107
SESSO = 9
STACIVX = 99
TIPO_INDDEM = "JAN"
#declare API varibles

api_url = "https://sdmx.istat.it/SDMXWS/rest/data/22_289/{}.{}.{}.{}.{}.{}/"
url = api_url.format (FREQ,ETA,ITTER107,SESSO,STACIVX,TIPO_INDDEM)
st.write(url)

class CustomHttpAdapter (requests.adapters.HTTPAdapter):
    # "Transport adapter" that allows us to use custom ssl_context.

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)


def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session
Then use it in place of the requests call:

get_legacy_session().get(url)
