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

**Step 1 · Direct Generation** (13003 ms)
```json
import type { ReactNode } from 'react';

const Navbar = () => (
  <nav className="bg-white border-b border-gray-200">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex justify-between items-center h-16">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-blue-600 rounded"></div>
          <span className="text-xl font-bold text-gray-900">Scriptwise</span>
        </div>
        <div className="flex gap-8 items-center">
          <a href="#features" className="text-gray-700 hover:text-gray-900">Features</a>
          <a href="#testimonials" className="text-gray-700 hover:text-gray-900">Testimonials</a>
          <a href="#pricing" className="text-gray-700 hover:text-gray-900">Pricing</a>
          <button className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700">
            Sign In
          </button>
        </div>
      </div>
    </div>
  </nav>
);

const Hero = () => (
  <section className="bg-wh
```

</details>

<details>
<summary><strong>SFT only</strong> — 2 steps</summary>

**Step 2 · Classification** (1301 ms)
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

**Step 5 · Code Generation (no CDO strategy)** (105979 ms)
```json
{
  "files": [
    {
      "path": "src/app/page.tsx",
      "content": "```json\n{\n  \"files\": [\n    {\n      \"path\": \"src/app/page.tsx\",\n      \"content\": \"\\\"use client\\\";\\nimport { useState } from \\\"react\\\";\\nimport {\\n  Film,\\n  Zap,\\n  BookOpen,\\n  BarChart3,\\n  Users,\\n  Star,\\n  ChevronRight,\\n  Menu,\\n  X,\\n  CheckCircle,\\n  Award,\\n  FileText,\\n  Layers,\\n  Sparkles,\\n  ArrowRight,\\n  Shield,\\n} from \\\"lucide-react\\\";\\n\\nexport default function Home() {\\n  const [mobileOpen, setMobileOpen] = useState(false);\\n\\n  const features = [\\n    {\\n      icon: <Sparkles className=\\\"w-6 h-6\\\" />,\\n      title: \\\"AI Scene Intelligence\\\",\\n      desc: \\\"Generate scene suggestions, dialogue alternatives, and dramatic tension notes in 
```

</details>

<details>
<summary><strong>AI CDO · Best</strong> — 5 steps</summary>

**Step 2 · Classification** (1977 ms)
```json
{
  "product_type": "B2C SaaS",
  "industry": "ai_platform",
  "page_type": "landing",
  "primary_user": "end_customer",
  "user_context": "first_time_visitor",
  "trust_sensitivity": "medium"
}
```

**Step 3 · CDO Strategy** (8328 ms)
```json
{
  "primary_intent": "accelerate_understanding",
  "key_risks": [
    "unclear_value_prop",
    "overpromising",
    "low_trust"
  ],
  "strategic_principles": [
    "credibility_over_creativity",
    "confidence_before_action",
    "clarity_over_novelty"
  ],
  "avoidances": [
    "marketing_fluff",
    "unsubstantiated_claims",
    "flashy_motion"
  ],
  "strategies": [
    {
      "intent": "product_first",
      "hero_focus": "product_visual",
      "information_order": [
        "headline",
        "subheadline",
        "product_demo",
        "benefits",
        "testimonials",
        "primary_cta",
        "footer"
      ],
      "risk_controls": [
        "simplify_language",
        "delay_cta"
      ],
      "rationale": "Lead with tangible demonstration of the craft tooling so creative professionals immediately grasp differentiation versus incumbents, reducing skepticism through evidence rather than claims."
    },
    {
      "intent": "trust_first",
      "hero_focus": 
```

**Step 3.5 · Brand Traits** (19955 ms)
```json
{
  "visual_tone": {
    "mood": [
      "cinematic",
      "auteur",
      "nocturnal",
      "craft-reverent",
      "underground-prestige"
    ],
    "energy": "contemplative",
    "formality": "editorial",
    "rationale": "A filmmaker-peer authority posture demands the hush of a darkened theater and the gravitas of a film journal \u2014 not startup gloss. The mood evokes late-night writing rooms, festival screening halls, and the reverence of craft, signaling this is a serious instrument for serious storytellers."
  },
  "brand_personality": {
    "primary_traits": [
      "craft-obsessed",
      "quietly-confident",
      "cinephile-literate",
      "peer-not-vendor"
    ],
    "voice": "A working screenwriter who has been in the trenches \u2014 speaks in scene terms, references beat sheets and act breaks naturally, respects the page, and treats AI as a collaborator at the writers' table rather than a magic shortcut.",
    "differentiation": "Where Final Draft feels like industry
```

**Step 4 · UI Intent** (2123 ms)
```json
{
  "primary_focus": "authority",
  "cta_policy": {
    "timing": "delayed",
    "intensity": "soft"
  },
  "proof_policy": "balanced",
  "content_density": "medium",
  "motion_policy": "subtle",
  "creative_license": "restricted",
  "language_style": "confident",
  "interaction_restraint": "moderate"
}
```

**Step 5 · Code Generation** (90057 ms)
```json
{
  "files": [
    {
      "path": "package.json",
      "content": "{\n  \"name\": \"craft-screenwriting\",\n  \"version\": \"0.1.0\",\n  \"private\": true,\n  \"scripts\": {\n    \"dev\": \"next dev\",\n    \"build\": \"next build\",\n    \"start\": \"next start\",\n    \"lint\": \"next lint\"\n  },\n  \"dependencies\": {\n    \"next\": \"14.2.5\",\n    \"react\": \"18.3.1\",\n    \"react-dom\": \"18.3.1\"\n  },\n  \"devDependencies\": {\n    \"@types/node\": \"20.11.30\",\n    \"@types/react\": \"18.2.66\",\n    \"@types/react-dom\": \"18.2.22\",\n    \"autoprefixer\": \"10.4.19\",\n    \"postcss\": \"8.4.38\",\n    \"tailwindcss\": \"3.4.4\",\n    \"typescript\": \"5.4.5\"\n  }\n}\n"
    },
    {
      "path": "next.config.js",
      "content": "/** @type {import('next').NextConfig} */
```

</details>

### B126
> Digital services portal for a mid-size city government enabling residents to complete permits, payments, and city services online — clear, accessible, WCAG AAA compliant with plain language, services catalog, average task completion time, and accessibility score. Positioned as replacing in-person city hall visits with digital-first services

| v0.dev · Baseline | SFT only | AI CDO · Best |
|:---:|:---:|:---:|
| ![v0](samples/B126/v0.png) | ![sft](samples/B126/sft.png) | ![aicdo](samples/B126/aicdo.png) |


<details>
<summary><strong>v0.dev · Baseline</strong> — 1 step</summary>

**Step 1 · Direct Generation** (14355 ms)
```json
import React from 'react';

export default function HomePage() {
  return (
    <div className="flex flex-col min-h-screen bg-white">
      {/* Navbar */}
      <nav className="border-b border-gray-200 sticky top-0 bg-white z-50">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-md flex items-center justify-center">
              <span className="text-white font-bold text-sm">CH</span>
            </div>
            <span className="font-semibold text-lg text-gray-900">City Hall Portal</span>
          </div>
          <div className="flex gap-8 items-center">
            <a href="#services" className="text-gray-700 hover:text-gray-900 text-sm font-medium">Services</a>
            <a href="#accessibility" className="text-gray-700 hover:text-gray-900 text-sm font-medium">Accessibility</a>
            <a href="#support" className="text-gray-70
```

</details>

<details>
<summary><strong>SFT only</strong> — 2 steps</summary>

**Step 2 · Classification** (3167 ms)
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

**Step 5 · Code Generation (no CDO strategy)** (94667 ms)
```json
{
  "files": [
    {
      "path": "src/app/page.tsx",
      "content": "{\"files\":[{\"path\":\"src/app/page.tsx\",\"content\":\"'use client';\\n\\nimport {\\n  CheckCircle,\\n  Clock,\\n  FileText,\\n  CreditCard,\\n  Home,\\n  Car,\\n  Leaf,\\n  Shield,\\n  Star,\\n  ChevronRight,\\n  Menu,\\n  X,\\n  Accessibility,\\n  BarChart3,\\n  Users,\\n  Zap,\\n  Phone,\\n  Mail,\\n  MapPin,\\n  ArrowRight,\\n  Building2,\\n  Globe,\\n} from 'lucide-react';\\nimport { useState } from 'react';\\n\\nexport default function Page() {\\n  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);\\n\\n  const services = [\\n    { icon: FileText, label: 'Building Permits', time: '8 min', color: 'bg-blue-50 text-blue-700 border-blue-100' },\\n    { icon: CreditCard, label: 'Pay Utility Bills', time: 
```

</details>

<details>
<summary><strong>AI CDO · Best</strong> — 5 steps</summary>

**Step 2 · Classification** (1254 ms)
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

**Step 3 · CDO Strategy** (5698 ms)
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
    "confidence_before_action"
  ],
  "avoidances": [
    "marketing_fluff",
    "visual_clutter",
    "flashy_motion"
  ],
  "strategies": [
    {
      "name": "Service-Led Clarity",
      "intent": "product_first",
      "hero_focus": "value_prop",
      "information_order": [
        "headline",
        "subheadline",
        "product_demo",
        "benefits",
        "security_compliance",
        "primary_cta",
        "faq",
        "footer"
      ],
      "risk_controls": [
        "simplify_language",
        "limit_choices"
      ],
      "rationale": "Prioritize immediate comprehension of available services so residents quickly understand what they can accomplish online, reducing confusion for first-time visitors."
    },
    {
      "name": "Civic A
```

**Step 3.5 · Brand Traits** (14562 ms)
```json
{
  "brand_personality": {
    "primary_traits": [
      "trustworthy",
      "accessible",
      "civic",
      "transparent"
    ],
    "tone": "clear, plain-spoken, respectful, reassuring",
    "voice_attributes": [
      "plain-language",
      "neutral",
      "informative",
      "human"
    ]
  },
  "visual_identity": {
    "design_language": "civic-modern",
    "aesthetic": "clean, utilitarian, dignified, accessible-first with generous whitespace and high-legibility hierarchy",
    "visual_weight": "balanced",
    "complexity": "minimal"
  },
  "color_strategy": {
    "palette_type": "institutional",
    "primary_color": "#1B4D89",
    "secondary_color": "#0B7A3B",
    "accent_color": "#C8511C",
    "neutral_base": "#F5F6F7",
    "text_primary": "#0E1726",
    "background": "#FFFFFF",
    "semantic_colors": {
      "success": "#0B7A3B",
      "warning": "#A86A00",
      "error": "#B3261E",
      "info": "#1B4D89"
    },
    "contrast_level": "AAA",
    "rationale": "Deep civic 
```

**Step 4 · UI Intent** (2029 ms)
```json
{
  "primary_focus": "value_prop",
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

**Step 5 · Code Generation** (81153 ms)
```json
{
  "files": [
    {
      "path": "package.json",
      "content": "{\n  \"name\": \"civic-portal\",\n  \"version\": \"0.1.0\",\n  \"private\": true,\n  \"scripts\": {\n    \"dev\": \"next dev\",\n    \"build\": \"next build\",\n    \"start\": \"next start\",\n    \"lint\": \"next lint\"\n  },\n  \"dependencies\": {\n    \"next\": \"14.2.5\",\n    \"react\": \"18.3.1\",\n    \"react-dom\": \"18.3.1\"\n  },\n  \"devDependencies\": {\n    \"@types/node\": \"20.11.30\",\n    \"@types/react\": \"18.2.74\",\n    \"@types/react-dom\": \"18.2.24\",\n    \"autoprefixer\": \"10.4.19\",\n    \"postcss\": \"8.4.38\",\n    \"tailwindcss\": \"3.4.4\",\n    \"typescript\": \"5.4.5\"\n  }\n}\n"
    },
    {
      "path": "next.config.js",
      "content": "/** @type {import('next').NextConfig} */\nmodul
```

</details>

### B077
> Direct-to-consumer electric commuter bike brand for urban commuters 25–45 seeking a car replacement — bold, high-contrast, and performance-forward with range stats, commute cost savings calculator, and test ride finder. Positioned against entry-level e-bikes as more commuter-engineered

| v0.dev · Baseline | SFT only | AI CDO · Best |
|:---:|:---:|:---:|
| ![v0](samples/B077/v0.png) | ![sft](samples/B077/sft.png) | ![aicdo](samples/B077/aicdo.png) |


<details>
<summary><strong>v0.dev · Baseline</strong> — 1 step</summary>

**Step 1 · Direct Generation** (14134 ms)
```json
import React from 'react';

export default function Home() {
  const [commuteDays, setCommuteDays] = React.useState(20);
  const [distancePerDay, setDistancePerDay] = React.useState(10);
  
  const monthlySavings = Math.round((commuteDays * distancePerDay * 0.15) / 100 * 1000);

  return (
    <div className="min-h-screen bg-white">
      {/* Navbar */}
      <nav className="border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-black rounded-full"></div>
            <span className="font-bold text-lg">UrbanPulse</span>
          </div>
          <div className="flex items-center gap-8">
            <a href="#features" className="text-sm text-gray-600 hover:text-black">Features</a>
            <a href="#savings" className="text-sm text-gray-600 hover:text-black">Savings</a>
            <a href="#footer" className="text-sm
```

</details>

<details>
<summary><strong>SFT only</strong> — 2 steps</summary>

**Step 2 · Classification** (1230 ms)
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

**Step 5 · Code Generation (no CDO strategy)** (102277 ms)
```json
{
  "files": [
    {
      "path": "src/app/page.tsx",
      "content": "```json\n{\n  \"files\": [\n    {\n      \"path\": \"src/app/page.tsx\",\n      \"content\": \"\\\"use client\\\";\\nimport { useState } from \\\"react\\\";\\nimport {\\n  Zap,\\n  MapPin,\\n  TrendingDown,\\n  Shield,\\n  Wind,\\n  Battery,\\n  ChevronRight,\\n  Star,\\n  ArrowRight,\\n  Check,\\n  Menu,\\n  X,\\n  Bike,\\n  DollarSign,\\n  Clock,\\n  Leaf,\\n} from \\\"lucide-react\\\";\\n\\nexport default function Home() {\\n  const [mobileOpen, setMobileOpen] = useState(false);\\n  const [miles, setMiles] = useState(10);\\n  const [daysPerWeek, setDaysPerWeek] = useState(5);\\n\\n  const gasCostPerMile = 0.18;\\n  const ebikeCostPerMile = 0.01;\\n  const weeklyGas = miles * 2 * daysPerWeek * gasCostPerMile;\\n  co
```

</details>

<details>
<summary><strong>AI CDO · Best</strong> — 5 steps</summary>

**Step 2 · Classification** (2313 ms)
```json
{
  "product_type": "content_site",
  "industry": "ecommerce",
  "page_type": "landing",
  "primary_user": "end_customer",
  "user_context": "first_time_visitor",
  "trust_sensitivity": "medium"
}
```

**Step 3 · CDO Strategy** (5928 ms)
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
      "name": "Performance Proof",
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
        "increase_proof_density",
        "simplify_language"
      ],
      "rationale": "Lead with concrete commuter-engineered differentiation and quantified performance to establish category superiority before inviting action."
    },
    {
      "name": "Confidence Through Utility",

```

**Step 3.5 · Brand Traits** (14195 ms)
```json
{
  "brand_personality": {
    "primary_traits": [
      "bold",
      "performance-driven",
      "engineered",
      "confident"
    ],
    "tone": "assertive and technical with urban edge",
    "voice_attributes": [
      "direct",
      "spec-forward",
      "punchy",
      "credible"
    ]
  },
  "visual_identity": {
    "aesthetic": "high-contrast performance tech",
    "design_language": "industrial-modern with motorsport influence",
    "visual_weight": "heavy",
    "imagery_style": "cinematic urban commute photography with motion blur, dawn cityscapes, and detail shots of engineered components"
  },
  "color_direction": {
    "palette_type": "high_contrast_mono_with_accent",
    "primary_mood": "electric and decisive",
    "background_treatment": "deep near-black with sharp white space breaks",
    "suggested_palette": {
      "base": "#0A0A0B",
      "surface": "#15161A",
      "text_primary": "#F5F5F2",
      "text_secondary": "#9A9CA3",
      "accent_primary": "#D7FF1E",
  
```

**Step 4 · UI Intent** (3394 ms)
```json
{
  "primary_focus": "social_proof",
  "cta_policy": {
    "timing": "delayed",
    "intensity": "assertive"
  },
  "proof_policy": "heavy",
  "content_density": "medium",
  "motion_policy": "subtle",
  "creative_license": "restricted",
  "language_style": "confident",
  "interaction_restraint": "moderate"
}
```

**Step 5 · Code Generation** (58976 ms)
```json
{
  "files": [
    {
      "path": "package.json",
      "content": "{\n  \"name\": \"validated-conversion\",\n  \"version\": \"0.1.0\",\n  \"private\": true,\n  \"scripts\": {\n    \"dev\": \"next dev\",\n    \"build\": \"next build\",\n    \"start\": \"next start\",\n    \"lint\": \"next lint\"\n  },\n  \"dependencies\": {\n    \"next\": \"14.2.5\",\n    \"react\": \"18.3.1\",\n    \"react-dom\": \"18.3.1\"\n  },\n  \"devDependencies\": {\n    \"@types/node\": \"20.11.0\",\n    \"@types/react\": \"18.3.3\",\n    \"@types/react-dom\": \"18.3.0\",\n    \"autoprefixer\": \"10.4.19\",\n    \"postcss\": \"8.4.39\",\n    \"tailwindcss\": \"3.4.7\",\n    \"typescript\": \"5.4.5\"\n  }\n}\n"
    },
    {
      "path": "next.config.js",
      "content": "/** @type {import('next').NextConfig} */\n
```

</details>

### B061
> Coding bootcamp for career changers entering software development — motivating, outcome-focused, and credible with strong job placement rates, average starting salary stats, and employer partner logos. Positioned against top bootcamps as more mentorship-intensive

| v0.dev · Baseline | SFT only | AI CDO · Best |
|:---:|:---:|:---:|
| ![v0](samples/B061/v0.png) | ![sft](samples/B061/sft.png) | ![aicdo](samples/B061/aicdo.png) |


<details>
<summary><strong>v0.dev · Baseline</strong> — 1 step</summary>

**Step 1 · Direct Generation** (15442 ms)
```json
'use client';

import React from 'react';

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navbar */}
      <nav className="border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded"></div>
            <span className="text-xl font-bold text-gray-900">CodePath</span>
          </div>
          <div className="hidden md:flex space-x-8">
            <a href="#" className="text-gray-700 hover:text-gray-900">Program</a>
            <a href="#" className="text-gray-700 hover:text-gray-900">Outcomes</a>
            <a href="#" className="text-gray-700 hover:text-gray-900">About</a>
            <a href="#" className="text-gray-700 hover:text-gray-900">Contact</a>
          </div>
          <button className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue
```

</details>

<details>
<summary><strong>SFT only</strong> — 2 steps</summary>

**Step 2 · Classification** (1145 ms)
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

**Step 5 · Code Generation (no CDO strategy)** (100019 ms)
```json
{
  "files": [
    {
      "path": "src/app/page.tsx",
      "content": "{\"files\":[{\"path\":\"src/app/page.tsx\",\"content\":\"'use client';\\nimport { useState } from 'react';\\nimport {\\n  Code2,\\n  Users,\\n  Briefcase,\\n  TrendingUp,\\n  CheckCircle,\\n  Star,\\n  ArrowRight,\\n  Menu,\\n  X,\\n  BookOpen,\\n  MessageSquare,\\n  Award,\\n  Clock,\\n  ChevronRight,\\n  Zap,\\n  Globe,\\n  Shield,\\n} from 'lucide-react';\\n\\nexport default function Home() {\\n  const [menuOpen, setMenuOpen] = useState(false);\\n\\n  const features = [\\n    {\\n      icon: <Users className=\\\"w-6 h-6\\\" />,\\n      title: 'Dedicated 1-on-1 Mentorship',\\n      description:\\n        'Every student gets a senior engineer mentor with weekly live sessions, code reviews, and career coaching \u2014 
```

</details>

<details>
<summary><strong>AI CDO · Best</strong> — 5 steps</summary>

**Step 2 · Classification** (4733 ms)
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

**Step 3 · CDO Strategy** (6975 ms)
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
      "name": "Outcomes-Backed Credibility",
      "intent": "trust_first",
      "hero_focus": "value_prop",
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
      "rationale": "Lead with verifiable outcomes and employer validation to neutralize skepticism inherent to bootcamp claims, earning the right to ask for action only after proof is esta
```

**Step 3.5 · Brand Traits** (15700 ms)
```json
{
  "brand_personality": {
    "primary_traits": [
      "motivating",
      "credible",
      "supportive"
    ],
    "tone": "encouraging-professional",
    "formality": "approachable",
    "energy": "high",
    "rationale": "Career changers need motivation balanced with credibility. Supportive tone reflects mentorship-intensive positioning while professional formality builds trust around major life decision."
  },
  "visual_style": {
    "aesthetic": "modern-editorial",
    "design_language": "human-centered-professional",
    "visual_density": "balanced",
    "imagery_style": "authentic-portraits",
    "iconography": "rounded-functional",
    "rationale": "Editorial aesthetic supports testimonial-heavy narrative. Authentic portraits of real graduates reinforce peer credibility over stock imagery."
  },
  "color_direction": {
    "palette_type": "confident-warm",
    "primary_hue": "deep-blue",
    "accent_strategy": "energetic-accent",
    "accent_hue": "vibrant-coral",
    "neutra
```

**Step 4 · UI Intent** (4658 ms)
```json
{
  "primary_focus": "social_proof",
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

**Step 5 · Code Generation** (53691 ms)
```json
{
  "files": [
    {
      "path": "package.json",
      "content": "{\n  \"name\": \"career-narrative\",\n  \"version\": \"0.1.0\",\n  \"private\": true,\n  \"scripts\": {\n    \"dev\": \"next dev\",\n    \"build\": \"next build\",\n    \"start\": \"next start\",\n    \"lint\": \"next lint\"\n  },\n  \"dependencies\": {\n    \"next\": \"14.2.5\",\n    \"react\": \"18.3.1\",\n    \"react-dom\": \"18.3.1\"\n  },\n  \"devDependencies\": {\n    \"@types/node\": \"20.11.0\",\n    \"@types/react\": \"18.3.3\",\n    \"@types/react-dom\": \"18.3.0\",\n    \"autoprefixer\": \"10.4.19\",\n    \"postcss\": \"8.4.38\",\n    \"tailwindcss\": \"3.4.7\",\n    \"typescript\": \"5.4.5\"\n  }\n}\n"
    },
    {
      "path": "next.config.js",
      "content": "/** @type {import('next').NextConfig} */\nmodu
```

</details>

### B116
> Immigration legal aid nonprofit providing pro bono services to immigrants and asylum seekers — compassionate, trustworthy, and multilingual with cases handled stats, languages supported, and pro bono attorney network. Positioned as the most accessible immigration legal resource for unrepresented immigrants

| v0.dev · Baseline | SFT only | AI CDO · Best |
|:---:|:---:|:---:|
| ![v0](samples/B116/v0.png) | ![sft](samples/B116/sft.png) | ![aicdo](samples/B116/aicdo.png) |


<details>
<summary><strong>v0.dev · Baseline</strong> — 1 step</summary>

**Step 1 · Direct Generation** (15056 ms)
```json
import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-white">
      {/* Navbar */}
      <nav className="border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
              <span className="text-white text-sm font-bold">L</span>
            </div>
            <span className="text-xl font-semibold text-gray-900">LegalAid</span>
          </div>
          <div className="hidden md:flex gap-8">
            <Link href="#" className="text-gray-600 hover:text-gray-900 text-sm">
              About
            </Link>
            <Link href="#" className="text-gray-600 hover:text-gray-900 text-sm">
              Services
            </Link>
            <Link href="#" className="text-gray-600 hover:tex
```

</details>

<details>
<summary><strong>SFT only</strong> — 2 steps</summary>

**Step 2 · Classification** (1463 ms)
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

**Step 5 · Code Generation (no CDO strategy)** (89701 ms)
```json
{
  "files": [
    {
      "path": "src/app/page.tsx",
      "content": "{\"files\":[{\"path\":\"src/app/page.tsx\",\"content\":\"'use client';\\nimport {\\n  Globe,\\n  Shield,\\n  Users,\\n  Scale,\\n  Phone,\\n  Mail,\\n  MapPin,\\n  ChevronRight,\\n  CheckCircle,\\n  Heart,\\n  BookOpen,\\n  Handshake,\\n  Star,\\n  ArrowRight,\\n  FileText,\\n  Clock,\\n  Award\\n} from 'lucide-react';\\nimport { useState } from 'react';\\n\\nexport default function Home() {\\n  const [menuOpen, setMenuOpen] = useState(false);\\n\\n  return (\\n    <div className=\\\"min-h-screen bg-white font-sans\\\">\\n      {/* Sticky Nav */}\\n      <header className=\\\"sticky top-0 z-50 bg-white/95 backdrop-blur border-b border-slate-100 shadow-sm\\\">\\n        <div className=\\\"max-w-7xl mx-auto px-6 py-4 fl
```

</details>

<details>
<summary><strong>AI CDO · Best</strong> — 5 steps</summary>

**Step 2 · Classification** (1263 ms)
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

**Step 3 · CDO Strategy** (6004 ms)
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
      "name": "Authority and Accessibility",
      "intent": "authority_first",
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
        "reinforce_authority",
        "simplify_language",
        "increase_proof_density"
      ],
      "rationale": "Establishes institutional legitimacy first to reassure a vulnerable audience that the organization is credible, safe, and competent before inviting enga
```

**Step 3.5 · Brand Traits** (8499 ms)
```json
{
  "brand_name": "Refugio Legal",
  "tone": [
    "compassionate",
    "trustworthy",
    "calm",
    "humanitarian",
    "accessible"
  ],
  "voice_descriptors": [
    "clear",
    "reassuring",
    "respectful",
    "non-judgmental",
    "plain-spoken"
  ],
  "visual_style": "humanitarian_editorial",
  "color_personality": {
    "primary_hue": "deep_teal",
    "accent_hue": "warm_amber",
    "neutral_base": "soft_ivory",
    "mood": "safe_and_grounded",
    "contrast_level": "medium_high",
    "saturation": "muted_with_warm_accents"
  },
  "typography_personality": {
    "heading_style": "humanist_serif",
    "body_style": "clean_humanist_sans",
    "pairing_mood": "trustworthy_and_human",
    "scale_contrast": "moderate",
    "weight_usage": "regular_to_semibold"
  },
  "spacing_density": "generous",
  "corner_radius_style": "soft_rounded",
  "shadow_style": "subtle_soft",
  "imagery_style": {
    "type": "documentary_photography",
    "subject_focus": "real_people_and_families",
 
```

**Step 4 · UI Intent** (2433 ms)
```json
{
  "primary_focus": "value_prop",
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

**Step 5 · Code Generation** (56895 ms)
```json
{
  "files": [
    {
      "path": "package.json",
      "content": "{\n  \"name\": \"clarity-of-value\",\n  \"version\": \"0.1.0\",\n  \"private\": true,\n  \"scripts\": {\n    \"dev\": \"next dev\",\n    \"build\": \"next build\",\n    \"start\": \"next start\",\n    \"lint\": \"next lint\"\n  },\n  \"dependencies\": {\n    \"next\": \"14.2.5\",\n    \"react\": \"18.3.1\",\n    \"react-dom\": \"18.3.1\"\n  },\n  \"devDependencies\": {\n    \"@types/node\": \"20.11.30\",\n    \"@types/react\": \"18.2.66\",\n    \"@types/react-dom\": \"18.2.22\",\n    \"autoprefixer\": \"10.4.19\",\n    \"postcss\": \"8.4.38\",\n    \"tailwindcss\": \"3.4.4\",\n    \"typescript\": \"5.4.5\"\n  }\n}\n"
    },
    {
      "path": "next.config.js",
      "content": "/** @type {import('next').NextConfig} */\nc
```

</details>

### B103
> Sleep and focus soundscape app with science-backed audio design for adults struggling with sleep onset or deep work — calm, dark-mode friendly with waveform visualizations, sound category previews, sleep improvement stats, and neuroscience credentials. Positioned against Calm as more focus-and-sleep-specific

| v0.dev · Baseline | SFT only | AI CDO · Best |
|:---:|:---:|:---:|
| ![v0](samples/B103/v0.png) | ![sft](samples/B103/sft.png) | ![aicdo](samples/B103/aicdo.png) |


<details>
<summary><strong>v0.dev · Baseline</strong> — 1 step</summary>

**Step 1 · Direct Generation** (9126 ms)
```json
'use client';

import { Volume2, Brain, Zap } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navbar */}
      <nav className="border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded"></div>
            <span className="text-xl font-semibold text-gray-900">SoundMind</span>
          </div>
          <div className="hidden md:flex items-center gap-8">
            <a href="#" className="text-gray-600 hover:text-gray-900 text-sm">Features</a>
            <a href="#" className="text-gray-600 hover:text-gray-900 text-sm">Science</a>
            <a href="#" className="text-gray-600 hover:text-gray-900 text-sm">Pricing</a>
            <a href="#" className="text-gray-600 hover:text-gray-900 text-sm">Blog</a>
          </div>
          <button
```

</details>

<details>
<summary><strong>SFT only</strong> — 2 steps</summary>

**Step 2 · Classification** (1624 ms)
```json
{
  "product_type": "B2C SaaS",
  "industry": "healthcare",
  "page_type": "landing",
  "primary_user": "end_customer",
  "user_context": "evaluating",
  "trust_sensitivity": "medium"
}
```

**Step 5 · Code Generation (no CDO strategy)** (96946 ms)
```json
{
  "files": [
    {
      "path": "src/app/page.tsx",
      "content": "{\"files\":[{\"path\":\"src/app/page.tsx\",\"content\":\"'use client';\\nimport { useState } from 'react';\\nimport {\\n  Brain,\\n  Moon,\\n  Waves,\\n  Zap,\\n  Shield,\\n  Play,\\n  Pause,\\n  ChevronRight,\\n  Star,\\n  Clock,\\n  Activity,\\n  Headphones,\\n  CheckCircle,\\n  ArrowRight,\\n  Volume2,\\n  Wind,\\n  CloudRain,\\n  Music\\n} from 'lucide-react';\\n\\nconst NAV_LINKS = ['Features', 'Science', 'Sounds', 'Pricing'];\\n\\nconst FEATURES = [\\n  {\\n    icon: Brain,\\n    title: 'Neuroscience-Backed Design',\\n    desc: 'Every soundscape is engineered with binaural beats, isochronic tones, and spectral masking protocols reviewed by sleep researchers.'\\n  },\\n  {\\n    icon: Moon,\\n    title: 'Sleep On
```

</details>

<details>
<summary><strong>AI CDO · Best</strong> — 5 steps</summary>

**Step 2 · Classification** (2424 ms)
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

**Step 3 · CDO Strategy** (5874 ms)
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
      "name": "Science-Led Credibility",
      "intent": "authority_first",
      "hero_focus": "authority",
      "information_order": [
        "headline",
        "subheadline",
        "security_compliance",
        "benefits",
        "product_demo",
        "testimonials",
        "primary_cta",
        "faq",
        "footer"
      ],
      "risk_controls": [
        "increase_proof_density",
        "reinforce_authority",
        "delay_cta"
      ],
      "rationale": "Lead with neuroscience credibility to differentiate from lifestyle competitors and justify the product's outcome claims before any conversio
```

**Step 3.5 · Brand Traits** (12670 ms)
```json
{
  "design_inference": {
    "design_keywords": [
      "serene",
      "nocturnal",
      "scientific",
      "immersive",
      "minimal",
      "atmospheric"
    ],
    "personality_tone": "Calm, intelligent, and grounded \u2014 speaks softly with clinical authority. Evokes the quiet clarity of late-night focus and the gentle pull of sleep. Confident but never clinical-cold.",
    "emotional_response": [
      "calm",
      "trust",
      "curiosity",
      "relief"
    ],
    "visual_metaphor": "A waveform dissolving into stillness \u2014 sound as visible texture against deep night space, like binaural frequencies rendered as light.",
    "design_principles": [
      "Sensory-first: let motion and sound visualizations carry the narrative",
      "Restful negative space \u2014 no visual noise competes with audio focus",
      "Scientific credibility through restraint, not clutter",
      "Dark-mode native, with luminous accents for hierarchy"
    ],
    "brand_archetype": "The Sage
```

**Step 4 · UI Intent** (2463 ms)
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

**Step 5 · Code Generation** (53201 ms)
```json
{
  "files": [
    {
      "path": "package.json",
      "content": "{\n  \"name\": \"experience-demonstration\",\n  \"version\": \"0.1.0\",\n  \"private\": true,\n  \"scripts\": {\n    \"dev\": \"next dev\",\n    \"build\": \"next build\",\n    \"start\": \"next start\",\n    \"lint\": \"next lint\"\n  },\n  \"dependencies\": {\n    \"next\": \"14.2.5\",\n    \"react\": \"18.3.1\",\n    \"react-dom\": \"18.3.1\"\n  },\n  \"devDependencies\": {\n    \"@types/node\": \"20.12.7\",\n    \"@types/react\": \"18.3.3\",\n    \"@types/react-dom\": \"18.3.0\",\n    \"autoprefixer\": \"10.4.19\",\n    \"postcss\": \"8.4.38\",\n    \"tailwindcss\": \"3.4.7\",\n    \"typescript\": \"5.4.5\"\n  }\n}\n"
    },
    {
      "path": "next.config.js",
      "content": "/** @type {import('next').NextConfig} 
```

</details>

### B040
> Cash management and yield optimization platform for Series A–C startup CFOs managing $1M–$50M in cash — sophisticated, precise, and dark-mode premium with yield rate comparisons, FDIC coverage explainer, and VC-backed client logos. Positioned against Mercury as yield-optimized rather than just banking

| v0.dev · Baseline | SFT only | AI CDO · Best |
|:---:|:---:|:---:|
| ![v0](samples/B040/v0.png) | ![sft](samples/B040/sft.png) | ![aicdo](samples/B040/aicdo.png) |


<details>
<summary><strong>v0.dev · Baseline</strong> — 1 step</summary>

**Step 1 · Direct Generation** (18475 ms)
```json
import React from 'react';

export default function CashManagementPage() {
  return (
    <div className="min-h-screen bg-slate-900 text-white">
      {/* Navbar */}
      <nav className="border-b border-slate-800 bg-slate-950">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded bg-blue-500 font-bold">
              CF
            </div>
            <span className="text-lg font-semibold">CashFlow Pro</span>
          </div>
          <div className="flex gap-8">
            <a href="#features" className="text-sm text-slate-300 hover:text-white">
              Features
            </a>
            <a href="#yields" className="text-sm text-slate-300 hover:text-white">
              Yields
            </a>
            <a href="#security" className="text-sm text-slate-300 hover:text-white">
              Security
            
```

</details>

<details>
<summary><strong>SFT only</strong> — 2 steps</summary>

**Step 2 · Classification** (1801 ms)
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

**Step 5 · Code Generation (no CDO strategy)** (95379 ms)
```json
{
  "files": [
    {
      "path": "src/app/page.tsx",
      "content": "{\"files\":[{\"path\":\"src/app/page.tsx\",\"content\":\"'use client';\\nimport { useState } from 'react';\\nimport {\\n  TrendingUp,\\n  Shield,\\n  Zap,\\n  ChevronRight,\\n  BarChart3,\\n  Lock,\\n  ArrowUpRight,\\n  CheckCircle2,\\n  Star,\\n  DollarSign,\\n  PieChart,\\n  RefreshCw,\\n  AlertCircle,\\n  Menu,\\n  X,\\n} from 'lucide-react';\\n\\nconst YIELD_DATA = [\\n  { label: 'Apex Treasury', rate: 5.42, highlight: true },\\n  { label: 'Mercury', rate: 4.71, highlight: false },\\n  { label: 'Brex', rate: 4.58, highlight: false },\\n  { label: 'Traditional Bank', rate: 0.48, highlight: false },\\n];\\n\\nconst FEATURES = [\\n  {\\n    icon: TrendingUp,\\n    title: 'Yield-Optimized Allocation',\\n    descriptio
```

</details>

<details>
<summary><strong>AI CDO · Best</strong> — 5 steps</summary>

**Step 2 · Classification** (1166 ms)
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

**Step 3 · CDO Strategy** (7042 ms)
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
      "rationale": "CFOs managing significant capital require institutional legitimacy before considering value. Leading with regulatory standing and authori
```

**Step 3.5 · Brand Traits** (11972 ms)
```json
{
  "brand_name": "Vault Yield",
  "brand_personality": [
    "sophisticated",
    "precise",
    "institutional",
    "analytical",
    "premium"
  ],
  "tone_of_voice": {
    "primary": "authoritative",
    "characteristics": [
      "data-driven",
      "concise",
      "confident",
      "technically-fluent"
    ],
    "avoid": [
      "playful",
      "casual",
      "hyperbolic",
      "consumer-friendly slang"
    ]
  },
  "visual_style": {
    "aesthetic": "dark-mode premium financial terminal",
    "design_language": "precision-engineered minimalism with data density",
    "mood": "serious, refined, institutional-grade",
    "inspiration": [
      "Bloomberg Terminal",
      "Linear",
      "Arc",
      "Ramp",
      "Brex"
    ]
  },
  "color_palette": {
    "mode": "dark",
    "primary_background": "#0A0B0D",
    "secondary_background": "#111316",
    "surface": "#16191D",
    "border": "#23272E",
    "primary_text": "#F5F6F7",
    "secondary_text": "#9BA1A8",
    "muted_tex
```

**Step 4 · UI Intent** (2089 ms)
```json
{
  "primary_focus": "product_clarity",
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

**Step 5 · Code Generation** (69082 ms)
```json
{
  "files": [
    {
      "path": "package.json",
      "content": "{\n  \"name\": \"treasury-landing\",\n  \"version\": \"0.1.0\",\n  \"private\": true,\n  \"scripts\": {\n    \"dev\": \"next dev\",\n    \"build\": \"next build\",\n    \"start\": \"next start\",\n    \"lint\": \"next lint\"\n  },\n  \"dependencies\": {\n    \"next\": \"14.2.5\",\n    \"react\": \"18.3.1\",\n    \"react-dom\": \"18.3.1\"\n  },\n  \"devDependencies\": {\n    \"@types/node\": \"20.12.7\",\n    \"@types/react\": \"18.3.3\",\n    \"@types/react-dom\": \"18.3.0\",\n    \"autoprefixer\": \"10.4.19\",\n    \"postcss\": \"8.4.38\",\n    \"tailwindcss\": \"3.4.7\",\n    \"typescript\": \"5.4.5\"\n  }\n}\n"
    },
    {
      "path": "next.config.js",
      "content": "/** @type {import('next').NextConfig} */\ncons
```

</details>

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
