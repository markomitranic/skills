---
name: meal-photo-logger
description: Estimate calories and macros for a meal the user did NOT cook themselves — work canteen lunches, restaurant meals, anything eaten out — using a menu description and/or a photo of the plate. Use this whenever the user shares a photo of food to log, pastes a canteen/cafeteria menu line, or asks "what's this" / "log this" / "how many calories is this" about a meal they ate. Always ask clarifying questions (with options) about ingredients or amounts you can't confidently judge from the photo. This is distinct from the meal-macro-planner skill, which is for meals cooked at home from scratch.
---

# Meal Photo Logger

Estimates macros for a single plate eaten outside the home, for manual entry into Lifesum. The user provides up to three inputs:

1. The day's official menu text (usually just names the main dish, sparse detail)
2. A photo of the actual plate
3. Verbal answers to follow-up questions

## Scope: one plate per submission

Each submission is exactly **one plate, one person, one Lifesum entry**. Estimate what is actually visible on that plate — not a generic cookbook version of the dish. If the photo contains multiple separable items (a dessert next to the plate, a drink), estimate only the main plate and tell the user to submit the other items separately.

## Workflow

1. **Read the menu text first.** It anchors what the dish is supposed to be (e.g. "Kylling i karry med ris") even if it's short on detail — cooking method, sauce, and sides are often implied by the dish name and worth a quick lookup if it's a specific known dish.
2. **Analyze the photo.** Identify:
   - Every visible component (protein, starch, veg, sauce, garnish)
   - Weight of each component — use plate diameter (standard canteen plate ≈ 26–28cm), cutlery, or other known-size objects in frame as scale references
   - Cooking method (fried vs steamed vs grilled — affects fat significantly)
   - Visible oil sheen, sauce pooling, breading, or dressing that adds hidden calories
3. **Ask about what you can't judge.** Questions are welcome and expected — photo-based estimates commonly go wrong on amounts and on ambiguous sauces/dressings (e.g. "is that white sauce on the potatoes mayo-based, crème fraîche, or yoghurt?"). Ask short, specific questions and **offer multiple-choice options** wherever possible so the user can answer with a tap or a word. Use the `AskUserQuestion` (or `ask_user_input_v0`) tool for these questions when available. Question targets, in priority order:
   - **Amounts — always confirm, this is the primary question.** For each starch and protein, offer three gram options where your geometric estimate (see Portion sizing below) is the **middle** option, with one clearly lower and one higher — e.g. "Pasta looks like ~70g cooked to me: 50g / 70g / 110g?" Never make your estimate the lowest option.
   - Sauce/dressing base (mayo vs dairy vs vinaigrette)
   - Cooking fat (butter vs oil vs dry)
   - Hidden components (cheese in the mash, sugar in the slaw)
4. **Produce the estimate** only after ambiguities are resolved (or the user says "just estimate"). The estimate is always delivered as the two tables described in "Final response format" below — ingredient breakdown first, then the logging table.

## Estimation discipline

### Portion sizing — the known failure mode

Photo-based weight estimates from this skill have **consistently overshot, sometimes by 2–3×** (documented examples: two small corn-bread slices under 50g total estimated as two full-size sourdough slices; ~60g of pasta estimated as 150g; a meatballs-with-rice plate totalled at 1,280 kcal). Root cause: anchoring on *typical serving sizes* for the recognized dish instead of measuring what is actually in the frame. Calorie density per gram has been fine — the weights are the problem. All of the following are mandatory:

1. **The dish name tells you WHAT; only the photo tells you HOW MUCH.** Never let a standard portion from a nutrition database become the weight estimate. If a weight estimate lands exactly on a textbook serving (150g pasta, 200g rice, 125g meat), treat that as a red flag that you anchored instead of measured — re-derive it from the photo.
2. **Measure geometrically, out loud.** Fix the scale first (canteen plate ≈ 26–28cm rim-to-rim with ~18cm well, dinner fork ≈ 19cm, or any known-size object in frame). Then for each component: fraction of plate area covered × layer thickness → volume → weight via density (cooked rice/pasta ≈ 0.6–0.8 g/cm³, sauces ≈ 1.0, cooked meat ≈ 1.05). Note the reasoning briefly in the Amount column or assumptions line so the user can veto it.
3. **When torn, go low.** After the geometric estimate, if two weights seem plausible, pick the lower one. The documented bias is overshoot; undershoot has not been observed.
4. **Plate-total sanity band.** A normal canteen lunch plate lands around 400–800 kcal. If the total exceeds ~900 kcal, stop and re-derive the weights of the two heaviest components before sending — historically such totals have been portion-size errors, not calorie-density errors.

### Numbers

- **Single point estimates only, never ranges.** "480 kcal", not "450–520 kcal" — Lifesum's form takes one number per field. State assumptions in the text instead of hedging with ranges.
- **Mandatory sanity check before finalizing:** verify Protein×4 + Carbs×4 + Fat×9 ≈ Calories (within ~5%), for each ingredient row and for the total. If numbers don't reconcile, fix them — an internally inconsistent breakdown is worse than an imprecise one.
- Round to sensible increments: nearest 5–10 kcal, nearest 1g per macro. No fake precision like "523.4 kcal".
- Metric only.

## Final response format

The final response **always contains exactly two tables, in this order**. Both are plain markdown in the chat text — **never** use `visualize:show_widget` or any other widget/card tool for this output (it does not render on the mobile client, where this skill is most often used).

### 1. Ingredient breakdown table — MANDATORY, never skip

This table is the whole point of the skill: it is what makes the estimate checkable and lets the user log against their own Lifesum product brands. **Omitting it is a failure**, even for simple single-component plates, even when the user seems to be in a hurry, even after a long clarifying-question exchange. Every component included in the calculation gets a row, with its estimated amount and macros:

| Ingredient | Amount | kcal | Carbs (g) | Fat (g) | Protein (g) |
|---|---|---|---|---|---|
| Corn bread | 2 pieces (~120g) | 310 | 48 | 9 | 8 |
| Potato salad, mayo-based | ~180g | 290 | 22 | 20 | 4 |

State any assumptions made (e.g. "assumed rapeseed oil mayo") as a brief line under the table.

### 2. Logging table

A second, compact table containing exactly what gets typed into Lifesum:

1. **The plate title** — English, under 50 characters, describing the plate (e.g. "Corn Bread with Mayo Potato Salad"). This becomes the Lifesum entry name. Render it as inline code (backticks) on its own line above the table, so it's easy to long-press-copy on mobile.
2. **The four totals, in this exact order and with these units** (mirrors Lifesum's entry form top-to-bottom): Calories (kcal), Carbs (g), Fat (g), Protein (g). Full names or single-letter abbreviations are both fine — the **order and units are the invariant**.

Format:

**Lifesum entry:** `Corn Bread with Mayo Potato Salad`

| | |
|---|---|
| Calories | 600 kcal |
| Carbs | 70 g |
| Fat | 29 g |
| Protein | 12 g |

Nothing else in the tables: no food icons, no disclaimers, no decoration.

### Pre-send checklist

Before sending the final response, verify all four are present:

1. ☐ Ingredient breakdown table (one row per component)
2. ☐ Assumptions line under it
3. ☐ Logging table (title as inline code + the four totals in Lifesum order)
4. ☐ Total within the sanity band — if over ~900 kcal, weights of the two heaviest components have been re-derived geometrically

If any is missing, the response is incomplete — fix it before sending.
