import fs from "fs";
import path from "path";
import { analyzeUIFromImage } from "./extract/analyze-image";
import { findScreenshots } from "./extract/find-screenshots";

async function main() {
  console.log("Begin Extraction!");

  const screenshotsDir = path.join(process.cwd(), "input", "screenshots");

  try {
    const fileInfo = findScreenshots(screenshotsDir);

    console.log("Files in input/screenshots:", {
      firstImage: fileInfo.length > 0 ? fileInfo[0] : "none",
      imageCount: fileInfo.length,
    });

    if (fileInfo.length > 0) {
      console.log("\n--- Analyzing first image with Florence-2-large ---");
      const firstImage = fileInfo[0];
      console.log(`Analyzing: ${firstImage.name}`);

      // Single comprehensive UI analysis call
      const analysis = await analyzeUIFromImage(firstImage.path);
      console.log("Comprehensive UI Analysis:", analysis);

      // Save analysis to output file
      const outputDir = path.join(process.cwd(), "output");
      if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
      }

      const outputFile = path.join(outputDir, "analyze-image.text");
      const analysisContent = `Image Analysis for: ${
        firstImage.name
      }\nAnalyzed at: ${new Date().toISOString()}\n\n${analysis}`;

      fs.writeFileSync(outputFile, analysisContent);
      console.log(`\nAnalysis saved to: ${outputFile}`);
    }
  } catch (error) {
    console.error("Error reading screenshots directory:", error);
  }
}

main().catch(console.error);

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
 * Then
 * 3. group images by screen
 * For each screen:
 * 4. summarize the extracted data from all images of a screen; UI layout, short description
 * 5. save the extracted data in output/screen/[screen_name].json
 */
