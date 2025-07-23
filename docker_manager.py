import streamlit as st
import subprocess
import time
import json


def get_containers():
    try:
        result = subprocess.check_output(["docker", "ps", "-a", "--format", "{{json .}}"]).decode()
        containers = [json.loads(line) for line in result.strip().split('\n') if line]
        return containers
    except subprocess.CalledProcessError:
        st.error("Failed to get Docker containers.")
        return []


def restart_container(container_name):
    try:
        subprocess.run(["docker", "restart", container_name], check=True)
    except subprocess.CalledProcessError:
        st.error(f"Failed to restart container: {container_name}")


def is_container_running(container_id):
    try:
        result = subprocess.check_output(["docker", "inspect", "-f", "{{.State.Running}}", container_id])
        return result.strip().decode() == "true"
    except subprocess.CalledProcessError:
        return False

