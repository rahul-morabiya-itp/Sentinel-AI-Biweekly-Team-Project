import os
from pathlib import Path

# =========================
# CONFIGURATION
# =========================

# Root folder of your application
ROOT_FOLDER = r"C:\proj\sentinel-ai-gateway"

# Output markdown file
OUTPUT_FILE = "combined_project_code.md"

# File extensions to include
INCLUDE_EXTENSIONS = {
    ".py",
    ".txt",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".sql",
    ".sh",
    ".bat",
    ".env",
}

# Folders to ignore
IGNORE_FOLDERS = {
    "__pycache__",
    ".git",
    ".idea",
    ".vscode",
    "node_modules",
    "venv",
    ".venv",
    "env",
    "dist",
    "build",
    ".pytest_cache",
    ".mypy_cache",
}

# Files to ignore
IGNORE_FILES = {
    OUTPUT_FILE,
}

# Map extensions to markdown code block languages
LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".jsx": "jsx",
    ".html": "html",
    ".css": "css",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".md": "markdown",
    ".sql": "sql",
    ".sh": "bash",
    ".bat": "bat",
    ".toml": "toml",
    ".ini": "ini",
}


# =========================
# HELPERS
# =========================

def should_include_file(file_path: Path):
    if file_path.name in IGNORE_FILES:
        return False

    if file_path.suffix.lower() in INCLUDE_EXTENSIONS:
        return True

    special_names = {
        "Dockerfile",
        ".gitignore",
        ".env",
    }

    if file_path.name in special_names:
        return True

    return False


def get_language(file_path: Path):
    if file_path.name == "Dockerfile":
        return "dockerfile"

    return LANGUAGE_MAP.get(file_path.suffix.lower(), "")


# =========================
# MAIN FUNCTION
# =========================

def combine_project_to_markdown(root_folder, output_file):
    root_path = Path(root_folder)

    with open(output_file, "w", encoding="utf-8") as outfile:

        # Optional project title
        outfile.write("# Combined Project Codebase\n\n")
        outfile.write(
            "This file contains the complete source code of the project.\n\n"
        )

        for current_root, dirs, files in os.walk(root_path):

            # Remove ignored folders
            dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]

            for file_name in files:

                file_path = Path(current_root) / file_name

                if not should_include_file(file_path):
                    continue

                relative_path = file_path.relative_to(root_path)

                try:
                    with open(file_path, "r", encoding="utf-8") as infile:
                        content = infile.read()

                except UnicodeDecodeError:
                    try:
                        with open(file_path, "r", encoding="latin-1") as infile:
                            content = infile.read()
                    except Exception as e:
                        print(f"Skipping unreadable file: {relative_path}")
                        print(f"Reason: {e}")
                        continue

                except Exception as e:
                    print(f"Skipping file: {relative_path}")
                    print(f"Reason: {e}")
                    continue

                language = get_language(file_path)

                # Write file header
                outfile.write("\n")
                outfile.write("---\n\n")
                outfile.write(f"# FILE: {relative_path}\n\n")

                # Write fenced code block
                outfile.write(f"```{language}\n")
                outfile.write(content)
                outfile.write("\n```\n\n")

                print(f"Added: {relative_path}")

    print(f"\nDone! Markdown file created: {output_file}")


# =========================
# RUN
# =========================

if __name__ == "__main__":
    combine_project_to_markdown(ROOT_FOLDER, OUTPUT_FILE)