"""
Command-Line Interface for Video Generation

Simple CLI for users who prefer terminal-based interaction.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dealership_video_app.chat.interface import DealershipChatInterface
from dealership_video_app.video.veo_client import VeoVideoGenerator
from dealership_video_app.utils.helpers import format_duration


def print_banner():
    """Print application banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║   Car Dealership Video Generation App                 ║
    ║   Powered by Gemini 3.0 & Veo                        ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main CLI entry point"""
    print_banner()
    
    print("\nInitializing video generation assistant...")
    chat = DealershipChatInterface()
    
    print("\n" + "="*60)
    print(chat.start_conversation())
    print("="*60 + "\n")
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\n👋 Thank you for using the Video Generation App!")
                break
            
            # Check for help command
            if user_input.lower() in ['help', '?']:
                print("\nAvailable commands:")
                print("  - Type your message to chat with the assistant")
                print("  - 'status' - Show current context")
                print("  - 'reset' - Start a new conversation")
                print("  - 'generate' - Generate video (when ready)")
                print("  - 'exit' - Exit the application")
                continue
            
            # Check for status command
            if user_input.lower() == 'status':
                print("\n📊 Current Context:")
                print(chat.get_context_summary())
                print(f"\nReady for generation: {chat.is_ready_for_generation()}")
                continue
            
            # Check for reset command
            if user_input.lower() == 'reset':
                print("\n🔄 Starting new conversation...")
                print(chat.reset_conversation())
                continue
            
            # Check for generate command
            if user_input.lower() == 'generate':
                if not chat.is_ready_for_generation():
                    print("\n⚠️  Not ready to generate yet. Please provide more information.")
                    missing = chat.context.get_missing_information()
                    if missing:
                        print(f"Missing: {', '.join(missing)}")
                    continue
                
                print("\n🎬 Generating video...")
                generate_video(chat)
                
                print("\n✅ Video generation complete!")
                print("Would you like to create another video? (yes/no)")
                response = input("You: ").strip().lower()
                if response in ['yes', 'y']:
                    print(chat.reset_conversation())
                else:
                    print("\n👋 Thank you for using the Video Generation App!")
                    break
                continue
            
            # Process user message
            if not user_input:
                continue
            
            response = chat.process_message(user_input)
            print(f"\n🤖 Assistant: {response}")
            
            # Check if ready for generation
            if chat.is_ready_for_generation() and chat.context.stage == "ready_for_generation":
                print("\n✨ Ready to generate! Type 'generate' to create your video.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Type 'help' for available commands or 'exit' to quit.")


def generate_video(chat: DealershipChatInterface):
    """Generate video from chat context"""
    # Get the generated prompt
    prompt = chat.get_video_prompt()
    
    print("\n📝 Generated Prompt:")
    print("-" * 60)
    print(prompt)
    print("-" * 60)
    
    # Create Veo client and generate
    print("\n⏳ Generating video (this may take a few moments)...")
    veo_client = VeoVideoGenerator()
    
    result = veo_client.generate_from_prompt(
        prompt=prompt,
        duration=chat.context.duration,
        quality=chat.context.quality,
    )
    
    if result.success:
        print(f"\n✅ Video generated successfully!")
        print(f"   Generation time: {result.generation_time:.1f}s")
        print(f"   Video URL: {result.video_url}")
        print(f"   Duration: {format_duration(result.metadata.get('duration', 30))}")
        print(f"   Quality: {result.metadata.get('quality', 'high')}")
        
        print("\n⚠️  Note: This is a demonstration. In production, this would")
        print("   generate an actual video using the Veo API.")
    else:
        print(f"\n❌ Video generation failed: {result.error_message}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
