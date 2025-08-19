console.log('Begin Extraction!');

/**
 * This script will extract the UI content from the screenshots of application.
 * The extracted content will be saved in output/extraction.json.
 * 
 * The extracted content need the following information:
 * - List of screens, with short description, UI layout
 * - List of features, with short description, MVP flag, which screen it belongs to
 * 
 * The extraction process will be as follows:
 * 1. Read image files in input/screenshots
 * For each image:
 * 2.1. call image_to_text to tell the image content in term of application screen, layout, components
 * 2.2. group images by screen
 * For each screen:
 * 3.1. extract UI layout from each image
 * 3.2. extract short description from each image
 * Then
 * 4. summarize the extracted data from all images of a screen
 * 5. save the extracted data in output/[screen_name]/screen.json
 */
