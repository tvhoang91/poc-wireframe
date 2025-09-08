#!/usr/bin/env python3
"""
Sophisticated Wireframe Generator - DSL Output

This script analyzes screenshots from input/screenshots/ and generates
sophisticated wireframe specifications in DSL format.

Focus: Clean DSL output, sophisticated AI analysis, production-ready wireframes.
"""

import os
import json
from pathlib import Path
from datetime import datetime
import base64
from openai import OpenAI

class WireframeDSLGenerator:
    def __init__(self):
        self.client = OpenAI()
        self.input_dir = Path("input/project-analyze/review-management")
        self.output_dir = Path("output/project-analyze/review-management")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def analyze_screenshots_to_dsl(self):
        """Main method: analyze all screenshots and generate DSL wireframes"""
        print("🚀 Starting Sophisticated Wireframe Analysis...")
        
        screenshots = self._find_screenshots()
        if not screenshots:
            print("❌ No screenshots found in input/project-analyze/review-management/")
            return
        
        print(f"📸 Found {len(screenshots)} screenshots to analyze")
        
        # Analyze each screenshot with sophisticated prompting
        wireframes = []
        for i, screenshot_path in enumerate(screenshots):
            print(f"🔍 Analyzing screenshot {i+1}/{len(screenshots)}: {screenshot_path.name}")
            dsl_wireframe = self._analyze_single_screenshot(screenshot_path)
            if dsl_wireframe:
                wireframes.append({
                    'filename': screenshot_path.name,
                    'dsl': dsl_wireframe
                })
        
        # Generate combined wireframe specification
        self._generate_combined_wireframe(wireframes)
        
        print("✅ Sophisticated wireframe analysis complete!")
    
    def _find_screenshots(self):
        """Find all screenshot files in input directory"""
        if not self.input_dir.exists():
            return []
        
        extensions = {'.png', '.jpg', '.jpeg', '.webp'}
        screenshots = []
        
        for file_path in self.input_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in extensions:
                screenshots.append(file_path)
        
        return sorted(screenshots)
    
    def _analyze_single_screenshot(self, screenshot_path):
        """Analyze single screenshot with sophisticated AI prompting"""
        
        # Encode image for OpenAI API
        with open(screenshot_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        sophisticated_prompt = """
You are a sophisticated wireframe analysis expert specializing in DSL generation.

TASK: Analyze this UI screenshot and generate a clean DSL wireframe specification.

DSL SYNTAX:
SCREEN ScreenName:
  SECTION SectionName (layout-properties):
    COMPONENT ComponentName (properties) [-> trigger: action]

ANALYSIS FOCUS:
1. Identify the screen type and primary purpose
2. Break down into logical sections (HEADER, SIDEBAR, MAIN, FOOTER)
3. Map UI components to semantic types
4. Capture interactive elements and their behaviors
5. Note layout patterns (grid, flex, positioning)

COMPONENT VOCABULARY:
- Navigation, Logo, SearchBar, UserMenu, Avatar
- Button, Input, Textarea, Select, Checkbox, Radio
- Card, Modal, Dropdown, Tooltip, Badge
- DataTable, Chart, StatsGrid, Timeline
- Sidebar, Breadcrumbs, Tabs, Accordion

LAYOUT PROPERTIES:
- Positioning: (left, right, center, full-width)
- Grid: (cols: 1-12, span: 2-12)
- Spacing: (gap: small/medium/large)
- Responsive: (mobile: stack, desktop: grid)

INTERACTION SYNTAX:
-> click: action
-> hover: show_tooltip
-> focus: highlight
-> submit: loading_state

EXAMPLE OUTPUT:
SCREEN Dashboard:
  HEADER (full-width, sticky):
    Logo (left)
    SearchBar (center, expandable)
    UserMenu (right) -> click: dropdown
  
  MAIN (grid-12, gap: large):
    StatsCards (cols: 1-9, responsive: stack-mobile)
    QuickActions (cols: 10-12)
    
    DataTable (cols: 1-8, sortable):
      Columns: Name, Status, Date, Actions
      Actions -> click: edit_modal
    
    ActivityFeed (cols: 9-12, scrollable)

Generate a sophisticated DSL wireframe for this screenshot:
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": sophisticated_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.1
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ Error analyzing {screenshot_path.name}: {e}")
            return None
    
    def _generate_combined_wireframe(self, wireframes):
        """Generate combined wireframe specification file"""
        
        # Save individual DSL files
        for wireframe in wireframes:
            filename = wireframe['filename'].replace('.', '_') + '.dsl'
            dsl_path = self.output_dir / filename
            
            with open(dsl_path, 'w') as f:
                f.write(f"// Generated from: {wireframe['filename']}\n")
                f.write(f"// Timestamp: {datetime.now().isoformat()}\n\n")
                f.write(wireframe['dsl'])
            
            print(f"📄 Generated: {dsl_path}")
        
        # Generate combined application wireframe
        combined_dsl_path = self.output_dir / "application_wireframe.dsl"
        
        with open(combined_dsl_path, 'w') as f:
            f.write(f"// Sophisticated Wireframe Specification\n")
            f.write(f"// Generated: {datetime.now().isoformat()}\n")
            f.write(f"// Source: {len(wireframes)} screenshots analyzed\n\n")
            
            for i, wireframe in enumerate(wireframes):
                f.write(f"// === SCREEN {i+1}: {wireframe['filename']} ===\n\n")
                f.write(wireframe['dsl'])
                f.write("\n\n")
        
        print(f"📋 Combined specification: {combined_dsl_path}")
        
        # Generate analysis summary
        self._generate_analysis_summary(wireframes)
    
    def _generate_analysis_summary(self, wireframes):
        """Generate analysis summary for review"""
        summary_path = self.output_dir / "analysis_summary.md"
        
        with open(summary_path, 'w') as f:
            f.write("# Wireframe Analysis Summary\n\n")
            f.write(f"**Generated**: {datetime.now().isoformat()}\n")
            f.write(f"**Screenshots Analyzed**: {len(wireframes)}\n\n")
            
            f.write("## Files Generated\n\n")
            for wireframe in wireframes:
                filename = wireframe['filename'].replace('.', '_') + '.dsl'
                f.write(f"- `{filename}` - Individual screen wireframe\n")
            
            f.write("- `application_wireframe.dsl` - Combined specification\n")
            f.write("- `analysis_summary.md` - This summary\n\n")
            
            f.write("## Next Steps\n\n")
            f.write("1. Review generated DSL wireframes\n")
            f.write("2. Refine component specifications\n")
            f.write("3. Generate HTML/Tailwind prototypes\n")
            f.write("4. Create design system documentation\n")
        
        print(f"📊 Analysis summary: {summary_path}")

def main():
    """Main entry point for sophisticated wireframe generation"""
    print("🎯 Sophisticated Wireframe Generator - DSL Solution")
    print("=" * 50)
    
    generator = WireframeDSLGenerator()
    generator.analyze_screenshots_to_dsl()

if __name__ == "__main__":
    main()