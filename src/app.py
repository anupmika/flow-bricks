import streamlit as st
import time
from databricks.sdk import WorkspaceClient

if 'is_processed' not in st.session_state:
    st.session_state.is_processed = False
    st.session_state.processed_data = None
    st.session_state.file_name = ''

st.title('Smart Data Pipeline Manager using Databricks APIs')

if not st.session_state.is_processed:
    with st.form('uploader_form'):
        db_token = st.text_input('Databricks Token', type='password', placeholder='')
        uploaded_files = st.file_uploader(
            'Upload any file', type=None, accept_multiple_files=False
        )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button('Submit', use_container_width=True)

    if submitted:
        if not db_token:
            st.error('Please enter your Databricks Token.')
        elif not uploaded_files:
            st.warning('Please upload a file.')
        else:
            status_container = st.empty()
            with st.spinner('Processing through Databricks...'):
                try:
                    w = WorkspaceClient(
                        host='https://dbc-3f896ab2-0af4.cloud.databricks.com',
                        token=db_token,
                    )

                    file_name = uploaded_files.name
                    base_path = '/Volumes/workspace/default/my_data_engineering'
                    raw_path = f"{base_path}/{file_name}"
                    output_path = f"{base_path}/cleaned_{file_name}"

                    # 1. Upload
                    w.files.upload(raw_path, uploaded_files, overwrite=True)

                    # 2. Trigger Job
                    run_info = w.jobs.run_now(
                        job_id=188709504602239,
                        notebook_params={
                            'input_path': raw_path,
                            'output_path': output_path,
                        },
                    )

                    run_id = run_info.run_id

                    # 3. Polling Loop
                    while True:
                        run_status = w.jobs.get_run(run_id)
                        current_state = str(
                            run_status.state.life_cycle_state.value
                        ).upper()
                        status_container.write(f"Current Status: {current_state}")

                        if current_state in ['TERMINATED', 'SKIPPED', 'INTERNAL_ERROR']:
                            res_state = (
                                str(run_status.state.result_state.value).upper()
                                if run_status.state.result_state
                                else ''
                            )
                            if res_state == 'FAILED':
                                st.error('Databricks Job Failed. Check logs.')
                                st.stop()
                            break
                        time.sleep(5)

                    # 4. FIXED DOWNLOAD LOGIC
                    status_container.write(
                        'Finalizing and searching for processed file...'
                    )
                    time.sleep(5)  # Spark/Volume consistency wait

                    files_list = list(w.files.list_directory_contents(output_path))
                    target_file_path = None

                    # Logic: Spark folder ke andar asli file dhoondna
                    for f in files_list:
                        f_path = f.path.lower()
                        # Metadata/Folder skip karo, asli data file uthao
                        if not f_path.endswith('_success') and not f_path.endswith('/'):
                            # Agar file part- se shuru ho ya extension match kare
                            if 'part-' in f_path or any(
                                ext in f_path for ext in ['.csv', '.xlsx', '.json']
                            ):
                                target_file_path = f.path
                                break

                    if target_file_path:
                        status_container.write('Downloading processed file...')
                        download_res = w.files.download(target_file_path)
                        st.session_state.processed_data = download_res.contents.read()
                        st.session_state.file_name = f"cleaned_{file_name}"
                        st.session_state.is_processed = True
                        st.rerun()
                    else:
                        st.error(
                            f"Processed file not found in {output_path}. Ensure Notebook uses coalesce(1)."
                        )

                except Exception as e:
                    st.error(f"Error: {e}")

else:
    st.success('✅ Processing Complete!')
    st.download_button(
        label='📥 Download Processed File',
        data=st.session_state.processed_data,
        file_name=st.session_state.file_name,
        mime='application/octet-stream',
        use_container_width=True,
    )

    if st.button('Upload Another File'):
        st.session_state.is_processed = False
        st.session_state.processed_data = None
        st.rerun()
