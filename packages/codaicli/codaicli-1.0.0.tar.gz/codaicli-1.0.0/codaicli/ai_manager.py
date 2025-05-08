"""AI model management for CodaiCLI."""

import re


class AIManager:
    """Manages AI model interactions."""
    
    def __init__(self, config, provider="openai"):
        """Initialize with configuration and provider."""
        self.config = config
        self.provider = provider
        self.model = self.config.get(f"{provider}_model")  # Get the selected model
        self.max_tokens = self.config.get("max_tokens", 4000)
        self.temperature = self.config.get("temperature", 0.2)
        self.openai = None
        self.genai = None
        self.anthropic = None
        self.client = None
        
        # Import required libraries lazily
        self._setup_provider()
    
    def _setup_provider(self):
        """Set up the AI provider."""
        provider = self.provider.lower()
        
        if provider == "openai":
            try:
                import openai
                self.openai = openai
                self.openai.api_key = self.config.get("openai_api_key")
                if not self.openai.api_key:
                    raise ValueError("OpenAI API key not configured")
            except ImportError:
                raise ImportError("OpenAI package not installed. Install with: pip install openai")
        
        elif provider == "gemini":
            try:
                import google.generativeai as genai
                self.genai = genai
                
                # Clear any previous configuration to avoid header conflicts
                if hasattr(self.genai, '_configured') and self.genai._configured:
                    # Reset configuration if possible
                    if hasattr(self.genai, '_reset_configuration'):
                        self.genai._reset_configuration()
                
                # Configure with the API key
                api_key = self.config.get("gemini_api_key")
                if not api_key:
                    raise ValueError("Gemini API key not configured")
                
                self.genai.configure(api_key=api_key)
            except ImportError:
                raise ImportError("Google Generative AI package not installed. Install with: pip install google-generativeai")
        
        elif provider == "claude":
            try:
                import anthropic
                self.anthropic = anthropic
                api_key = self.config.get("claude_api_key")
                if not api_key:
                    raise ValueError("Claude API key not configured")
                self.client = anthropic.Anthropic(api_key=api_key)
            except ImportError:
                raise ImportError("Anthropic package not installed. Install with: pip install anthropic")
        
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def set_provider(self, provider):
        """Change the AI provider."""
        if provider == self.provider:
            return True
        
        # Store current provider and model in case we need to revert
        current_provider = self.provider
        current_model = self.model
        
        try:
            # Validate provider before setting
            if provider.lower() not in ["openai", "gemini", "claude"]:
                print(f"Error setting provider: Unknown provider: {provider}")
                return False
                
            self.provider = provider
            self.model = self.config.get(f"{provider}_model")  # Update model for new provider
            self._setup_provider()
            return True
        except Exception as e:
            # Revert to previous provider and model on error
            self.provider = current_provider
            self.model = current_model
            print(f"Error setting provider: {str(e)}")
            return False
    
    def process_query(self, query, files):
        """Process a user query against project files."""
        # Build prompt with project context
        prompt = self._build_prompt(query, files)
        
        # Call appropriate AI model
        if self.provider == "openai":
            return self._call_openai(prompt)
        elif self.provider == "gemini":
            return self._call_gemini(prompt)
        elif self.provider == "claude":
            return self._call_claude(prompt)
    
    def _build_prompt(self, query, files):
        """Build a prompt with query and project context."""
        # Determine number of files to include based on size
        max_token_estimate = 100000  # Conservative estimate
        current_tokens = 0
        included_files = {}
        
        # Sort files by size and include smallest first
        sorted_files = sorted(files.items(), key=lambda x: len(x[1]))
        
        for file_path, content in sorted_files:
            # Rough token estimate (characters / 4)
            file_tokens = len(content) // 4
            
            if current_tokens + file_tokens < max_token_estimate:
                included_files[file_path] = content
                current_tokens += file_tokens
        
        # Build the prompt
        prompt = f"""You are an AI programming assistant embedded in a CLI tool called CodaiCLI. You help developers understand and modify their code.

USER QUERY: {query}

PROJECT FILES:
"""
        
        for file_path, content in included_files.items():
            prompt += f"\n--- {file_path} ---\n{content}\n"
        
        prompt += """
INSTRUCTIONS:
1. Answer the query based on the project files.
2. If you need to suggest code changes, use unified diff format:
   ```diff
   --- path/to/file
   +++ path/to/file
   @@ line_number,line_count @@
   - removed line
   + added line
   ```

3. If you need to create a new file, use:
   ```
   CREATE path/to/file
   file content here
   ```

4. If you need to delete a file, use:
   ```
   DELETE path/to/file
   ```

5. If you need to suggest running a command, use:
   ```
   RUN command
   ```

Remember to explain your reasoning before suggesting any changes. Each change must be confirmed by the user before execution.
"""
        
        return prompt
    
    def _call_openai(self, prompt):
        """Call OpenAI API."""
        try:
            # Use the configured model or default to o4-mini
            model = self.model or "o4-mini"
            response = self.openai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant embedded in a code editor CLI."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_completion_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling OpenAI API: {str(e)}"
    
    def _call_gemini(self, prompt):
        """Call Google Gemini API."""
        try:
            # Use the configured model or default to gemini-2.5-flash-preview-04-17
            model_name = self.model or "gemini-2.5-flash-preview-04-17"
            model = self.genai.GenerativeModel(model_name)
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": self.temperature,
                    "max_output_tokens": self.max_tokens
                }
            )
            
            # Check if we have a text response
            if hasattr(response, 'text'):
                return response.text
            # Try to extract text from parts if available
            elif hasattr(response, 'parts'):
                return ''.join(part.text for part in response.parts if hasattr(part, 'text'))
            # Fallback if we can't extract text
            else:
                return str(response)
        except Exception as e:
            return f"Error calling Gemini API: {str(e)}"
    
    def _call_claude(self, prompt):
        """Call Anthropic Claude API."""
        try:
            # Use the configured model or default to claude-3-7-sonnet-latest
            model = self.model or "claude-3-7-sonnet-latest"
            response = self.client.messages.create(
                model=model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system="You are a helpful assistant embedded in a code editor CLI.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error calling Claude API: {str(e)}"
    
    def extract_actions(self, response):
        """Extract actionable commands from AI response."""
        actions = []
        
        # Check if the response is an error message
        if response.startswith("Error calling"):
            return []
        
        # Extract diff blocks
        diff_pattern = r"```diff\n([\s\S]*?)```"
        for diff_match in re.finditer(diff_pattern, response):
            diff_content = diff_match.group(1)
            
            # Extract file path
            file_match = re.search(r"--- (.*?)\n", diff_content)
            if file_match:
                file_path = file_match.group(1).strip()
                actions.append({
                    "type": "diff",
                    "file": file_path,
                    "diff": diff_content
                })
        
        # Extract CREATE blocks
        create_pattern = r"CREATE (.*?)(?:\n|\r\n)([\s\S]*?)(?=(?:CREATE|DELETE|RUN|```|\n\n\n|$))"
        for create_match in re.finditer(create_pattern, response):
            file_path = create_match.group(1).strip()
            content = create_match.group(2).strip()
            actions.append({
                "type": "create",
                "file": file_path,
                "content": content
            })
        
        # Extract DELETE commands
        delete_pattern = r"DELETE (.*?)(?=\n|$)"
        for delete_match in re.finditer(delete_pattern, response):
            file_path = delete_match.group(1).strip()
            actions.append({
                "type": "delete",
                "file": file_path
            })
        
        # Extract RUN commands
        run_pattern = r"RUN (.*?)(?=\n|$)"
        for run_match in re.finditer(run_pattern, response):
            command = run_match.group(1).strip()
            actions.append({
                "type": "run",
                "command": command
            })
        
        return actions