# AI-CDO Evaluation Results Summary

This document summarizes the primary quantitative evaluation outcomes for hypotheses H1–H5 in the AI-CDO study.

---

# H1 — Preference Outcomes

| Comparison | Wins | Ties | Losses | Preference Rate (%) | 95% CI Low | 95% CI High |
|---|---:|---:|---:|---:|---:|---:|
| AI-CDO vs Baseline | 339 | 111 | 0 | 75.33% | 71.08% | 79.25% |
| AI-CDO vs SFT | 450 | 0 | 0 | 100.00% | 99.18% | 100.00% |
| SFT vs Baseline | 264 | 96 | 90 | 58.67% | 53.96% | 63.26% |

### Interpretation
AI-CDO achieved the strongest overall human preference rates across the evaluated conditions. Against the SFT-only condition, AI-CDO achieved complete preference across all evaluated comparisons. AI-CDO also substantially outperformed the direct baseline condition, while SFT-only maintained a moderate advantage over the baseline.

---

# H2 — Business Alignment

| Metric | Value |
|---|---:|
| Business Alignment Win Rate | 89.41% |
| Mean Alignment Score (AI-CDO) | 8.66 |
| Mean Alignment Score (Baseline) | 6.13 |

### Interpretation
AI-CDO outputs were consistently rated as more strategically aligned with business goals, brand positioning, and communication priorities than baseline-generated interfaces.

---

# H3 — Distinctness

| Metric | Value |
|---|---:|
| Distinctness Threshold | 7 |
| Pass Rate | 100.00% |
| Mean Distinctness Score | 8.67 |

### Interpretation
All evaluated AI-CDO outputs met or exceeded the predefined threshold for meaningful distinctness, suggesting that raters perceived the generated interfaces as strategically differentiated rather than superficially varied.

---

# H4 — Confidence & Collaboration

| Metric | Value |
|---|---:|
| Mean Score (Rationale Visible) | 7.57 |
| Mean Score (Rationale Hidden) | 6.13 |
| Relative Improvement | 23.49% |
| T-statistic | 107.3150 |
| P-value | 0.000000 |

### Interpretation
Providing visible rationale for design decisions significantly improved evaluator confidence and perceived collaboration quality. Raters consistently reported greater trust and stronger human-AI collaboration when the system’s reasoning process was exposed.

---

# H5 — Time to Acceptable Output

| Metric | Value |
|---|---:|
| Mean Time (AI-CDO) | 11.67 min |
| Mean Time (Baseline) | 21.28 min |
| Reduction | 45.16% |

### Interpretation
AI-CDO substantially reduced the estimated time required to reach an acceptable business-ready interface compared to baseline generation approaches.

---

# Overall Findings

Across all evaluated hypotheses, AI-CDO demonstrated improvements in:
- human preference,
- business alignment,
- strategic distinctness,
- perceived collaboration quality,
- and estimated production efficiency.

These findings support the central claim of the study: separating strategic reasoning from direct code generation can improve both the quality of AI-generated interfaces and the effectiveness of human-AI design collaboration.

# Repository Structure

## Held-Out Brief Dataset

The held-out evaluation briefs used throughout the study are located at:

```bash
platform/results/briefs/heldout_briefs.csv
```

This dataset contains the benchmark product briefs used for blind evaluation, preference testing, business-alignment analysis, and strategic distinctness evaluation.

---

## Study Results and Analysis

All generated evaluation outputs, statistical analyses, graphs, and supporting study artifacts are located in:

```bash
platform/results
```

This directory includes:
- pairwise evaluation outputs,
- rationale-study analysis,
- generated figures,
- summary statistics,
- preference outcomes,
- business-alignment metrics,
- distinctness evaluations,
- confidence/collaboration analysis,
- and time-to-acceptable-output measurements.

---

## Demo Samples
<!-- demo-samples -->
### B131
> AI-assisted screenwriting and story development platform for independent filmmakers and screenwriters — dark, cinematic, and filmmaker-peer with script editor UI preview, beat sheet visualization, scripts developed stats, WGA-awareness callout, and festival alumni testimonials. Positioned against Final Draft as AI-augmented and more structured for story development

| v0.dev · Baseline | SFT only | AI CDO · Best |
|:---:|:---:|:---:|
| ![v0](samples/B131/v0.png) | ![sft](samples/B131/sft.png) | ![aicdo](samples/B131/aicdo.png) |


<details>
<summary><strong>v0.dev · Baseline</strong> — 1 step</summary>

**Step 1 · Direct Generation** (16538 ms)
```json
import React from 'react';

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navbar */}
      <nav className="sticky top-0 z-50 bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-blue-600 rounded"></div>
              <span className="font-semibold text-lg text-gray-900">Frameforge</span>
            </div>
            <div className="hidden md:flex gap-8">
              <a href="#features" className="text-gray-700 hover:text-gray-900 text-sm">Features</a>
              <a href="#about" className="text-gray-700 hover:text-gray-900 text-sm">About</a>
              <a href="#testimonials" className="text-gray-700 hover:text-gray-900 text-sm">Testimonials</a>
              <a href="#contact" className="text-gray-700 hover:text-gray-
```

</details>

<details>
<summary><strong>SFT only</strong> — 2 steps</summary>

**Step 2 · Classification** (1172 ms)
```json
{
  "product_type": "B2C SaaS",
  "industry": "ai_platform",
  "page_type": "landing",
  "primary_user": "end_customer",
  "user_context": "evaluating",
  "trust_sensitivity": "medium"
}
```

**Step 5 · Code Generation (no CDO strategy)** (108756 ms)
```json
{
  "files": [
    {
      "path": "src/app/page.tsx",
      "content": "```json\n{\n  \"files\": [\n    {\n      \"path\": \"src/app/page.tsx\",\n      \"content\": \"export default function Home() {\\n  return (\\n    <div className=\\\"bg-[#0d0f14] text-gray-100 min-h-screen font-sans\\\">\\n\\n      {/* NAV */}\\n      <nav className=\\\"sticky top-0 z-50 bg-[#0d0f14]/95 backdrop-blur border-b border-white/10\\\">\\n        <div className=\\\"max-w-6xl mx-auto px-6 py-4 flex items-center justify-between\\\">\\n          <div className=\\\"flex items-center gap-2\\\">\\n            <div className=\\\"w-7 h-7 rounded bg-indigo-500 flex items-center justify-center\\\">\\n              <svg width=\\\"16\\\" height=\\\"16\\\" viewBox=\\\"0 0 16 16\\\" fill=\\\"none\\\">\\n                <p
```

</details>

<details>
<summary><strong>AI CDO · Best</strong> — 5 steps</summary>

**Step 2 · Classification** (1221 ms)
```json
{
  "product_type": "B2C SaaS",
  "industry": "other",
  "page_type": "landing",
  "primary_user": "end_customer",
  "user_context": "first_time_visitor",
  "trust_sensitivity": "medium"
}
```

**Step 3 · CDO Strategy** (5448 ms)
```json
{
  "primary_intent": "drive_conversion",
  "key_risks": [
    "unclear_value_prop",
    "low_trust",
    "overpromising"
  ],
  "strategic_principles": [
    "credibility_over_creativity",
    "confidence_before_action"
  ],
  "avoidances": [
    "marketing_fluff",
    "unsubstantiated_claims",
    "flashy_motion"
  ],
  "strategies": [
    {
      "intent": "trust_first",
      "hero_focus": "social_proof",
      "information_order": [
        "headline",
        "subheadline",
        "testimonials",
        "product_demo",
        "benefits",
        "primary_cta",
        "footer"
      ],
      "risk_controls": [
        "delay_cta",
        "increase_proof_density"
      ],
      "rationale": "Lead with peer credibility from festival alumni to overcome skepticism toward AI in a craft-driven creative community before asking for commitment."
    },
    {
      "intent": "product_first",
      "hero_focus": "product_visual",
      "information_order": [
        "headline",
        
```

**Step 3.5 · Brand Traits** (15951 ms)
```json
{
  "visual_tone": {
    "mood": [
      "cinematic",
      "moody",
      "auteur",
      "crafted",
      "nocturnal"
    ],
    "energy": "contemplative",
    "aesthetic": "editorial-cinema",
    "formality": "elevated-craft",
    "vibe_descriptors": [
      "screening-room",
      "indie-festival",
      "writers-room",
      "celluloid-grain",
      "after-hours"
    ]
  },
  "color_profile": {
    "scheme_type": "dark",
    "palette_intent": "Deep theatrical blacks and inky charcoals as the dominant canvas, evoking a darkened cinema. Accented with a single warm signature hue \u2014 projector amber or marquee gold \u2014 used sparingly for emphasis, CTAs, and beat-sheet highlights. Secondary muted film-stock tones (desaturated sepia, ember red) for testimonial moments and accents.",
    "contrast_level": "high",
    "saturation": "muted-with-warm-accent",
    "primary_hue_suggestion": "near-black with amber/gold accent",
    "avoid": [
      "bright tech blues",
      "saas pastel
```

**Step 4 · UI Intent** (1936 ms)
```json
{
  "primary_focus": "authority",
  "cta_policy": {
    "timing": "delayed",
    "intensity": "neutral"
  },
  "proof_policy": "heavy",
  "content_density": "medium",
  "motion_policy": "subtle",
  "creative_license": "restricted",
  "language_style": "confident",
  "interaction_restraint": "moderate"
}
```

**Step 5 · Code Generation** (86303 ms)
```json
{
  "files": [
    {
      "path": "package.json",
      "content": "{\n  \"name\": \"authority-screenwriting\",\n  \"version\": \"0.1.0\",\n  \"private\": true,\n  \"scripts\": {\n    \"dev\": \"next dev\",\n    \"build\": \"next build\",\n    \"start\": \"next start\",\n    \"lint\": \"next lint\"\n  },\n  \"dependencies\": {\n    \"next\": \"14.2.5\",\n    \"react\": \"18.3.1\",\n    \"react-dom\": \"18.3.1\"\n  },\n  \"devDependencies\": {\n    \"@types/node\": \"20.11.0\",\n    \"@types/react\": \"18.3.3\",\n    \"@types/react-dom\": \"18.3.0\",\n    \"autoprefixer\": \"10.4.19\",\n    \"postcss\": \"8.4.39\",\n    \"tailwindcss\": \"3.4.7\",\n    \"typescript\": \"5.4.5\"\n  }\n}\n"
    },
    {
      "path": "next.config.js",
      "content": "/** @type {import('next').NextConfig} *
```

</details>

### B126
> Digital services portal for a mid-size city government enabling residents to complete permits, payments, and city services online — clear, accessible, WCAG AAA compliant with plain language, services catalog, average task completion time, and accessibility score. Positioned as replacing in-person city hall visits with digital-first services

| v0.dev · Baseline | SFT only | AI CDO · Best |
|:---:|:---:|:---:|
| ![v0](samples/B126/v0.png) | ![sft](samples/B126/sft.png) | ![aicdo](samples/B126/aicdo.png) |


<details>
<summary><strong>v0.dev · Baseline</strong> — 1 step</summary>

**Step 1 · Direct Generation** (11856 ms)
```json
import React from 'react';

export default function Page() {
  return (
    <div className="min-h-screen bg-white flex flex-col">
      {/* Navbar */}
      <nav className="border-b border-gray-200 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg"></div>
            <span className="text-xl font-semibold text-gray-900">City Services</span>
          </div>
          <div className="hidden md:flex gap-8">
            <a href="#services" className="text-gray-600 hover:text-gray-900 text-sm">Services</a>
            <a href="#features" className="text-gray-600 hover:text-gray-900 text-sm">Features</a>
            <a href="#help" className="text-gray-600 hover:text-gray-900 text-sm">Help</a>
          </div>
          <button className="text-gray-600 hover:text-gray-900 md:hidden">
            <svg className="w-6 h-
```

</details>

<details>
<summary><strong>SFT only</strong> — 2 steps</summary>

**Step 2 · Classification** (1700 ms)
```json
{
  "product_type": "B2C SaaS",
  "industry": "other",
  "page_type": "dashboard",
  "primary_user": "end_customer",
  "user_context": "first_time_visitor",
  "trust_sensitivity": "high"
}
```

**Step 5 · Code Generation (no CDO strategy)** (95044 ms)
```json
{
  "files": [
    {
      "path": "src/app/page.tsx",
      "content": "```json\n{\n  \"files\": [\n    {\n      \"path\": \"src/app/page.tsx\",\n      \"content\": \"export default function Home() {\\n  return (\\n    <div className=\\\"min-h-screen bg-white text-gray-900 font-sans\\\">\\n\\n      {/* Sticky Nav */}\\n      <header className=\\\"sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm\\\">\\n        <div className=\\\"max-w-6xl mx-auto px-6 py-4 flex items-center justify-between\\\">\\n          <div className=\\\"flex items-center gap-3\\\">\\n            <div className=\\\"w-8 h-8 rounded-md bg-blue-700 flex items-center justify-center\\\">\\n              <svg width=\\\"18\\\" height=\\\"18\\\" viewBox=\\\"0 0 24 24\\\" fill=\\\"none\\\" stroke=\\\"white\\\" stro
```

</details>

<details>
<summary><strong>AI CDO · Best</strong> — 5 steps</summary>

**Step 2 · Classification** (1266 ms)
```json
{
  "product_type": "internal_tool",
  "industry": "other",
  "page_type": "landing",
  "primary_user": "end_customer",
  "user_context": "first_time_visitor",
  "trust_sensitivity": "high"
}
```

**Step 3 · CDO Strategy** (7030 ms)
```json
{
  "primary_intent": "accelerate_understanding",
  "key_risks": [
    "cognitive_overload",
    "unclear_value_prop",
    "low_trust"
  ],
  "strategic_principles": [
    "clarity_over_density",
    "familiarity_over_novelty",
    "progressive_disclosure"
  ],
  "avoidances": [
    "marketing_fluff",
    "visual_clutter",
    "flashy_motion"
  ],
  "strategies": [
    {
      "intent": "product_first",
      "hero_focus": "value_prop",
      "information_order": [
        "headline",
        "subheadline",
        "product_demo",
        "benefits",
        "security_compliance",
        "faq",
        "footer"
      ],
      "risk_controls": [
        "simplify_language",
        "limit_choices"
      ],
      "rationale": "Lead with the practical value of digital service access so residents immediately understand what they can accomplish, reducing confusion for a broad and diverse first-time audience."
    },
    {
      "intent": "authority_first",
      "hero_focus": "authority",

```

**Step 3.5 · Brand Traits** (12623 ms)
```json
{
  "brand_personality": {
    "primary_traits": [
      "trustworthy",
      "accessible",
      "civic",
      "straightforward"
    ],
    "tone": "clear, reassuring, and respectful \u2014 plain language that treats residents as capable adults without bureaucratic jargon",
    "voice_attributes": [
      "plain-spoken",
      "patient",
      "inclusive",
      "authoritative-but-warm"
    ]
  },
  "visual_identity": {
    "aesthetic": "civic-modern",
    "design_language": "clean, structured, and unmistakably governmental \u2014 evoking public-sector credibility while feeling contemporary and digitally native",
    "visual_density": "comfortable",
    "whitespace": "generous",
    "corner_radius": "subtle",
    "border_treatment": "defined-borders",
    "shadow_usage": "minimal",
    "texture": "flat"
  },
  "color_direction": {
    "palette_type": "restrained-institutional",
    "primary_hue": "deep civic blue",
    "secondary_hue": "neutral slate gray",
    "accent_hue": "trustwo
```

**Step 4 · UI Intent** (2122 ms)
```json
{
  "primary_focus": "value_prop",
  "cta_policy": {
    "timing": "delayed",
    "intensity": "soft"
  },
  "proof_policy": "heavy",
  "content_density": "low",
  "motion_policy": "none",
  "creative_license": "restricted",
  "language_style": "plain",
  "interaction_restraint": "strict"
}
```

**Step 5 · Code Generation** (81347 ms)
```json
{
  "files": [
    {
      "path": "package.json",
      "content": "{\n  \"name\": \"city-services\",\n  \"version\": \"0.1.0\",\n  \"private\": true,\n  \"scripts\": {\n    \"dev\": \"next dev\",\n    \"build\": \"next build\",\n    \"start\": \"next start\",\n    \"lint\": \"next lint\"\n  },\n  \"dependencies\": {\n    \"next\": \"14.2.5\",\n    \"react\": \"18.3.1\",\n    \"react-dom\": \"18.3.1\"\n  },\n  \"devDependencies\": {\n    \"@types/node\": \"20.12.7\",\n    \"@types/react\": \"18.3.3\",\n    \"@types/react-dom\": \"18.3.0\",\n    \"autoprefixer\": \"10.4.19\",\n    \"postcss\": \"8.4.38\",\n    \"tailwindcss\": \"3.4.7\",\n    \"typescript\": \"5.4.5\"\n  }\n}\n"
    },
    {
      "path": "next.config.js",
      "content": "/** @type {import('next').NextConfig} */\nconst n
```

</details>

### B077
> Direct-to-consumer electric commuter bike brand for urban commuters 25–45 seeking a car replacement — bold, high-contrast, and performance-forward with range stats, commute cost savings calculator, and test ride finder. Positioned against entry-level e-bikes as more commuter-engineered

| v0.dev · Baseline | SFT only | AI CDO · Best |
|:---:|:---:|:---:|
| ![v0](samples/B077/v0.png) | ![sft](samples/B077/sft.png) | ![aicdo](samples/B077/aicdo.png) |


<details>
<summary><strong>v0.dev · Baseline</strong> — 1 step</summary>

**Step 1 · Direct Generation** (14335 ms)
```json
'use client';

import { useState } from 'react';

export default function Home() {
  const [monthlyCommute, setMonthlyCommute] = useState(500);
  const [gasSavings, setGasSavings] = useState(100);

  const handleCommuteChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseFloat(e.target.value);
    setMonthlyCommute(value);
    // Assume $0.20 per km on car, $0.02 per km on e-bike
    setGasSavings(Math.round((value * (0.20 - 0.02)) / 12));
  };

  return (
    <div className="min-h-screen bg-white flex flex-col">
      {/* Navbar */}
      <nav className="border-b border-gray-200 sticky top-0 z-50 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-black rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">⚡</span>
            </div>
            <span class
```

</details>

<details>
<summary><strong>SFT only</strong> — 2 steps</summary>

**Step 2 · Classification** (1244 ms)
```json
{
  "product_type": "B2C SaaS",
  "industry": "ecommerce",
  "page_type": "landing",
  "primary_user": "end_customer",
  "user_context": "evaluating",
  "trust_sensitivity": "medium"
}
```

**Step 5 · Code Generation (no CDO strategy)** (95735 ms)
```json
{
  "files": [
    {
      "path": "src/app/page.tsx",
      "content": "```json
{
  \"files\": [
    {
      \"path\": \"src/app/page.tsx\",
      \"content\": \"export default function Home() {\n  return (\n    <div className=\\"min-h-screen bg-zinc-950 text-white\\">\n      {/* Sticky Nav */}\n      <nav className=\\"sticky top-0 z-50 bg-zinc-950/95 border-b border-zinc-800 backdrop-blur\\">\n        <div className=\\"max-w-7xl mx-auto px-6 py-4 flex items-center justify-between\\">\n          <div className=\\"flex items-center gap-2\\">\n            <div className=\\"w-8 h-8 bg-lime-400 rounded-md flex items-center justify-center\\">\n              <svg width=\\"18\\" height=\\"18\\" viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"#09090b\\" strokeWi
```

</details>

<details>
<summary><strong>AI CDO · Best</strong> — 5 steps</summary>

**Step 2 · Classification** (1414 ms)
```json
{
  "product_type": "ecommerce",
  "industry": "ecommerce",
  "page_type": "landing",
  "primary_user": "end_customer",
  "user_context": "first_time_visitor",
  "trust_sensitivity": "medium"
}
```

**Step 3 · CDO Strategy** (6247 ms)
```json
{
  "primary_intent": "drive_conversion",
  "key_risks": [
    "unclear_value_prop",
    "overpromising",
    "premature_cta"
  ],
  "strategic_principles": [
    "confidence_before_action",
    "clarity_over_density",
    "credibility_over_creativity"
  ],
  "avoidances": [
    "marketing_fluff",
    "unsubstantiated_claims",
    "aggressive_ctas"
  ],
  "strategies": [
    {
      "intent": "product_first",
      "hero_focus": "value_prop",
      "information_order": [
        "headline",
        "subheadline",
        "product_demo",
        "benefits",
        "testimonials",
        "primary_cta",
        "faq",
        "footer"
      ],
      "risk_controls": [
        "simplify_language",
        "increase_proof_density"
      ],
      "rationale": "Lead with the differentiated commuter-engineered value proposition and let the product itself carry conviction, since the audience is evaluating a significant lifestyle and financial shift away from cars."
    },
    {
      "intent"
```

**Step 3.5 · Brand Traits** (17523 ms)
```json
{
  "design_personality": {
    "primary": "bold",
    "secondary": [
      "performance",
      "engineered",
      "confident"
    ],
    "avoid": [
      "playful",
      "delicate",
      "decorative",
      "vintage"
    ]
  },
  "visual_tone": {
    "energy": "high",
    "formality": "casual_premium",
    "warmth": "cool",
    "density": "spacious_with_data_moments"
  },
  "color_strategy": {
    "scheme": "high_contrast_dark",
    "base": "near_black",
    "surface": "deep_charcoal",
    "text": "off_white",
    "accent_role": "performance_signal",
    "accent": "electric_lime",
    "secondary_accent": "signal_orange",
    "contrast_level": "very_high",
    "usage_notes": "Dark canvas with punchy accent for stats, CTAs, and range/savings numerics. Avoid pastels and gradients-as-decor; use accent sparingly to preserve impact."
  },
  "typography": {
    "style": "industrial_geometric",
    "headline_weight": "extra_bold",
    "headline_treatment": "tight_tracking_large_scale",
  
```

**Step 4 · UI Intent** (1931 ms)
```json
{
  "primary_focus": "value_prop",
  "cta_policy": {
    "timing": "immediate",
    "intensity": "assertive"
  },
  "proof_policy": "balanced",
  "content_density": "medium",
  "motion_policy": "subtle",
  "creative_license": "restricted",
  "language_style": "confident",
  "interaction_restraint": "moderate"
}
```

**Step 5 · Code Generation** (97264 ms)
```json
{
  "files": [
    {
      "path": "package.json",
      "content": "{
  \"name\": \"commuter-ebike\",
  \"version\": \"0.1.0\",
  \"private\": true,
  \"scripts\": {
    \"dev\": \"next dev\",
    \"build\": \"next build\",
    \"start\": \"next start\",
    \"lint\": \"next lint\"
  },
  \"dependencies\": {
    \"next\": \"14.2.5\",
    \"react\": \"18.3.1\",
    \"react-dom\": \"18.3.1\"
  },
  \"devDependencies\": {
    \"@types/node\": \"20.12.7\",
    \"@types/react\": \"18.3.3\",
    \"@types/react-dom\": \"18.3.0\",
    \"autoprefixer\": \"10.4.19\",
    \"postcss\": \"8.4.38\",
    \"tailwindcss\": \"3.4.4\",
    \"typescript\": \"5.4.5\"
  }
}
"
    },
    {
      "path": "next.config.js",
      "content": "/** @type {import('next').NextConfig} */
const 
```

</details>

### B061
> Coding bootcamp for career changers entering software development — motivating, outcome-focused, and credible with strong job placement rates, average starting salary stats, and employer partner logos. Positioned against top bootcamps as more mentorship-intensive

| v0.dev · Baseline | SFT only | AI CDO · Best |
|:---:|:---:|:---:|
| ![v0](samples/B061/v0.png) | ![sft](samples/B061/sft.png) | ![aicdo](samples/B061/aicdo.png) |


<details>
<summary><strong>v0.dev · Baseline</strong> — 1 step</summary>

**Step 1 · Direct Generation** (17230 ms)
```json
import React from 'react';

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navbar */}
      <nav className="sticky top-0 z-50 bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0 font-bold text-2xl text-blue-600">
                DevCareer
              </div>
            </div>
            <div className="hidden md:flex space-x-8">
              <a href="#features" className="text-gray-700 hover:text-blue-600 text-sm font-medium">
                Features
              </a>
              <a href="#outcomes" className="text-gray-700 hover:text-blue-600 text-sm font-medium">
                Outcomes
              </a>
              <a href="#mentorship" className="text-gray-700 hover:text-blue-600 text-sm font-medium">
              
```

</details>

<details>
<summary><strong>SFT only</strong> — 2 steps</summary>

**Step 2 · Classification** (1287 ms)
```json
{
  "product_type": "B2C SaaS",
  "industry": "education",
  "page_type": "landing",
  "primary_user": "end_customer",
  "user_context": "evaluating",
  "trust_sensitivity": "high"
}
```

**Step 5 · Code Generation (no CDO strategy)** (80623 ms)
```json
{
  "files": [
    {
      "path": "src/app/page.tsx",
      "content": "export default function Home() {
  return (
    <div className=\"min-h-screen bg-white text-gray-900 font-sans\">
      {/* Sticky Nav */}
      <nav className=\"sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm\">
        <div className=\"max-w-6xl mx-auto px-6 py-4 flex items-center justify-between\">
          <div className=\"flex items-center gap-2\">
            <div className=\"w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center\">
              <span className=\"text-white font-bold text-sm\">L</span>
            </div>
            <span className=\"text-xl font-bold text-gray-900\">LaunchCode Academy</span>
          </div>
          <div className=\"hidden md:flex items-
```

</details>

<details>
<summary><strong>AI CDO · Best</strong> — 5 steps</summary>

**Step 2 · Classification** (1215 ms)
```json
{
  "product_type": "content_site",
  "industry": "education",
  "page_type": "landing",
  "primary_user": "end_customer",
  "user_context": "first_time_visitor",
  "trust_sensitivity": "high"
}
```

**Step 3 · CDO Strategy** (6539 ms)
```json
{
  "primary_intent": "increase_confidence",
  "key_risks": [
    "overpromising",
    "low_trust",
    "unclear_value_prop"
  ],
  "strategic_principles": [
    "credibility_over_creativity",
    "confidence_before_action",
    "clarity_over_density"
  ],
  "avoidances": [
    "unsubstantiated_claims",
    "marketing_fluff",
    "aggressive_ctas"
  ],
  "strategies": [
    {
      "name": "Outcomes as Proof",
      "intent": "trust_first",
      "hero_focus": "social_proof",
      "information_order": [
        "headline",
        "subheadline",
        "customer_logos",
        "benefits",
        "testimonials",
        "primary_cta",
        "faq",
        "footer"
      ],
      "risk_controls": [
        "increase_proof_density",
        "delay_cta",
        "simplify_language"
      ],
      "rationale": "Career changers face significant personal and financial risk, so leading with verifiable outcomes and employer credibility addresses skepticism before any commitment is request
```

**Step 3.5 · Brand Traits** (11785 ms)
```json
{
  "brand_personality": {
    "primary_traits": [
      "motivating",
      "credible",
      "outcome-driven"
    ],
    "tone": "confident-mentor",
    "energy_level": "high",
    "formality": "approachable-professional"
  },
  "visual_direction": {
    "aesthetic": "modern-editorial",
    "design_era": "contemporary-2024",
    "visual_metaphor": "upward-trajectory",
    "complexity": "structured-clean"
  },
  "color_strategy": {
    "palette_type": "purposeful-accent",
    "primary_mood": "trustworthy-ambitious",
    "base": "warm-neutral-white",
    "primary": "deep-navy",
    "accent": "vibrant-coral",
    "supporting": [
      "soft-sand",
      "success-green"
    ],
    "contrast_level": "high",
    "rationale": "Navy conveys credibility and academic rigor while coral injects motivational energy and signals transformation; high contrast supports scannability for first-time visitors"
  },
  "typography": {
    "personality": "editorial-confident",
    "heading_style": "bold-dis
```

**Step 4 · UI Intent** (2309 ms)
```json
{
  "primary_focus": "value_prop",
  "cta_policy": {
    "timing": "delayed",
    "intensity": "neutral"
  },
  "proof_policy": "heavy",
  "content_density": "medium",
  "motion_policy": "subtle",
  "creative_license": "restricted",
  "language_style": "plain",
  "interaction_restraint": "moderate"
}
```

**Step 5 · Code Generation** (102848 ms)
```json
{
  "files": [
    {
      "path": "package.json",
      "content": "{
  \"name\": \"clear-value-path\",
  \"version\": \"0.1.0\",
  \"private\": true,
  \"scripts\": {
    \"dev\": \"next dev\",
    \"build\": \"next build\",
    \"start\": \"next start\",
    \"lint\": \"next lint\"
  },
  \"dependencies\": {
    \"next\": \"14.2.5\",
    \"react\": \"18.3.1\",
    \"react-dom\": \"18.3.1\"
  },
  \"devDependencies\": {
    \"@types/node\": \"20.12.7\",
    \"@types/react\": \"18.3.3\",
    \"@types/react-dom\": \"18.3.0\",
    \"autoprefixer\": \"10.4.19\",
    \"postcss\": \"8.4.38\",
    \"tailwindcss\": \"3.4.7\",
    \"typescript\": \"5.4.5\"
  }
}
"
    },
    {
      "path": "next.config.js",
      "content": "/** @type {import('next').NextConfig} */
modu
```

</details>

### B116
> Immigration legal aid nonprofit providing pro bono services to immigrants and asylum seekers — compassionate, trustworthy, and multilingual with cases handled stats, languages supported, and pro bono attorney network. Positioned as the most accessible immigration legal resource for unrepresented immigrants

| v0.dev · Baseline | SFT only | AI CDO · Best |
|:---:|:---:|:---:|
| ![v0](samples/B116/v0.png) | ![sft](samples/B116/sft.png) | ![aicdo](samples/B116/aicdo.png) |


<details>
<summary><strong>v0.dev · Baseline</strong> — 1 step</summary>

**Step 1 · Direct Generation** (11854 ms)
```json
'use client';

import { Mail, Phone, Heart, Globe, Users, Scale } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navbar */}
      <nav className="border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg"></div>
            <span className="text-xl font-bold text-gray-900">ImmigrantAid</span>
          </div>
          <div className="flex items-center gap-8">
            <a href="#" className="text-gray-700 hover:text-blue-600 text-sm">About</a>
            <a href="#" className="text-gray-700 hover:text-blue-600 text-sm">Services</a>
            <a href="#" className="text-gray-700 hover:text-blue-600 text-sm">Contact</a>
            <a href="#" className="text-gray-700 hover:text-blue-600 text-sm">Donate</a>
          </div>
        </div>
      
```

</details>

<details>
<summary><strong>SFT only</strong> — 2 steps</summary>

**Step 2 · Classification** (2658 ms)
```json
{
  "product_type": "content_site",
  "industry": "other",
  "page_type": "landing",
  "primary_user": "end_customer",
  "user_context": "first_time_visitor",
  "trust_sensitivity": "high"
}
```

**Step 5 · Code Generation (no CDO strategy)** (90721 ms)
```json
{
  "files": [
    {
      "path": "src/app/page.tsx",
      "content": "```json
{
  \"files\": [
    {
      \"path\": \"src/app/page.tsx\",
      \"content\": \"export default function Home() {\n  return (\n    <div className=\\"min-h-screen bg-white text-gray-800 font-sans\\">\n      {/* Sticky Nav */}\n      <nav className=\\"sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm\\">\n        <div className=\\"max-w-6xl mx-auto px-6 py-4 flex items-center justify-between\\">\n          <div className=\\"flex items-center gap-2\\">\n            <div className=\\"w-8 h-8 rounded-full bg-teal-600 flex items-center justify-center\\">\n              <svg className=\\"w-5 h-5 text-white\\" fill=\\"none\\" stroke=\\"currentColor\\" viewBox=\\"0 0 24 24\\"
```

</details>

<details>
<summary><strong>AI CDO · Best</strong> — 5 steps</summary>

**Step 2 · Classification** (1215 ms)
```json
{
  "product_type": "content_site",
  "industry": "other",
  "page_type": "landing",
  "primary_user": "end_customer",
  "user_context": "first_time_visitor",
  "trust_sensitivity": "high"
}
```

**Step 3 · CDO Strategy** (6023 ms)
```json
{
  "primary_intent": "signal_legitimacy",
  "key_risks": [
    "low_trust",
    "unclear_value_prop",
    "overpromising"
  ],
  "strategic_principles": [
    "credibility_over_creativity",
    "clarity_over_density",
    "confidence_before_action"
  ],
  "avoidances": [
    "marketing_fluff",
    "aggressive_ctas",
    "unsubstantiated_claims"
  ],
  "strategies": [
    {
      "name": "Credibility Foundation",
      "intent": "trust_first",
      "hero_focus": "authority",
      "information_order": [
        "headline",
        "subheadline",
        "security_compliance",
        "benefits",
        "testimonials",
        "primary_cta",
        "faq",
        "footer"
      ],
      "risk_controls": [
        "increase_proof_density",
        "reinforce_authority",
        "simplify_language"
      ],
      "rationale": "Vulnerable first-time visitors require institutional legitimacy before engagement; leading with authority mitigates skepticism in a high-stakes legal context."
 
```

**Step 3.5 · Brand Traits** (11890 ms)
```json
{
  "visual_tone": {
    "descriptors": [
      "compassionate",
      "trustworthy",
      "humanitarian",
      "dignified",
      "accessible"
    ],
    "energy": "calm",
    "formality": "professional",
    "warmth": "warm"
  },
  "color_direction": {
    "palette_type": "warm_humanitarian",
    "primary_hue": "deep_teal",
    "accent_hue": "warm_amber",
    "background_strategy": "soft_neutral",
    "contrast_level": "high",
    "rationale": "Deep teal conveys legal authority and trust while warm amber accents add humanity and hope. Soft neutral backgrounds with high contrast ensure readability for multilingual users and accessibility compliance."
  },
  "typography_direction": {
    "style": "humanist_sans",
    "personality": [
      "clear",
      "approachable",
      "globally_legible"
    ],
    "scale_contrast": "moderate",
    "rationale": "Humanist sans-serif typefaces offer warmth while maintaining the clarity needed for legal content and multilingual support including 
```

**Step 4 · UI Intent** (1980 ms)
```json
{
  "primary_focus": "social_proof",
  "cta_policy": {
    "timing": "delayed",
    "intensity": "soft"
  },
  "proof_policy": "heavy",
  "content_density": "low",
  "motion_policy": "subtle",
  "creative_license": "restricted",
  "language_style": "plain",
  "interaction_restraint": "strict"
}
```

**Step 5 · Code Generation** (74774 ms)
```json
{
  "files": [
    {
      "path": "package.json",
      "content": "{
  \"name\": \"proof-led-assurance\",
  \"version\": \"0.1.0\",
  \"private\": true,
  \"scripts\": {
    \"dev\": \"next dev\",
    \"build\": \"next build\",
    \"start\": \"next start\",
    \"lint\": \"next lint\"
  },
  \"dependencies\": {
    \"next\": \"14.2.5\",
    \"react\": \"18.3.1\",
    \"react-dom\": \"18.3.1\"
  },
  \"devDependencies\": {
    \"@types/node\": \"20.12.7\",
    \"@types/react\": \"18.3.3\",
    \"@types/react-dom\": \"18.3.0\",
    \"autoprefixer\": \"10.4.19\",
    \"postcss\": \"8.4.38\",
    \"tailwindcss\": \"3.4.7\",
    \"typescript\": \"5.4.5\"
  }
}
"
    },
    {
      "path": "next.config.js",
      "content": "/** @type {import('next').NextConfig} */
c
```

</details>

### B103
> Sleep and focus soundscape app with science-backed audio design for adults struggling with sleep onset or deep work — calm, dark-mode friendly with waveform visualizations, sound category previews, sleep improvement stats, and neuroscience credentials. Positioned against Calm as more focus-and-sleep-specific

| v0.dev · Baseline | SFT only | AI CDO · Best |
|:---:|:---:|:---:|
| ![v0](samples/B103/v0.png) | ![sft](samples/B103/sft.png) | ![aicdo](samples/B103/aicdo.png) |


<details>
<summary><strong>v0.dev · Baseline</strong> — 1 step</summary>

**Step 1 · Direct Generation** (14337 ms)
```json
import React from 'react';

export default function SoundscapeApp() {
  return (
    <div className="min-h-screen bg-white text-gray-900">
      {/* Navbar */}
      <nav className="border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <svg
                className="w-5 h-5 text-white"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V17a2 2 0 01-2 2h-1C9.716 19 3 12.284 3 4V3z" />
              </svg>
            </div>
            <span className="text-xl font-bold">SoundMind</span>
          </div>
          <div className="flex gap-6 t
```

</details>

<details>
<summary><strong>SFT only</strong> — 2 steps</summary>

**Step 2 · Classification** (2734 ms)
```json
{
  "product_type": "B2C SaaS",
  "industry": "healthcare",
  "page_type": "landing",
  "primary_user": "end_customer",
  "user_context": "first_time_visitor",
  "trust_sensitivity": "medium"
}
```

**Step 5 · Code Generation (no CDO strategy)** (95533 ms)
```json
{
  "files": [
    {
      "path": "src/app/page.tsx",
      "content": "```json
{
  \"files\": [
    {
      \"path\": \"src/app/page.tsx\",
      \"content\": \"export default function Home() {\n  return (\n    <div className=\\"min-h-screen bg-gray-950 text-gray-100\\">\n      {/* Sticky Nav */}\n      <nav className=\\"sticky top-0 z-50 bg-gray-950/90 backdrop-blur border-b border-gray-800\\">\n        <div className=\\"max-w-6xl mx-auto px-6 py-4 flex items-center justify-between\\">\n          <div className=\\"flex items-center gap-2\\">\n            <div className=\\"w-8 h-8 rounded-lg bg-indigo-500 flex items-center justify-center\\">\n              <svg width=\\"18\\" height=\\"18\\" viewBox=\\"0 0 18 18\\" fill=\\"none\\">\n                <path d
```

</details>

<details>
<summary><strong>AI CDO · Best</strong> — 5 steps</summary>

**Step 2 · Classification** (1204 ms)
```json
{
  "product_type": "B2C SaaS",
  "industry": "other",
  "page_type": "landing",
  "primary_user": "end_customer",
  "user_context": "first_time_visitor",
  "trust_sensitivity": "medium"
}
```

**Step 3 · CDO Strategy** (6019 ms)
```json
{
  "primary_intent": "increase_confidence",
  "key_risks": [
    "unclear_value_prop",
    "overpromising",
    "low_trust"
  ],
  "strategic_principles": [
    "credibility_over_creativity",
    "clarity_over_density",
    "confidence_before_action"
  ],
  "avoidances": [
    "marketing_fluff",
    "unsubstantiated_claims",
    "flashy_motion"
  ],
  "strategies": [
    {
      "name": "Science-Led Confidence",
      "intent": "authority_first",
      "hero_focus": "authority",
      "information_order": [
        "headline",
        "subheadline",
        "benefits",
        "product_demo",
        "testimonials",
        "primary_cta",
        "faq",
        "footer"
      ],
      "risk_controls": [
        "reinforce_authority",
        "increase_proof_density",
        "delay_cta"
      ],
      "rationale": "Lead with neuroscience credibility to differentiate from lifestyle-focused competitors and justify category-specific claims before asking for commitment."
    },
    {
    
```

**Step 3.5 · Brand Traits** (11809 ms)
```json
{
  "brand_name_suggestion": "Hush",
  "brand_personality": [
    "calm",
    "scientific",
    "immersive",
    "minimal",
    "trustworthy"
  ],
  "tone_of_voice": {
    "style": "quiet-confident",
    "characteristics": [
      "soft-spoken",
      "precise",
      "evocative",
      "unhurried"
    ],
    "avoid": [
      "hype",
      "exclamations",
      "jargon-heavy claims",
      "aggressive CTAs"
    ],
    "example_phrases": [
      "Sound, engineered for stillness.",
      "Fall asleep in 12 minutes. On average.",
      "Built with neuroscientists, tuned for your brain."
    ]
  },
  "visual_identity": {
    "aesthetic": "ambient-minimal",
    "design_language": "dark-first, generous whitespace, waveform-driven visuals, soft gradients evoking dusk and deep focus",
    "color_palette": {
      "primary": "#0B0F1A",
      "secondary": "#141A2B",
      "accent": "#7DA8FF",
      "accent_secondary": "#B8A4FF",
      "background": "#070912",
      "surface": "#0F1422",
      "t
```

**Step 4 · UI Intent** (3329 ms)
```json
{
  "primary_focus": "product_clarity",
  "cta_policy": {
    "timing": "delayed",
    "intensity": "soft"
  },
  "proof_policy": "balanced",
  "content_density": "low",
  "motion_policy": "subtle",
  "creative_license": "restricted",
  "language_style": "precise",
  "interaction_restraint": "moderate"
}
```

**Step 5 · Code Generation** (66650 ms)
```json
{
  "files": [
    {
      "path": "package.json",
      "content": "{
  \"name\": \"lumen-landing\",
  \"version\": \"0.1.0\",
  \"private\": true,
  \"scripts\": {
    \"dev\": \"next dev\",
    \"build\": \"next build\",
    \"start\": \"next start\",
    \"lint\": \"next lint\"
  },
  \"dependencies\": {
    \"next\": \"14.2.5\",
    \"react\": \"18.3.1\",
    \"react-dom\": \"18.3.1\"
  },
  \"devDependencies\": {
    \"@types/node\": \"20.11.30\",
    \"@types/react\": \"18.2.73\",
    \"@types/react-dom\": \"18.2.22\",
    \"autoprefixer\": \"10.4.19\",
    \"postcss\": \"8.4.38\",
    \"tailwindcss\": \"3.4.4\",
    \"typescript\": \"5.4.5\"
  }
}
"
    },
    {
      "path": "next.config.js",
      "content": "/** @type {import('next').NextConfig} */
modu
```

</details>

### B040
> Cash management and yield optimization platform for Series A–C startup CFOs managing $1M–$50M in cash — sophisticated, precise, and dark-mode premium with yield rate comparisons, FDIC coverage explainer, and VC-backed client logos. Positioned against Mercury as yield-optimized rather than just banking

| v0.dev · Baseline | SFT only | AI CDO · Best |
|:---:|:---:|:---:|
| ![v0](samples/B040/v0.png) | ![sft](samples/B040/sft.png) | ![aicdo](samples/B040/aicdo.png) |


<details>
<summary><strong>v0.dev · Baseline</strong> — 1 step</summary>

**Step 1 · Direct Generation** (11214 ms)
```json
'use client';

import { ArrowRight, BarChart3, Shield, Zap } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Navbar */}
      <nav className="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded bg-emerald-500 flex items-center justify-center font-bold text-sm">
              CF
            </div>
            <span className="font-semibold text-lg">CashFlow</span>
          </div>
          <div className="flex items-center gap-8">
            <a href="#features" className="text-slate-300 hover:text-white transition text-sm">
              Features
            </a>
            <a href="#security" className="text-slate-300 hover:text-white transition text-sm">
              Security
            </a
```

</details>

<details>
<summary><strong>SFT only</strong> — 2 steps</summary>

**Step 2 · Classification** (1621 ms)
```json
{
  "product_type": "B2B SaaS",
  "industry": "fintech",
  "page_type": "landing",
  "primary_user": "founder",
  "user_context": "evaluating",
  "trust_sensitivity": "high"
}
```

**Step 5 · Code Generation (no CDO strategy)** (84537 ms)
```json
{
  "files": [
    {
      "path": "src/app/page.tsx",
      "content": "```json\n{\n  \"files\": [\n    {\n      \"path\": \"src/app/page.tsx\",\n      \"content\": \"export default function Home() {\\n  return (\\n    <div className=\\\"min-h-screen bg-gray-950 text-gray-100\\\">\\n\\n      {/* Sticky Nav */}\\n      <nav className=\\\"sticky top-0 z-50 bg-gray-950/90 backdrop-blur border-b border-gray-800\\\">\\n        <div className=\\\"max-w-6xl mx-auto px-6 py-4 flex items-center justify-between\\\">\\n          <div className=\\\"flex items-center gap-2\\\">\\n            <div className=\\\"w-7 h-7 rounded-lg bg-indigo-500 flex items-center justify-center\\\">\\n              <span className=\\\"text-white text-xs font-bold\\\">Y</span>\\n            </div>\\n            <span clas
```

</details>

<details>
<summary><strong>AI CDO · Best</strong> — 5 steps</summary>

**Step 2 · Classification** (1517 ms)
```json
{
  "product_type": "B2B SaaS",
  "industry": "fintech",
  "page_type": "landing",
  "primary_user": "founder",
  "user_context": "evaluating",
  "trust_sensitivity": "high"
}
```

**Step 3 · CDO Strategy** (6642 ms)
```json
{
  "primary_intent": "signal_legitimacy",
  "key_risks": [
    "low_trust",
    "overpromising",
    "unclear_value_prop"
  ],
  "strategic_principles": [
    "credibility_over_creativity",
    "confidence_before_action",
    "clarity_over_density"
  ],
  "avoidances": [
    "marketing_fluff",
    "unsubstantiated_claims",
    "aggressive_ctas"
  ],
  "strategies": [
    {
      "name": "Authority-Led Legitimacy",
      "intent": "authority_first",
      "hero_focus": "authority",
      "information_order": [
        "headline",
        "subheadline",
        "security_compliance",
        "customer_logos",
        "benefits",
        "product_demo",
        "primary_cta",
        "faq",
        "footer"
      ],
      "risk_controls": [
        "reinforce_authority",
        "increase_proof_density",
        "delay_cta"
      ],
      "rationale": "CFOs custodying significant capital prioritize institutional credibility above all. Leading with regulatory posture and proof reduces per
```

**Step 3.5 · Brand Traits** (17215 ms)
```json
{
  "brand_personality": {
    "primary_traits": [
      "sophisticated",
      "precise",
      "authoritative",
      "data-driven"
    ],
    "tone": "confident-analytical",
    "formality": "high",
    "energy": "calm-deliberate"
  },
  "visual_identity": {
    "mode": "dark",
    "aesthetic": "premium-financial-terminal",
    "color_palette": {
      "background": "#0A0B0D",
      "surface": "#121418",
      "surface_elevated": "#1A1D23",
      "border": "#262A31",
      "border_subtle": "#1F232A",
      "text_primary": "#F5F7FA",
      "text_secondary": "#A1A8B3",
      "text_tertiary": "#6B7280",
      "accent_primary": "#7FFFB0",
      "accent_secondary": "#4ADE80",
      "accent_muted": "#1F3A2A",
      "data_positive": "#7FFFB0",
      "data_negative": "#F87171",
      "data_neutral": "#60A5FA"
    },
    "color_strategy": "Near-black canvas with mint-green yield accents to evoke financial terminals and Bloomberg-style precision; green signals yield/growth without being flash
```

**Step 4 · UI Intent** (2147 ms)
```json
{
  "primary_focus": "value_prop",
  "cta_policy": {
    "timing": "delayed",
    "intensity": "neutral"
  },
  "proof_policy": "heavy",
  "content_density": "medium",
  "motion_policy": "subtle",
  "creative_license": "restricted",
  "language_style": "precise",
  "interaction_restraint": "moderate"
}
```

**Step 5 · Code Generation** (95543 ms)
```json
{
  "files": [
    {
      "path": "package.json",
      "content": "{\n  \"name\": \"clarified-value-prop\",\n  \"version\": \"0.1.0\",\n  \"private\": true,\n  \"scripts\": {\n    \"dev\": \"next dev\",\n    \"build\": \"next build\",\n    \"start\": \"next start\",\n    \"lint\": \"next lint\"\n  },\n  \"dependencies\": {\n    \"next\": \"14.2.5\",\n    \"react\": \"18.3.1\",\n    \"react-dom\": \"18.3.1\"\n  },\n  \"devDependencies\": {\n    \"@types/node\": \"20.11.30\",\n    \"@types/react\": \"18.2.73\",\n    \"@types/react-dom\": \"18.2.22\",\n    \"autoprefixer\": \"10.4.19\",\n    \"postcss\": \"8.4.38\",\n    \"tailwindcss\": \"3.4.4\",\n    \"typescript\": \"5.4.5\"\n  }\n}\n"
    },
    {
      "path": "next.config.js",
      "content": "/** @type {import('next').NextConfig} *
```

</details>

### B037
> Micro-investment platform for first-generation investors from underrepresented backgrounds — empowering, accessible, and jargon-free with $5 minimum investment, diversification education, and SIPC protection. Positioned against Robinhood as education-first rather than trading-first

| v0.dev · Baseline | SFT only | AI CDO · Best |
|:---:|:---:|:---:|
| ![v0](samples/B037/v0.png) | ![sft](samples/B037/sft.png) | ![aicdo](samples/B037/aicdo.png) |


<details>
<summary><strong>v0.dev · Baseline</strong> — 1 step</summary>

**Step 1 · Direct Generation** (11809 ms)
```json
'use client';

import React from 'react';

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navbar */}
      <nav className="border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded"></div>
            <span className="text-xl font-semibold text-gray-900">InvestStart</span>
          </div>
          <div className="hidden md:flex gap-8">
            <a href="#" className="text-gray-600 hover:text-gray-900 text-sm">
              About
            </a>
            <a href="#" className="text-gray-600 hover:text-gray-900 text-sm">
              Features
            </a>
            <a href="#" className="text-gray-600 hover:text-gray-900 text-sm">
              Security
            </a>
            <a href="#" className="text-gray-600 hover:text-gray-900 text-
```

</details>

<details>
<summary><strong>SFT only</strong> — 2 steps</summary>

**Step 2 · Classification** (2095 ms)
```json
{
  "product_type": "B2C SaaS",
  "industry": "fintech",
  "page_type": "landing",
  "primary_user": "end_customer",
  "user_context": "first_time_visitor",
  "trust_sensitivity": "high"
}
```

**Step 5 · Code Generation (no CDO strategy)** (96007 ms)
```json
{
  "files": [
    {
      "path": "src/app/page.tsx",
      "content": "```json
{
  \"files\": [
    {
      \"path\": \"src/app/page.tsx\",
      \"content\": \"export default function Home() {\n  return (\n    <div className=\\"min-h-screen bg-white text-slate-800 font-sans\\">\n\n      {/* Sticky Nav */}\n      <header className=\\"sticky top-0 z-50 bg-white border-b border-slate-200 shadow-sm\\">\n        <div className=\\"max-w-6xl mx-auto px-6 py-4 flex items-center justify-between\\">\n          <div className=\\"flex items-center gap-2\\">\n            <div className=\\"w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center\\">\n              <span className=\\"text-white font-bold text-sm\\">S</span>\n            </div>\n            <span cl
```

</details>

<details>
<summary><strong>AI CDO · Best</strong> — 5 steps</summary>

**Step 2 · Classification** (1233 ms)
```json
{
  "product_type": "B2C SaaS",
  "industry": "fintech",
  "page_type": "landing",
  "primary_user": "end_customer",
  "user_context": "first_time_visitor",
  "trust_sensitivity": "high"
}
```

**Step 3 · CDO Strategy** (6148 ms)
```json
{
  "primary_intent": "increase_confidence",
  "key_risks": [
    "low_trust",
    "unclear_value_prop",
    "premature_cta"
  ],
  "strategic_principles": [
    "confidence_before_action",
    "clarity_over_density",
    "credibility_over_creativity"
  ],
  "avoidances": [
    "marketing_fluff",
    "aggressive_ctas",
    "unsubstantiated_claims"
  ],
  "strategies": [
    {
      "name": "Education-led confidence building",
      "intent": "trust_first",
      "hero_focus": "value_prop",
      "information_order": [
        "headline",
        "subheadline",
        "benefits",
        "product_demo",
        "security_compliance",
        "testimonials",
        "faq",
        "primary_cta",
        "footer"
      ],
      "risk_controls": [
        "delay_cta",
        "simplify_language",
        "increase_proof_density"
      ],
      "rationale": "Prioritizes lowering psychological barriers for first-time investors by leading with accessible value framing and education before an
```

**Step 3.5 · Brand Traits** (13887 ms)
```json
{
  "personality": {
    "primary_traits": [
      "empowering",
      "approachable",
      "trustworthy"
    ],
    "secondary_traits": [
      "warm",
      "confident",
      "educational"
    ],
    "voice": "friendly_human",
    "formality": "casual_professional",
    "energy": "calm_assured"
  },
  "visual_style": {
    "aesthetic": "warm_modern",
    "design_era": "2024_contemporary",
    "inspiration": [
      "Cash App approachability",
      "Ellevest empowerment",
      "Public.com community",
      "Acorns simplicity"
    ],
    "avoid": [
      "Wall Street imagery",
      "bull/bear iconography",
      "intimidating charts",
      "corporate stock photos",
      "neon trading aesthetics",
      "casino-like gamification"
    ]
  },
  "color_direction": {
    "palette_type": "warm_inclusive",
    "primary_hue": "deep_teal",
    "accent_hue": "warm_coral",
    "mood": "welcoming_grounded",
    "contrast_level": "high",
    "background_treatment": "soft_off_white_with_warm_
```

**Step 4 · UI Intent** (2192 ms)
```json
{
  "primary_focus": "social_proof",
  "cta_policy": {
    "timing": "delayed",
    "intensity": "soft"
  },
  "proof_policy": "heavy",
  "content_density": "low",
  "motion_policy": "subtle",
  "creative_license": "restricted",
  "language_style": "plain",
  "interaction_restraint": "moderate"
}
```

**Step 5 · Code Generation** (91036 ms)
```json
{
  "files": [
    {
      "path": "package.json",
      "content": "{
  \"name\": \"peer-validation-landing\",
  \"version\": \"0.1.0\",
  \"private\": true,
  \"scripts\": {
    \"dev\": \"next dev\",
    \"build\": \"next build\",
    \"start\": \"next start\",
    \"lint\": \"next lint\"
  },
  \"dependencies\": {
    \"next\": \"14.2.5\",
    \"react\": \"18.3.1\",
    \"react-dom\": \"18.3.1\"
  },
  \"devDependencies\": {
    \"@types/node\": \"20.12.12\",
    \"@types/react\": \"18.3.3\",
    \"@types/react-dom\": \"18.3.0\",
    \"autoprefixer\": \"10.4.19\",
    \"postcss\": \"8.4.38\",
    \"tailwindcss\": \"3.4.4\",
    \"typescript\": \"5.4.5\"
  }
}
"
    },
    {
      "path": "next.config.js",
      "content": "/** @type {import('next').NextConfig} 
```

</details>

### B021
> Teletherapy platform connecting adults 25–45 to therapists for anxiety, burnout, and life transitions — warm, safe, and non-clinical with HIPAA compliance, therapist matching quiz, and insurance coverage checker. Positioned against BetterHelp as more therapist-quality-focused

| v0.dev · Baseline | SFT only | AI CDO · Best |
|:---:|:---:|:---:|
| ![v0](samples/B021/v0.png) | ![sft](samples/B021/sft.png) | ![aicdo](samples/B021/aicdo.png) |


<details>
<summary><strong>v0.dev · Baseline</strong> — 1 step</summary>

**Step 1 · Direct Generation** (14829 ms)
```json
'use client';

import React from 'react';

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navbar */}
      <nav className="border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="text-2xl font-semibold text-blue-600">TherapyMatch</div>
          <div className="hidden md:flex gap-8 text-sm text-gray-700">
            <a href="#" className="hover:text-blue-600 transition">How it Works</a>
            <a href="#" className="hover:text-blue-600 transition">About</a>
            <a href="#" className="hover:text-blue-600 transition">Insurance</a>
            <a href="#" className="hover:text-blue-600 transition">Contact</a>
          </div>
          <button className="bg-blue-600 text-white px-6 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition">
            Start Quiz
          </button>
        </div>
      </nav>

      {
```

</details>

<details>
<summary><strong>SFT only</strong> — 2 steps</summary>

**Step 2 · Classification** (1482 ms)
```json
{
  "product_type": "marketplace",
  "industry": "healthcare",
  "page_type": "landing",
  "primary_user": "end_customer",
  "user_context": "evaluating",
  "trust_sensitivity": "high"
}
```

**Step 5 · Code Generation (no CDO strategy)** (93267 ms)
```json
{
  "files": [
    {
      "path": "src/app/page.tsx",
      "content": "{\"files\":[{\"path\":\"src/app/page.tsx\",\"content\":\"'use client';\nimport { useState } from 'react';\nimport {\n  Heart,\n  Shield,\n  Star,\n  CheckCircle,\n  ArrowRight,\n  Menu,\n  X,\n  Clock,\n  Users,\n  Award,\n  Lock,\n  ChevronRight,\n  Sparkles,\n  Brain,\n  Leaf,\n} from 'lucide-react';\n\nexport default function Home() {\n  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);\n\n  return (\n    <div className=\\"min-h-screen bg-[#FAFAF8] text-[#1C1C1E] font-sans\\">\n      {/* Sticky Nav */}\n      <nav className=\\"sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-[#E8E4DE]\\">\n        <div className=\\"max-w-6xl mx-auto px-6 py-4 flex items-cente
```

</details>

<details>
<summary><strong>AI CDO · Best</strong> — 5 steps</summary>

**Step 2 · Classification** (1297 ms)
```json
{
  "product_type": "B2C SaaS",
  "industry": "healthcare",
  "page_type": "landing",
  "primary_user": "end_customer",
  "user_context": "first_time_visitor",
  "trust_sensitivity": "high"
}
```

**Step 3 · CDO Strategy** (6045 ms)
```json
{
  "primary_intent": "signal_legitimacy",
  "key_risks": [
    "low_trust",
    "overpromising",
    "premature_cta"
  ],
  "strategic_principles": [
    "credibility_over_creativity",
    "confidence_before_action",
    "clarity_over_density"
  ],
  "avoidances": [
    "unsubstantiated_claims",
    "aggressive_ctas",
    "marketing_fluff"
  ],
  "strategies": [
    {
      "name": "Credibility-Led Reassurance",
      "intent": "trust_first",
      "hero_focus": "value_prop",
      "information_order": [
        "headline",
        "subheadline",
        "security_compliance",
        "benefits",
        "testimonials",
        "product_demo",
        "primary_cta",
        "faq",
        "footer"
      ],
      "risk_controls": [
        "delay_cta",
        "increase_proof_density",
        "simplify_language"
      ],
      "rationale": "In a high-sensitivity healthcare context for first-time visitors, leading with safety, compliance, and human reassurance reduces skepticism before
```

**Step 3.5 · Brand Traits** (13400 ms)
```json
{
  "brand_personality": {
    "primary_traits": [
      "warm",
      "trustworthy",
      "calming",
      "human"
    ],
    "tone_of_voice": "empathetic_conversational",
    "formality_level": "casual_professional",
    "emotional_register": "reassuring"
  },
  "visual_identity": {
    "design_style": "soft_modern_editorial",
    "aesthetic_direction": "warm_minimal_with_organic_touches",
    "visual_metaphor": "safe_space_natural_light",
    "imagery_style": "candid_lifestyle_photography",
    "illustration_style": "soft_organic_shapes",
    "iconography": "rounded_outline_friendly"
  },
  "color_system": {
    "palette_type": "warm_earthy_calming",
    "primary_color": {
      "hue": "sage_green",
      "hex": "#5C7F6B",
      "rationale": "Evokes calm, growth, and natural healing without clinical sterility"
    },
    "secondary_color": {
      "hue": "warm_terracotta",
      "hex": "#D4906F",
      "rationale": "Adds human warmth and approachability"
    },
    "accent_color": 
```

**Step 4 · UI Intent** (1991 ms)
```json
{
  "primary_focus": "product_clarity",
  "cta_policy": {
    "timing": "progressive",
    "intensity": "soft"
  },
  "proof_policy": "balanced",
  "content_density": "low",
  "motion_policy": "subtle",
  "creative_license": "restricted",
  "language_style": "plain",
  "interaction_restraint": "moderate"
}
```

**Step 5 · Code Generation** (60994 ms)
```json
{
  "files": [
    {
      "path": "package.json",
      "content": "{
  \"name\": \"guided-understanding\",
  \"version\": \"0.1.0\",
  \"private\": true,
  \"scripts\": {
    \"dev\": \"next dev\",
    \"build\": \"next build\",
    \"start\": \"next start\",
    \"lint\": \"next lint\"
  },
  \"dependencies\": {
    \"next\": \"14.2.5\",
    \"react\": \"18.3.1\",
    \"react-dom\": \"18.3.1\"
  },
  \"devDependencies\": {
    \"@types/node\": \"20.11.0\",
    \"@types/react\": \"18.3.3\",
    \"@types/react-dom\": \"18.3.0\",
    \"autoprefixer\": \"10.4.19\",
    \"postcss\": \"8.4.39\",
    \"tailwindcss\": \"3.4.7\",
    \"typescript\": \"5.4.5\"
  }
}
"
    },
    {
      "path": "next.config.js",
      "content": "/** @type {import('next').NextConfig} */

```

</details>

### B007
> AI contract review and redlining platform for in-house counsel and legal ops at mid-market companies, offering bar association-endorsed accuracy with Fortune 500 client validation — positioned against Ironclad as more affordable for non-enterprise legal teams

| v0.dev · Baseline | SFT only | AI CDO · Best |
|:---:|:---:|:---:|
| ![v0](samples/B007/v0.png) | ![sft](samples/B007/sft.png) | ![aicdo](samples/B007/aicdo.png) |


<details>
<summary><strong>v0.dev · Baseline</strong> — 1 step</summary>

**Step 1 · Direct Generation** (17232 ms)
```json
'use client';

import React from 'react';

export default function Page() {
  return (
    <div className="min-h-screen flex flex-col bg-white">
      {/* Navbar */}
      <nav className="border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded"></div>
            <span className="text-xl font-semibold text-gray-900">ContractAI</span>
          </div>
          <div className="flex items-center gap-8">
            <a href="#features" className="text-sm text-gray-600 hover:text-gray-900">Features</a>
            <a href="#accuracy" className="text-sm text-gray-600 hover:text-gray-900">Why Us</a>
            <a href="#pricing" className="text-sm text-gray-600 hover:text-gray-900">Pricing</a>
            <button className="px-4 py-2 bg-blue-600 text-white text-sm rounded hover:bg-blue-700">
              Get Started
         
```

</details>

<details>
<summary><strong>SFT only</strong> — 2 steps</summary>

**Step 2 · Classification** (1121 ms)
```json
{
  "product_type": "B2B SaaS",
  "industry": "fintech_compliance",
  "page_type": "landing",
  "primary_user": "compliance_officer",
  "user_context": "evaluating",
  "trust_sensitivity": "high"
}
```

**Step 5 · Code Generation (no CDO strategy)** (101584 ms)
```json
{
  "files": [
    {
      "path": "src/app/page.tsx",
      "content": "```json
{
  \"files\": [
    {
      \"path\": \"src/app/page.tsx\",
      \"content\": \"\\"use client\\";\nimport {\n  Shield,\n  CheckCircle,\n  Zap,\n  FileText,\n  BarChart2,\n  Lock,\n  ArrowRight,\n  Star,\n  Users,\n  Clock,\n  Award,\n  ChevronRight,\n  Menu,\n  X,\n} from \\"lucide-react\\";\nimport { useState } from \\"react\\";\n\nexport default function Home() {\n  const [menuOpen, setMenuOpen] = useState(false);\n\n  return (\n    <div className=\\"min-h-screen bg-[#0A0F1E] text-white font-sans\\">\n      {/* STICKY NAV */}\n      <nav className=\\"sticky top-0 z-50 bg-[#0A0F1E]/95 backdrop-blur border-b border-white/10\\">\n        <div className=\\"max-w-7xl mx
```

</details>

<details>
<summary><strong>AI CDO · Best</strong> — 5 steps</summary>

**Step 2 · Classification** (1243 ms)
```json
{
  "product_type": "B2B SaaS",
  "industry": "other",
  "page_type": "landing",
  "primary_user": "operations_manager",
  "user_context": "evaluating",
  "trust_sensitivity": "high"
}
```

**Step 3 · CDO Strategy** (6490 ms)
```json
{
  "primary_intent": "signal_legitimacy",
  "key_risks": [
    "low_trust",
    "unclear_value_prop",
    "overpromising"
  ],
  "strategic_principles": [
    "credibility_over_creativity",
    "confidence_before_action",
    "clarity_over_density"
  ],
  "avoidances": [
    "marketing_fluff",
    "unsubstantiated_claims",
    "aggressive_ctas"
  ],
  "strategies": [
    {
      "name": "Authority-Led Validation",
      "intent": "authority_first",
      "hero_focus": "authority",
      "information_order": [
        "headline",
        "subheadline",
        "security_compliance",
        "customer_logos",
        "benefits",
        "product_demo",
        "primary_cta",
        "faq",
        "footer"
      ],
      "risk_controls": [
        "reinforce_authority",
        "increase_proof_density",
        "delay_cta"
      ],
      "rationale": "Lead with institutional endorsement and enterprise validation to establish legitimacy before any persuasion, addressing the high trust se
```

**Step 3.5 · Brand Traits** (9881 ms)
```json
{
  "brand_personality": {
    "primary_traits": [
      "authoritative",
      "precise",
      "trustworthy"
    ],
    "tone": "professional",
    "formality_level": "formal"
  },
  "visual_style": {
    "design_language": "editorial-minimal",
    "aesthetic": "legal-professional",
    "visual_density": "balanced",
    "decorative_elements": "minimal"
  },
  "color_direction": {
    "palette_type": "monochromatic-with-accent",
    "primary_hue": "deep-navy",
    "accent_hue": "burgundy",
    "neutral_base": "warm-ivory",
    "saturation": "low",
    "brightness": "medium-light",
    "contrast_level": "high",
    "mood": "serious-establishment"
  },
  "typography_direction": {
    "font_personality": "editorial-serif-pairing",
    "heading_style": "transitional-serif",
    "body_style": "neutral-sans",
    "type_scale_contrast": "high",
    "letter_spacing_feel": "precise",
    "rationale": "Serif headings convey legal tradition and authority while a clean sans body ensures scannable
```

**Step 4 · UI Intent** (2090 ms)
```json
{
  "primary_focus": "value_prop",
  "cta_policy": {
    "timing": "delayed",
    "intensity": "neutral"
  },
  "proof_policy": "heavy",
  "content_density": "medium",
  "motion_policy": "subtle",
  "creative_license": "restricted",
  "language_style": "precise",
  "interaction_restraint": "moderate"
}
```

**Step 5 · Code Generation** (65766 ms)
```json
{
  "files": [
    {
      "path": "package.json",
      "content": "{
  \"name\": \"clarity-landing\",
  \"version\": \"0.1.0\",
  \"private\": true,
  \"scripts\": {
    \"dev\": \"next dev\",
    \"build\": \"next build\",
    \"start\": \"next start\",
    \"lint\": \"next lint\"
  },
  \"dependencies\": {
    \"next\": \"14.2.5\",
    \"react\": \"18.3.1\",
    \"react-dom\": \"18.3.1\"
  },
  \"devDependencies\": {
    \"@types/node\": \"20.12.7\",
    \"@types/react\": \"18.3.3\",
    \"@types/react-dom\": \"18.3.0\",
    \"autoprefixer\": \"10.4.19\",
    \"postcss\": \"8.4.38\",
    \"tailwindcss\": \"3.4.7\",
    \"typescript\": \"5.4.5\"
  }
}
"
    },
    {
      "path": "next.config.js",
      "content": "/** @type {import('next').NextConfig} */
const
```

</details>
