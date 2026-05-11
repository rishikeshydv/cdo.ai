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
### B037
> Micro-investment platform for first-generation investors from underrepresented backgrounds — empowering, accessible, and jargon-free with $5 minimum investment, diversification education, and SIPC protection. Positioned against Robinhood as education-first rather than trading-first

| v0.dev · Baseline | SFT only | AI CDO · Best |
|:---:|:---:|:---:|
| ![v0](samples/B037/v0.png) | ![sft](samples/B037/sft.png) | ![aicdo](samples/B037/aicdo.png) |


<details>
<summary><strong>v0.dev · Baseline</strong> — 1 step</summary>

**Step 1 · Direct Generation** (12219 ms)
```json
'use client';

import React from 'react';

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navbar */}
      <nav className="border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded"></div>
            <span className="text-xl font-semibold text-gray-900">InvestStart</span>
          </div>
          <div className="hidden md:flex space-x-8">
            <a href="#features" className="text-gray-600 hover:text-gray-900 text-sm">
              Features
            </a>
            <a href="#" className="text-gray-600 hover:text-gray-900 text-sm">
              Learn
            </a>
            <a href="#" className="text-gray-600 hover:text-gray-900 text-sm">
              About
            </a>
            <a href="#" className="text-gray-600 hover:text-g
```

</details>

<details>
<summary><strong>SFT only</strong> — 2 steps</summary>

**Step 2 · Classification** (971 ms)
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

**Step 5 · Code Generation (no CDO strategy)** (97154 ms)
```json
{
  "files": [
    {
      "path": "src/app/page.tsx",
      "content": "{\"files\":[{\"path\":\"src/app/page.tsx\",\"content\":\"\\\"use client\\\";\\nimport {\\n  Shield,\\n  TrendingUp,\\n  BookOpen,\\n  DollarSign,\\n  Users,\\n  CheckCircle,\\n  ArrowRight,\\n  Star,\\n  Layers,\\n  Lock,\\n  ChevronRight,\\n  BarChart2,\\n  Zap,\\n} from \\\"lucide-react\\\";\\n\\nexport default function Home() {\\n  return (\\n    <div className=\\\"min-h-screen bg-[#0a0f1e] text-white font-sans\\\">\\n      {/* NAV */}\\n      <nav className=\\\"sticky top-0 z-50 bg-[#0a0f1e]/90 backdrop-blur-md border-b border-white/10\\\">\\n        <div className=\\\"max-w-7xl mx-auto px-6 py-4 flex items-center justify-between\\\">\\n          <div className=\\\"flex items-center gap-2\\\">\\n            <div c
```

</details>

<details>
<summary><strong>AI CDO · Best</strong> — 5 steps</summary>

**Step 2 · Classification** (1345 ms)
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

**Step 3 · CDO Strategy** (7263 ms)
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
      "name": "Education-Led Confidence Build",
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
      "rationale": "First-generation investors need understanding before commitment. Leading with accessible value framing and education establishes psychol
```

**Step 3.5 · Brand Traits** (12956 ms)
```json
{
  "brand_personality": {
    "primary_traits": [
      "empowering",
      "approachable",
      "trustworthy"
    ],
    "secondary_traits": [
      "educational",
      "inclusive",
      "confident"
    ],
    "tone_of_voice": "warm_clear_encouraging",
    "formality_level": "casual_professional",
    "emotional_register": "uplifting_and_reassuring"
  },
  "visual_style": {
    "design_language": "modern_friendly_editorial",
    "aesthetic_direction": "soft_minimalism_with_human_warmth",
    "visual_complexity": "moderate",
    "whitespace_usage": "generous",
    "imagery_style": "diverse_real_people_and_illustrative_charts",
    "iconography": "rounded_simple_didactic",
    "data_visualization": "simplified_annotated_friendly",
    "motion_principles": "gentle_purposeful_guiding"
  },
  "color_direction": {
    "palette_type": "warm_optimistic_with_trust_anchor",
    "primary_hue_family": "deep_teal_or_indigo",
    "accent_hue_family": "warm_coral_or_golden_yellow",
    "neutral_
```

**Step 4 · UI Intent** (2189 ms)
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
  "language_style": "plain",
  "interaction_restraint": "moderate"
}
```

**Step 5 · Code Generation** (55398 ms)
```json
{
  "files": [
    {
      "path": "package.json",
      "content": "{\n  \"name\": \"accessible-investing\",\n  \"version\": \"0.1.0\",\n  \"private\": true,\n  \"scripts\": {\n    \"dev\": \"next dev\",\n    \"build\": \"next build\",\n    \"start\": \"next start\",\n    \"lint\": \"next lint\"\n  },\n  \"dependencies\": {\n    \"next\": \"14.2.5\",\n    \"react\": \"18.3.1\",\n    \"react-dom\": \"18.3.1\"\n  },\n  \"devDependencies\": {\n    \"@types/node\": \"20.12.12\",\n    \"@types/react\": \"18.3.3\",\n    \"@types/react-dom\": \"18.3.0\",\n    \"autoprefixer\": \"10.4.19\",\n    \"postcss\": \"8.4.38\",\n    \"tailwindcss\": \"3.4.4\",\n    \"typescript\": \"5.4.5\"\n  }\n}\n"
    },
    {
      "path": "next.config.js",
      "content": "/** @type {import('next').NextConfig} */\
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
