# pyinitpro
---

✅ How to Set Up and Use pyinitpro CLI (Cross-Platform Guide)

🚀 Install pyinitpro using pipx (preferred)

pipx install pyinitpro

Alternatively, install via pip:

pip install pyinitpro

This makes the pyinitpro command available globally.

---

✅ Usage

Run pyinitpro from anywhere in your terminal:

pyinitpro

It will prompt you to set up your project folders.

Optional flags:

--no-venv  
 Skip creating a Python virtual environment.

--python-version <version>  
 Specify the Python version for the virtual environment.

--dependencies <deps>  
 Provide a comma-separated list of dependencies to add to requirements.txt. If omitted, a default template is created.

--git-remote <url>  
 Add a remote Git repository URL.

--interactive  
 Enable interactive setup to customize folder names.

Example usage with flags:

pyinitpro --interactive --dependencies flask,requests --python-version 3.9

---

💡 Notes

To uninstall pyinitpro:

pipx uninstall pyinitpro

or

pip uninstall pyinitpro

For more information, visit the project's GitHub repository: https://github.com/Martins-O/pyinitpro
