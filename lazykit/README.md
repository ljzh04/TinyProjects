# **lazykit**

An extensible CLI project automation tool.
lazykit is a command-line utility designed to streamline common project automation tasks, making project setup and maintenance more efficient. It provides built-in commands for generating boilerplate files like README.md and LICENSE, analyzing project structure, and is built with an extensible plugin architecture for future custom automations.

## **✨ Features**

* **Project Initialization:** Quickly set up new projects with lazykit init.
* **License Generation:** Generate LICENSE files for your project, supporting various open-source licenses (e.g., MIT, Apache, GPLv3, BSD, Creative Commons, etc.) with lazykit gen-license.
* **README Generation:** Automatically generate README.md files based on project context using lazykit gen-readme.
* **File Tree Visualization:** Display your project's directory structure with lazykit tree, allowing for exclusions.
* **Extensible Architecture:** Designed to be easily extended with custom plugins, allowing developers to add new commands and automation workflows.
* **Contextual Understanding:** Utilizes project context (file trees, comments, metadata) to provide intelligent automation.

## **🚀 Installation**

lazykit can be installed directly from your project directory if you have cloned the repository,

#### **Option 1: Clone only lazykit directory using git sparse-checkout**
1. **Clone the directory**
git clone \--no-checkout https://github.com/ljzh04/TinyProjects.git lazykit
cd lazykit
git sparse-checkout init \--cone
git sparse-checkout set lazykit/
git checkout main \# Or your desired branch, e.g., 'master'
cd lazykit

2. **Install dependecies**
pip install -r requirements.txt

3. **You can now run. Or add lazykit/ to your shell PATH**
python -m lazykit [OPTIONS]

#### **Option 2: Clone the whole monorepo (simple, but may be large)**

1. **Clone the repository (if you haven't already):**
git clone https://github.com/ljzh04/TinyProjects.git
cd TinyProjects/lazykit

2. **Install dependecies**
pip install -r requirements.txt

3. **You can now run. Or add lazykit/ to your shell PATH**
python -m lazykit [OPTIONS]

## **💡 Usage**

lazykit operates through a main command-line interface with subcommands for each specific task.

### **General Command Structure**

lazykit \<command\> \[options\]

### **Available Commands**

#### **lazykit init**

Initialize a lazykit project in the current directory or a specified path. This typically sets up configuration files.
lazykit init \[--path \<DIR\>\]

* \--path \<DIR\>: Directory to initialize lazykit in (defaults to current directory).

#### **lazykit gen-license**

Generate a LICENSE file for your project.
lazykit gen-license \[-c DIR\] \[-o FILE\] \[-t TYPE\] \[--overwrite\]

* \-c DIR, \--context-dir DIR: Directory to crawl for project context.
* \-o FILE, \--output FILE: Output file path for the license (e.g., LICENSE).
* \-t TYPE, \--type TYPE: Type of license to generate (e.g., MIT, Apache, GPLv3).
* \--overwrite: Overwrite existing license file if it exists.

**Example:**
lazykit gen-license \-t MIT \-o LICENSE

#### **lazykit gen-readme**

Generate a README.md file for your project.
lazykit gen-readme \[-c DIR\] \[-o FILE\] \[--overwrite\]

* \-c DIR, \--context-dir DIR: Directory to crawl for project context.
* \-o FILE, \--output FILE: Output file path for the README (e.g., README.md).
* \--overwrite: Overwrite existing README file if it exists.

**Example:**
lazykit gen-readme \-o README.md

#### **lazykit tree**

Show the project file tree, similar to the tree command, with options for exclusion.
lazykit tree \[-c DIR\] \[-x \[DIR ...\]\] \[-X \[FILE ...\]\] \[-n\] \[-l\]

* \-c DIR, \--context-dir DIR: Directory to crawl for project context.
* \-x \[DIR ...\], \--exclude-dir \[DIR ...\]: Directories to exclude from the tree.
* \-X \[FILE ...\], \--exclude-file \[FILE ...\]: Files to exclude from the tree.
* \-n, \--no-summary: Do not show summary.
* \-l, \--list-only: List files only, without tree structure.

**Example:**
lazykit tree \-x venv .git \-X \*.pyc

## **⚙️ Configuration**

lazykit uses a configuration system (lazykit/core/config.py) to manage global and user-specific settings. You might find a settings.json file (or similar) where you can configure default behaviors, such as:

* **Default License Type:** Set a preferred license for gen-license.
* **LLM Provider and Model:** If lazykit integrates with Language Model features (e.g., for more intelligent README generation), you can specify your LLM provider (e.g., openai) and model (e.g., gpt-4).

## **🔌 Extensibility and Plugins**

lazykit is designed with extensibility in mind. The plugins/ directory is intended to house user- or developer-provided plugins that can dynamically extend lazykit's functionality. This allows you to integrate lazykit with your specific tools or workflows.
Plugins can expose a register() function to hook into the main CLI, adding new subcommands or modifying existing behaviors.

## **📂 Project Structure**

The lazykit codebase is organized as follows:
lazykit/
├── commands/             \# Built-in CLI commands (e.g., gen\_license, gen\_readme, init, tree)
├── core/                 \# Core reusable logic and business layer
│   ├── config.py         \# Handles global/user configuration and paths
│   ├── context.py        \# Reads file trees, comments, and metadata for project context
│   ├── extractors.py     \# Logic for extracting content (e.g., docstrings, declarations)
│   └── generator.py      \# Functions for generating files from templates
├── docs/                 \# Documentation for lazykit commands
├── plugins/              \# Directory for user or developer-provided plugins
├── templates/            \# Stores templates for generating files (e.g., licenses, READMEs)
│   ├── license/          \# Various license text templates
│   └── readme/           \# README template files
├── utils.py              \# Small, common utility functions (e.g., path helpers, display)
├── \_\_init\_\_.py           \# Python package initialization
├── \_\_main\_\_.py           \# Entrypoint for \`python \-m lazykit\`
├── .lazykitignore        \# Specifies files/directories to ignore during context crawling
├── cli.py                \# Main CLI parser: maps commands to their handlers
├── pyproject.toml        \# Project metadata and build configuration
└── requirements.txt      \# Core Python dependencies

## **🤝 Contributing**

Contributions are welcome\! If you have ideas for new features, improvements, or bug fixes, please feel free to:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and ensure tests pass.
4. Submit a pull request with a clear description of your changes.

For major changes, please open an issue first to discuss what you would like to change.

## **📄 License**

This project is licensed under the MIT License \- see the LICENSE file for details.
