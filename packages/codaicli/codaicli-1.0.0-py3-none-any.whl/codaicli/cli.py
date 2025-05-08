#!/usr/bin/env python3
"""
CodaiCLI - AI-powered CLI assistant for code projects.
Main CLI entry point.
"""

import os
import click
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

from codaicli.config import Config
from codaicli.file_manager import FileManager
from codaicli.ai_manager import AIManager
from codaicli.ui import UI


@click.group(invoke_without_command=True)
@click.version_option()
@click.pass_context
def cli(ctx):
    """CodaiCLI - AI-powered CLI assistant for code projects."""
    if ctx.invoked_subcommand is None:
        # Main interactive mode
        interactive_mode()


@cli.command()
@click.option('--view', is_flag=True, help='View current configuration')
@click.option('--reset', is_flag=True, help='Reset configuration to defaults')
@click.option('--profile', help='Configuration profile to use')
def configure(view, reset, profile):
    """Configure API keys and settings."""
    console = Console()
    config = Config()
    
    # Handle view flag
    if view:
        _show_configuration(console, config)
        return
    
    # Handle reset flag
    if reset:
        if Prompt.ask("Are you sure you want to reset all configuration?", choices=["y", "n"]) == "y":
            config.config = {}
            config.save()
            console.print("[green]Configuration reset to defaults![/green]")
        return
    
    # Handle profile
    if profile:
        config.set("current_profile", profile)
    
    console.print(Panel.fit(
        "[bold blue]CodaiCLI Configuration[/bold blue]\n\n"
        "Select which settings you want to configure. Leave blank to keep current values."
    ))
    
    # Configuration sections with descriptions
    sections = [
        ("Provider Settings", _configure_provider, "Configure default AI provider"),
        ("API Keys", _configure_api_keys, "Set up API keys for different providers"),
        ("Model Settings", _configure_models, "Select models for each provider"),
        ("Advanced Settings", _configure_advanced, "Configure advanced options like tokens and temperature")
    ]
    
    while True:
        # Show current configuration
        _show_configuration(console, config)
        
        # Show menu
        console.print("\n[bold cyan]Configuration Menu[/bold cyan]")
        for i, (name, _, desc) in enumerate(sections, 1):
            console.print(f"{i}. {name} - {desc}")
        console.print("5. Save and Exit")
        console.print("6. Exit without saving")
        
        # Get user choice
        choice = Prompt.ask(
            "\nSelect an option",
            choices=[str(i) for i in range(1, 7)],
            default="5"
        )
        
        if choice == "5":
            try:
                config.save()
                console.print("\n[green]Configuration saved successfully![/green]")
            except Exception as e:
                console.print(f"\n[red]Error saving configuration: {str(e)}[/red]")
            break
        elif choice == "6":
            if Prompt.ask("Are you sure you want to exit without saving?", choices=["y", "n"]) == "y":
                break
            continue
        else:
            # Run the selected configuration function
            section_name, section_func, _ = sections[int(choice) - 1]
            console.print(f"\n[bold cyan]{section_name}[/bold cyan]")
            section_func(console, config)
            console.print("\n[green]Section configured successfully![/green]")

def _show_configuration(console, config):
    """Display current configuration in a formatted way."""
    console.print(Panel.fit(
        "[bold blue]Current Configuration[/bold blue]"
    ))
    
    # Provider settings
    console.print("\n[bold cyan]Provider Settings[/bold cyan]")
    console.print(f"Default Provider: {config.get('default_provider', 'Not set')}")
    
    # API Keys
    console.print("\n[bold cyan]API Keys[/bold cyan]")
    for provider in ["openai", "gemini", "claude"]:
        key = config.get(f"{provider}_api_key", "")
        masked_key = "•" * 8 if key else "Not set"
        console.print(f"{provider.title()}: {masked_key}")
    
    # Model settings
    console.print("\n[bold cyan]Model Settings[/bold cyan]")
    for provider in ["openai", "gemini", "claude"]:
        model = config.get(f"{provider}_model", "Not set")
        console.print(f"{provider.title()}: {model}")
    
    # Advanced settings
    console.print("\n[bold cyan]Advanced Settings[/bold cyan]")
    console.print(f"Current Profile: {config.get('current_profile', 'default')}")
    console.print(f"Max Tokens: {config.get('max_tokens', '4000')}")
    console.print(f"Temperature: {config.get('temperature', '0.2')}")

def _configure_provider(console, config):
    """Configure provider settings."""
    providers = ["openai", "gemini", "claude"]
    provider = Prompt.ask(
        "Select default AI provider",
        choices=providers,
        default=config.get("default_provider", "openai")
    )
    config.set("default_provider", provider)

def _configure_api_keys(console, config):
    """Configure API keys for all providers."""
    console.print("\n[bold]API Key Configuration[/bold]")
    console.print("You'll need API keys for the providers you want to use.")
    console.print("\nGet your API keys from:")
    console.print("- OpenAI: [link=https://platform.openai.com/api-keys]https://platform.openai.com/api-keys[/link]")
    console.print("- Google AI Studio: [link=https://makersuite.google.com/app/apikey]https://makersuite.google.com/app/apikey[/link]")
    console.print("- Anthropic: [link=https://console.anthropic.com/settings/keys]https://console.anthropic.com/settings/keys[/link]")
    
    # OpenAI
    if Prompt.ask("\nConfigure OpenAI API key?", choices=["y", "n"], default="y") == "y":
        api_key = Prompt.ask("Enter your OpenAI API key", password=True)
        if api_key:
            config.set_api_key("openai", api_key)
            console.print("[green]OpenAI API key configured successfully![/green]")
    
    # Google Gemini
    if Prompt.ask("\nConfigure Google Gemini API key?", choices=["y", "n"], default="y") == "y":
        api_key = Prompt.ask("Enter your Google AI Studio API key", password=True)
        if api_key:
            config.set_api_key("gemini", api_key)
            console.print("[green]Google Gemini API key configured successfully![/green]")
    
    # Anthropic Claude
    if Prompt.ask("\nConfigure Anthropic Claude API key?", choices=["y", "n"], default="y") == "y":
        api_key = Prompt.ask("Enter your Anthropic API key", password=True)
        if api_key:
            config.set_api_key("claude", api_key)
            console.print("[green]Anthropic Claude API key configured successfully![/green]")
    
    config.save()
    console.print("\n[green]API key configuration completed![/green]")

def _configure_models(console, config):
    """Configure model settings."""
    # Show current models
    console.print("\n[bold]Current Models:[/bold]")
    for provider in ["openai", "gemini", "claude"]:
        model = config.get(f"{provider}_model", "Not set")
        console.print(f"{provider.title()}: {model}")
    
    # Ask which provider's model to update
    provider = Prompt.ask(
        "\nWhich provider's model do you want to update?",
        choices=["openai", "gemini", "claude", "none"],
        default="none"
    )
    
    if provider == "openai":
        # Allow any model name for OpenAI
        model = Prompt.ask(
            "Enter OpenAI model name",
            default=config.get("openai_model", "o4-mini")
        )
        config.set("openai_model", model)
    
    elif provider == "gemini":
        # Allow any model name for Gemini
        model = Prompt.ask(
            "Enter Gemini model name",
            default=config.get("gemini_model", "gemini-2.5-flash-preview-04-17")
        )
        config.set("gemini_model", model)
    
    elif provider == "claude":
        # Allow any model name for Claude
        model = Prompt.ask(
            "Enter Claude model name",
            default=config.get("claude_model", "claude-3-7-sonnet-latest")
        )
        config.set("claude_model", model)

def _configure_advanced(console, config):
    """Configure advanced settings."""
    # Show current advanced settings
    console.print("\n[bold]Current Advanced Settings:[/bold]")
    console.print(f"Max Tokens: {config.get('max_tokens', '4000')}")
    console.print(f"Temperature: {config.get('temperature', '0.2')}")
    console.print(f"Profile: {config.get('current_profile', 'default')}")
    
    # Ask which setting to update
    setting = Prompt.ask(
        "\nWhich setting do you want to update?",
        choices=["max_tokens", "temperature", "profile", "none"],
        default="none"
    )
    
    if setting == "max_tokens":
        max_tokens = Prompt.ask(
            "Max tokens per response",
            default=str(config.get("max_tokens", "4000"))
        )
        try:
            max_tokens = int(max_tokens)
            config.set("max_tokens", max_tokens)
        except ValueError:
            console.print("[yellow]Invalid max tokens value, using default[/yellow]")
    
    elif setting == "temperature":
        temperature = Prompt.ask(
            "Temperature (0.0 to 1.0)",
            default=str(config.get("temperature", "0.2"))
        )
        try:
            temperature = float(temperature)
            if 0 <= temperature <= 1:
                config.set("temperature", temperature)
            else:
                console.print("[yellow]Temperature must be between 0 and 1, using default[/yellow]")
        except ValueError:
            console.print("[yellow]Invalid temperature value, using default[/yellow]")
    
    elif setting == "profile":
        profile = Prompt.ask(
            "Configuration profile name",
            default=config.get("current_profile", "default")
        )
        config.set("current_profile", profile)


def interactive_mode():
    """Run the main interactive mode."""
    ui = UI()
    config = Config()
    
    # Check if API keys are configured
    if not any([
        config.get("openai_api_key"),
        config.get("gemini_api_key"),
        config.get("claude_api_key")
    ]):
        ui.console.print(
            "[yellow]No API keys configured. Running configuration wizard...[/yellow]"
        )
        configure()
    
    # Get project path
    project_path = os.getcwd()
    file_manager = FileManager(project_path)
    
    # Initialize AI manager with the default provider
    default_provider = config.get("default_provider", "openai")
    ai_manager = AIManager(config, default_provider)
    
    ui.show_welcome(project_path)
    
    while True:
        # Get user input
        query = ui.get_input()
        
        if query.lower() in ["exit", "quit", "q"]:
            ui.console.print("[bold blue]Goodbye![/bold blue]")
            break
            
        if query.lower() in ["clear", "cls"]:
            ui.clear()
            continue
            
        if query.lower() == "help":
            ui.show_help()
            continue
            
        if query.lower().startswith("use "):
            # Change AI provider
            provider = query.lower().split(" ")[1].strip()
            if provider in ["openai", "gemini", "claude"]:
                if ai_manager.set_provider(provider):
                    ui.console.print(f"[green]Switched to {provider}[/green]")
                else:
                    ui.console.print(
                        f"[red]Failed to switch to {provider}. API key not configured.[/red]"
                    )
            else:
                ui.console.print("[red]Unknown provider. Use 'openai', 'gemini', or 'claude'[/red]")
            continue
        
        # Process the query
        try:
            # Use progress spinner for loading
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}[/bold blue]"),
                transient=True
            ) as progress:
                # Loading files task
                file_task = progress.add_task("Loading project files...", total=1)
                files = file_manager.load_files()
                progress.update(file_task, completed=1)
                
                # AI processing task
                ai_task = progress.add_task(f"Processing with {ai_manager.provider}...", total=1)
                start_time = time.time()
                response = ai_manager.process_query(query, files)
                elapsed = time.time() - start_time
                progress.update(ai_task, completed=1)
            
            # Process and display the response
            ui.show_response(response, elapsed)
            
            # Handle potential actions in the response
            actions = ai_manager.extract_actions(response)
            
            if actions:
                for action in actions:
                    if action["type"] == "diff":
                        if ui.confirm_diff(action["file"], action["diff"]):
                            file_manager.apply_diff(action["file"], action["diff"])
                            ui.console.print(f"[green]Applied changes to {action['file']}[/green]")
                    
                    elif action["type"] == "create":
                        if ui.confirm_create(action["file"], action["content"]):
                            file_manager.create_file(action["file"], action["content"])
                            ui.console.print(f"[green]Created file {action['file']}[/green]")
                    
                    elif action["type"] == "delete":
                        if ui.confirm_delete(action["file"]):
                            file_manager.delete_file(action["file"])
                            ui.console.print(f"[green]Deleted file {action['file']}[/green]")
                    
                    elif action["type"] == "run":
                        if ui.confirm_run(action["command"]):
                            result = file_manager.run_command(action["command"])
                            ui.console.print(f"[bold]Command output:[/bold]")
                            ui.console.print(result)
            
        except Exception as e:
            ui.console.print(f"[bold red]Error:[/bold red] {str(e)}")


if __name__ == "__main__":
    cli()