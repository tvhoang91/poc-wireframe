import { InferenceClient } from "@huggingface/inference";
import { pipeline } from "@huggingface/transformers";
import fs from "fs";
import dotenv from "dotenv";

dotenv.config();
if (!process.env.HUGGINGFACE_API_TOKEN) {
  throw new Error("HUGGINGFACE_API_TOKEN not found in environment variables");
}

export async function analyzeImageWithFlorence(
  imagePath: string,
  task: string = "<DETAILED_CAPTION>"
): Promise<string> {
  try {
    const hf = new InferenceClient(process.env.HUGGINGFACE_API_TOKEN);
    const imageBuffer = fs.readFileSync(imagePath);
    const imageBlob = new Blob([imageBuffer], { type: "image/png" });

    const pipe = pipeline("image-text-to-text", {
      model: "Qwen/Qwen2.5-VL-7B-Instruct",
    });

    const result = await hf.imageToText({
      inputs: imageBlob,
      model: "Qwen/Qwen2.5-VL-7B-Instruct",
      parameters: {
        task_prompt: task,
      },
    });

    return JSON.stringify(result, null, 2);
  } catch (error) {
    console.error("Error analyzing image:", error);
    throw error;
  }
}

export async function analyzeUIFromImage(imagePath: string): Promise<string> {
  const comprehensivePrompt = `Analyze this application UI screenshot and provide:
1. Overall screen description and purpose
2. List of UI components (buttons, forms, navigation, etc.)
3. Text content visible in the interface
4. Layout structure and organization
5. Any interactive elements or features identified
6. Screen type/category (dashboard, form, settings, etc.)

IMPORTANT GUIDELINES:
- SKIP platform navigation menus (WordPress admin sidebar, Shopify navigation, etc.)
- IGNORE standard platform headers and footers
- FOCUS ONLY on the main content area and application-specific UI elements
- DO NOT include generic platform layout elements like admin menus, top bars, or standard CMS navigation
- Concentrate on the actual application features and custom content being built

Format the response as structured information for extracting application wireframe data.`;

  const analysis = await analyzeImageWithFlorence(
    imagePath,
    comprehensivePrompt
  );

  return analysis;
}
