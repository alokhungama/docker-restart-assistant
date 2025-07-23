import streamlit as st
import time
from docker_manager import get_containers, restart_container, is_container_running

st.set_page_config(page_title="Docker Control Panel", layout="wide")
st.title("🛠️ Docker Container Manager")

containers = get_containers()

if not containers:
    st.warning("No containers found.")

for container in containers:
    col1, col2, col3 = st.columns([4, 2, 2])
    with col1:
        st.markdown(f"**{container['Names']}**")
        st.caption(f"Status: `{container['Status']}`")

    with col2:
        if st.button(f"Restart {container['Names']}", key=f"restart_{container['ID']}"):
            with st.spinner(f"Restarting {container['Names']}..."):
                restart_container(container['Names'])
                for _ in range(30):  # Wait max 30 seconds
                    time.sleep(1)
                    if is_container_running(container['ID']):
                        break
                st.success(f"{container['Names']} is running again.")
                st.rerun()

    with col3:
        st.code(container['ID'][:12], language="bash")

