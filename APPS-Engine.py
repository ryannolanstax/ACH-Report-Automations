#python-test % python3 -m streamlit run Carlos_App/test_streamlit.py 
import pandas as pd
import streamlit as st
import base64

def merge_csv_files(engine_df, open_tickets_df):
    engine_df_filtered = engine_df[engine_df['is_reattempted'] == False]
    engine_df_filtered['matched_id'] = 'No'
    merged_df = pd.merge(engine_df_filtered, open_tickets_df, left_on='merchant_id', right_on='stax_id', how='left')
    merged_df.loc[merged_df['ticket_id'].notnull(), 'matched_id'] = 'Yes'
    merged_df.drop(['merchant_id_y', 'stax_id'], axis=1, inplace=True)
    return merged_df

def main():
    st.title("Stax Engine Daily Report Builder")

    st.header("Upload CSV Files")
    st.write("Stax Engine Daily CSV Download  [link](https://app.mode.com/editor/fattmerchant/reports/2fcbf2f57767/queries/8cf6ab01968f)")
    engine_df = st.file_uploader("Upload Daily Stax Engine CSV file", type=['csv'])
    st.write("Current Open Tickets CSV Download [link](https://app.mode.com/editor/fattmerchant/reports/c80539741d0e/queries/5a6857e8df40)")
    open_tickets_df = st.file_uploader("Upload Current Tickets CSV File", type=['csv'])

    if engine_df is not None and open_tickets_df is not None:
        df1 = pd.read_csv(engine_df)
        df2 = pd.read_csv(open_tickets_df)

        if st.button('Merge CSV Files'):
            merged_data = merge_csv_files(df1, df2)
            st.markdown(get_table_download_link(merged_data), unsafe_allow_html=True)

def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="merged_data.csv">Download Merged CSV File</a>'
    return href

if __name__ == "__main__":
    main()
