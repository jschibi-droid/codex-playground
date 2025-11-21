# Car Dealership Video Generation App

An AI-powered custom video generation application for car dealerships, powered by Google's Gemini 3.0 and Veo.

## Overview

This application provides an intelligent chat interface that helps car dealerships create professional video content for both sales and service advertising. It supports two main workflows:

1. **Prompt-based Generation**: Describe your video needs, and the AI creates it from scratch
2. **Upload & Customize**: Upload an existing video and customize it through conversation

## Features

### Intelligent Chat Interface
- Conversational video creation workflow
- Automatic intent detection (sales vs. service)
- Context-aware suggestions
- Professional prompt engineering

### Video Generation
- Text-to-video generation using Veo
- Video customization and modification
- Dealership-specific templates
- Brand consistency options

### Templates
- **Sales**: Inventory showcase, promotions, financing offers
- **Service**: Maintenance packages, seasonal offers, service highlights

## Quick Start

### Prerequisites
- Python 3.9 or higher
- Google AI Studio account
- Gemini API key
- Veo API access

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure API keys:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

3. Run the application:

**Streamlit Interface (Recommended)**:
```bash
streamlit run dealership_video_app/app.py
```

**Python Script**:
```bash
python dealership_video_app/app.py
```

**Google AI Studio Notebook**:
- Upload the `notebook_interface.ipynb` file to Google AI Studio
- Follow the in-notebook instructions

## Usage Examples

### Example 1: Create a Sales Video
```
You: "I need a video for our new SUV sale"
AI: "I'll help you create a sales video. What type of SUVs are you featuring?"
You: "2024 Honda CR-V, we have 15 in stock with 0% financing"
AI: "Great! What tone would you like - professional, exciting, or family-friendly?"
You: "Family-friendly"
AI: [Generates video with family-friendly SUV showcase and financing offer]
```

### Example 2: Customize a Service Video
```
You: "I want to update our tire service video" [uploads video]
AI: "I've analyzed your video. What would you like to change?"
You: "Update pricing to $399 for winter tire package"
AI: "Should I update the visuals for a winter theme?"
You: "Yes, make it more winter-appropriate"
AI: [Generates modified video with winter theme and new pricing]
```

## Application Structure

```
dealership_video_app/
├── app.py                      # Main Streamlit application
├── config/
│   ├── gemini_config.py       # Gemini 3.0 settings
│   ├── veo_config.py          # Veo API settings
│   └── templates.py           # Template definitions
├── chat/
│   ├── interface.py           # Chat interface logic
│   ├── intent_classifier.py  # Sales/Service detection
│   ├── conversation_flow.py  # Dialog management
│   └── context_manager.py    # Session context
├── video/
│   ├── prompt_builder.py      # Veo prompt construction
│   ├── veo_client.py          # Veo API client
│   ├── video_analyzer.py      # Video analysis
│   └── customizer.py          # Video modification
├── templates/
│   ├── sales_templates.json   # Sales templates
│   └── service_templates.json # Service templates
└── utils/
    ├── validators.py          # Input validation
    └── helpers.py             # Utility functions
```

## Configuration

### Environment Variables

Create a `.env` file with:

```env
# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.0-pro

# Veo API Configuration
VEO_API_KEY=your_veo_api_key_here
VEO_MODEL=veo-001

# Application Settings
MAX_VIDEO_DURATION=60
DEFAULT_VIDEO_QUALITY=high
ENABLE_ANALYTICS=true
```

### Template Customization

Templates are defined in JSON format:

```json
{
  "id": "new_inventory_showcase",
  "name": "New Inventory Showcase",
  "type": "sales",
  "duration": 30,
  "style": "dynamic",
  "description": "Showcase new vehicle inventory with pricing and features"
}
```

## API Integration

### Gemini 3.0 (Chat Interface)
```python
from chat.interface import DealershipChatInterface

chat = DealershipChatInterface()
response = chat.process_message("I need a sales video")
```

### Veo (Video Generation)
```python
from video.veo_client import VeoVideoGenerator

generator = VeoVideoGenerator()
video = generator.generate_from_prompt(
    prompt="Professional SUV showcase...",
    duration=30,
    style="professional"
)
```

## Advanced Features

### Custom Templates
Create your own templates by adding to `templates/custom_templates.json`

### Brand Guidelines
Configure brand colors, logos, and styles in `config/brand_settings.json`

### Inventory Integration
Connect to MarketCheck or other inventory systems for dynamic pricing

## Troubleshooting

### Common Issues

**API Key Errors**:
- Verify API keys are correctly set in `.env`
- Check API quota and billing status

**Video Generation Timeout**:
- Reduce video duration
- Lower quality settings
- Check network connection

**Template Not Found**:
- Verify template ID exists
- Check templates directory

## Best Practices

1. **Be Specific**: Provide detailed descriptions for better video quality
2. **Use Templates**: Start with templates for consistent results
3. **Iterate**: Refine videos through conversation
4. **Test**: Preview videos before final export
5. **Brand Consistency**: Use brand guidelines for all videos

## Support & Resources

- **Documentation**: See `DEALERSHIP_VIDEO_APP_PLAN.md` for architecture details
- **Templates**: Browse `templates/` directory for examples
- **Examples**: Check `examples/` for sample workflows

## License

This project is part of the codex-playground repository.

## Contributing

Contributions are welcome! Please follow the existing code structure and add tests for new features.
