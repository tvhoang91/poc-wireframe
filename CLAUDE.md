# POC Wireframe - Sophisticated DSL Solution

## Project Overview
**poc-wireframe** generates sophisticated wireframes from application screenshots using AI analysis and a custom Domain Specific Language (DSL) for clean, readable output.

## Business Goal
Transform tedious manual wireframe creation into automated workflow:
1. Analyze screenshots of existing applications
2. Extract UI components, layouts, and interactions  
3. Generate clean DSL wireframe descriptions
4. Output production-ready wireframe specifications

## Solution Architecture

### Input
- `input/project-analyze/review-management/` - Contains screenshots for one application feature
- Multiple screenshots showing different screens/states of the same feature

### Output
- `output/project-analyze/review-management/` - DSL files , for complex screen split to multiple wireframes

### Processing Pipeline
1. **Screenshot Analysis**: AI models analyze each screenshot to identify:
   - UI components (buttons, forms, navigation, cards)
   - Layout structure (grids, sections, positioning)
   - Interactive elements and their behaviors
   - Content hierarchy and organization

2. **DSL Generation**: Convert analysis into clean DSL format:
   ```
   SCREEN Dashboard:
     HEADER (full-width):
       Logo (left)
       Navigation: Dashboard, Analytics, Settings
       UserMenu (right) -> click: dropdown
     
     MAIN (grid-12):
       StatsCards (cols: 1-8)
       Sidebar (cols: 9-12)
   ```

3. **Output**: Save wireframe specifications as `.dsl` files

### Key Features
- **DSL-First**: Clean, readable wireframe specifications
- **AI-Powered**: Sophisticated screenshot analysis
- **Component-Focused**: Identifies reusable UI patterns
- **Interaction-Aware**: Captures UI states and behaviors
- **Production-Ready**: Generates specifications suitable for development handoff

## DSL Advantages
- **90% more token-efficient** than JSON for AI generation
- **Human-readable** format for easy review and editing
- **Error-tolerant** parsing with graceful degradation
- **Natural language proximity** matches designer thinking
- **Easy iteration** and targeted modifications

## Implementation Focus
- Ignore existing `extract/` folder solutions
- Implement project-analyze.py , and project-analyze folder for more python code split module files
- Focus entirely on DSL output generation
- Sophisticated AI prompting for detailed analysis
- Clean, production-ready wireframe specifications

## Development Commands
```bash
# Run sophisticated wireframe analysis
python src/project-analyze.py

# Output: DSL files in output/ directory
```

## File Structure
```
poc-wireframe/
├── input/screenshots/     # Input screenshots for analysis
├── output/               # Generated DSL wireframe files
├── src/
│   └── project-analyze.py # Main sophisticated implementation
└── CLAUDE.md            # This documentation
```