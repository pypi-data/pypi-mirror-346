"""BuildProject implementation for creating new theory projects.

This module provides the BuildProject class for creating new theory implementation 
projects from templates. It handles directory structure creation, file copying, 
and initial setup of new modal logic theory implementations.
"""

import os
import shutil
import subprocess
from typing import Union

class BuildProject:
    """Creates a new theory implementation project from templates.
    
    This class handles the creation of a new modal logic theory implementation
    by copying and configuring template files. It sets up the directory structure
    and initializes the basic implementation files.
    
    Attributes:
        theory (str): Name of the source theory to use as template
        source_dir (str): Directory path to the source theory
        project_name (str): Name of the new project (will be prefixed with 'project_')
        destination_dir (str): Directory path for the new project
        log_messages (list): Log of actions and messages during project generation
    """

    # No longer enforcing essential files to allow for flexible project structures

    def __init__(self, theory: str = 'default'):
        """Initialize project builder with specified theory.
        
        Args:
            theory: Name of the source theory to use as template
            
        Raises:
            FileNotFoundError: If the source theory directory doesn't exist
        """
        self.theory = theory
        self.source_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'theory_lib', theory)
        self.project_name = ""
        self.destination_dir = ""
        self.log_messages = []
        
        # Validate source directory exists
        if not os.path.exists(self.source_dir):
            raise FileNotFoundError(
                f"The semantic theory '{self.theory}' was not found at '{self.source_dir}'."
            )
    
    def log(self, message, level="INFO"):
        """Log a message with a specified level.
        
        Args:
            message (str): The message to log
            level (str): The log level (INFO, WARNING, ERROR)
        """
        self.log_messages.append(f"[{level}] {message}")
        # Only print error and warning messages immediately
        if level == "ERROR":
            print(f"Error: {message}")
        elif level == "WARNING":
            print(f"Warning: {message}")
    
    def ask_generate(self):
        """Prompt user to create a new theory implementation project.
        
        Asks the user if they want to generate a new project for the current theory.
        If yes, prompts for a project name and calls generate(). If no, displays
        information about running existing example files.
        """
        result = input(f"Would you like to generate a new {self.theory}-project? (y/n): ")
        if result.lower() not in {'yes', 'ye', 'y'}:
            print("\nYou can run an example.py file that already exists with the command:\n")
            print("  $ model-checker example.py\n")
            return
        
        test_name = input("Enter the name of your project using snake_case: ")
        if not test_name:
            print("Project name cannot be empty.")
            return
            
        try:
            project_dir = self.generate(test_name)
            self._print_success_message(project_dir)
            self._handle_example_script(project_dir)
        except Exception as e:
            print(f"Error creating project: {e}")
        
    def generate(self, name: str, destination_dir: Union[str, None] = None):
        """Generate a new theory implementation project from templates.
        
        Args:
            name: Name for the new project
            destination_dir: Target directory (defaults to current directory)
            
        Returns:
            str: Path to the created project
            
        Raises:
            ValueError: If project name is invalid
            FileExistsError: If project directory already exists
            FileNotFoundError: If source theory not found
        """
        if not name:
            raise ValueError("Project name cannot be empty")
            
        # Create project path
        self.project_name = f"project_{name}"
        
        # Use current directory if no destination specified
        if destination_dir is None:
            destination_dir = os.getcwd()
            
        self.destination_dir = os.path.join(destination_dir, self.project_name)
        
        # Verify destination doesn't exist
        if os.path.exists(self.destination_dir):
            raise FileExistsError(f"Directory '{self.destination_dir}' already exists.")
            
        # Create the project directory and collect files that were copied
        os.makedirs(self.destination_dir)
        
        try:
            # Copy files from source to destination, without printing progress
            self._copy_files(self.destination_dir)
            
            # Customize project files
            self._update_file_contents(self.destination_dir)
            
            # No longer verifying essential files
            # Simply return the created directory
            return self.destination_dir
            
        except Exception as e:
            # Clean up on failure
            if os.path.exists(self.destination_dir):
                shutil.rmtree(self.destination_dir)
            raise
    
    def _copy_files(self, project_dir):
        """Copy all files from source to destination directory.
        
        Args:
            project_dir: Path to the destination project directory
            
        Raises:
            FileNotFoundError: If source files don't exist
            PermissionError: If files can't be copied due to permissions
        """
        # Directories to ignore
        ignore_dirs = ['__pycache__', '.ipynb_checkpoints']
        
        # Copy all files from source to destination
        for item in os.listdir(self.source_dir):
            # Skip ignored directories
            if item in ignore_dirs:
                continue
                
            source_item = os.path.join(self.source_dir, item)
            dest_item = os.path.join(project_dir, item)
            
            try:
                if os.path.isdir(source_item):
                    # Copy directories recursively, but ignore __pycache__ and .ipynb_checkpoints
                    shutil.copytree(
                        source_item, 
                        dest_item,
                        ignore=shutil.ignore_patterns(*ignore_dirs)
                    )
                    self.log(f"Copied directory: {item}")
                else:
                    # Copy files
                    shutil.copy2(source_item, dest_item)
                    self.log(f"Copied file: {item}")
            except Exception as e:
                self.log(f"Error copying {item}: {str(e)}", "ERROR")
    
    def _update_file_contents(self, project_dir):
        """Update file contents with project-specific information.
        
        Args:
            project_dir: Path to the project directory
            
        Raises:
            FileNotFoundError: If files to update don't exist
            PermissionError: If files can't be modified
        """
        # Update __init__.py with current version
        init_path = os.path.join(project_dir, "__init__.py")
        if os.path.exists(init_path):
            with open(init_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Get current version
            version = self._get_current_version()
            
            # Replace version in content
            # Look specifically for the __version__ line and replace it
            import re
            version_pattern = re.compile(r'__version__\s*=\s*["\'].*?["\']')
            new_content = version_pattern.sub(f'__version__ = "{version}"', content)
            
            # If no replacement was made (no pattern match), default to simple replacement
            if new_content == content:
                new_content = content.replace('__version__ = "unknown"', f'__version__ = "{version}"')
            
            with open(init_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
    
    def _get_current_version(self):
        """Extract the current version from the installed model-checker package.
        
        Returns:
            str: Current version number, or fallback version if not found
        """
        try:
            # First try to get version from importlib.metadata (most reliable)
            try:
                from importlib.metadata import version
                return version("model-checker")
            except (ImportError, ModuleNotFoundError):
                # Fallback to package __version__
                from model_checker import __version__
                if __version__ != "unknown":
                    return __version__
                
                # Final fallback to pyproject.toml
                current_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                pyproject_path = os.path.join(current_dir, 'pyproject.toml')
                
                if os.path.exists(pyproject_path):
                    with open(pyproject_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Find version line
                    for line in content.split('\n'):
                        if line.strip().startswith('version = '):
                            return line.split('=')[1].strip().strip('"\'')
            
            return "unknown"  # Fallback to unknown
            
        except Exception:
            return "unknown"  # Fallback on any error
    
    # The _verify_essential_files method has been removed to allow for more flexible project structures
    
    def _print_success_message(self, project_dir):
        """Print success message with created files as a tree structure.
        
        Args:
            project_dir: Path to the project directory
        """
        print(f"\nProject generated at: {project_dir}\n")
        print("Project structure:")
        
        # Print the project root
        print(f"└── {os.path.basename(project_dir)}/")
        
        # Get all items in the project directory
        all_items = sorted(os.listdir(project_dir))
        files = [item for item in all_items if os.path.isfile(os.path.join(project_dir, item))]
        dirs = [item for item in all_items if os.path.isdir(os.path.join(project_dir, item))]
        
        # Print files first
        for i, file in enumerate(files):
            prefix = "    ├── " if i < len(files) - 1 or dirs else "    └── "
            print(f"{prefix}{file}")
        
        # Then print directories and their contents
        for i, directory in enumerate(dirs):
            dir_prefix = "    ├── " if i < len(dirs) - 1 else "    └── "
            print(f"{dir_prefix}{directory}/")
            
            # Get files in the subdirectory
            subdir_path = os.path.join(project_dir, directory)
            subdir_items = sorted(os.listdir(subdir_path))
            
            # Filter out __pycache__ directories
            subdir_items = [item for item in subdir_items if not item.startswith('__pycache__')]
            
            for j, subitem in enumerate(subdir_items):
                sub_prefix = "    │   ├── " if i < len(dirs) - 1 else "        ├── "
                if j == len(subdir_items) - 1:
                    sub_prefix = "    │   └── " if i < len(dirs) - 1 else "        └── "
                print(f"{sub_prefix}{subitem}")
    
    def _handle_example_script(self, project_dir):
        """Handle running the example script if requested.
        
        Args:
            project_dir: Path to the project directory
        """
        result = input("Would you like to test an example in your project? (y/n): ")
        if result.lower() not in {'yes', 'ye', 'y'}:
            print(f"\nYou can test your project by running:\n\nmodel-checker <path-to-example-file>\n")
            return

        # Check for examples.py or examples/__init__.py
        example_script = os.path.join(project_dir, "examples.py")
        examples_init = os.path.join(project_dir, "examples", "__init__.py")
        
        if os.path.exists(example_script):
            selected_example = example_script
        elif os.path.exists(examples_init):
            selected_example = examples_init
        else:
            print("\nNo examples.py or examples/__init__.py found.")
            print(f"\nYou can test your project by running:\n\nmodel-checker <path-to-example-file>\n")
            return
            
        print(f"\nRunning example: {selected_example}")
        try:
            # Use subprocess to run the example script
            subprocess.run(["model-checker", selected_example], 
                         check=True,
                         timeout=30)  # Add 30 second timeout
        except subprocess.TimeoutExpired:
            print("\nScript execution timed out. You can run it manually with:")
            print(f"model-checker {selected_example}")
        except subprocess.CalledProcessError as e:
            print(f"\nError running example: {e}")
            print(f"You can run it manually with: model-checker {selected_example}")
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            print(f"You can run it manually with: model-checker {selected_example}")
