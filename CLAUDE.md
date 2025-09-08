# POC Wireframe - Sophisticated DSL Solution

## Project Overview
**poc-wireframe** generates sophisticated wireframes for new application . With similar product screenshots as example .

## Business Goal
Transform tedious manual wireframe creation into automated workflow:
1. Analyze, understand screenshots of existing example applications
2. Generate clean DSL wireframe descriptions

## Solution Architecture

### Input
- `input/project-analyze/<feature-name>/` - Contains screenshots for one application feature
- Multiple screenshots showing different screens/states of the same feature

### Output
- `output/project-analyze/<feature-name>/` - DSL files , for complex screen split to multiple wireframes

## The generated wireframes

- Need to be details , more details than example
- Need to be specific about feature: main sections cards, form title, form fields, action button, action menu, table columns etc
- Need to be good layout, good UX, good usability
- DO NOT need to be specific about spacing, color, font-size, etc
- DO NOT need to be specific about icon, image, etc
