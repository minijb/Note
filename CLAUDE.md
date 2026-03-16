# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview
This repository contains a collection of programming notes and documentation managed via Obsidian. It is not a traditional software codebase but rather a personal knowledge management system. There are no build steps, tests, or compilation processes.

The repository currently consists of three distinct versions or structures of notes:
- **`Blog/`**: Structured using a numbered folder system (e.g., `0_Areas`, `1_Projects`, `2_TechStack`, `10_Archive`). This likely follows a methodology like PARA or Johnny.Decimal.
- **`Note/`**: Organized by broad topic categories (e.g., `Language`, `Project`, `Resources`, `Skill`, `Tools`, `Unity`).
- **`remote/`**: Contains a mix of Chinese-named root files (e.g., `备忘录.md`, `目标.md`), templates, and subdirectories. The presence of `.stfolder` suggests this directory is synced across devices (e.g., via Syncthing).

## Formatting and Conventions
- **Markdown:** All content should be written in standard Markdown, compatible with Obsidian.
- **Obsidian Features:** Support Obsidian-specific syntax such as wikilinks (`[[Note Name]]`) and frontmatter (YAML) where appropriate.
- **File Naming:** When creating new notes, follow the naming conventions of the directory you are working in. In `Blog/`, use appropriate numbered prefixes if placing files in root structures. In `remote/`, Chinese filenames are common and acceptable.
- **Assets:** Images and attachments (like Excalidraw files or PDFs) are stored locally in the vault (e.g., `remote/Excalidraw/`, `remote/PDF/`). Use relative paths or Obsidian link syntax when embedding assets.

## Common Tasks
- **Refactoring Notes:** When asked to reorganize or plan note structures, consider the differences between the three existing versions (`Blog`, `Note`, `remote`) and help consolidate or migrate notes based on the user's preferred methodology.
- **Content Creation:** Provide clear, concise, and well-structured Markdown when writing new notes or summarizing concepts.
- **Searching:** Use the `Glob` and `Grep` tools to find specific concepts or code snippets across the markdown files, as there are many files spread across different directory structures.
