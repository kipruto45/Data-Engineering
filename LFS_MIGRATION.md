# Git LFS Migration Notice

Date: 2025-11-16

This repository recently had large CSV files moved into Git LFS and history rewritten to avoid storing multi-hundred-megabyte files directly in Git.

What changed
- Git LFS was enabled in this repository.
- The following patterns were tracked and migrated into LFS:
  - `external/KRA_Project_2_KRA_Tax_ETL/data/processed/*.csv`
  - `external/KRA_Project_2_KRA_Tax_ETL/data/raw/*.csv`
- A history rewrite was performed on `main` and the branch was force-pushed to `origin/main` to replace prior commits containing the large file objects.

Important: repository history rewritten
- Because commits were rewritten, any existing local clones that fetched the previous `main` will be incompatible with the new `main` history.
- To update a local clone safely you can either re-clone the repository, or reset your local branch to the remote `main` (this will overwrite local changes):

```powershell
# Option A (recommended): reclone
git clone https://github.com/kipruto45/Data-Engineering.git

# Option B (overwrite local main with remote main)
git fetch origin
git checkout main
git reset --hard origin/main
```

Notes and recommendations
- If you have uncommitted work, stash or branch it before resetting or recloning.
- If you prefer large data to be kept outside Git entirely, consider removing `external/.../data/` and storing it in cloud storage (S3). I can help migrate the data to S3 and replace files in the repo with small download scripts.
- If you need additional file patterns tracked by LFS, open an issue or request and I'll add them.

Contact
- If you didn't expect this change or need assistance recovering local work, contact the repository maintainer.
