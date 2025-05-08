import os
from openai import OpenAI
import google.generativeai as genai
from anthropic import Anthropic, APIError
import json # Added for JSON parsing

def call_openai_api(model_name, system_prompt, user_prompt, temperature):
    """Sends a request to the OpenAI API, requesting JSON, and returns the response string."""
    try:
        client = OpenAI() # Assumes OPENAI_API_KEY is set in environment
        print(f"Calling OpenAI model: {model_name} for JSON output")
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            response_format={ "type": "json_object" } # Request JSON output
        )
        # Return the raw JSON string; parsing happens in the agent
        json_string = response.choices[0].message.content
        return json_string # Return potentially non-stripped string to preserve JSON structure
    except Exception as e:
        print(f"Error calling OpenAI API or processing response: {e}")
        return None # Return None to indicate failure

def call_google_api(model_name, system_prompt, user_prompt, temperature):
    """
    Sends a request to the Google Gemini API, requesting JSON.
    Requires 'google-generativeai' library and GOOGLE_API_KEY environment variable.
    """
    try:
        # Configure the Google Generative AI with API key
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        # Initialize the model with the system instruction
        model = genai.GenerativeModel(
            model_name,
            system_instruction=system_prompt
        )

        # Set up the generation configuration for JSON output
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            response_mime_type="application/json" # Request JSON output
        )

        # Generate the response
        response = model.generate_content(user_prompt, generation_config=generation_config)

        # Check for safety blocks or empty responses
        if response.parts:
             # Return the raw JSON string; parsing happens in the agent
            json_string = response.text
            return json_string # Return potentially non-stripped string
        else:
            print("Google API returned no content, possibly due to safety settings.")
            # Inspect feedback if needed: print(response.prompt_feedback)
            # Provide a structured error message or specific code if possible
            return json.dumps({"error": "Content generation blocked by safety settings or API issue."})
    except Exception as e:
        print(f"Error calling Google API: {e}")
        # Return a JSON string indicating the error
        return json.dumps({"error": f"Error calling Google API: {str(e)}"}) 

def call_anthropic_api(model_name, system_prompt, user_prompt, temperature, dynamic_schema):
    """
    Sends a request to the Anthropic API, requesting JSON output using a dynamically generated tool schema.
    
    Args:
        model_name: The name of the Anthropic model to use (e.g. 'claude-3-opus-20240229')
        system_prompt: The system prompt to provide context to Claude for the main task.
        user_prompt: The user's message/prompt for the main task.
        dynamic_schema: The pre-generated JSON schema to use for the tool.
        temperature: Controls randomness in the response (0.0 to 1.0)
        
    Returns:
        str: The model's response as a JSON string.
        
    Raises:
        Exception: If there's an error calling the API (now handled by returning JSON error)
    """
    try:
        client = Anthropic()  # Assumes ANTHROPIC_API_KEY is set in environment

        if not dynamic_schema:
            return json.dumps({"error": "Failed to generate or parse dynamic JSON schema for Anthropic tool."})
        
        # 2. Define a tool that enforces JSON output structure using the dynamic schema
        json_tool_name = "dynamic_json_response"
        json_tool = {
            "name": json_tool_name,
            "description": "Outputs the response in a dynamically specified JSON format based on the user query.",
            "input_schema": dynamic_schema
        }
        
        response = client.messages.create(
            model=model_name,
            max_tokens=4096, # Max tokens for the main response
            temperature=temperature,
            system=system_prompt, # Original system prompt for the main task
            messages=[
                {"role": "user", "content": user_prompt} # Original user prompt for the main task
            ],
            tools=[json_tool],
            tool_choice={"type": "tool", "name": json_tool_name} 
        )
        
        for content_block in response.content:
            if content_block.type == 'tool_use' and content_block.name == json_tool_name:
                return json.dumps(content_block.input)
        
        return json.dumps({"error": "No tool_use content block found in Anthropic API response with dynamic schema."})
        
    except APIError as e: # More specific error handling for the main call
        print(f"Anthropic API error: {e}")
        return json.dumps({"error": f"Anthropic API error: {str(e)}"})
    except Exception as e:
        print(f"Error calling Anthropic API with dynamic schema: {e}")
        return json.dumps({"error": f"Error calling Anthropic API with dynamic schema: {str(e)}"}) 