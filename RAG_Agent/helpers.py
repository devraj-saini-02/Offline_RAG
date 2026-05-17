import os
import shutil

DATA_DIR = "data"

def ensure_directories():
    os.makedirs(DATA_DIR, exist_ok=True)

def get_all_projects():
    if not os.path.exists(DATA_DIR):
        return []
    return [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))]

def get_project_pdfs(project_name):
    proj_path = os.path.join(DATA_DIR, project_name)
    if not os.path.exists(proj_path):
        return []
    return [f for f in os.listdir(proj_path) if f.lower().endswith('.pdf')]

def create_project(project_name):
    proj_name = project_name.strip().replace(" ", "_")
    if not proj_name:
        print("[Helper]: Project name parameter cannot be empty.")
        return False
    
    proj_path = os.path.join(DATA_DIR, proj_name)
    if os.path.exists(proj_path):
        print(f"[Helper]: Project directory '{proj_name}' already exists.")
        return False
    
    os.makedirs(proj_path)
    print(f"[Helper]: Created clean workspace directory structure: data/{proj_name}")
    return True

def stage_pdf_file(project_name, source_path):
    """Safely stages a localized replica copy of target raw documents."""
    proj_path = os.path.join(DATA_DIR, project_name)
    
    clean_path = source_path.strip().strip('"')
    if not os.path.exists(clean_path) or not clean_path.lower().endswith('.pdf'):
        print("[Helper Error]: Targeted asset file path invalid or document is not a PDF format.")
        return None, None

    file_name = os.path.basename(clean_path)
    destination_path = os.path.join(proj_path, file_name)
    
    shutil.copy(clean_path, destination_path)
    return destination_path, file_name

def delete_physical_project(project_name):
    """Deletes raw stored folder directory contents."""
    proj_path = os.path.join(DATA_DIR, project_name)
    if os.path.exists(proj_path):
        shutil.rmtree(proj_path)
        print(f"[Helper]: Removed data tracking workspace folder: {proj_path}")
        return True
    return False

def delete_physical_pdf(project_name, pdf_name):
    """Deletes an isolated tracking document replica file."""
    file_path = os.path.join(DATA_DIR, project_name, pdf_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"[Helper]: Removed localized document source tracking instance: {file_path}")
        return True
    return False