import os


def generate_job_description(short_prompt: str) -> str:
    """Generate a job description with Gemini.

    This is intentionally isolated so students can see where AI value is added
    to an existing application. If no API key is present, the app returns a
    deterministic placeholder so the class can run without cloud credentials.
    """
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return (
            '[PLACEHOLDER GENERATED DESCRIPTION - no GEMINI_API_KEY set]\n\n'
            f'Based on the prompt: {short_prompt}\n\n'
            'We are seeking a motivated candidate who is eager to learn, communicate clearly, '
            'solve business problems, and contribute to the department. Responsibilities include '
            'working with internal stakeholders, using appropriate tools, documenting work, and '
            'supporting team goals. The ideal candidate is curious, reliable, and willing to build new skills.'
        )
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content('Write a polished job posting for this request: ' + short_prompt)
        return response.text
    except Exception as exc:
        return f'[PLACEHOLDER GENERATED DESCRIPTION - Gemini call failed: {exc}]\n\nPrompt: {short_prompt}'
