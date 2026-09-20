# AI Chat Transfer

**One skill that lets Codex, Claude Code, or Cursor transfer saved conversations from any of the three tools between computers or project folders.**

Install **`ai-chat-transfer`** in the assistant you want to perform the work, then describe the conversation and destination. The assistant follows the appropriate storage procedure, copies the selected conversation, checks the destination, and explains how to resume it.

For example, Codex can copy a Claude Code conversation to another computer, and Cursor can relocate a Codex conversation to another project folder. The conversation still resumes in the application that created it: this skill transfers saved chats, not chat formats between applications.

## What is included

| Assistant performing the transfer | Install from | Conversation formats covered |
| --- | --- | --- |
| Codex | [`codex/`](codex/SKILL.md) | Codex, Claude Code, Cursor |
| Claude Code | [`claude/`](claude/SKILL.md) | Codex, Claude Code, Cursor |
| Cursor | [`cursor/`](cursor/SKILL.md) | Codex, Claude Code, Cursor |

All three folders contain identical, complete copies of the skill. You need only one copy per assistant. The folder names organize installation choices; they do not limit which conversations an assistant can transfer.

Each distribution contains:

```text
ai-chat-transfer/                 # Installed folder name
├── SKILL.md                      # Shared workflow and all three procedures
├── references/
│   └── storage-transfer.md       # Detailed Codex storage migration procedure
└── scripts/
    └── transfer-chat.sh          # Limited Claude Code transcript-copy helper
```

Copy the entire distribution, including its supporting directories. Copying only `SKILL.md` leaves the Codex reference and Claude helper unavailable.

## Requirements

- An assistant with local file and shell access, and permission to read the selected conversation and write its destination.
- The original chat application installed and independently authenticated on the destination if you want to continue the chat there.
- For transfers over SSH, a reachable destination with working SSH authentication. The assistant may use tools such as `scp` or `rsync`.
- Compatible source and destination storage formats. The assistant must inspect installed versions and schemas before migration.
- Appropriate local utilities for the selected procedure: the Claude helper needs Bash; Codex database inspection commonly uses Python 3 with SQLite support.

The commands below use a POSIX shell, suitable for Linux, macOS, or an appropriate WSL environment. Native Windows paths and shell commands need adaptation. Install the skill in the environment where the assistant actually runs; a skill installed on your laptop is not automatically installed inside a remote worker or container.

## Installation

### 1. Download the repository

Download and extract the repository ZIP, or clone it:

```bash
git clone https://github.com/numanzahid/ai-chat-transfer.git
cd ai-chat-transfer
```

Run the installation commands below from this repository's root. They are for a fresh installation. If `ai-chat-transfer` already exists at the destination, inspect or back it up first rather than creating an extra nested directory or overwriting customizations.

### 2. Choose personal or project installation

Personal installation makes the skill available across your local projects. Project installation keeps it with a particular project. `~` means the home directory of the user running the assistant; `<project>` means your target project's root.

| Assistant | Personal installation directory | Project installation directory |
| --- | --- | --- |
| Codex | `~/.agents/skills/ai-chat-transfer/` | `<project>/.agents/skills/ai-chat-transfer/` |
| Claude Code | `~/.claude/skills/ai-chat-transfer/` | `<project>/.claude/skills/ai-chat-transfer/` |
| Cursor | `~/.cursor/skills/ai-chat-transfer/` | `<project>/.cursor/skills/ai-chat-transfer/` |

These locations follow the [official Codex skill documentation](https://learn.chatgpt.com/docs/build-skills), [Claude Code skill documentation](https://code.claude.com/docs/en/skills), and [Cursor skill documentation](https://cursor.com/help/customization/skills). Codex's skill discovery directory is separate from its conversation storage directory, which is commonly `~/.codex`.

### Codex

Personal installation:

```bash
mkdir -p "$HOME/.agents/skills"
cp -R codex "$HOME/.agents/skills/ai-chat-transfer"
```

Project installation instead:

```bash
mkdir -p /absolute/path/to/project/.agents/skills
cp -R codex /absolute/path/to/project/.agents/skills/ai-chat-transfer
```

### Claude Code

Personal installation:

```bash
mkdir -p "$HOME/.claude/skills"
cp -R claude "$HOME/.claude/skills/ai-chat-transfer"
```

Project installation instead:

```bash
mkdir -p /absolute/path/to/project/.claude/skills
cp -R claude /absolute/path/to/project/.claude/skills/ai-chat-transfer
```

### Cursor

Personal installation:

```bash
mkdir -p "$HOME/.cursor/skills"
cp -R cursor "$HOME/.cursor/skills/ai-chat-transfer"
```

Project installation instead:

```bash
mkdir -p /absolute/path/to/project/.cursor/skills
cp -R cursor /absolute/path/to/project/.cursor/skills/ai-chat-transfer
```

Replace `/absolute/path/to/project` with your real path and quote it if it contains spaces. Choose either the personal or project installation for each assistant. Some assistants also discover compatible skill directories belonging to other tools; avoid redundant installations if the skill already appears.

### 3. Confirm discovery

Start a new assistant session, or reload the application if the skill is not discovered. For a project installation, open that project. Check that the installed file is exactly `<skill-directory>/ai-chat-transfer/SKILL.md`, with no extra `codex`, `claude`, or `cursor` directory between them.

Ask the assistant whether `ai-chat-transfer` is available, or look for it in its skill selector. In Cursor, check **Customize → Skills**. See [Cursor's skill documentation](https://cursor.com/docs/skills).

## How to use it

Enter these requests in the assistant's chat, not your terminal. The skill name is always **`ai-chat-transfer`**.

### Codex

Mention the skill explicitly:

```text
Use $ai-chat-transfer to copy my Claude Code session <SESSION_ID>
to SSH host <HOST> and workspace /absolute/destination/project.
Keep the source and transfer only the chat.
```

You can also select the installed skill through your Codex client's skill picker, or explicitly ask it to use the `ai-chat-transfer` skill by name.

### Claude Code

Invoke the skill as a slash command:

```text
/ai-chat-transfer Copy my Cursor conversation <SESSION_ID> to SSH host
<HOST>, using /absolute/destination/project. Keep the source copy.
```

Claude Code exposes installed skills as `/skill-name` commands; see its [skill invocation documentation](https://code.claude.com/docs/en/skills).

### Cursor

Type `/` in Agent chat and select `ai-chat-transfer` when available, then enter your request. Alternatively, name the skill explicitly:

```text
Use the ai-chat-transfer skill to copy my Codex conversation <SESSION_ID>
to /absolute/destination/project on this computer.
```

Cursor documents skill selection through its [Agent skill interface](https://cursor.com/docs/skills).

### What to include in a request

| Detail | Example or guidance |
| --- | --- |
| Source application | Codex, Claude Code, or Cursor |
| Conversation | Session ID, identifiable title, or “this chat” when it belongs to the assistant you are currently using |
| Source workspace | Include it when the assistant cannot infer it |
| Destination | Local folder, or SSH host/user plus an absolute workspace path |
| Project files | Say whether to copy them too; existing project files do not need to be recopied for a chat-only transfer |
| Copy or move | Copy keeps the original; removal requires explicit authorization and successful destination continuation |

When asking one assistant to transfer another application's chat, identify the source application and conversation. “This chat” ordinarily means the current assistant's conversation, not whichever chat was most recently used in another tool.

### Example requests

Copy the current conversation to another computer:

```text
Use the ai-chat-transfer skill to copy this chat to SSH host <HOST>.
The destination workspace is /absolute/destination/project.
The project files are already there; transfer only this chat and keep the source.
```

Continue in a different local folder:

```text
Use the ai-chat-transfer skill to resume Codex session <SESSION_ID>
in /absolute/new/project on this computer. Reuse the existing session.
```

Include project files:

```text
Use the ai-chat-transfer skill to copy Claude Code session <SESSION_ID>
and its project to <HOST>:/absolute/destination/project.
Exclude node_modules and build output. Preserve the original files and chat.
```

Find a chat by title:

```text
Use the ai-chat-transfer skill to find the Cursor conversation titled
“Database migration” in /absolute/source/project and copy it to <HOST>.
Use /absolute/destination/project there. Ask me if multiple conversations match.
```

Move only after confirming success:

```text
Use the ai-chat-transfer skill to copy Codex session <SESSION_ID> to <HOST>
at /absolute/destination/project. Keep the source until I confirm that
I can continue the destination chat; then help me remove the source copy.
```

Angle-bracket values are placeholders. Substitute your actual session and host details. You do not need to run the bundled transfer script yourself; the assistant selects the appropriate procedure and tools.

## What the assistant does

1. Identifies the requested conversation, source storage, and destination workspace.
2. Inspects storage compatibility and existing destination data.
3. Captures the selected conversation and required companion records, using a consistent snapshot where necessary.
4. Copies the selected data and adapts destination workspace metadata.
5. Verifies copied content and records, then provides instructions to resume.
6. Reports whether actual interactive continuation was tested and whether the source remains.

This is an instruction-driven workflow, not an unattended migration service. The assistant may need missing destination details, tool permissions, or clarification about conflicting destination data.

## Continue the transferred conversation

Use the application that originally created the chat. After connecting to the destination, typical commands are:

**Codex:**

```bash
codex resume <SESSION_ID> --cd /absolute/destination/project
```

For a nondefault Codex home, use the destination's `CODEX_HOME` setting. Resuming in another folder on the same machine reuses the session; it does not make an independent duplicate.

**Claude Code:**

```bash
cd /absolute/destination/project
claude --resume <SESSION_ID>
```

**Cursor:** Open the destination workspace folder, locate the conversation in history, and continue it. Refresh or restart Cursor if needed.

The assistant should confirm the installed CLI syntax and give you commands for your actual destination. Valid files and database rows do not by themselves prove that an interactive resume succeeded.

## Scope and limitations

- **Same-format transfers:** Each chat stays in its original application. ChatGPT web conversations and cross-application format conversion are outside this skill's scope.
- **Snapshots:** Messages created after the snapshot are not copied. There is no continuous sync or automatic merging of chats used on both machines.
- **Project files are separate:** A transcript does not restore missing source files, databases, running terminals, containers, or application services.
- **Version-dependent storage:** Local chat formats can change. Unknown schemas or required companion data can prevent a reliable transfer.
- **Historical paths:** Old absolute paths may remain in messages. The resumed assistant needs the new working directory and available project files.
- **Credentials stay separate:** Destination authentication and required tools must be available independently; the skill does not copy account credentials.
- **Selected data only:** Memory, unrelated chats, and global settings are not included by default. Existing destination chats must not be silently overwritten.
- **Codex history:** Paginated sessions can require SQLite history records as well as JSONL transcripts. See the bundled [storage procedure](codex/references/storage-transfer.md).
- **Claude helper limitations:** The script assumes a conventional storage layout and simple paths, copies main transcripts only, and can overwrite destination files. Without explicit session selection it may copy all project sessions. The skill requires preflight checks and an explicit `--session`; incompatible paths or required companion data need another transfer method.

The Codex procedure was derived from a transfer between CLI versions 0.155.1 and 0.154.0, with storage records verified. That observation is not an end-to-end compatibility guarantee for every version or application.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| Skill is not listed | Installation scope, exact folder name, `SKILL.md` placement, and application reload; check whether your environment permits local skills |
| Supporting file is missing | Copy the entire distribution, not only `SKILL.md` |
| Wrong conversation selected | Specify the source application and session ID; do not rely on “latest” across applications |
| SSH fails | Verify the host alias, destination user, connection, and authentication before transferring |
| Destination session already exists | Ask the assistant to inspect the collision; do not overwrite or merge divergent histories automatically |
| Chat copied but not listed | Try the explicit session ID where supported; check workspace association, permissions, indexes, and installed version |
| History refers to missing files | Copy the required project files separately and tell the resumed assistant the new workspace root |
| Custom application storage | Tell the assistant about settings such as a nondefault `CODEX_HOME`; default paths may not apply |

## Updating and maintaining the skill

To update an installed copy, compare it with the new distribution and preserve any local edits before replacing it. Reload the assistant if necessary. Remove duplicate older installations if they cause ambiguous skill selection.

For contributors, keep `codex/`, `claude/`, and `cursor/` byte-for-byte identical, including supporting files. Use the same frontmatter name, `ai-chat-transfer`, in every `SKILL.md`. Validate referenced files and script syntax when changing the distributions.

This repository contains reusable instructions and supporting code. Do not contribute real chat exports, databases, authentication files, private hostnames, or personal filesystem paths.
