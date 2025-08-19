import fs from "fs";
import path from "path";

export function findScreenshots(screenshotsDir: string) {
  const files = fs
    .readdirSync(screenshotsDir)
    .filter(
      (file) =>
        file.toLowerCase().endsWith(".png") ||
        file.toLowerCase().endsWith(".jpg") ||
        file.toLowerCase().endsWith(".jpeg")
    );

  const fileInfo = files.map((fileName) => {
    const filePath = path.join(screenshotsDir, fileName);
    const stats = fs.statSync(filePath);
    return {
      name: fileName,
      path: filePath,
      size: stats.size,
      sizeInMB: (stats.size / (1024 * 1024)).toFixed(2),
      created: stats.birthtime,
      modified: stats.mtime,
      isFile: stats.isFile(),
    };
  });

  return fileInfo;
}
