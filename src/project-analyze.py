#!/usr/bin/env python3
"""
Enhanced project-analyze.py - Generates sophisticated wireframes for new applications
using similar product screenshots as examples and inspiration.

This script analyzes example screenshots to extract UI patterns and design principles,
then generates detailed DSL wireframes for new applications with enhanced functionality.
"""

import os
import sys
import json
import base64
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# Third-party imports
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class AnalysisConfig:
    """Configuration for wireframe analysis and generation."""
    input_dir: Path
    output_dir: Path
    feature_name: str
    ai_provider: str = "openai"  # openai, anthropic
    model: str = "gpt-4o"  # gpt-4o, claude-3-5-sonnet-20241022
    max_tokens: int = 4000
    temperature: float = 0.3
    
class PromptEngineering:
    """Advanced prompt engineering system for generating detailed wireframes."""
    
    @staticmethod
    def get_pattern_analysis_prompt() -> str:
        """Stage 1: Extract UI patterns and design principles from screenshots."""
        return """
You are a UX/UI expert analyzing screenshots of existing applications to extract design patterns and principles. 

Analyze the provided screenshot and identify:

1. **Layout Structure:**
   - Main navigation patterns (top nav, sidebar, breadcrumbs)
   - Content organization (grid, list, cards, tables)
   - Information hierarchy and visual grouping

2. **Component Patterns:**
   - Form elements (input fields, dropdowns, buttons, validation)
   - Data display (tables, cards, lists, statistics widgets)
   - Interactive elements (filters, search, bulk actions)
   - Navigation elements (tabs, pagination, sorting)

3. **Functional Patterns:**
   - User workflows evident in the interface
   - Action patterns (CRUD operations, bulk operations)
   - Status indicators and feedback mechanisms
   - User management and permission systems

4. **Design Principles:**
   - Information density and spacing approach
   - Visual hierarchy techniques
   - User experience patterns
   - Accessibility considerations

Provide a detailed analysis focusing on extractable patterns that could inspire new application designs.
Return your analysis in structured JSON format with clear categories.
"""

    @staticmethod
    def get_wireframe_generation_prompt(patterns_analysis: str, feature_context: str) -> str:
        """Stage 2: Generate sophisticated wireframes based on extracted patterns."""
        return f"""
You are a senior UX designer tasked with creating sophisticated wireframes for a NEW APPLICATION feature.

**Context:** You are designing a {feature_context} feature for a new application.

**Design Patterns Analysis:**
{patterns_analysis}

**Task:** Create detailed wireframes that are INSPIRED by but SIGNIFICANTLY ENHANCED compared to the analyzed patterns.

**Requirements for the wireframes:**
1. **More sophisticated than the examples** - Add advanced functionality
2. **Detailed component specifications:**
   - Navigation: exact menu items, breadcrumbs, user controls
   - Forms: specific field types, validation rules, helper text
   - Tables: exact column definitions, sorting, filtering, actions
   - Cards: precise content structure, metadata, action buttons
   - Search/Filter: advanced filtering options, search suggestions
   - Bulk operations: comprehensive action sets

3. **Enhanced UX features:**
   - Advanced search and filtering capabilities
   - Smart defaults and auto-completion
   - Contextual help and tooltips
   - Progressive disclosure for complex features
   - Responsive design considerations
   - Error handling and validation feedback

4. **Specific functional details:**
   - User permissions and role-based access
   - Data validation and business rules
   - Integration touchpoints with other systems
   - Analytics and reporting features
   - Export/import capabilities

**Output Format:** Generate wireframes in detailed DSL format with specific sections:
- Header/Navigation
- Main Content Areas
- Sidebar/Filters (if applicable)
- Forms and Input Elements
- Data Display Components
- Action Areas
- Footer/Status

Make the wireframes significantly more detailed and sophisticated than typical examples. Focus on functionality and user experience, not visual styling.
"""

    @staticmethod
    def get_refinement_prompt(initial_wireframe: str) -> str:
        """Stage 3: Refine and enhance wireframe details."""
        return f"""
You are a UX expert reviewing and enhancing wireframe specifications.

**Current Wireframe:**
{initial_wireframe}

**Enhancement Task:**
Review the wireframe and add missing sophisticated details:

1. **Missing Components:** Identify and add any missing standard components
2. **Enhanced Interactions:** Add advanced user interaction patterns
3. **Data Relationships:** Specify how different data elements connect
4. **Edge Cases:** Address error states, empty states, loading states
5. **Advanced Features:** Add power-user features and shortcuts
6. **Integration Points:** Specify API integrations and data sources
7. **Performance Considerations:** Add pagination, lazy loading, caching

**Focus Areas:**
- Make every interactive element specific (exact button text, field labels)
- Add comprehensive validation and error handling
- Include sophisticated filtering and search capabilities
- Specify exact data structures and relationships
- Add contextual help and user guidance features

Return the enhanced wireframe with significantly more detail and sophistication.
"""

class ScreenshotAnalyzer:
    """Handles screenshot processing and analysis."""
    
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.client = self._initialize_ai_client()
    
    def _initialize_ai_client(self):
        """Initialize the appropriate AI client."""
        if self.config.ai_provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            return openai.OpenAI(api_key=api_key)
        else:
            raise ValueError(f"Unsupported AI provider: {self.config.ai_provider}")
    
    def encode_image(self, image_path: Path) -> str:
        """Encode image file to base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def analyze_screenshot_patterns(self, image_path: Path) -> Dict[str, Any]:
        """Analyze a single screenshot to extract UI patterns."""
        base64_image = self.encode_image(image_path)
        
        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": PromptEngineering.get_pattern_analysis_prompt()
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature
        )
        
        try:
            # Try to parse as JSON, fallback to plain text
            content = response.choices[0].message.content
            return {"analysis": content, "image_path": str(image_path)}
        except Exception as e:
            return {"analysis": response.choices[0].message.content, "error": str(e)}

class WireframeGenerator:
    """Generates sophisticated wireframes based on pattern analysis."""
    
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.client = self._initialize_ai_client()
    
    def _initialize_ai_client(self):
        """Initialize the appropriate AI client."""
        if self.config.ai_provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            return openai.OpenAI(api_key=api_key)
        else:
            raise ValueError(f"Unsupported AI provider: {self.config.ai_provider}")
    
    def generate_wireframe(self, patterns_analyses: List[Dict], feature_context: str) -> str:
        """Generate sophisticated wireframe based on pattern analyses."""
        
        # Combine all pattern analyses
        combined_patterns = "\n\n".join([
            f"**Screenshot Analysis {i+1}:**\n{analysis['analysis']}" 
            for i, analysis in enumerate(patterns_analyses)
        ])
        
        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[
                {
                    "role": "user",
                    "content": PromptEngineering.get_wireframe_generation_prompt(
                        combined_patterns, 
                        feature_context
                    )
                }
            ],
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature
        )
        
        return response.choices[0].message.content
    
    def refine_wireframe(self, initial_wireframe: str) -> str:
        """Refine and enhance wireframe with additional details."""
        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[
                {
                    "role": "user",
                    "content": PromptEngineering.get_refinement_prompt(initial_wireframe)
                }
            ],
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature
        )
        
        return response.choices[0].message.content

class DSLWireframeProcessor:
    """Processes and formats wireframes into structured DSL format."""
    
    def __init__(self, config: AnalysisConfig):
        self.config = config
    
    def format_wireframe_dsl(self, wireframe_content: str, metadata: Dict) -> str:
        """Format wireframe into consistent DSL structure."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        dsl_header = f"""# Wireframe DSL - {self.config.feature_name}
# Generated on: {timestamp}
# Feature Context: {metadata.get('feature_context', 'N/A')}
# Analysis Method: Multi-stage AI pattern analysis
# Screenshots Analyzed: {len(metadata.get('source_images', []))}

---

"""
        return dsl_header + wireframe_content
    
    def save_wireframe(self, wireframe_content: str, metadata: Dict, filename: Optional[str] = None) -> Path:
        """Save wireframe to output directory."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.config.feature_name}_wireframe_{timestamp}.md"
        
        output_path = self.config.output_dir / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        formatted_content = self.format_wireframe_dsl(wireframe_content, metadata)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        
        return output_path

class ProjectAnalyzer:
    """Main orchestrator for the project analysis and wireframe generation."""
    
    def __init__(self, feature_name: str, ai_provider: str = "openai", model: str = "gpt-4o"):
        self.feature_name = feature_name
        self.input_dir = Path(f"input/project-analyze/{feature_name}")
        self.output_dir = Path(f"output/project-analyze/{feature_name}")
        
        self.config = AnalysisConfig(
            input_dir=self.input_dir,
            output_dir=self.output_dir,
            feature_name=feature_name,
            ai_provider=ai_provider,
            model=model
        )
        
        self.screenshot_analyzer = ScreenshotAnalyzer(self.config)
        self.wireframe_generator = WireframeGenerator(self.config)
        self.dsl_processor = DSLWireframeProcessor(self.config)
    
    def find_screenshots(self) -> List[Path]:
        """Find all screenshot files in the input directory."""
        screenshot_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
        screenshots = []
        
        if not self.input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {self.input_dir}")
        
        for file_path in self.input_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in screenshot_extensions:
                screenshots.append(file_path)
        
        return sorted(screenshots)
    
    def analyze_feature(self) -> Dict[str, Any]:
        """Complete analysis pipeline for a feature."""
        print(f"Analyzing feature: {self.feature_name}")
        
        # Step 1: Find screenshots
        screenshots = self.find_screenshots()
        print(f"Found {len(screenshots)} screenshots")
        
        if not screenshots:
            raise ValueError(f"No screenshots found in {self.input_dir}")
        
        # Step 2: Analyze each screenshot for patterns
        print("Analyzing UI patterns in screenshots...")
        pattern_analyses = []
        for i, screenshot in enumerate(screenshots):
            print(f"   Analyzing {screenshot.name}...")
            analysis = self.screenshot_analyzer.analyze_screenshot_patterns(screenshot)
            pattern_analyses.append(analysis)
        
        # Step 3: Generate initial wireframe
        print("Generating sophisticated wireframe...")
        feature_context = self.feature_name.replace('-', ' ').replace('_', ' ').title()
        initial_wireframe = self.wireframe_generator.generate_wireframe(
            pattern_analyses, 
            feature_context
        )
        
        # Step 4: Refine wireframe
        print("Refining wireframe with enhanced details...")
        refined_wireframe = self.wireframe_generator.refine_wireframe(initial_wireframe)
        
        # Step 5: Save results
        metadata = {
            'feature_context': feature_context,
            'source_images': [str(p) for p in screenshots],
            'analysis_timestamp': datetime.now().isoformat(),
            'ai_model': self.config.model
        }
        
        output_path = self.dsl_processor.save_wireframe(refined_wireframe, metadata)
        print(f"Wireframe saved to: {output_path}")
        
        # Save analysis data for debugging
        debug_path = self.output_dir / f"{self.feature_name}_analysis_debug.json"
        debug_data = {
            'pattern_analyses': pattern_analyses,
            'initial_wireframe': initial_wireframe,
            'metadata': metadata
        }
        
        with open(debug_path, 'w', encoding='utf-8') as f:
            json.dump(debug_data, f, indent=2, ensure_ascii=False)
        
        print(f"Debug data saved to: {debug_path}")
        
        return {
            'wireframe_path': output_path,
            'debug_path': debug_path,
            'screenshots_analyzed': len(screenshots),
            'metadata': metadata
        }

def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python src/project-analyze.py <feature-name> [ai_provider] [model]")
        print("Example: python src/project-analyze.py review-management openai gpt-4o")
        print("\nAvailable features:")
        
        input_base = Path("input/project-analyze")
        if input_base.exists():
            for feature_dir in input_base.iterdir():
                if feature_dir.is_dir():
                    screenshots = list(feature_dir.glob("*.png")) + list(feature_dir.glob("*.jpg"))
                    print(f"  - {feature_dir.name} ({len(screenshots)} screenshots)")
        
        return 1
    
    feature_name = sys.argv[1]
    ai_provider = sys.argv[2] if len(sys.argv) > 2 else "openai"
    model = sys.argv[3] if len(sys.argv) > 3 else "gpt-4o"
    
    try:
        analyzer = ProjectAnalyzer(feature_name, ai_provider, model)
        result = analyzer.analyze_feature()
        
        print("\nAnalysis completed successfully!")
        print(f"Wireframe: {result['wireframe_path']}")
        print(f"Screenshots analyzed: {result['screenshots_analyzed']}")
        print(f"AI Model: {result['metadata']['ai_model']}")
        
        return 0
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())