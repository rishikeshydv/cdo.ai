import json
import os
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from dotenv import load_dotenv
from openai import OpenAI

# --------------------------------------------------------------------------- #
# Setup
# --------------------------------------------------------------------------- #

# Find project root (current directory)
BASE_DIR = Path(__file__).resolve().parent

# Load the .env.prod file from the project root
load_dotenv(dotenv_path=BASE_DIR / ".env.development", override=True)

# Setting up LLM
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = "gpt-5-mini"

openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


class MissingClientError(RuntimeError):
    """Raised when an OpenAI client is required but not configured."""


class InvalidStrategyError(ValueError):
    """Raised when the Step 3 strategy JSON cannot be parsed or is empty."""


class JSONHandler:
    """
    Thin orchestrator for the multi-step JSON/strategy pipeline.
    Each step delegates the heavy lifting to the LLM with tight schemas.
    """

    def __init__(self, client: Optional[OpenAI] = openai_client, model: str = DEFAULT_MODEL):
        self.client = client
        self.model = model

    # ----------------------------- internals -------------------------------- #
    def _ensure_client(self) -> OpenAI:
        if not self.client:
            raise MissingClientError("OpenAI client is not initialized. Check your API key.")
        return self.client

    def llm_response(self, messages: Iterable[Dict[str, str]]) -> str:
        """
        Shared chat completion helper. Expects an iterable of {"role","content"} dicts.
        """
        client = self._ensure_client()
        response = client.chat.completions.create(model=self.model, messages=list(messages))
        return response.choices[0].message.content

    def _first_strategy(self, step_3_json: str) -> Dict:
        """
        Extract the first strategy object from a Step 3 JSON string.
        Raises InvalidStrategyError if parsing fails or strategies are missing.
        """
        try:
            parsed = json.loads(step_3_json)
        except json.JSONDecodeError as exc:
            raise InvalidStrategyError(f"Step 3 JSON is invalid: {exc}") from exc

        strategies: List[Dict] = parsed.get("strategies") or []
        if not strategies or not isinstance(strategies, list):
            raise InvalidStrategyError("No strategies found in Step 3 JSON.")
        return strategies[-1]

    def write_manifest(self, manifest_json: str, target_root: Path) -> None:
        """
        Materialize a manifest of files (path + content) under target_root.
        Manifest shape:
        {
          "files": [{"path": "package.json", "content": "..."}],
          "instructions": "npm install && npm run dev"
        }
        """
        try:
            manifest = json.loads(manifest_json)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid manifest JSON: {exc}") from exc

        files = manifest.get("files")
        if not isinstance(files, list):
            raise ValueError("Manifest must contain a 'files' array.")

        target_root = target_root.resolve()
        target_root.mkdir(parents=True, exist_ok=True)

        for entry in files:
            rel_path = entry.get("path")
            content = entry.get("content")
            if not rel_path or content is None:
                raise ValueError(f"Each file needs 'path' and 'content': {entry}")

            full_path = (target_root / rel_path).resolve()

            # prevent escaping the target root
            if target_root not in full_path.parents and full_path != target_root:
                raise ValueError(f"Refusing to write outside target root: {full_path}")

            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")

    def step2_classification(self, raw_prompt: str):
        system_prompt = """
                You are a classification engine in a multi-stage UI generation system.
                Your task is to analyze a user's product description and return a single JSON object that classifies the context using a fixed schema.

                You must:
                - Choose ONLY from the allowed enum values provided.
                - Select the MOST appropriate single value for each field.
                - Avoid inventing new categories or explanations.
                - Return VALID JSON ONLY.
                - Do not include markdown, comments, or natural language.
                - If uncertain, choose the most conservative or broadly applicable option.
            """
            
        developer_prompt = f"""
        Classify the user request into the following JSON schema.

        Allowed values:

        product_type:
        - "B2B SaaS"
        - "B2C SaaS"
        - "marketplace"
        - "internal_tool"
        - "content_site"

        industry:
        - "fintech"
        - "fintech_compliance"
        - "healthcare"
        - "devtools"
        - "ai_platform"
        - "ecommerce"
        - "education"
        - "marketing"
        - "hr_tech"
        - "other"

        page_type:
        - "landing"
        - "pricing"
        - "dashboard"
        - "onboarding"
        - "auth"
        - "settings"

        primary_user:
        - "founder"
        - "developer"
        - "compliance_officer"
        - "operations_manager"
        - "marketer"
        - "end_customer"
        - "admin"

        user_context:
        - "first_time_visitor"
        - "evaluating"
        - "returning_user"
        - "power_user"

        trust_sensitivity:
        - "low"
        - "medium"
        - "high"

        Rules:
        - Always return exactly one value per field.
        - Use the user's intent, not surface wording.
        - Prefer higher trust_sensitivity if the domain involves money, data, compliance, or security.
        - If the product supports multiple roles, select the PRIMARY decision-maker.
        - If the page type is unclear, infer the most likely default based on context.

        Return format (example only):

        {
        {"product_type": "...",
        "industry": "...",
        "page_type": "...",
        "primary_user": "...",
        "user_context": "...",
        "trust_sensitivity": "..."}
        }
        
        User Request: {raw_prompt}
        
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": developer_prompt}
        ]

        response_content = self.llm_response(messages)
        return response_content

    def step3_strategy(self, user_prompt: str, step_2_json: str):

        system_prompt = """
        You are a Chief Design Officer (CDO) reasoning module in a multi-stage UI system.

        Your role is to make EXECUTIVE-LEVEL STRATEGIC DECISIONS only.

        You do NOT:
        - design layouts
        - choose colors or typography
        - mention UI components
        - write marketing copy
        - suggest animations or visuals

        You ONLY:
        - decide strategic intent
        - identify risks
        - define principles and avoidances
        - propose 2-3 competing high-level strategies

        You must strictly follow the provided JSON schema.
        Return VALID JSON ONLY.
        No explanations, no markdown, no commentary.

        """
        
        developer_prompt = f"""
        You will be given:

        1) A user request (natural language)
        2) A Step 2 classification JSON describing the context

        Your task:
        Generate a CDO Strategy JSON that conforms EXACTLY to the following schema and enum values.

        IMPORTANT RULES:
        - Use ONLY the enum values provided in the schema.
        - Do not invent new risks, principles, or avoidances.
        - Select values conservatively when uncertain.
        - Strategies must be meaningfully different from each other.
        - All rationale text must be executive-level and abstract (no UI or implementation details).
        - The output must include 2 or 3 strategies, never fewer or more.
        - All arrays must respect min/max length constraints.
        - Do not include additional properties.

        If a choice involves trust, regulation, compliance, finance, or sensitive data:
        - Prefer intent and principles that emphasize legitimacy, clarity, and authority.

        Return ONLY the JSON object.
        
        Schema summary (do not repeat in output):

        primary_intent ∈ {{
        reduce_skepticism,
        drive_conversion,
        signal_legitimacy,
        accelerate_understanding,
        increase_confidence
        }}

        key_risks ∈ {{
        low_trust,
        overpromising,
        cognitive_overload,
        unclear_value_prop,
        premature_cta,
        visual_noise
        }}

        strategic_principles ∈ {{
        clarity_over_density,
        credibility_over_creativity,
        familiarity_over_novelty,
        confidence_before_action,
        progressive_disclosure
        }}

        avoidances ∈ {{
        flashy_motion,
        marketing_fluff,
        visual_clutter,
        aggressive_ctas,
        unsubstantiated_claims
        }}

        strategy.intent ∈ {{
        trust_first,
        authority_first,
        product_first,
        conversion_first
        }}

        strategy.hero_focus ∈ {{
        authority,
        value_prop,
        product_visual,
        social_proof
        }}

        strategy.information_order ∈ {{
        headline,
        subheadline,
        security_compliance,
        customer_logos,
        product_demo,
        benefits,
        testimonials,
        primary_cta,
        faq,
        footer
        }}

        strategy.risk_controls ∈ {{
        delay_cta,
        increase_proof_density,
        simplify_language,
        limit_choices,
        reinforce_authority
        }}


        User request:
        {user_prompt}

        Step 2 classification:
        {step_2_json}

        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": developer_prompt}
        ]
        response_content = self.llm_response(messages)
        return response_content

    # ui intent for each strategy
    def step4_ui_intent(self, step_2_json: str, step_3_json: str):
        selected_strategy = self._first_strategy(step_3_json)

        system_prompt = """
            You are an executive UI intent translator in a multi-stage design system.

            Your role is to translate a SINGLE approved CDO strategy into EXECUTION BOUNDS for a UI generator.

            You do NOT:
            - invent or modify strategy
            - describe layouts, components, or visuals
            - write copy
            - explain your reasoning

            You ONLY:
            - translate strategic intent into UI constraints
            - gate creativity, motion, and interaction
            - decide CTA behavior, proof intensity, and tone

            You must strictly follow the provided JSON schema.
            Return VALID JSON ONLY.
            No markdown, no explanations, no extra text.

        """
        
        developer_prompt = f"""
        You will be given:

        1) A Step 2 classification JSON (context)
        2) A Step 3 CDO Strategy JSON
        3) ONE selected strategy object from Step 3

        Your task:
        Translate the selected strategy into a UI Intent JSON that defines execution boundaries for a UI generator.

        CRITICAL RULES:
        - Use ONLY enum values provided in the schema.
        - The output must reflect the selected strategy, not the entire strategy set.
        - UI Intent must be conservative by default unless the strategy clearly supports expressiveness.
        - Creative license and motion policy must align with trust sensitivity and strategy intent.
        - CTA policy must respect risk controls implied by the strategy.
        - Do not invent new fields or modify the schema.
        - All fields are REQUIRED.

        If the context involves:
        - compliance, finance, healthcare, or security → bias toward restraint
        - first-time visitors → delay or soften CTAs
        - high trust sensitivity → increase proof and reduce motion

        Schema summary (do not repeat in output):

        primary_focus ∈ {{authority, value_prop, product_clarity, social_proof}}

        cta_policy.timing ∈ {{ immediate, delayed, progressive }}
        cta_policy.intensity ∈ {{ soft, neutral, assertive }}

        proof_policy ∈ {{ minimal, balanced, heavy }}

        content_density ∈ {{ low, medium, high }}

        motion_policy ∈ {{ none, subtle, expressive }}

        creative_license ∈ {{ none, restricted, expressive }}

        language_style ∈ {{ precise, plain, confident, inspirational }}

        interaction_restraint ∈ {{ strict, moderate, loose }}
        
        Step 2 classification:
        {step_2_json}
        
        Step 3 CDO Strategy:
        {step_3_json}
        
        Selected strategy:
        {selected_strategy}
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": developer_prompt}
        ]
        response_content = self.llm_response(messages)
        return response_content

    def step5_code_generation(self, ui_intent_json: str, step_3_json: str, selected_strategy_object: str):
        system_prompt = """
        You are a senior frontend engineer executing a pre-approved design strategy.

        Your job is to produce a JSON manifest describing a minimal, runnable Next.js (App Router) project.

        You do NOT:
        - invent strategy
        - modify intent
        - explain decisions
        - add features beyond instructions
        - add creativity beyond what is explicitly permitted

        You MUST:
        - strictly obey UI Intent constraints
        - strictly follow the selected strategy
        - generate clean, modular, readable code
        - return the manifest only (no prose, no markdown)
        """
        
        developer_prompt = f"""
        You will be given:

        1) A UI Intent JSON (execution bounds)
        2) A full CDO Strategy JSON (contextual grounding)
        3) ONE selected strategy object (authoritative)

        Your task:
        Emit a JSON manifest that describes a minimal, runnable Next.js App Router project (TypeScript + Tailwind) that satisfies the UI Intent and selected strategy.

        MANIFEST FORMAT (required):
        {{
          "files": [
            {{"path": "package.json", "content": "<file content>"}},
            {{"path": "tsconfig.json", "content": "<file content>"}},
            ...
          ],
          "instructions": "npm install && npm run dev"
        }}

        REQUIRED FILES (keep concise):
        - package.json (pin Next/Tailwind/TS deps; scripts: dev, build, lint; DO NOT set "type": "module")
        - next.config.js (CJS, module.exports)
        - tsconfig.json (minimal, valid; jsx set to "preserve" or "automatic"; allowImportingTsExtensions = false)
        - postcss.config.cjs (CJS)
        - tailwind.config.js (CJS; include any custom colors/fonts/tokens used)
        - src/app/layout.tsx
        - src/app/page.tsx (single-page landing)
        - src/app/globals.css (must include @tailwind base; @tailwind components; @tailwind utilities; plus any custom utilities)
        - src/app/favicon.ico (get it from https://github.com/grommet/nextjs-boilerplate/blob/master/public/favicon.ico)
        - src/components/* (only if needed; keep small)

        CONTENT RULES:
        - Use Next.js App Router conventions.
        - Use TypeScript (.tsx) and Tailwind utilities.
        - Keep the design compact: one page, a few components.
        - Use remote assets or inline SVG only. No large binaries; only the tiny base64 icon is allowed.
        - Honor creative_license, motion_policy, cta_policy, proof_policy, content_density, language_style, and interaction_restraint from UI Intent.
        - If cta_policy.timing is delayed/progressive, keep CTAs below the hero fold.
        - Keep copy/tone aligned to language_style without fluffy marketing.
        - Keep motion consistent with motion_policy (none/subtle/expressive).
        - Default to conservative proof if trust is high or unclear.

        OUTPUT RULES:
        - Return VALID JSON only (the manifest).
        - Do NOT wrap in markdown.
        - Do NOT include explanations.
        
        UI Intent:
        {ui_intent_json}

        Full CDO Strategy:
        {step_3_json}

        Selected Strategy:
        {selected_strategy_object}
        """

        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": developer_prompt}
        ]
        response_content = self.llm_response(messages)
        return response_content

    #generic LLM call (standalone manifest pipeline)
    def generic_llm_call(
        self,
        user_prompt: str,
        system_prompt: Optional[str] = None,
        expect_manifest: bool = False,
        write_manifest_to: Optional[Path] = None,
    ):
        """
        General-purpose chat helper, independent of steps 2-5.
        If expect_manifest is True and write_manifest_to is provided, the response
        is treated as a manifest and written to disk via write_manifest.
        """
        manifest_system_prompt = """
        You are a senior frontend engineer.
                Your task:
        Emit a JSON manifest that describes a minimal, runnable Next.js App Router project (TypeScript + Tailwind) that satisfies the UI Intent and selected strategy.

        MANIFEST FORMAT (required):
        {{
          "files": [
            {{"path": "package.json", "content": "<file content>"}},
            {{"path": "tsconfig.json", "content": "<file content>"}},
            ...
          ],
          "instructions": "npm install && npm run dev"
        }}

        REQUIRED FILES (keep concise):
        - package.json (pin Next/Tailwind/TS deps; scripts: dev, build, lint; DO NOT set "type": "module")
        - next.config.js (CJS, module.exports)
        - tsconfig.json (minimal, valid; jsx set to "preserve" or "automatic"; allowImportingTsExtensions = false)
        - postcss.config.cjs (CJS)
        - tailwind.config.js (CJS; include any custom colors/fonts/tokens used)
        - src/app/layout.tsx
        - src/app/page.tsx (single-page landing)
        - src/app/globals.css (must include @tailwind base; @tailwind components; @tailwind utilities; plus any custom utilities)
        - src/app/favicon.ico (get it from https://github.com/grommet/nextjs-boilerplate/blob/master/public/favicon.ico)
        - src/components/* (only if needed; keep small)

        CONTENT RULES:
        - Use Next.js App Router conventions.
        - Use TypeScript (.tsx) and Tailwind utilities.
        - Keep the design compact: one page, a few components.
        - Use remote assets or inline SVG only. No large binaries; only the tiny base64 icon is allowed.
        - Honor creative_license, motion_policy, cta_policy, proof_policy, content_density, language_style, and interaction_restraint from UI Intent.
        - If cta_policy.timing is delayed/progressive, keep CTAs below the hero fold.
        - Keep copy/tone aligned to language_style without fluffy marketing.
        - Keep motion consistent with motion_policy (none/subtle/expressive).
        - Default to conservative proof if trust is high or unclear.

        OUTPUT RULES:
        - Return VALID JSON only (the manifest).
        - Do NOT wrap in markdown.
        - Do NOT include explanations.
        """

        active_system_prompt = system_prompt or (manifest_system_prompt if expect_manifest else "You are a helpful assistant.")
        messages = [
            {"role": "system", "content": active_system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        response_content = self.llm_response(messages)

        if expect_manifest:
            if not write_manifest_to:
                raise ValueError("write_manifest_to is required when expect_manifest is True.")
            self.write_manifest(response_content, write_manifest_to.resolve())

        return response_content
    
    
if __name__ == "__main__":
    json_handler = JSONHandler()
    print("Starting AI-CDO Pipeline...")
    
    user_input = input("Please enter your product description or UI request:\n")
    
    # Step 2
    step2_json = json_handler.step2_classification(user_input)
    print("✓ Step 2 Completed")
    
    # Step 3
    step3_json = json_handler.step3_strategy(user_input, step2_json)
    print("✓ Step 3 Completed")
    
    # Step 4
    step4_json = json_handler.step4_ui_intent(step2_json, step3_json)
    print("✓ Step 4 Completed")
    
    # Step 5
    selected_strategy = json_handler._first_strategy(step3_json)
    step5_manifest = json_handler.step5_code_generation(step4_json, step3_json, json.dumps(selected_strategy))
    print("✓ Step 5 Completed")
    
    # Write manifest to disk
    output_dir = BASE_DIR / "generated/aicdo"
    json_handler.write_manifest(step5_manifest, target_root=output_dir)
    print(f"✓ AI-CDO Response written to: {output_dir}")
    
    #generic LLM call example
    generic_response = json_handler.generic_llm_call(
        user_prompt=user_input,
        expect_manifest=True,
        write_manifest_to=BASE_DIR / "generated/generic"
    )
    print(f"✓ Generic LLM response written to: {BASE_DIR / 'generated/generic'}")
