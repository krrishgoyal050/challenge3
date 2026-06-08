import { expect, test } from "@playwright/test";

test("dashboard is usable", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Carbon Footprint Awareness Platform" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Log activity" })).toBeVisible();
  await page.getByLabel("Message for assistant").fill("Give me a plan");
  await page.getByRole("button", { name: "Send message" }).click();
  await expect(page.getByText(/Start with|Ask for a plan/)).toBeVisible();
});
