#!/usr/bin/env bash
# deploy_hf.sh — Push this project to a Hugging Face Space
#
# Usage:
#   bash deploy_hf.sh                          # defaults to Faniyi/quantflow-agent
#   bash deploy_hf.sh <hf-username> <space>    # custom
#
# Prerequisites:
#   - git lfs installed  (brew install git-lfs)
#   - hf CLI logged in:
#       uv tool install hf
#       hf auth login

set -e

HF_USER="${1:-Faniyi}"
SPACE_NAME="${2:-quantflow-agent}"
SPACE_URL="https://huggingface.co/spaces/${HF_USER}/${SPACE_NAME}"
REMOTE_URL="https://huggingface.co/spaces/${HF_USER}/${SPACE_NAME}"

echo "🚀 Deploying to HF Space: ${SPACE_URL}"

# 1. Ensure git lfs is active
git lfs install

# 2. Temporarily allow data/chroma_db in this repo for the HF push
#    by adding a special remote that includes the data directory.
#    We do this via a worktree push — no changes to .gitignore on main.

# 3. Add HF remote if not present
if git remote get-url hf-space &>/dev/null; then
    echo "ℹ️  Remote 'hf-space' already exists, updating URL..."
    git remote set-url hf-space "$REMOTE_URL"
else
    echo "➕ Adding remote 'hf-space'..."
    git remote add hf-space "$REMOTE_URL"
fi

# 4. Stage .gitattributes (LFS tracking rules)
git add .gitattributes
git commit -m "chore: add git-lfs tracking for ChromaDB files" 2>/dev/null || echo "ℹ️  .gitattributes already committed"

# 5. Force-add the chroma_db directory (overriding .gitignore)
echo "📦 Staging ChromaDB (~740MB via LFS, this may take a moment)..."
git add -f data/chroma_db/
git commit -m "chore: bundle ChromaDB for HF Spaces deployment [lfs]" 2>/dev/null || echo "ℹ️  ChromaDB already staged"

# 6. Push to HF Space
echo "⬆️  Pushing to Hugging Face Space (LFS upload may take 2-5 min)..."
git push hf-space main

echo ""
echo "✅ Done! Your Space will build at:"
echo "   ${SPACE_URL}"
echo ""
echo "⚠️  Remember to add your env vars in the Space settings:"
echo "   OPENAI_API_KEY, ALPHAVANTAGE_KEY, NEWSAPI_KEY, NAME, EMAIL"
echo "   LANGCHAIN_TRACING_V2=true, LANGCHAIN_API_KEY, LANGCHAIN_PROJECT=QuantFlow-Agent"
