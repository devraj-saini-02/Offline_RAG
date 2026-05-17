import os
from dotenv import load_dotenv

load_dotenv()

import helpers
import rag_app

def check_environment():
    pass

def main():
    check_environment()
    helpers.ensure_directories()
    
    while True:
        print("\n" + "="*52)
        print("📚 Multi-Project Interactive RAG Interface Environment")
        print("="*52)
        print(" 1. Create a New Project Workspace")
        print(" 2. Ingest / Upload a PDF Document")
        print(" 3. Ask Questions (Mandatory Project Filter Scope)")
        print(" 4. Delete Data Assets (Project or Specific PDF Source)")
        print(" 5. Inspect Active Catalog Assets Index Tree")
        print(" 6. Exit Environment Framework")
        print("="*52)
        
        choice = input("Select operation index step (1-6): ").strip()
        
        if choice == "1":
            name_input = input("\nEnter name for the new tracking project: ").strip()
            if name_input:
                helpers.create_project(name_input)
            else:
                print("[Console Error]: Project execution name requirements evaluated empty.")
                
        elif choice == "2":
            projects = helpers.get_all_projects()
            if not projects:
                print("\n[Notice]: No active projects initialized yet. Create a project first.")
                continue
                
            print("\nSelect target project directory branch:")
            for idx, proj in enumerate(projects):
                print(f"  [{idx}] {proj}")
            
            proj_idx = input(f"Enter project selection number (0-{len(projects)-1}): ").strip()
            try:
                selected_project = projects[int(proj_idx)]
            except (ValueError, IndexError):
                print("[Console Error]: Project entry choice verification bound error.")
                continue

            file_path = input("Provide path source directory tracking location to target PDF: ").strip()
            dest_path, file_name = helpers.stage_pdf_file(selected_project, file_path)
            if dest_path and file_name:
                rag_app.ingest_pdf(selected_project, dest_path, file_name)

        elif choice == "3":
            projects = helpers.get_all_projects()
            if not projects:
                print("\n[Notice]: Zero matching structural project entities exist to query against.")
                continue
                
            print("\nSelect project space context to query (Mandatory Step):")
            for idx, proj in enumerate(projects):
                print(f"  [{idx}] {proj}")
                
            proj_idx = input(f"Enter selected target project number (0-{len(projects)-1}): ").strip()
            try:
                selected_project = projects[int(proj_idx)]
            except (ValueError, IndexError):
                print("[Console Error]: Invalid project selection.")
                continue

            print(f"\nTarget Context Track Scope: [{selected_project}]")
            print("  1. Query EVERYTHING stored globally within this project branch")
            print("  2. Filter queries to isolate a SINGLE targeted file source")
            query_scope = input("Choose query evaluation filter structure option (1-2): ").strip()
            
            if query_scope == "1":
                query = input(f"\nAsk anything about the full scope of '{selected_project}': ").strip()
                if query:
                    rag_app.query_vector_store(query, selected_project)

            elif query_scope == "2":
                pdfs = helpers.get_project_pdfs(selected_project)
                if not pdfs:
                    print("[Notice]: This project directory contains zero document assets. Routing to full scope.")
                    query = input(f"Ask a question about full project '{selected_project}': ").strip()
                    if query:
                        rag_app.query_vector_store(query, selected_project)
                else:
                    print(f"\nSelect structured document asset contained inside '{selected_project}':")
                    for idx, f in enumerate(pdfs):
                        print(f"  [{idx}] {f}")
                    file_idx = input(f"Enter file index context number (0-{len(pdfs)-1}): ").strip()

                    try:
                        selected_pdf = pdfs[int(file_idx)]
                    except (ValueError, IndexError):
                        print("[Console Error]: Invalid file index entered.")
                        continue

                    query = input(f"\nEnter question targeted strictly to file '{selected_pdf}': ").strip()
                    if query:
                        rag_app.query_vector_store(query, selected_project, selected_pdf)

        elif choice == "4":
            projects = helpers.get_all_projects()
            if not projects:
                print("\n[Notice]: Vector records catalog is empty.")
                continue
                
            print("\nSelect targeted data clearing purge option:")
            print("  1. Wipe out an ENTIRE Project (Deletes directory content AND database vectors)")
            print("  2. Delete a single targeted file source (Removes file instance AND database vectors)")
            del_choice = input("Select scope selection (1-2): ").strip()
            
            if del_choice == "1":
                print("\nSelect target project directory branch to erase:")
                for idx, proj in enumerate(projects):
                    print(f"  [{idx}] {proj}")
                proj_idx = input(f"Enter target instance (0-{len(projects)-1}): ").strip()
                try:
                    selected_project = projects[int(proj_idx)]
                except (ValueError, IndexError):
                    print("[Console Error]: Selected project configuration out of bounds.")
                    continue

                confirm = input(f"CRITICAL WARNING: Wipe out ALL records/files for '{selected_project}' permanently? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    rag_app.delete_project_embeddings(selected_project)
                    helpers.delete_physical_project(selected_project)
                    print(f"[Purge Process Complete]: Erased tracking metadata branches for '{selected_project}'.")
                    
            elif del_choice == "2":
                print("\nSelect parent project directory track parameter:")
                for idx, proj in enumerate(projects):
                    print(f"  [{idx}] {proj}")
                proj_idx = input(f"Enter tracking target index choice (0-{len(projects)-1}): ").strip()
                try:
                    selected_project = projects[int(proj_idx)]
                except (ValueError, IndexError):
                    print("[Console Error]: Target project selection validation exception.")
                    continue

                pdfs = helpers.get_project_pdfs(selected_project)
                if not pdfs:
                    print("[Notice]: Parent framework node does not track active data assets.")
                    continue
                    
                print(f"\nSelect target tracking node to drop from '{selected_project}':")
                for idx, f in enumerate(pdfs):
                    print(f"  [{idx}] {f}")
                file_idx = input(f"Enter file entry tracking index key (0-{len(pdfs)-1}): ").strip()
                try:
                    selected_pdf = pdfs[int(file_idx)]
                except (ValueError, IndexError):
                    print("[Console Error]: Specified file structural reference mapping missing.")
                    continue

                rag_app.delete_pdf_embeddings(selected_project, selected_pdf)
                helpers.delete_physical_pdf(selected_project, selected_pdf)
                print(f"[Purge Process Complete]: Erased metadata properties for target asset file '{selected_pdf}'.")

        elif choice == "5":
            projects = helpers.get_all_projects()
            print("\n" + "-"*35)
            print("📁 Current Active Tracking Catalog:")
            print("-"*35)
            if not projects:
                print("  (Empty. Create a workspace parameter.)")
            for proj in projects:
                print(f" 📂 Project Space Reference Name: {proj}")
                pdfs = helpers.get_project_pdfs(proj)
                if pdfs:
                    for f in pdfs:
                        print(f"    └── 📄 Source Tracking Asset File: {f}")
                else:
                    print("    └── (Zero document source dependencies attached)")
            print("-"*35)
            
        elif choice == "6":
            print("Exiting multi-project application runtime thread. Environment dropped.")
            break
        else:
            print("[Console Error]: Selection input out of bounds. Pick a parameter between 1 and 6.")

if __name__ == "__main__":
    main()