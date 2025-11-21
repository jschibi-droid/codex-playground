"""
Car Dealership Video Generation App - Main Application

Streamlit-based interface for generating custom dealership videos
using Gemini 3.0 and Veo.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import streamlit as st
except ImportError:
    print("Streamlit not installed. Please run: pip install streamlit")
    sys.exit(1)

from dealership_video_app.chat.interface import DealershipChatInterface
from dealership_video_app.video.veo_client import VeoVideoGenerator
from dealership_video_app.video.prompt_builder import PromptBuilder
from dealership_video_app.config.templates import (
    list_all_templates,
    get_template_by_id,
    get_templates_by_type,
)
from dealership_video_app.utils.helpers import format_duration, generate_filename


def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'chat_interface' not in st.session_state:
        st.session_state.chat_interface = DealershipChatInterface()
    
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    
    if 'video_generated' not in st.session_state:
        st.session_state.video_generated = False
    
    if 'current_video_url' not in st.session_state:
        st.session_state.current_video_url = None


def render_sidebar():
    """Render sidebar with app information and settings"""
    with st.sidebar:
        st.title("🚗 Video Generator")
        st.markdown("---")
        
        st.subheader("About")
        st.write(
            "AI-powered video generation for car dealerships. "
            "Create professional videos for sales and service advertising."
        )
        
        st.markdown("---")
        
        st.subheader("Features")
        st.markdown("""
        - 🤖 Intelligent chat interface
        - 📹 Text-to-video generation
        - 🎨 Video customization
        - 📋 Professional templates
        - ⚡ Quick turnaround
        """)
        
        st.markdown("---")
        
        st.subheader("Settings")
        
        # Video quality setting
        quality = st.selectbox(
            "Video Quality",
            ["high", "medium", "ultra", "low"],
            index=0
        )
        st.session_state.video_quality = quality
        
        # Video duration
        duration = st.slider(
            "Default Duration (seconds)",
            min_value=15,
            max_value=60,
            value=30,
            step=5
        )
        st.session_state.video_duration = duration
        
        st.markdown("---")
        
        # Reset button
        if st.button("🔄 Start New Video"):
            st.session_state.chat_interface.reset_conversation()
            st.session_state.conversation_started = False
            st.session_state.video_generated = False
            st.session_state.current_video_url = None
            st.rerun()


def render_templates_section():
    """Render templates browser"""
    st.subheader("📋 Video Templates")
    
    tab1, tab2 = st.tabs(["Sales Templates", "Service Templates"])
    
    with tab1:
        sales_templates = get_templates_by_type("sales")
        for template in sales_templates:
            with st.expander(f"**{template.name}**"):
                st.write(f"**Description:** {template.description}")
                st.write(f"**Duration:** {template.duration} seconds")
                st.write(f"**Style:** {template.style}")
                if st.button(f"Use this template", key=f"sales_{template.id}"):
                    st.session_state.chat_interface.context.template_id = template.id
                    st.success(f"Template '{template.name}' selected!")
    
    with tab2:
        service_templates = get_templates_by_type("service")
        for template in service_templates:
            with st.expander(f"**{template.name}**"):
                st.write(f"**Description:** {template.description}")
                st.write(f"**Duration:** {template.duration} seconds")
                st.write(f"**Style:** {template.style}")
                if st.button(f"Use this template", key=f"service_{template.id}"):
                    st.session_state.chat_interface.context.template_id = template.id
                    st.success(f"Template '{template.name}' selected!")


def render_chat_interface():
    """Render main chat interface"""
    st.subheader("💬 Video Creation Assistant")
    
    chat = st.session_state.chat_interface
    
    # Start conversation if not started
    if not st.session_state.conversation_started:
        initial_message = chat.start_conversation()
        st.session_state.conversation_started = True
    
    # Display conversation history
    messages_container = st.container()
    with messages_container:
        for message in chat.context.messages:
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                with st.chat_message("user"):
                    st.write(content)
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.write(content)
    
    # Show context summary
    if chat.context.video_intent:
        with st.expander("📊 Current Context"):
            st.write(chat.get_context_summary())
            
            # Show what's been collected
            context_dict = chat.context.to_dict()
            for key, value in context_dict.items():
                if value and key not in ['session_id', 'stage', 'messages']:
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    
    # Chat input
    user_input = st.chat_input("Type your message...")
    
    if user_input:
        # Process message
        response = chat.process_message(user_input)
        
        # Check if ready for generation
        if chat.is_ready_for_generation() and not st.session_state.video_generated:
            st.rerun()
    
    # Generate video button
    if chat.is_ready_for_generation() and not st.session_state.video_generated:
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.success("✅ Ready to generate video!")
        
        with col2:
            if st.button("🎬 Generate Video", type="primary"):
                generate_video()


def generate_video():
    """Generate video from conversation context"""
    chat = st.session_state.chat_interface
    
    with st.spinner("Generating your video... This may take a few moments."):
        # Build prompt
        prompt = chat.get_video_prompt()
        
        # Show prompt in expander
        with st.expander("📝 Generated Prompt"):
            st.code(prompt, language="text")
        
        # Generate video (mock for demonstration)
        veo_client = VeoVideoGenerator()
        result = veo_client.generate_from_prompt(
            prompt=prompt,
            duration=chat.context.duration,
            quality=st.session_state.get('video_quality', 'high'),
        )
        
        if result.success:
            st.session_state.video_generated = True
            st.session_state.current_video_url = result.video_url
            
            st.success(f"✅ Video generated successfully in {result.generation_time:.1f}s!")
            
            # Display video info
            st.info(f"**Video URL:** {result.video_url}")
            st.info(f"**Duration:** {format_duration(result.metadata.get('duration', 30))}")
            st.info(f"**Quality:** {result.metadata.get('quality', 'high')}")
            
            # Note about mock implementation
            st.warning(
                "⚠️ **Note:** This is a demonstration. In production, "
                "this would generate an actual video using Veo API. "
                "The URL shown is a placeholder."
            )
        else:
            st.error(f"❌ Video generation failed: {result.error_message}")


def render_video_upload_section():
    """Render video upload and customization section"""
    st.subheader("📤 Customize Existing Video")
    
    uploaded_file = st.file_uploader(
        "Upload a video to customize",
        type=['mp4', 'mov', 'avi', 'mkv', 'webm'],
        help="Upload an existing video to modify"
    )
    
    if uploaded_file:
        st.success(f"✅ Video uploaded: {uploaded_file.name}")
        
        # Save uploaded file
        video_path = f"/tmp/{uploaded_file.name}"
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.session_state.chat_interface.context.uploaded_video_path = video_path
        st.session_state.chat_interface.context.workflow_type = "upload_based"
        
        st.info("Now describe what you'd like to change in the chat above.")


def main():
    """Main application entry point"""
    # Page config
    st.set_page_config(
        page_title="Dealership Video Generator",
        page_icon="🚗",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Title
    st.title("🚗 Car Dealership Video Generation App")
    st.markdown(
        "Create professional videos for your dealership using AI. "
        "Powered by Google Gemini 3.0 and Veo."
    )
    st.markdown("---")
    
    # Initialize
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Main content - two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Chat interface
        render_chat_interface()
    
    with col2:
        # Templates and upload
        render_templates_section()
        st.markdown("---")
        render_video_upload_section()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Car Dealership Video Generator | Powered by Gemini 3.0 & Veo"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
