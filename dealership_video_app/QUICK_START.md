# Quick Start Guide

Get started with the Car Dealership Video Generation App in minutes!

## Prerequisites

- Python 3.9 or higher
- Google AI Studio account
- API keys for Gemini 3.0 and Veo

## Installation

### 1. Clone or Download

If you haven't already, get the code:
```bash
git clone https://github.com/jschibi-droid/codex-playground.git
cd codex-playground
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
GEMINI_API_KEY=your_gemini_api_key_here
VEO_API_KEY=your_veo_api_key_here  # Optional: uses GEMINI_API_KEY if not set
```

## Running the App

### Option 1: Streamlit Web Interface (Recommended)

Launch the web interface:
```bash
streamlit run dealership_video_app/app.py
```

The app will open in your browser at `http://localhost:8501`

### Option 2: Command-Line Interface

For terminal-based interaction:
```bash
python dealership_video_app/cli.py
```

### Option 3: Python Script

Use the app programmatically:
```python
from dealership_video_app.chat.interface import DealershipChatInterface

# Initialize
chat = DealershipChatInterface()

# Start conversation
print(chat.start_conversation())

# Process messages
response = chat.process_message("I need a sales video for new SUVs")
print(response)
```

## Quick Example Workflow

### Creating a Sales Video

1. **Start the app** (Streamlit or CLI)

2. **Answer the first question**:
   ```
   Assistant: "Are you creating content for sales or service advertising?"
   You: "Sales"
   ```

3. **Provide vehicle details**:
   ```
   Assistant: "What vehicle(s) would you like to feature?"
   You: "2024 Honda CR-V"
   ```

4. **Add special offers**:
   ```
   Assistant: "Do you have any special offers?"
   You: "0% APR financing for 60 months"
   ```

5. **Choose tone**:
   ```
   Assistant: "What tone would you like?"
   You: "Family-friendly"
   ```

6. **Add call-to-action**:
   ```
   Assistant: "What call-to-action?"
   You: "Visit us today for a test drive"
   ```

7. **Generate!**:
   ```
   Assistant: "Ready to generate!"
   Click "Generate Video" or type "generate"
   ```

### Using Templates

Quick start with pre-built templates:

**In Streamlit:**
- Browse templates in the right panel
- Click "Use this template" on any template
- Provide customization details
- Generate!

**In CLI:**
```python
from dealership_video_app.config.templates import get_template_by_id

template = get_template_by_id("new_inventory_showcase")
# Use template in your workflow
```

## Available Templates

### Sales Templates
- **New Inventory Showcase**: Feature new arrivals
- **Special Financing Offer**: Highlight financing deals
- **Trade-In Event**: Promote trade-in offers
- **Seasonal Sale Event**: Seasonal promotions
- **Luxury Vehicle Showcase**: Premium vehicle presentation

### Service Templates
- **Seasonal Maintenance Package**: Winter/summer prep
- **Express Service Convenience**: Quick service highlight
- **Tire Service Special**: Tire service promotions
- **Service Loyalty Program**: Membership benefits
- **Certified Technician Expertise**: Technician credentials

## Tips for Best Results

1. **Be Specific**: Provide detailed information about vehicles, offers, and target audience
2. **Use Templates**: Start with templates for consistent professional results
3. **Iterate**: Refine your video through conversation if the first result isn't perfect
4. **Test Different Tones**: Try different styles (professional, dynamic, friendly, luxury)
5. **Keep it Concise**: 30-second videos typically perform best

## Troubleshooting

### "Module not found" errors
```bash
# Ensure you're in the right directory
cd codex-playground
python -m pip install -r requirements.txt
```

### "API key not found" errors
```bash
# Check your .env file exists and has the right keys
cat .env

# Or set directly in terminal (Linux/Mac):
export GEMINI_API_KEY="your_key_here"

# Windows PowerShell:
$env:GEMINI_API_KEY="your_key_here"
```

### Streamlit won't start
```bash
# Try installing streamlit directly
pip install --upgrade streamlit

# Run with full path
python -m streamlit run dealership_video_app/app.py
```

## Common Commands

### Streamlit Interface
- **Start**: `streamlit run dealership_video_app/app.py`
- **Stop**: Press `Ctrl+C` in terminal
- **Change Port**: `streamlit run dealership_video_app/app.py --server.port 8080`

### CLI Interface
- **Start**: `python dealership_video_app/cli.py`
- **Help**: Type `help` in the app
- **Status**: Type `status` to see current context
- **Reset**: Type `reset` to start over
- **Exit**: Type `exit` or `quit`

## Getting Help

- **Documentation**: See `dealership_video_app/README.md`
- **Examples**: Check `dealership_video_app/EXAMPLE_USAGE.md`
- **Architecture**: Read `DEALERSHIP_VIDEO_APP_PLAN.md`
- **Google AI Studio**: See `GOOGLE_AI_STUDIO_PROMPT.md`

## Next Steps

1. **Explore Templates**: Browse all available templates
2. **Customize**: Modify templates or create your own
3. **Integrate**: Connect with your inventory system
4. **Deploy**: Upload to Google AI Studio for production use

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the documentation files
3. Ensure API keys are correctly configured
4. Verify Python version (3.9+)

---

**Ready to create amazing dealership videos? Let's go! 🚗🎬**
