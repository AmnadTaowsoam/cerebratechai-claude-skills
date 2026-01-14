# Make it executable:

bashchmod +x tools/skill-selector.py

# Usage:
    
bashpython tools/skill-selector.py

## Make executable
chmod +x tools/generate-all-skills.py

## Generate all skills
python tools/generate-all-skills.py

## Generate specific batch
python tools/generate-all-skills.py --batch 01

## Generate batch range
python tools/generate-all-skills.py --batch 01-05

## Generate high priority only
python tools/generate-all-skills.py --priority high

## Retry failed
python tools/generate-all-skills.py --retry

## With custom delay
python tools/generate-all-skills.py --delay 10

## Export report
python tools/generate-all-skills.py --report