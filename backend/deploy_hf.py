import sys
import os
from huggingface_hub import HfApi

def deploy_to_hf(repo_id):
    # Verify the user set the HF_TOKEN environment variable
    if not os.environ.get("HF_TOKEN"):
        print("ERROR: HF_TOKEN environment variable is not set.")
        print("Please set your token by running:")
        print("    set HF_TOKEN=hf_your_actual_token_here")
        print("Then run this script again.")
        sys.exit(1)

    print(f"Deploying current directory to Hugging Face Space: {repo_id}")
    print("This may take a few minutes depending on your internet connection...")

    api = HfApi()
    
    try:
        api.upload_folder(
            folder_path=".",
            repo_id=repo_id,
            repo_type="space",
            # We skip the .git and scratch folders to avoid uploading history/temp files
            ignore_patterns=[".git/*", "scratch/*", "__pycache__/*", "*.mp4"]
        )
        print("✅ Deployment Successful!")
        print(f"Your app will be live at: https://huggingface.co/spaces/{repo_id}")
    except Exception as e:
        print("❌ Deployment Failed:")
        print(e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deploy_hf.py <your_username/your_space_name>")
        sys.exit(1)
        
    repo_id = sys.argv[1]
    deploy_to_hf(repo_id)
