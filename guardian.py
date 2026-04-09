import ollama

def xml_cage_wrapper(user_query, external_data, system_rules):
    return f"""
    SYSTEM INSTRUCTION: {system_rules}
    <untrusted_data>{external_data}</untrusted_data>
    <user_query>{user_query}</user_query>
    """

def shadow_model_audit(full_prompt, security_policy):
    print("🛡️ AI-Sentinel: Auditing prompt security...")
    try:
        response = ollama.chat(model='phi3', messages=[
            {'role': 'system', 'content': security_policy},
            {'role': 'user', 'content': f"Audit this: {full_prompt}"},
        ])
        return response['message']['content'].strip().upper()
    except Exception as e:
        return f"ERROR: {str(e)}"

def ai_sentinel_check(query, data, system_rules, security_policy):
    # Now accepting all 4 arguments dynamically
    final_prompt = xml_cage_wrapper(query, data, system_rules)
    verdict = shadow_model_audit(final_prompt, security_policy)
    
    if "MALICIOUS" in verdict:
        return "ACCESS DENIED", None
    return "SAFE", final_prompt