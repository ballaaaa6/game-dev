import "./styles.css";
import { createSocialDevRuntime } from "./app/runtime";

const root = document.querySelector<HTMLElement>("#app");
if (!root) {
  throw new Error("Social Dev app root is missing");
}

try {
  createSocialDevRuntime(root);
} catch (error) {
  root.innerHTML = "";
  const message = document.createElement("pre");
  message.style.padding = "24px";
  message.style.color = "#ff9eaa";
  message.textContent = error instanceof Error ? error.stack ?? error.message : String(error);
  root.append(message);
  throw error;
}
