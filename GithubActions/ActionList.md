
# Collection of Actions

## Setup

### Specify your components and scope (when to run and what we can operate on)

```yaml
name: Create Branch Pull or Push on New Issue

on:
  issues:
    types: [opened, edited]
  pull_request:
    types: [opened, synchronize]

jobs:
  create-branch-and-update-files:
    runs-on: ubuntu-latest
    permissions:
      actions: write
      checks: write
      contents: write
      deployments: write
      id-token: write
      issues: write
      discussions: write
      packages: write
      pages: write
      pull-requests: write
      repository-projects: write
      security-events: write
      statuses: write

    steps:
      - name: Check out the repository
        uses: actions/checkout@v2

      - name: Set up Git
        run: |
          git config user.email "actions@wcrp-cmip.org"
          git config user.name "CMIP-IPO GitHub Action"
          git config credential.helper store
          git config --global user.email "actions@wcrp-cmip.org"
          git config --global user.name "CMIP-IPO GitHub Action"
          git config --global push.default current
          GH_TOKEN=${{ secrets.GITHUB_TOKEN }}
          echo "GH_TOKEN=${GH_TOKEN}" >> $GITHUB_ENV
          echo "GITHUB_TOKEN=${GH_TOKEN}" >> $GITHUB_ENV
        shell: bash
```

## Bash Script and Assigning to Environment Variables

```yaml
      - name: Create Branch
        run: |
          ISSUE_NUMBER="${{ github.event.issue.number }}"
          echo "ISSUE_NUMBER=${ISSUE_NUMBER}" >> $GITHUB_ENV

      - name: Create Branch
        run: |
          BRANCH_NAME="issue-${ISSUE_NUMBER}-test"
          echo "BRANCH_NAME=${BRANCH_NAME}" >> $GITHUB_ENV

          git checkout -b $BRANCH_NAME
          # Save the last update to file.
          echo "This file was last updated at $(date)" > last-updated-file.txt

      - name: Get issue body
        id: get_issue_body
        run: |
          issue_body=$(jq -r '.issue.body' $GITHUB_EVENT_PATH)
          echo "Issue Body: $issue_body"
          echo "::set-output name=issue_body::$issue_body"
```

### Branch Operations

```yaml
## Create a new Branch
      - name: Create Branch
        run: |
          BRANCH_NAME="issue-${ISSUE_NUMBER}-test"
          echo "BRANCH_NAME=${BRANCH_NAME}" >> $GITHUB_ENV

          git checkout -b $BRANCH_NAME
          # Save the last update to file.
          echo "This file was last updated at $(date)" > last-updated-file.txt
```

## Python Script Execution

```yaml
## Run a Python Script 
  - name: Write the issue to a file
    run: python .github/workflows/read_issue.py
    working-directory: .github/workflows/
    env:
      PYTHON_SCRIPT_OUTPUT: ${{ steps.run-python-script.outputs.stdout }}
      PYTHON_SCRIPT_ERROR: ${{ env.PYTHON_SCRIPT_ERROR }}
    continue-on-error: true
```

### Git Operations

```yaml
## Git Issues Change
      - name: Check Python script output
        run: |
          echo "Python script output: $PYTHON_SCRIPT_OUTPUT"
          if [[ $PYTHON_SCRIPT_OUTPUT == "FAILED"* ]]; then
            echo "Issue processing failed. Closing the issue..."
            gh issue close "${{ github.event.issue.number }}"
            gh issue comment "${{ github.event.issue.number }}" --body "Processing failed with the following error: $PYTHON_SCRIPT_OUTPUT"
          else
            echo "Issue processed successfully."
          fi
        shell: bash

      - name: Commit and Push Changes
        run: |
          if [[ $PYTHON_SCRIPT_OUTPUT != "FAILED"* ]]; then
            git add -A
            git commit -m "Update last updated file and create new file based on issue"
            git push --force --set-upstream origin $BRANCH_NAME
            echo "BRANCH_LINK=[${BRANCH_NAME}](${{ github.event.repository.html_url }}/tree/${BRANCH_NAME})" >> $GITHUB_ENV
            gh issue comment ${{ github.event.issue.number }} --body "The current branch (\`${BRANCH_NAME}\`) has been created and changes have been pushed. [${BRANCH_NAME}](${{ github.event.repository.html_url }}/tree/${BRANCH_NAME})"
          fi
```

### Additional Categories and Examples

#### Environment Variable Usage

```yaml
## Get the Branch URL
      - name: Get Branch URL
        id: branch-url
        run: echo "BRANCH_URL=${{ github.event.repository.html_url }}/tree/${BRANCH_NAME}" >> $GITHUB_ENV
```

#### Conditional Workflow Execution

```yaml
# Conditional Workflow Execution
jobs:
  conditional-job:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.event.pull_request == 'false'
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Run build
        run: |
          # Your build commands here
```

#### Workflow Dependency

```yaml
# Workflow Dependency
jobs:
  dependent-job:
    runs-on: ubuntu-latest
    needs: [job1, job2]
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Run dependent job
        run: |
          # Your dependent job commands here
```
