import argparse
import requests
import sys
import re
import os
import json
import cmd

SERVER_URL = "https://shellscribe.onrender.com/generate"
HISTORY_FILE = os.path.expanduser("~/.shellscribe_history.json")

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history[-10:], f, ensure_ascii=False, indent=2)

def add_to_history(history, prompt, response):
    history.append({"prompt": prompt, "response": response})
    return history[-10:]

def stream_response(prompt, loaded_files=None):
    history = load_history()
    payload = {
        "prompt": prompt,
        "history": history[-10:]
    }
    
    # Add loaded files to the payload if provided
    if loaded_files:
        file_contents = {}
        for filename, content in loaded_files.items():
            file_contents[filename] = content
        payload["files"] = file_contents
    
    try:
        response = requests.post(
            SERVER_URL,
            json=payload,
            stream=True
        )
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            sys.exit(1)

        code_buffer = ['<code>']
        explanation_buffer = []
        in_code = False
        full_response = ""

        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue
            full_response += line
            if "<code>" in line:
                in_code = True
                line = line.split("<code>", 1)[1]
            if "</code>" in line:
                code_part, rest = line.split("</code>", 1)
                code_buffer.append(code_part)
                code_buffer.append("</code>")
                in_code = False
                if rest:
                    explanation_buffer.append(rest)
                continue
            if in_code:
                code_buffer.append(line)
            else:
                explanation_buffer.append(line)

        code = code_buffer
        if code:
            for code_line in code:
                code_line = code_line.strip("\n")
                if code_line.startswith("```python"):
                    code_line = code_line[9:]
                if code_line.endswith("```"):
                    code_line = code_line[:-3]
                if code_line:
                    print(code_line)
        explanation = "".join(explanation_buffer).strip()
        if explanation:
            print(explanation)
        # Save to history
        history = add_to_history(history, prompt, full_response)
        save_history(history)
        return full_response
    except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError):
        pass
    return None

def extract_code_from_stream(prompt, file_path, mode="w", loaded_files=None):
    history = load_history()
    payload = {
        "prompt": prompt,
        "history": history[-10:]
    }
    
    # Add loaded files to the payload if provided
    if loaded_files:
        file_contents = {}
        for filename, content in loaded_files.items():
            file_contents[filename] = content
        payload["files"] = file_contents
    
    response = requests.post(
        SERVER_URL,
        json=payload,
        stream=True
    )
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        sys.exit(1)
    full_response = ""
    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
        if chunk:
            print(chunk, end="", flush=True)
            full_response += chunk
    code = ""
    start = full_response.find("<code>")
    end = full_response.find("</code>")
    if start != -1 and end != -1 and end > start:
        code = full_response[start + len("<code>"):end]
        code = code.replace("```python", "").replace("```", "").lstrip("\n")
    with open(file_path, mode, encoding="utf-8") as f:
        f.write(code)
    print(f"\nCode written to {file_path}")
    # Save to history
    history = add_to_history(history, prompt, full_response)
    save_history(history)

def display_title():
    title = """
    ███████╗██╗  ██╗███████╗██╗     ██╗     ███████╗ ██████╗██████╗ ██╗██████╗ ███████╗
    ██╔════╝██║  ██║██╔════╝██║     ██║     ██╔════╝██╔════╝██╔══██╗██║██╔══██╗██╔════╝
    ███████╗███████║█████╗  ██║     ██║     ███████╗██║     ██████╔╝██║██████╔╝█████╗  
    ╚════██║██╔══██║██╔══╝  ██║     ██║     ╚════██║██║     ██╔══██╗██║██╔══██╗██╔══╝  
    ███████║██║  ██║███████╗███████╗███████╗███████║╚██████╗██║  ██║██║██████╔╝███████╗
    ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝
    """
    print(title)
    print("Welcome to ShellScribe! Type 'help' to see available commands.")

class ShellScribeInteractive(cmd.Cmd):
    prompt = ">> "
    intro = ""
    
    def __init__(self):
        super().__init__()
        self.loaded_files = {}  # Dictionary to store loaded files: {filename: content}
    
    def do_prompt(self, arg):
        """Process a prompt and display the AI response: prompt "your prompt here" """
        if not arg:
            print("Please provide a prompt. Usage: prompt \"your prompt here\"")
            return
        
        # Extract the prompt from quotes if present
        if arg.startswith('"') and arg.endswith('"'):
            arg = arg[1:-1]
        
        # Pass loaded files to stream_response
        stream_response(arg, self.loaded_files if self.loaded_files else None)
    
    def do_write(self, arg):
        """Generate code and write to a file: write "your prompt here", filename.ext"""
        if not arg:
            print("Please provide a prompt and filename. Usage: write \"your prompt here\", filename.ext")
            return
        
        try:
            # Split by comma and handle quotes
            parts = arg.split(',', 1)
            if len(parts) != 2:
                print("Invalid format. Usage: write \"your prompt here\", filename.ext")
                return
            
            prompt = parts[0].strip()
            filepath = parts[1].strip()
            
            # Remove quotes if present
            if prompt.startswith('"') and prompt.endswith('"'):
                prompt = prompt[1:-1]
            
            extract_code_from_stream(prompt, filepath, loaded_files=self.loaded_files if self.loaded_files else None)
        except Exception as e:
            print(f"Error: {e}")
    
    def do_read(self, arg):
        """Read a file into memory: read filename.ext"""
        if not arg:
            print("Please provide a filename. Usage: read filename.ext")
            return
        
        filepath = arg.strip()
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            self.loaded_files[filepath] = content
            print(f"File '{filepath}' loaded into memory. You can now refer to it in your prompts.")
            
        except Exception as e:
            print(f"Error reading file: {e}")
    
    def do_forget(self, arg):
        """Remove a file from memory: forget filename.ext"""
        if not arg:
            print("Please provide a filename. Usage: forget filename.ext")
            return
        
        filepath = arg.strip()
        
        if filepath in self.loaded_files:
            del self.loaded_files[filepath]
            print(f"File '{filepath}' has been removed from memory.")
        else:
            print(f"File '{filepath}' was not in memory.")
    
    def do_refactor(self, arg):
        """Refactor an entire file: refactor filename.ext"""
        if not arg:
            print("Please provide a filename. Usage: refactor filename.ext")
            return
        
        filepath = arg.strip()
        
        try:
            # First read the file if not already in memory
            if filepath not in self.loaded_files:
                with open(filepath, "r", encoding="utf-8") as f:
                    self.loaded_files[filepath] = f.read()
            
            # Create a prompt for refactoring
            prompt = f"Please refactor the following code from file {filepath}. Improve its structure, readability, and efficiency without changing its functionality:\n\n{self.loaded_files[filepath]}"
            
            # Get the refactored code
            response = stream_response(prompt, self.loaded_files)
            
            # Ask for confirmation before saving
            confirm = input("\nDo you want to save the refactored code to the original file? (y/n): ")
            if confirm.lower() == 'y':
                # Extract code from the response
                code = ""
                start = response.find("<code>")
                end = response.find("</code>")
                if start != -1 and end != -1 and end > start:
                    code = response[start + len("<code>"):end]
                    code = code.replace("```python", "").replace("```", "").lstrip("\n")
                
                if code:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(code)
                    print(f"Refactored code saved to {filepath}")
                    # Update the loaded file in memory
                    self.loaded_files[filepath] = code
                else:
                    print("No code was found in the response to save.")
            
        except Exception as e:
            print(f"Error refactoring file: {e}")
    
    def do_list(self, arg):
        """List all files currently loaded in memory"""
        if not self.loaded_files:
            print("No files are currently loaded in memory.")
            return
        
        print("\nCurrently loaded files:")
        for filepath in self.loaded_files:
            print(f"  - {filepath} ({len(self.loaded_files[filepath])} characters)")
        print()
    
    def do_exit(self, arg):
        """Exit the ShellScribe interactive mode"""
        print("Goodbye!")
        return True
    
    def do_help(self, arg):
        """Show help information"""
        print("\nAvailable commands:")
        print("  prompt \"your prompt here\"           - Process a prompt and display the AI response")
        print("  write \"your prompt here\", file.ext  - Generate code and write to a file")
        print("  read filename.ext                   - Read a file into memory for reference")
        print("  forget filename.ext                 - Remove a file from memory")
        print("  refactor filename.ext               - Refactor an entire file")
        print("  list                                - List all files currently in memory")
        print("  exit                                - Exit ShellScribe")
        print("  help                                - Show this help message\n")

def main():
    parser = argparse.ArgumentParser(description="Shellscribe CLI")
    parser.add_argument('--legacy', action='store_true', help='Use legacy command-line mode')
    
    # Check if any arguments were provided
    if len(sys.argv) > 1 and sys.argv[1] != '--legacy':
        # Legacy mode with subcommands
        subparsers = parser.add_subparsers(dest='command')
        
        write_parser = subparsers.add_parser('write', help='Generate code and output to terminal')
        write_parser.add_argument('prompt', help='Prompt for code generation')
        
        file_parser = subparsers.add_parser('file', help='Generate code and write to a file')
        file_parser.add_argument('prompt', help='Prompt for code generation')
        file_parser.add_argument('filepath', help='File to write code to')
        file_parser.add_argument('--append', action='store_true', help='Append to file instead of overwrite')
        
        # Add new subcommands for file management
        read_parser = subparsers.add_parser('read', help='Read a file into memory')
        read_parser.add_argument('filepath', help='File to read')
        
        refactor_parser = subparsers.add_parser('refactor', help='Refactor an entire file')
        refactor_parser.add_argument('filepath', help='File to refactor')
        
        args = parser.parse_args()
        
        # Create an instance to store loaded files
        interactive = ShellScribeInteractive()
        
        if args.command == 'write':
            stream_response(args.prompt, interactive.loaded_files if interactive.loaded_files else None)
            print()
        elif args.command == 'file':
            mode = "a" if args.append else "w"
            extract_code_from_stream(args.prompt, args.filepath, mode, 
                                    interactive.loaded_files if interactive.loaded_files else None)
        elif args.command == 'read':
            interactive.do_read(args.filepath)
        elif args.command == 'refactor':
            interactive.do_refactor(args.filepath)
    else:
        # Interactive mode
        display_title()
        ShellScribeInteractive().cmdloop()

if __name__ == "__main__":
    main()