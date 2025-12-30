from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
import os
from typing import Dict

# Find project root (current directory)
BASE_DIR = Path(__file__).resolve().parent

# Load the .env.prod file from the project root
load_dotenv(dotenv_path=BASE_DIR / ".env.development", override=True)

# Setting up LLM
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

class JSONHandler:
    def __init__(self):
        pass
    def llm_response(self, messages: list[Dict[str, str]]) -> str:
        if not openai_client:
            raise ValueError("OpenAI client is not initialized. Please check your API key.")
        # Expect `messages` to be a list of {"role": "...", "content": "..."} dicts
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return response.choices[0].message.content
        
    def step2_classification(self, raw_prompt: str):
        print("Executing step 2: JSON Classification")
        
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
        "product_type": "...",
        "industry": "...",
        "page_type": "...",
        "primary_user": "...",
        "user_context": "...",
        "trust_sensitivity": "..."
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
        
        
        