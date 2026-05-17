# Trend Letter Bot

Claude Code agent that auto-generates a Korean trend newsletter HTML from a Telegram trigger.

## Setup (new machine)

### 1. Prerequisites
- [Claude Code](https://claude.ai/code) installed and logged in
- Telegram plugin enabled: run `/telegram:configure` inside Claude Code

### 2. Clone and open
```bash
git clone https://github.com/Ooohje/Trend-Letter.git
cd Trend-Letter
claude
```

### 3. Telegram access
Run `/telegram:access` in Claude Code to pair your Telegram account.

### 4. Trigger
Send this message from Telegram:
```
트렌드 레터 만들어줘
```

The agent runs fully autonomously — no confirmation prompts. Two Telegram messages will arrive:
1. Start notification
2. Completion with the HTML file attached

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
    role5_publisher.md           # Writes file + sends Telegram reply
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
