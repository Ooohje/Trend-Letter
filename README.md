# Trend Letter Bot

Claude Code agent that auto-generates a Korean trend newsletter, Canva card news, and Instagram caption.

## Setup (new machine)

### 1. Prerequisites
- [Claude Code](https://claude.ai/code) installed and logged in

### 2. Clone and open
```bash
git clone https://github.com/Ooohje/Trend-Letter.git
cd Trend-Letter
claude
```

### 3. Trigger
Type this message in Claude Code:
```
트렌드 레터 만들어줘
```

The agent runs fully autonomously — no confirmation prompts. When done, a completion summary appears in chat with:
- Paths to the generated HTML and caption files
- The Canva edit link

## Project structure

```
CLAUDE.md                        # Orchestrator (loads roles via @import)
.claude/
  settings.json                  # bypassPermissions + validation hooks
  roles/
    role1_style_analyst.md       # Extracts CSS from references/
    role2_trend_researcher.md    # Searches for 4 recent trends
    role3_image_sourcer.md       # Sources & verifies images (Pexels/Unsplash/Wikimedia)
    role4_content_writer.md      # Assembles final HTML
    role5_publisher.md           # Writes file to disk
    role6_cardnews_maker.md      # Builds Canva card news + Instagram caption
  hooks/
    validate_html.ps1            # Blocks write if HTML structure is invalid
    check_output.ps1             # Reports output file status on session end
references/                      # Reference HTML files for style extraction
output/                          # Generated newsletters (gitignored)
```

## Harness engineering

The `PostToolUse(Write)` hook auto-validates every `trend_letter*.html` write:
- Requires 4 `.trend-card` blocks
- Requires 8+ `<img>` tags
- Blocks placeholder URLs
- Blocks the file save and injects error context so Claude auto-retries

**Note:** Hooks use PowerShell — Windows only. On macOS/Linux, replace `.ps1` scripts with `.sh` equivalents and update the commands in `.claude/settings.json`.
