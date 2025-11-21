# Car Dealership Video Generation App - Technical Planning Document

## Executive Summary

This document outlines the architecture and implementation plan for an AI-powered custom video generation application specifically designed for car dealerships, to be executed in Google AI Studio with Gemini 3.0 and Veo.

## Application Overview

### Purpose
Enable car dealerships to create professional, customized video content for:
- **Sales advertising**: Showcase inventory, promotions, special offers
- **Service advertising**: Highlight service capabilities, maintenance packages, seasonal campaigns

### Target Platform
- **Execution Environment**: Google AI Studio
- **AI Models**: 
  - Gemini 3.0 (chat interface, content understanding, workflow orchestration)
  - Veo (video generation and customization)

## Core Features

### 1. Intelligent Chat Interface
**Purpose**: Guide users through video creation process with context-aware assistance

**Capabilities**:
- Initial intent classification (sales vs. service)
- Natural conversation flow for gathering requirements
- Context retention throughout session
- Proactive suggestions based on dealership best practices

**Key Questions to Ask Users**:
- "Are you creating content for sales or service?"
- "What's the main message you want to convey?"
- "What's your target audience?" (first-time buyers, luxury, family, etc.)
- "Do you have specific vehicles/services to highlight?"
- "What's the tone?" (professional, friendly, exciting, trustworthy)
- "Any specific call-to-action?" (visit showroom, schedule test drive, book service)

### 2. Dual Video Creation Workflows

#### A. Prompt-Based Generation (From Scratch)
**Process**:
1. User describes desired video through chat
2. AI constructs comprehensive video generation prompt
3. Veo generates video based on prompt
4. User can refine through conversational feedback

**Prompt Engineering Considerations**:
- Scene composition (showroom, outdoor, service bay)
- Vehicle highlighting (close-ups, 360 views, features)
- Text overlays (pricing, contact info, offers)
- Brand consistency (colors, logos, style)
- Duration and pacing
- Music/audio mood

#### B. Upload & Customize Workflow
**Process**:
1. User uploads reference video
2. AI analyzes video content and style
3. User specifies desired changes via chat
4. AI generates modified version using Veo
5. Iterative refinement through conversation

**Customization Options**:
- Replace vehicles/backgrounds
- Update text/pricing overlays
- Modify color grading/style
- Adjust pacing/duration
- Add/remove segments
- Change music/voiceover

### 3. Dealership-Specific Intelligence

**Sales-Focused Templates**:
- New inventory showcase
- Special financing offers
- Trade-in promotions
- Seasonal sales events
- Model comparisons
- Virtual test drive experiences

**Service-Focused Templates**:
- Oil change specials
- Tire rotation packages
- Seasonal maintenance (winter prep, summer check)
- Warranty service highlights
- Express service convenience
- Customer testimonials

**Smart Data Integration** (Optional Enhancement):
- Pull from MarketCheck inventory data
- Dynamic pricing displays
- Competitive positioning
- Availability status

## Technical Architecture

### Application Structure

```
dealership_video_app/
├── app.py                          # Main application entry point
├── config/
│   ├── gemini_config.py           # Gemini 3.0 configuration
│   ├── veo_config.py              # Veo API configuration
│   └── templates.py               # Video templates & presets
├── chat/
│   ├── interface.py               # Chat UI and session management
│   ├── intent_classifier.py      # Sales vs Service detection
│   ├── conversation_flow.py      # Dialog management
│   └── context_manager.py        # Session context handling
├── video/
│   ├── prompt_builder.py          # Veo prompt construction
│   ├── veo_client.py              # Veo API integration
│   ├── video_analyzer.py          # Upload video analysis
│   └── customizer.py              # Video modification logic
├── templates/
│   ├── sales_templates.json       # Sales video templates
│   └── service_templates.json     # Service video templates
├── utils/
│   ├── validators.py              # Input validation
│   └── helpers.py                 # Utility functions
└── README.md                      # Documentation
```

### Key Components

#### 1. Chat Interface Module
```python
class DealershipChatInterface:
    """Main chat interface for video creation workflow"""
    
    def __init__(self, gemini_client):
        self.gemini = gemini_client
        self.context = ConversationContext()
        self.intent_classifier = IntentClassifier()
    
    def start_conversation(self):
        """Initialize conversation and determine intent"""
        pass
    
    def process_message(self, user_input):
        """Handle user messages and guide workflow"""
        pass
    
    def generate_video_prompt(self):
        """Create final Veo prompt from conversation"""
        pass
```

#### 2. Video Generation Module
```python
class VeoVideoGenerator:
    """Interface to Veo video generation API"""
    
    def generate_from_prompt(self, prompt, style_params):
        """Generate new video from text prompt"""
        pass
    
    def customize_existing(self, source_video, modifications):
        """Modify uploaded video based on requirements"""
        pass
    
    def analyze_video(self, video_file):
        """Extract features from uploaded video"""
        pass
```

#### 3. Template Management
```python
class TemplateManager:
    """Manage video templates and presets"""
    
    def get_sales_templates(self):
        """Return sales-focused templates"""
        pass
    
    def get_service_templates(self):
        """Return service-focused templates"""
        pass
    
    def apply_template(self, template_id, custom_params):
        """Apply template with customizations"""
        pass
```

## Google AI Studio Integration

### Implementation Approach

**Option 1: Python Notebook**
- Use Google Colab-style notebook interface
- Each cell handles different workflow stages
- Interactive widgets for chat interface
- Direct integration with Gemini and Veo APIs

**Option 2: Streamlit App (Recommended)**
- More polished UI/UX
- Better chat interface experience
- Easier video preview and management
- Can be hosted in AI Studio environment

**Option 3: Pure Python Script**
- Command-line based interaction
- Simpler but less user-friendly
- Good for automation/batch processing

### API Authentication
```python
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key='YOUR_API_KEY')

# Initialize models
gemini_model = genai.GenerativeModel('gemini-3.0-pro')
veo_model = genai.VideoModel('veo-001')  # Hypothetical API
```

## Prompt Engineering Strategy

### Structured Prompt Template for Veo

```
[VIDEO TYPE]: {sales|service}
[DURATION]: {15s|30s|60s}
[STYLE]: {professional|dynamic|friendly|luxury}

SCENE DESCRIPTION:
{detailed scene composition}

VEHICLE/SERVICE FOCUS:
{specific elements to highlight}

VISUAL ELEMENTS:
- Camera movements: {pan, zoom, static, etc.}
- Lighting: {bright, dramatic, natural, etc.}
- Environment: {showroom, outdoor, service bay, etc.}

TEXT OVERLAYS:
- Headline: {main message}
- Details: {pricing, features, benefits}
- Call-to-action: {contact info, action prompt}

BRAND GUIDELINES:
- Colors: {brand colors}
- Logo placement: {position and timing}
- Typography: {font style}

MOOD/TONE:
{emotional direction and pacing}
```

## Workflow Examples

### Example 1: Sales Video Creation Flow
```
User: "I need a video for our new SUV sale"
AI: "Great! I'll help you create a sales video. What type of SUVs are you featuring?"
User: "2024 Honda CR-V, we have 15 in stock"
AI: "Perfect! What's your main offer or message?"
User: "0% financing for 60 months"
AI: "Excellent. What tone would you like - professional, exciting, or family-friendly?"
User: "Family-friendly"
AI: "Got it. Let me create a video showing the CR-V in family scenarios with your financing offer..."
[Generates video]
AI: "Here's your video. Would you like to adjust anything?"
```

### Example 2: Service Video Customization Flow
```
User: "I have a service video I want to update" [uploads video]
AI: "I'll analyze this video... It's a tire service promotion. What would you like to change?"
User: "Update the pricing and change it to winter tire package"
AI: "Understood. What's the new pricing?"
User: "$399 for full winter tire package with installation"
AI: "Should I update any other visual elements for winter theme?"
User: "Yes, make it look more winter-appropriate"
AI: "I'll modify the video with winter imagery and updated pricing..."
[Generates modified video]
```

## Enhanced Features (Future Considerations)

### 1. Multi-Video Campaigns
- Create series of related videos
- Consistent branding across videos
- A/B testing variations

### 2. Performance Analytics Integration
- Track video engagement
- Optimize based on performance
- Suggest improvements

### 3. Inventory Integration
- Real-time pricing from MarketCheck
- Automated video updates when inventory changes
- Dynamic content based on availability

### 4. Compliance Checking
- Ensure legal disclaimers
- Validate pricing accuracy
- Check brand guideline adherence

### 5. Multi-Language Support
- Generate videos in multiple languages
- Market-specific customizations
- Cultural considerations

## Technical Recommendations

### API Configuration
1. **Authentication**: Use service account or API keys
2. **Rate Limiting**: Implement request throttling
3. **Error Handling**: Robust retry logic for API failures
4. **Caching**: Cache template responses and common requests

### Performance Optimization
1. **Async Processing**: Use async/await for API calls
2. **Progress Indicators**: Show generation status
3. **Streaming Responses**: Stream chat responses for better UX
4. **Preview Generation**: Quick low-res previews before full render

### Security Considerations
1. **Input Validation**: Sanitize all user inputs
2. **Content Filtering**: Check for inappropriate content
3. **API Key Protection**: Secure credential management
4. **Usage Monitoring**: Track and limit API usage

## Implementation Priority

### Phase 1: MVP (Minimum Viable Product)
- [x] Chat interface with Gemini integration
- [x] Basic prompt-based video generation
- [x] Sales vs. Service intent detection
- [x] Simple template system
- [x] Basic Veo integration

### Phase 2: Enhanced Features
- [ ] Video upload and analysis
- [ ] Advanced customization options
- [ ] Template library expansion
- [ ] Better error handling and validation

### Phase 3: Advanced Capabilities
- [ ] Inventory data integration
- [ ] Performance analytics
- [ ] Multi-video campaigns
- [ ] Advanced brand customization

## Optimal Prompt for Code Generation

Based on this analysis, here's the optimal prompt for generating the foundational code:

---

**OPTIMAL GENERATION PROMPT:**

```
Create a Python application framework for a car dealership video generation tool to run in Google AI Studio. 

REQUIREMENTS:
1. Use Gemini 3.0 for an intelligent chat interface that:
   - Asks if the user is creating sales or service advertising
   - Guides users through video creation via natural conversation
   - Maintains context throughout the session
   - Builds comprehensive video generation prompts

2. Integrate with Veo for video generation supporting:
   - Text-to-video generation from detailed prompts
   - Video upload and customization workflow
   - Iterative refinement based on user feedback

3. Include dealership-specific features:
   - Sales templates (inventory showcase, promotions, financing)
   - Service templates (maintenance, seasonal offers, packages)
   - Professional video prompt engineering
   - Brand consistency options

4. Structure:
   - Main app.py with Streamlit interface (or notebook cells)
   - Modular architecture (chat/, video/, templates/ folders)
   - Configuration management for API keys
   - Template system for common video types

5. Key workflows:
   - Prompt-based: User describes → AI creates prompt → Veo generates
   - Upload-based: User uploads video → Describes changes → AI customizes

6. Include comprehensive documentation, example usage, and configuration guide.

Target: Production-ready code that can be directly used in Google AI Studio with minimal setup.
```

---

## Conclusion

This planning document provides a comprehensive blueprint for building a specialized video generation app for car dealerships. The architecture balances sophistication with practical implementation, focusing on user experience through intelligent conversation and powerful video generation capabilities.

**Next Steps**:
1. Review and approve this plan
2. Generate foundational code using the optimal prompt above
3. Implement core modules (chat, video, templates)
4. Test in Google AI Studio environment
5. Iterate based on feedback

**Success Metrics**:
- Intuitive chat interface requiring minimal user training
- High-quality video output matching dealership needs
- Fast iteration cycles for video refinement
- Scalable architecture for future enhancements
