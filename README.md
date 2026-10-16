# AI Chat Transfer

**One skill that lets Codex, Claude Code, or Cursor transfer saved conversations from any of the three tools between computers or project folders.**

Clone this repository and open it in Codex, Claude Code, or Cursor. Each assistant already has a project copy of **`ai-chat-transfer`**. Describe the conversation and destination. The assistant follows the appropriate storage procedure, copies the selected conversation, checks the destination, and explains how to resume it.

For example, Codex can copy a Claude Code conversation to another computer, and Cursor can relocate a Codex conversation to another project folder. The conversation still resumes in the application that created it: this skill transfers saved chats, not chat formats between applications.

## What is included

| Assistant performing the transfer | Skill directory in this repository | Conversation formats covered |
| --- | --- | --- |
| Codex | [`.agents/skills/ai-chat-transfer/`](.agents/skills/ai-chat-transfer/SKILL.md) | Codex, Claude Code, Cursor |
| Claude Code | [`.claude/skills/ai-chat-transfer/`](.claude/skills/ai-chat-transfer/SKILL.md) | Codex, Claude Code, Cursor |
| Cursor | [`.cursor/skills/ai-chat-transfer/`](.cursor/skills/ai-chat-transfer/SKILL.md) | Codex, Claude Code, Cursor |

All three directories contain identical, complete copies of the skill. Opening this repository is enough for each assistant to discover its own copy. The directory names match each assistant's project skill location; they do not limit which conversations an assistant can transfer.

Each distribution contains:

```text
ai-chat-transfer/                 # Installed folder name
├── SKILL.md                      # Shared rules and application routing
├── references/
│   ├── codex.md                  # Codex resume and copy procedures
│   ├── claude-code.md            # Claude Code procedure and helper usage
│   ├── cursor.md                 # Cursor procedure and client discovery
│   └── storage-transfer.md       # Detailed Codex storage migration procedure
└── scripts/
    ├── transfer-chat.sh          # Bash entrypoint for the Claude helper
    └── transfer-chat.py          # Validated, collision-protected transcript copy
```

The agent reads the shared rules, then only the reference for the application that owns the selected chat. Codex storage migration loads its detailed storage reference when needed.

Copy the entire distribution, including its supporting directories. Copying only `SKILL.md` leaves the Codex reference and Claude helper unavailable.

## Requirements

- An assistant with local file and shell access, and permission to read the selected conversation and write its destination.
- The original chat application installed and independently authenticated on the destination if you want to continue the chat there.
- For transfers over SSH, a reachable destination with working SSH authentication. The assistant may use tools such as `scp` or `rsync`.
- Compatible source and destination storage formats. The assistant must inspect installed versions and schemas before migration.
- Appropriate local utilities for the selected procedure: the Claude helper needs Bash and Python 3 (also Python 3 on an SSH destination); Codex database inspection commonly uses Python 3 with SQLite support.

The commands below use a POSIX shell, suitable for Linux, macOS, or an appropriate WSL environment. Native Windows paths and shell commands need adaptation. Install the skill in the environment where the assistant actually runs; a skill installed on your laptop is not automatically installed inside a remote worker or container.

## Installation

### Use this repository

Download and extract the repository ZIP, or clone it:

```bash
git clone https://github.com/numanzahid/ai-chat-transfer.git
cd ai-chat-transfer
```

Open that folder in Codex, Claude Code, or Cursor. Each assistant's project skill directory is already in the repository:

| Assistant | Path in this repository |
| --- | --- |
| Codex | `.agents/skills/ai-chat-transfer/` |
| Claude Code | `.claude/skills/ai-chat-transfer/` |
| Cursor | `.cursor/skills/ai-chat-transfer/` |

These locations follow the [official Codex skill documentation](https://learn.chatgpt.com/docs/build-skills), [Claude Code skill documentation](https://code.claude.com/docs/en/skills), and [Cursor skill documentation](https://cursor.com/help/customization/skills). Codex's skill discovery directory is separate from its conversation storage directory, which is commonly `~/.codex`.

No copy step is required to use the skill in this folder. Start a new assistant session here, or reload the application if the skill is not discovered.

### Install for every project, or into a different project

Copy one directory when you want the skill outside this repository. Run the commands below from this repository's root. They are for a fresh installation. If `ai-chat-transfer` already exists at the destination, inspect or back it up first rather than creating an extra nested directory or overwriting customizations.

Personal installation makes the skill available across your local projects. Project installation keeps it with a particular project. `~` means the home directory of the user running the assistant; `<project>` means your target project's root.

| Assistant | Personal installation directory | Project installation directory |
| --- | --- | --- |
| Codex | `~/.agents/skills/ai-chat-transfer/` | `<project>/.agents/skills/ai-chat-transfer/` |
| Claude Code | `~/.claude/skills/ai-chat-transfer/` | `<project>/.claude/skills/ai-chat-transfer/` |
| Cursor | `~/.cursor/skills/ai-chat-transfer/` | `<project>/.cursor/skills/ai-chat-transfer/` |

#### Codex

Personal installation:

```bash
mkdir -p "$HOME/.agents/skills"
cp -R .agents/skills/ai-chat-transfer "$HOME/.agents/skills/"
```

Project installation instead:

```bash
mkdir -p /absolute/path/to/project/.agents/skills
cp -R .agents/skills/ai-chat-transfer /absolute/path/to/project/.agents/skills/
```

#### Claude Code

Personal installation:

```bash
mkdir -p "$HOME/.claude/skills"
cp -R .claude/skills/ai-chat-transfer "$HOME/.claude/skills/"
```

Project installation instead:

```bash
mkdir -p /absolute/path/to/project/.claude/skills
cp -R .claude/skills/ai-chat-transfer /absolute/path/to/project/.claude/skills/
```

#### Cursor

Personal installation:

```bash
mkdir -p "$HOME/.cursor/skills"
cp -R .cursor/skills/ai-chat-transfer "$HOME/.cursor/skills/"
```

Project installation instead:

```bash
mkdir -p /absolute/path/to/project/.cursor/skills
cp -R .cursor/skills/ai-chat-transfer /absolute/path/to/project/.cursor/skills/
```

Replace `/absolute/path/to/project` with your real path and quote it if it contains spaces. Choose either the personal or project installation for each assistant. Some assistants also discover compatible skill directories belonging to other tools; avoid redundant installations if the skill already appears.

### Confirm discovery

Start a new assistant session, or reload the application if the skill is not discovered. For a project installation, open that project. Check that the installed file is exactly `<skill-directory>/ai-chat-transfer/SKILL.md`.

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

For a nondefault Codex home, use the destination's `CODEX_HOME` setting. Resuming in another folder on the same machine reuses the session; it does not make an independent duplicate. An independent local copy needs a separate Codex home and the storage migration procedure, or a verified application-supported fork operation.

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
- **Codex history:** Paginated sessions can require SQLite history records as well as JSONL transcripts. See the bundled [storage procedure](.agents/skills/ai-chat-transfer/references/storage-transfer.md).
- **Claude helper limitations:** The helper requires explicit `--session` selection and refuses to overwrite existing files. It checks JSONL and SHA-256 hashes and transports remote paths as data. It still requires verified slash-only workspace encoding and copies main transcripts only; required companions need separate handling. Custom config directories can be supplied with `--source-config-dir` and `--destination-config-dir`. A partial batch failure reports created files for inspection before retrying.

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

For contributors, edit `.agents/skills/ai-chat-transfer/` as the master, then copy the complete distribution to `.claude/skills/ai-chat-transfer/` and `.cursor/skills/ai-chat-transfer/`. Keep `.agents/skills/ai-chat-transfer/`, `.claude/skills/ai-chat-transfer/`, and `.cursor/skills/ai-chat-transfer/` byte-for-byte identical, including supporting files. Use the same frontmatter name, `ai-chat-transfer`, in every `SKILL.md`. Validate referenced files and script syntax when changing the distributions.

This repository contains reusable instructions and supporting code. Do not contribute real chat exports, databases, authentication files, private hostnames, or personal filesystem paths.

### Validation

Run the isolated helper regression tests from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
bash -n .agents/skills/ai-chat-transfer/scripts/transfer-chat.sh
```

The tests use synthetic transcripts and temporary config directories. They cover explicit selection, existing-file and symlink collisions, a collision during installation, batch preflight, private file permissions, malformed inputs, and remote command execution through a local shell. They do not contact an SSH host or test application continuation.

For application compatibility tests, record the executing agent, source and destination application/client versions, storage layout, verification performed, and whether the destination resumed and accepted a follow-up message. Keep chat content and machine identifiers out of published results. Procedure coverage across all three agents and chat formats does not imply every version combination has been tested.
